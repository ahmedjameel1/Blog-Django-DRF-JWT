import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Article


class LatestArticlesFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('articles')
    description = 'New articles of my blog.'

    def items(self):
        return Article.published.all()[:5]

    def item_title(self, item):
        return item.subject

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
