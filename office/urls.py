from django.urls import path
from .views import office_list, office_page, create_appointment, appointment_detail


urlpatterns = [
    path('', office_list, name='office-list'),
    path('<pk>/', office_page, name='office-page'),
    path('create/appointment/', create_appointment, name='create-appointment'),
    path('appointment/<pk>/', appointment_detail, name='appointment-detail'),
]
