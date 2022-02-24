# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
# from django.contrib.auth.mixins import LoginRequiredMixin  # New
# from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect, reverse
# from .models import *
# from .forms import *
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login, logout
# from django.urls import reverse_lazy
# from .models import Activity
# # from nca import request
# from .forms import ActivityForm
# from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
#
#
# Create your views here.
#
# def volunteerLogin(request):
#     if request.method == "GET":
#         return render(request, "nca/volunteer_login.html", {})
#
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(username=email, password=password,)
#             if user is None:
#                 return render(
#                     request,
#                     "nca/volunteer_login.html",
#                     {"errors": {"account_error": ["Invalid email or password"]}},
#                 )
#
#             elif user is not None:
#                 if user.is_active and user.is_volunteer:
#                     login(request, user)
#                     return HttpResponseRedirect(reverse("nca:home_volunteer",))
#                 elif user.is_active and user.is_volunteer is False:
#                     return render(
#                         request,
#                         "nca/volunteer_login.html",
#                         {
#                             "errors": {
#                                 "account_error": ["Email is not associated with Mentor"]
#                             }
#                         },
#                     )
#
#                 else:
#                     return HttpResponse(
#                         "# your account is inactive contact admin for details user@example.com"
#                     )
#
#             else:
#                 pass
#         else:
#             return render(request, "nca/volunteer_login.html", {"errors": form.errors})
#
#
# def staffLogin(request):
#     if request.method == "GET":
#         return render(request, "nca/staff_login.html", {})
#
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(username=email, password=password,)
#             if user is None:
#                 return render(
#                     request,
#                     "nca/staff_login.html",
#                     {"errors": {"account_error": ["Invalid email or password"]}},
#                 )
#
#             elif user is not None:
#                 if user.is_active and user.is_staff:
#                     login(request, user)
#                     return HttpResponseRedirect(reverse("nca:home_staff",))
#                 elif user.is_active and user.is_volunteer is False:
#                     return render(
#                         request,
#                         "nca/staff_login.html",
#                         {
#                             "errors": {
#                                 "account_error": ["Email is not associated with Staff"]
#                             }
#                         },
#                     )
#
#                 else:
#                     return HttpResponse(
#                         "# your account is inactive contact admin for details user@example.com"
#                     )
#
#             else:
#                 pass
#         else:
#             return render(request, "nca/staff_login.html", {"errors": form.errors})
#
#
# def change_password(request):
#     form = PasswordChangeForm(user=request.user, data=request.POST)
#     if request.method == 'GET':
#         return render(request, "nca/password_change_form.html", {"form": form})
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return render(
#                 request, "nca/password_change_done.html", {}
#             )
#         return render(
#             request, "nca/password_change_form.html", {"errors": form.errors}
#         )
#
#
#
# """def homepage(request):
#     print('yessss')
#     return render(request, "nca/landing_page.html", {})"""
#
# # Create your views here.
# now = timezone.now()
# def home(request):
#    return render(request, 'nca/home.html',
#                  {'nca': home})
#
# def home_volunteer(request):
#    return render(request, 'nca/home_volunteer.html',
#                  {'nca': home_volunteer})
#
# def home_staff(request):
#    return render(request, 'nca/home_staff.html',
#                  {'nca': home_staff})
#
# def user_logout(request):
#     logout(request)
#     return redirect(reverse("nca:home"))
#
# -------------------------------------------------------------------------------------------------------------
#
#
# @login_required
# def activity_list(request):
#     activity = Activity.objects.all()
#     activity = Activity.objects.filter(created_date__lte=timezone.now())
#
#     return render(request, 'staff/activity_list.html', {'activity': activity})
#
#
# @login_required
# def activity_edit(request, pk):
#     activity = get_object_or_404(Activity, pk=pk)
#     if request.method == "POST":
#         # update
#         form = ActivityForm(request.POST, instance=activity)
#         if form.is_valid():
#             activity = form.save(commit=False)
#             activity.updated_date = timezone.now()
#             activity.save()
#             activity = Activity.objects.filter(created_date__lte=timezone.now())
#             return render(request, 'staff/activity_list.html',
#                           {'activity': activity})
#     else:
#         # edit
#         form = ActivityForm(instance=activity)
#     return render(request, 'staff/activity_edit.html', {'form': form})
#
#
# @login_required
# def activity_delete(request, pk):
#     activity = get_object_or_404(Activity, pk=pk)
#     activity.delete()
#     return redirect('staff:activity_list')
#
#
# def activity_new(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = ActivityForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             activity = form.save(commit=False)
#             activity.created_date = timezone.now()
#             activity.save()
#             activity = Activity.objects.filter(created_date__lte=timezone.now())
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return render(request, 'nca/activity_list.html', {'activity': activity})
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = ActivityForm()
#
#     return render(request, 'nca/activity_new.html', {'form': form})
#
#
# def activity_detail(request, pk):
#     model = Activity
#     activity = get_object_or_404(Activity, pk=pk)
#     context = {'activity': activity}
#     return render(request, 'nca/activity_detail.html', {'activity': activity})
#
#
# def activity_notes(request, pk):
#     activity = get_object_or_404(Activity, pk=pk)
#     if request.method == "POST":
#         # update
#         form = ActivityForm(request.POST, instance=activity)
#         if form.is_valid():
#             activity = form.save(commit=False)
#             activity.updated_date = timezone.now()
#             activity.save()
#             activity = Activity.objects.filter(created_date__lte=timezone.now())
#             return render(request, 'nca/activity_notes.html',
#                           {'activity': activity})
#     else:
#         # edit
#         form = ActivityForm(instance=activity)
#     return render(request, 'nca/activity_edit.html', {'form': form})
#
#
