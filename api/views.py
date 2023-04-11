from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from app.models import *
# Create your views here.


class GetRoutes(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"accounts/login/", "accounts/register/", "articles/", "article/:article.id", "reply/:reply.id"})


class ArticleList(APIView):
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        serializer = self.serializer_class(articles, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        article = Article.objects.create(
            subject=request.data['subject'],
            body=request.data['body'],
            author=self.request.user,
        )
        serializer = self.serializer_class(article, many=False)
        return Response(serializer.data)


class ArticleDetails(APIView):
    serializer_class = ArticleSerializer

    def get(self, request, pk):
        try:
            article = Article.objects.get(id=pk)
        except:
            return Response('Couldn\'t Find this article', status=404)
        serializer = self.serializer_class(article, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        article = Article.objects.get(id=pk)
        if article.author == request.user:
            article.subject = request.data['subject']
            article.body = request.data['body']
            article.save()
        else:
            return Response('Couldn\'t Update this article You Don\'t own it!', status=404)
        serializer = self.serializer_class(article, many=False)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            article = Article.objects.get(id=pk, author=self.request.user)
        except:
            return Response('Couldn\'t Delete this Article You don\'t own it!', status=404)
        article.delete()
        return Response('Article Was Deleted!')


class ReplyDetails(APIView):
    serializer_class = ReplySerializer

    def get(self, request, pk):
        try:
            reply = Reply.objects.get(id=pk)
        except:
            return Response('Couldn\'t Find this reply', status=404)
        serializer = self.serializer_class(reply, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        reply = Reply.objects.get(id=pk)
        if reply.author == request.user:
            reply.body = request.data['body']
            reply.save()
        else:
            return Response('Couldn\'t Update this reply You Don\'t own it!', status=404)
        serializer = self.serializer_class(reply, many=False)
        return Response(serializer.data)

    def delete(self, request, pk):
        reply = Reply.objects.get(id=pk)
        if reply.author == request.user:
            reply.delete()
            return Response('Reply Was Deleted!')
        else:
            return Response('Couldn\'t Delete this Reply You don\'t own it!', status=404)
