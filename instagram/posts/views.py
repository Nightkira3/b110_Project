from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, UpdateView, DetailView

from .forms import PostForm, PostModelForm
from .models import Post


def index(request):
    posts = Post.objects.all().annotate(
        likes_count=Count('likes')
    ).order_by(
        '-likes_count'
    )[:10]
    output = render_to_string('posts/index.html', {'posts': posts}, request=request)
    return HttpResponse(output)


def lenta_of_posts(request):
    user = request.user
    if user.is_authenticated:
        friends = user.friends.all()
        posts = Post.objects.filter(author__target_friends__in=friends).annotate(
            likes_count=Count('likes')
        )
        return render(request, 'posts/lenta_of_posts.html', {'posts': posts})
    else:
        raise PermissionDenied("Пожалуйста авторизируйтесь")


class DetailPostView(DetailView):
    model = Post
    pk_url_kwarg = 'post_pk'
    template_name = 'posts/post_detail.html'


@login_required
def post_create(request):

    if request.method == 'GET':
        form = PostModelForm()
    else:
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:index')

    return render(request, 'posts/post_create.html', {
        'form': form, 'header': "Создание поста",
    })


@method_decorator(login_required, name='dispatch')
class UpdatePostView(UpdateView):
    model = Post
    pk_url_kwarg = 'post_pk'
    template_name = 'posts/post_update.html'
    form_class = PostModelForm

    def get_success_url(self):
        object = self.get_object()
        return reverse('posts:post-detail', kwargs={'post_pk': object.pk})

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if self.request.user == object.author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("Вы не автор! Вам нельзя! :0")


@method_decorator(login_required, name='dispatch')
class DeletePostView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_pk'
    template_name = 'posts/post_delete.html'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if self.request.user == object.author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("Вы не автор! Вам нельзя! :0")

    def get_success_url(self):
        return reverse('posts:index')


@login_required
def post_like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(request.META.get('HTTP_REFERER'), request)
