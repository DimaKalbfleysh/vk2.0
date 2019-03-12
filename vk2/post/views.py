from django.http import JsonResponse
from django.views import View
from account.models import Account, Photo, Post, Group, Like


class PostView(View):
    def post(self, request):
        if request.POST['url'] == '/id{}/'.format(request.user.pk):
            main_user = Account.objects.get(pk=request.user.pk)
            content = request.POST['content']
            post = Post.objects.create(author=main_user, content=content)
            return JsonResponse({})
        if request.POST['url'] == '/public{}/'.format(request.POST['public_pk']):
            group = Group.objects.get(pk=request.POST['public_pk'])
            content = request.POST['content']
            post = Post.objects.create(group=group, content=content)
            return JsonResponse({})


class DeletePostView(View):
    def get(self, request):
        post = Post.objects.get(pk=request.GET['pk'])
        post.delete()
        return JsonResponse({})


class PutLikePost(View):
    def get(self, request):
        main_user = Account.objects.get(pk=request.user.pk)
        post = Post.objects.get(pk=request.GET['pk'])
        try:
            like = post.likes.get(user=main_user)
            like.delete()
            count_likes = post.likes.all().count()
            likes_put = False
        except:
            like = Like.objects.create(user=main_user, post=post)
            main_user.likes.add(like)
            post.likes.add(like)
            count_likes = post.likes.all().count()
            likes_put = True
        return JsonResponse({'likes_put': likes_put,
                             'count_likes': count_likes})
