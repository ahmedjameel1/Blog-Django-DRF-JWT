from django.utils.safestring import mark_safe
import markdown
from django import template
from ..models import Article
from django.db.models import Count

register = template.Library()


@register.simple_tag
def total_articles():
    return Article.published.count()


@register.inclusion_tag('app/latest_articles.html')
def show_latest_articles(count=5):
    latest_articles = Article.published.order_by('-publish')[:count]
    return {'latest_articles': latest_articles}


@register.simple_tag
def get_most_replied_articles(count=5):
    return Article.published.annotate(
        total_reply=Count('reply')
    ).order_by('-total_reply')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
