from django.shortcuts import render
from django.views import generic
from .models import Post

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = 'index.html'
    paginate_by = 5

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
