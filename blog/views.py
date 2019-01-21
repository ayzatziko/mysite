from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

# Create your views here.
class AboutView(TemplateView):
  template_name = 'blog/about.html'

class PostsListView(ListView):
  model = Post
  template_name = 'blog/posts_list.html'
  context_object_name = 'posts'

  def get_queryset(self):
    return Post.objects.filter(published__lte=timezone.now()).order_by('-published')


class PostDetail(DetailView):
  model = Post


class CreatePostView(CreateView, LoginRequiredMixin):
  login_url = '/login/'
  redirect_field_name = 'blog/post_detail.html'
  form_class = PostForm
  model = Post


class UpdatePostView(UpdateView, LoginRequiredMixin):
  login_url = '/login/'
  redirect_field_name = 'blog/post_detail.html'
  form_class = PostForm
  model = Post


class DeletePostView(DeleteView, LoginRequiredMixin):
  login_url = '/login/'
  redirect_field_name = 'blog/post_detail.html'
  model = Post
  template_name = 'blog/confirm_delete_post.html'

  success_url = reverse_lazy('blog:posts_list')


class DraftsListView(ListView, LoginRequiredMixin):
  login_url = '/login/'
  redirect_field_name = 'blog/post_detail.html'
  model = Post
  template_name = 'blog/posts_list.html'

  context_object_name = 'posts'

  def get_queryset(self):
    return Post.objects.filter(published__isnull=True)


@login_required
def add_comment_to_post(request, pk):
  post = get_object_or_404(Post, pk=pk)

  if request.method == "POST":
    form = CommentForm(request.POST)

    if form.is_valid():
      comment = form.save(commit=False)

      comment.post = post
      comment.save()
      return redirect('blog:post_detail', pk=post.pk)
  else:
    form = CommentForm()

  return render(request, 'blog/comment_form.html', context={'form': form})


@login_required
def approve_comment(request, pk):
  comment = get_object_or_404(Comment, pk=pk)
  comment.approve()

  return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def remove_comment(request, pk):
  comment = get_object_or_404(Comment, pk=pk)
  post_pk = comment.post.pk
  comment.delete()

  return redirect('blog:post_detail', pk=post_pk)


@login_required
def publish_post(request, pk):
  post = get_object_or_404(Post, pk=pk)
  post.publish()

  return redirect('blog:post_detail', pk=post.pk)
