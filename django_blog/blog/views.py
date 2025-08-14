from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.db.models import Prefetch, Q
from taggit.models import Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UpdateProfileForm, UpdateUserForm, PostForm, CommentForm
from .models import Post, Comment


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
        else:
            u_form = UpdateUserForm(instance=request.user)
            p_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'blog/Profile.html', {
            'u_form': u_form,
            'p_form': p_form
        })


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    content_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = self.object.comments.select_relataed('author')
        ctx['comment_form'] = CommentForm()
        return ctx

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    
    def test_func(self):
        return self.get_object().author == self.request.user
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        return self.get_object().author == self.request.user
    

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post = get_list_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(self, form)
    
    def get_success_url(self):
        return self.object.post.get_success_url()
    
class CommentAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        comment = self.get_object()
        return comment.author_id == self.request.user.id


class CommentUpdateView(LoginRequiredMixin, CommentAuthorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return self.object.post.get_success_url()
    

class CommentDeleteView(LoginRequiredMixin, CommentAuthorRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.post.get_success_url()
    

class PostsByTagView(ListView):
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags__slug=tag_slug).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag'] = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return ctx
    
def search_view(request):
    q = request.GET.get('q', '').strip()
    results = Post.objects.none()
    if q:
        results = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)  
        ).distinct().order_by('-published_date')
    return render(request, 'blog/search_results.html', {'query': q, 'results': results})

