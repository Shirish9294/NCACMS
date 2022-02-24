from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from ..forms import *
from ..models import *

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admins:signup')
        elif request.user.is_staffs:
            return redirect('staff:staff_home')
        else:
            return redirect('volunteer:volunteer_home')
    return render(request, 'nca/home.html')


def volunteer_request(request):
    if request.method == "POST":
        form = VolunteerRequestForm(request.POST)
        if form.is_valid():
            request = form.save(commit=False)
            request.created_date = timezone.now()
            request.save()
            requests = Volunteerinfo.objects.filter(created_date__lte=timezone.now())
            return redirect('request_sent')
    else:
        form = VolunteerRequestForm()
    return render(request, 'registration/volunteer_request.html', {'form': form})


def request_sent(request):
    return render(request, 'registration/request_sent.html')
