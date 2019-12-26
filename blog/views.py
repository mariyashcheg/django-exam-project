from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Blog, Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
class BlogListView(ListView):    
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blog_list'

class BlogDetailView(DetailView): 
    model = Blog
    template_name = 'blog/blog_details.html'
    context_object_name = 'blog_details'

class PostListView(ListView):    
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

class PostDetailView(DetailView): 
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
    
class PostCreateView(CreateView):
    model = Post  
    form_class = PostForm
    template_name = 'blog/create_post.html'
    success_url = 'post-list'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user  
        instance.save()
        return redirect(reverse(self.success_url))



