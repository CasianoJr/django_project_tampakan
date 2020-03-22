from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Office, Appointment
from .forms import CreateAppointmentForm
from django.contrib import messages


def office_list(request):
    context = {'offices': Office.objects.all()}
    return render(request, 'office/office_list.html', context)


def office_page(request, pk):
    context = {'office': get_object_or_404(Office, pk=pk)}
    return render(request, 'office/office_page.html', context)


def create_appointment(request):
    form = CreateAppointmentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            office = form.cleaned_data.get('office')
            messages.success(
                request, f'Your Appoinment to "{office}" is successfully created.')
            return redirect(reverse('appointment-detail', kwargs={
                'pk': form.instance.pk}))
    context = {'form': form}
    return render(request, 'office/create_appointment.html', context)


def appointment_detail(request, pk):
    context = {'appointment': get_object_or_404(Appointment, pk=pk)}
    return render(request, 'office/appointment_detail.html', context)
