from django.db import models
from .option import BARANGAY_OPTION, OFFICE_OPTION
from django.shortcuts import reverse
from tinymce.models import HTMLField


class Office(models.Model):
    name = models.CharField(max_length=120)
    head = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('office-page', kwargs={'pk': self.pk})

    @property
    def get_appointments(self):
        return self.related_appoinment.all()

    @property
    def get_services(self):
        return self.related_service.all()


class Appointment(models.Model):
    office = models.ForeignKey(
        Office, related_name='related_appoinment', on_delete=models.CASCADE)
    transaction = models.TextField(max_length=250, help_text=(
        'Input your transaction. e.g. "Meeting po tayo, tungkol sa kaularan" Maximum of 3000 characters'))
    name = models.CharField(max_length=100)
    barangay = models.CharField(max_length=2, choices=BARANGAY_OPTION)
    contact = models.CharField(max_length=15)
    date = models.DateField(auto_now=False, auto_now_add=False)
    timestamp = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('appointment-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name} to {self.office}'


class Service(models.Model):
    office = models.ForeignKey(
        Office, related_name='related_service', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    content = models.TextField()
    annotate = HTMLField('Content', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('service-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title} for {self.office}'
