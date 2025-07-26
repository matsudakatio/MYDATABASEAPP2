from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from .models import Post

class TopView(ListView):
    """トップページ（投稿一覧）"""
    model = Post
    template_name = 'posts/top.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # クエリパラメータから並び替え順を取得
        sort = self.request.GET.get('sort')
        queryset = Post.objects.annotate(likes_count=Count('likes'))

        if sort == 'likes':
            # いいね数順で並び替え
            return queryset.order_by('-likes_count', '-created_at')
        else:
            # デフォルトは新着順
            return queryset.order_by('-created_at')


class PostDetailView(DetailView):
    """投稿詳細ページ"""
    model = Post
    template_name = 'posts/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    """新規投稿ページ"""
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'posts/post_form.html'
    success_url = "/"

    def form_valid(self, form):
        # 投稿ユーザーを現在ログインしているユーザーに設定
        form.instance.user = self.request.user
        return super().form_valid(form)


class LikeView(LoginRequiredMixin, View):
    """いいね機能"""
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        user = request.user

        if user in post.likes.all():
            # いいねを解除
            post.likes.remove(user)
            liked = False
        else:
            # いいねを付ける
            post.likes.add(user)
            liked = True

        # いいね数といいね状態をJSONで返す
        return JsonResponse({'likes_count': post.total_likes, 'liked': liked})