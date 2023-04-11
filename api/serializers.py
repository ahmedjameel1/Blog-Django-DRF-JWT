from rest_framework import serializers
from app.models import *
from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username']


class ArticleSerializer(serializers.ModelSerializer):
    author = AccountSerializer(many=False)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_replies(self, obj):
        replies = obj.reply_set.all()
        serializer = ReplySerializer(replies, many=True)
        return serializer.data


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'
