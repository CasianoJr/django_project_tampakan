from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile, Statistics
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic import View, ListView
from blog.models import Post


class HomeView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Tampakan Website',
            'tourism_latest': Post.objects.filter(category__exact='TM').order_by('-timestamp')[:7],
            'tourism_featured': Post.objects.filter(featured__exact=True, category__exact='TM').order_by('-timestamp')[:3],
            'tampakan_stats': Statistics.objects.all().order_by('pk')[:5],
            'carousel6': Post.objects.filter(featured__exact=True).order_by('-timestamp')[:6],
            'featured_news': Post.objects.filter(category__exact='NS').order_by('-timestamp')[:4]
        }
        return render(request, 'home.html', context)


class TouristAttractionView(ListView):
    queryset = Post.objects.filter(category__exact='TM')
    context_object_name = 'tourist_attraction'
    ordering = ['-timestamp']
    template_name = 'touristAttraction.html'
    paginate_by = 5


class NewsView(ListView):
    queryset = Post.objects.filter(category__exact='NS')
    context_object_name = 'tourist_attraction'
    ordering = ['-timestamp']
    template_name = 'news.html'
    paginate_by = 5


class ServicesView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'services.html', context)


class CarrersView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'carrers.html', context)


def register(request):
    if request.method == 'POST':
        registration = UserCreationForm(request.POST)
        if registration.is_valid():
            registration.save()
            username = registration.cleaned_data.get('username')
            password = registration.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(
                request, f'Your account, {username} has been successfully created, You may now create a post or update your profile.')
            return redirect('user-profile-update')
    context = {
        'title': 'Register',
        'form': UserCreationForm()
    }
    return render(request, 'user/register.html', context)


@login_required
def profile_user(request, pk):
    user_profile = get_object_or_404(Profile, pk=pk)
    context = {
        'title': 'Profile page',
        'obj': user_profile
    }
    return render(request, 'user/profile.html', context)


@login_required
def profile_update(request):
    user_form = UserUpdateForm(
        request.POST or None, request.FILES or None, instance=request.user)
    profile_form = ProfileUpdateForm(
        request.POST or None, request.FILES or None, instance=request.user.profile)
    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'You profile is successfully updated!')
            return redirect('/')
    context = {
        'title': 'Update Profile',
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user/update_profile.html', context)
