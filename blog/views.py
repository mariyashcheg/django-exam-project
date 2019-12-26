from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import Blog, Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
class BlogListView(ListView):    
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blog_list'

class BlogDetailView(LoginRequiredMixin, DetailView): 
    model = Blog
    template_name = 'blog/blog_details.html'
    context_object_name = 'blog_details'

class PostListView(ListView):    
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

class PostDetailView(LoginRequiredMixin, DetailView): 
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post_details'

    def post(self, request,  **kwargs):
        form = CommentForm(request.POST)
        post_inst = get_object_or_404(Post, pk=kwargs['pk'])

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post_inst
            comment.save()
            return redirect('post-details', **kwargs)
        
        return redirect('post-details', **kwargs)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post  
    form_class = PostForm
    template_name = 'blog/create_post.html'
    success_url = 'post-list'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user  
        instance.save()
        return redirect(reverse(self.success_url))

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post  
    form_class = PostForm
    template_name = 'blog/create_post.html'
    success_url = 'post-details'

    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.update_date = timezone.now()  
        instance.save()
        return redirect(reverse(self.success_url, kwargs={'pk':instance.pk}))

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post  
    template_name = 'blog/delete_post.html'
    success_url = 'post-list'

    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(self.success_url)

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment  
    form_class = CommentForm
    template_name = 'blog/edit_comment.html'
    success_url = 'post-details'

    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.update_date = timezone.now()  
        instance.save()
        return redirect(reverse(self.success_url, kwargs={'pk':instance.post.pk}))

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment  
    template_name = 'blog/delete_comment.html'
    success_url = 'post-details'

    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        instance = self.get_object()
        return reverse(self.success_url, kwargs={'pk':instance.post.pk})
