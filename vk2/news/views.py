from django.shortcuts import render

# Create your views here.
from django.views import View

from account.models import Account

from post.models import Post


class NewsView(View):
    def get(self, request):
        main_user = Account.objects.select_related().get(pk=request.user.pk)
        news = Post.objects.filter(group__in=main_user.group.all())
        return render(request, 'news/feed.html', context={'main_user': main_user,
                                                          'news': news})
