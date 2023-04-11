from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import View
from .forms import *
from django.urls import reverse_lazy
from .models import *
from django.core.paginator import Paginator,  EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import *
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


# class Articles(ListView):
#     """
#     Alternative post list view
#     """
#     queryset = Article.published.all()
#     context_object_name = 'articles'
#     paginate_by = 3
#     template_name = 'app/articles.html'


def article_detail(request, year, month, day, id, slug):
    article = get_object_or_404(
        Article, status=Article.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug,
        id=id)
    replies = Reply.objects.filter(article=article)
    # Form for users to comment
    form = ReplyForm()
    # List of similar articles
    article_tags_ids = article.tags.values_list('id', flat=True)
    similar_articles = Article.published.filter(tags__in=article_tags_ids)\
        .exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-publish')[:4]

    return render(request, 'app/article.html', {'article': article, 'form': form, 'replies': replies, 'similar_articles': similar_articles})


def articles(request, tag_slug=None):
    tag = None
    articles = Article.published.all()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = articles.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page', 1)

    try:
        articles = paginator.page(page_number)

    except EmptyPage:
        # If page_number is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        articles = paginator.page(1)
    return render(request, 'app/articles.html', {'articles': articles, 'tag': tag})


def article_share(request, article_id):
    # Retrieve particleost by id
    article = get_object_or_404(
        Article, id=article_id, status=Article.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            article_url = request.build_absolute_uri(
                article.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                f"{article.subject}"
            message = f"Read {article.subject} at {article_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'app/share.html', {'article': article,
                                              'form': form, 'sent': sent})


# ...
@require_POST
def article_reply(request, article_id):
    article = get_object_or_404(
        Article, id=article_id, status=Article.Status.PUBLISHED)
    reply = None
    # A reply was posted
    form = ReplyForm(data=request.POST)
    if form.is_valid():
        # Create a reply object without saving it to the database
        reply = form.save(commit=False)
        # Assign the post to the reply
        reply.article = article
        reply.author = request.user
        # Save the reply to the database
        reply.save()
    return render(request, 'app/reply.html',
                  {'article': article,
                   'form': form,
                   'reply': reply})


def article_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        search_vector = SearchVector('subjects', 'body')
        search_query = SearchQuery(query)
        results = Article.published.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')
    return render(request,
                  'app/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
