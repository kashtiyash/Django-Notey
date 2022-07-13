from msilib.schema import ListView
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.contrib.staticfiles.views import serve
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)



# Create your views here.


def index(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'mainapp/home.html', context)


def search(request):
    template = 'mainapp/home.html'

    query = request.GET.get('q')

    result = Post.objects.filter(
                    Q(title_icontains=query) |
                    Q(author__username__icontains=query) |
                    Q(content__icontains=query)
        )
    
    context = {'posts': result}
    return render(request,template,context)
    

def getFile(request):
    return serve(request, 'File')


class PostDetailView(DetailView):
    model = Post
    template_name = 'mainapp/post_detail.html'


class PostListView(ListView):
    model = Post
    template_name = 'mainapp/home.html'
    context_object_name =  'posts'
    ordering = ['-date_posted']



class UserPostListView(ListView):
    model = Post
    template_name = 'mainapp/user_posts.html' 
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'mainapp/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'mainapp/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'mainapp/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def about(request):
    return render(request, 'mainapp/about.html', {'title': 'About'})