from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView
from .forms import CreatePostForm
from .models import Post, Comment
from core.models import Profile


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        comments = Comment()
        comments.comment = request.POST['comment']
        comments.post = post
        comments.user = request.user
        comments.save()
    context = {
        'title': 'Blog Details',
        'post': post,
        'latest_post': Post.objects.all().order_by('-timestamp').exclude(slug=slug)[:4],
    }
    return render(request, 'blog/post.html', context)


@login_required
def blog_create(request):
    form = CreatePostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = request.user.profile
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(
                request, f'Your article titled "{title}" is now posted.')
            return redirect(reverse('blog-detail', kwargs={
                'slug': form.instance.slug}))
    context = {
        'title': 'Create',
        'form': form
    }
    return render(request, 'blog/create.html', context)


@login_required
def blog_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author.user:
        form = CreatePostForm(request.POST or None,
                              request.FILES or None, instance=post)
        if request.method == 'POST':
            if form.is_valid():
                form.instance.author = Profile.objects.get(
                    user=request.user)
                form.save()
                title = form.cleaned_data.get('title')
                messages.success(
                    request, f'Your post titled "{title}" is now updated')
                return redirect(reverse('blog-detail', kwargs={
                    'slug': form.instance.slug}))
        context = {
            'title': 'Update',
            'form': form
        }
        return render(request, 'blog/create.html', context)
    else:
        messages.info(request,
                      'You are trying to update someones post, please log in correct credentials.')
        return redirect('user-login')


@login_required
def blog_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        Post.objects.get(slug=slug).delete()
        return redirect('blog-featured')
    return render(request, 'blog/delete.html', {'post': post})


def blog_search(request):
    queryset = ''
    query = request.GET.get('search')
    latest_post = Post.objects.all().order_by('-timestamp')[:10]
    if query:
        query = query.strip(' ')
        queryset = Post.objects.filter(Q(title__icontains=query) | Q(
            heading__icontains=query) | Q(content__icontains=query)).distinct()
    context = {
        'queryset': queryset,
        'query': query,
        'latest_post': latest_post
    }
    return render(request, 'blog/search.html', context)


class ArticleList(ListView):
    model = Post
    template_name = 'blog/articles.html'
    context_object_name = 'posts'
    ordering = ['-timestamp']
    paginate_by = 5
