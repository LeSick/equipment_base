from django.shortcuts import render, redirect
from .forms import RegistrationRequestForm

def registration_request_view(request):
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/request_sent.html')
    else:
        form = RegistrationRequestForm()
    return render(request, 'accounts/request_access.html', {'form': form})
