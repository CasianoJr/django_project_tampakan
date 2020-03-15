from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('touristAttraction/', views.TouristAttractionView.as_view(),
         name='touristAtrraction'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('carrers/', views.CarrersView.as_view(), name='carrers'),


    path('user/register/', views.register, name='user-register'),
    path('user/profile/<pk>/', views.profile_user, name='user-profile'),
    path('user/profile/', views.profile_update, name='user-profile-update'),
    path('user/login/', auth_views.LoginView.as_view(template_name='user/login.html'),
         name='user-login'),
    path('user/logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'),
         name='user-logout'),

]
