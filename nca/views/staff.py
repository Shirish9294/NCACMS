from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from ..forms import *
from ..models import *
from itertools import chain

now = timezone.now()


class StaffSignUpView(CreateView):
    model = User
    form_class = StaffsSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'staffs'
        # Staff.objects.create(user=**kwargs)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = form.save()
        subject = 'NCA Signup'
        message = f"Your form has been verified and your account has been created, you can login to  your account by " \
                  f"using the Username:{username} and Password:{password} "
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)
        return redirect('admins:signup')


class staff_home(ListView):
    model = Staff
    template_name = 'staff/staff.html'


@login_required
def activity_list(request):
    # activity = Activity.objects.all()
    activity = Activity.objects.filter(created_date__lte=timezone.now())
    return render(request, 'staff/activity_list.html', {'activity': activity})


@login_required
def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        # update
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.updated_date = timezone.now()
            activity.save()
            activity = Activity.objects.filter(created_date__lte=timezone.now())
            return render(request, 'staff/activity_list.html',
                          {'activity': activity})
    else:
        # edit
        form = ActivityForm(instance=activity)
    return render(request, 'staff/activity_edit.html', {'form': form})


@login_required
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    activity.delete()
    return redirect('staff:activity_list')


@login_required
def activity_new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ActivityForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            activity = form.save(commit=False)
            activity.created_date = timezone.now()
            activity.updated_date = timezone.now()
            activity.save()
            activity = Activity.objects.filter(created_date__lte=timezone.now())
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'staff/activity_list.html', {'activity': activity})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ActivityForm()

    return render(request, 'staff/activity_new.html', {'form': form})


@login_required
def activity_detail(request, pk):
    model = Activity
    activity = get_object_or_404(Activity, pk=pk)
    context = {'activity': activity}
    return render(request, 'staff/activity_detail.html', {'activity': activity})


@login_required
def activity_notes_list(request, pk):
    volunteer_activity_detail = get_object_or_404(Activity, pk=pk)
    notes_list = Notes.objects.filter(created_date__lte=timezone.now(), victim=volunteer_activity_detail.victim.id,
                                      activity=volunteer_activity_detail.id)
    return render(request, 'staff/activity_notes_list.html', {'notes_list': notes_list})

# @login_required
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
#             return render(request, 'staff/activity_notes.html',
#                           {'activity': activity})
#     else:
#         # edit
#         form = ActivityForm(instance=activity)
#     return render(request, 'staff/activity_edit.html', {'form': form})


# ----------------------------------------------------------------------------------------------------------------------

@login_required
def victim_list(request):
    victims = Victim.objects.filter(created_date__lte=timezone.now())

    page = request.GET.get('page', 1)
    paginator = Paginator(victims, 6)
    try:
        victims = paginator.page(page)
    except PageNotAnInteger:
        victims = paginator.page(1)
    except EmptyPage:
        victims = paginator.page(paginator.num_pages)

    return render(request, 'staff/victim_list.html', {'victims': victims})


@login_required
def victim_edit(request, pk):
    victim = get_object_or_404(Victim, pk=pk)
    if request.method == "POST":
        # update
        form = VictimForm(request.POST, instance=victim)
        if form.is_valid():
            victim = form.save(commit=False)
            victim.updated_date = timezone.now()
            victim.save()
            victims = Victim.objects.filter(created_date__lte=timezone.now())
            return render(request, 'staff/victim_list.html',
                          {'victims': victims})
    else:
        # edit
        form = VictimForm(instance=victim)
    return render(request, 'staff/victim_edit.html', {'form': form})


@login_required
def victim_new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VictimForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            victim = form.save(commit=False)
            victim.created_date = timezone.now()
            victim.save()
            victims = Victim.objects.filter(created_date__lte=timezone.now())
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            return render(request, 'staff/victim_list.html', {'victims': victims})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VictimForm()

    return render(request, 'staff/victim_new.html', {'form': form})


@login_required
def victim_detail(request, pk):
    victim = get_object_or_404(Victim, pk=pk)
    return render(request, 'staff/victim_detail.html', {'victim': victim})

# @login_required
# def victim_delete(request, pk):
#     victim = get_object_or_404(Victim, pk=pk)
#     victim.delete()
#     return redirect('staff:victim_list')

from django.contrib import messages


@login_required
def victim_delete(request, pk):
    victim = get_object_or_404(Victim, pk=pk)
    victims_without_activitys = Victim.objects.filter(
        activities__isnull=True)  # checking volunteers who doesnot have any entry in the activities table.
    if victim in victims_without_activitys:  # we can delete victim in this case where the choosen victim doesnot have any activity.
        # Don't remove the print statements, useful to check how the values are getting saved in each variable
        # print(victims_without_activitys) #o/p - e.g. --> <QuerySet [<Victim: Goerge>, <Victim: Katherine>, <Victim: Tom>]>
        # print(victim)
        victim.delete()
    else:  # we have to generate a pop up message in this case,where victim has an entry in the activities have an en
        messages.warning(request,
                         'The Victim you are trying to Delete is asscociated with an Activity. Delete the Activity first then delete the Victim.')
    return redirect('staff:victim_list')


# ----------------------------------------------------------------------------------------------------------------------
@login_required
def location_list(request):
    # location = Location.objects.all()
    location = Location.objects.filter(created_date__lte=timezone.now())
    return render(request, 'staff/location_list.html', {'location': location})


@login_required
def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        # update
        form = LocationForm2(request.POST, instance=location)
        if form.is_valid():
            location = form.save(commit=False)
            location.updated_date = timezone.now()
            location.save()
            location = Location.objects.filter(created_date__lte=timezone.now())
            return render(request, 'staff/location_list.html',
                          {'location': location})
    else:
        # edit
        form = LocationForm2(instance=location)
    return render(request, 'staff/location_edit.html', {'form': form})


# @login_required
# def location_delete(request, pk):
#     location = get_object_or_404(Location, pk=pk)
#     location.delete()
#     return redirect('staff:location_list')


@login_required
def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    locations_without_activitys = Location.objects.filter(
        activities__isnull=True)  # checking locations who doesnot have any entry in the activities table.
    if location in locations_without_activitys:  # we can delete volunteer in this case where the choosen volunteer doesnot have any activity.
        # Don't remove the print statements, useful to check how the values are getting saved in each variable
        # print(volunteers_without_activitys) #o/p - e.g. --> <QuerySet [<Volunteer: Goerge>, <Volunteer: Katherine>, <Volunteer: Tom>]>
        # print(volunteer)
        location.delete()
    else:  # we have to generate a pop up message in this case,where volunteer has an entry in the activities have an en
        print("do nothing")
        messages.warning(request,
                         'The Location you are trying to Delete is asscociated with an Activity. Delete the Activity first then delete the Location.')
    return redirect('staff:location_list')


@login_required
def location_new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LocationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            location = form.save(commit=False)
            location.created_date = timezone.now()
            location.save()
            location = Location.objects.filter(created_date__lte=timezone.now())
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'staff/location_list.html', {'location': location})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LocationForm()

    return render(request, 'staff/location_new.html', {'form': form})


@login_required
def location_detail(request, pk):
    model = Location
    location = get_object_or_404(Location, pk=pk)
    context = {'location': location}
    return render(request, 'staff/location_detail.html', {'location': location})


@login_required
def location_notes(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        # update
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            location = form.save(commit=False)
            location.updated_date = timezone.now()
            location.save()
            location = Location.objects.filter(created_date__lte=timezone.now())
            return render(request, 'staff/location_notes.html',
                          {'location': location})
    else:
        # edit
        form = LocationForm(instance=location)
    return render(request, 'staff/location_edit.html', {'form': form})


# ----------------------------------------------------------------------------------------------------------------------
@login_required
def volunteer_list(request):
    if User.is_volunteer:
        volunteers_list = Volunteer.objects.select_related('user')
        # volunteers_list = User.objects.filter(is_volunteer=True)   #print(volunteers_list1) #print(volunteers_other_details.user.is_volunteer)
        """page = request.GET.get('page', 2)
        paginator = Paginator(volunteers_list, 6)
        try:
            volunteers_list = paginator.page(page)
        except PageNotAnInteger:
            volunteers_list = paginator.page(1)
        except EmptyPage:
            volunteers_list = paginator.page(paginator.num_pages)"""
        return render(request, 'staff/volunteer_list.html', {'volunteer_info': volunteers_list})
    else:
        print("condition not satisfied")

@login_required
def volunteer_detail(request, pk):
    volunteer = get_object_or_404(Volunteer, pk=pk)
    user = get_object_or_404(User, pk=pk)
    return render(request, 'staff/volunteer_detail.html', {'volunteer': volunteer,'user': user})

@login_required
def volunteer_edit(request, pk):
    volunteer = get_object_or_404(Volunteer, pk=pk)
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        # update
        form = VolunteerForm2(request.POST, instance=volunteer)
        form_user = UserForm(request.POST, instance=user)
        if form.is_valid() and form_user.is_valid():
            volunteer = form.save(commit=False)
            volunteer_user = form_user.save(commit=False)
            volunteer.updated_date = timezone.now()
            volunteer.save()
            volunteer_user.save()
            volunteers = Volunteer.objects.filter(created_date__lte=timezone.now())
            # users = User.objects.filter(created_date__lte=timezone.now())
            volunteers_list = Volunteer.objects.select_related(
                'user')  # giving this statement is important, since we have to return to volunteer_list page and the data in that page is viewable only when we pass the data again to that page
            return render(request, 'staff/volunteer_list.html',
                          {'volunteers': volunteers, 'volunteer_info': volunteers_list})
    else:
        # edit
        form = VolunteerForm2(instance=volunteer)
        form_user = UserForm(instance=user)
    return render(request, 'staff/volunteer_edit.html', {'form': form, 'form_user': form_user})


# @login_required
# def volunteer_delete(request, pk):
#     volunteer = get_object_or_404(Volunteer, pk=pk)
#     user = get_object_or_404(User, pk=pk)
#     volunteer.delete()
#     user.delete()
#     return redirect('staff:volunteer_list')

# F-Implement functionality to show Warning Message “Delete the Activity associated with the volunteer/victim first to delete this volunteer/victim.” message when deleting a victim/volunteer who is associated with an activity.
from django.contrib import messages


@login_required
def volunteer_delete(request, pk):
    volunteer = get_object_or_404(Volunteer, pk=pk)
    user = get_object_or_404(User, pk=pk)
    volunteers_without_activitys = Volunteer.objects.filter(
        activities__isnull=True)  # checking volunteers who doesnot have any entry in the activities table.
    if volunteer in volunteers_without_activitys:  # we can delete volunteer in this case where the choosen volunteer doesnot have any activity.
        # Don't remove the print statements, useful to check how the values are getting saved in each variable
        # print(volunteers_without_activitys) #o/p - e.g. --> <QuerySet [<Volunteer: Goerge>, <Volunteer: Katherine>, <Volunteer: Tom>]>
        # print(volunteer)
        volunteer.delete()
        user.delete()
    else:  # we have to generate a pop up message in this case,where volunteer has an entry in the activities have an en
        print("do nothing")
        messages.warning(request,
                         'The Volunteer you are trying to Delete is asscociated with an Activity. Delete the Activity first then delete the Volunteer.')
    return redirect('staff:volunteer_list')


# ----------------------------------------------------------------------------------------------------------------------


def staff_details(request):
    current_user = request.user
    staff = Staff.objects.get(user_id=current_user.id)
    return render(request, 'staff/staff_account.html', {'staff': staff})


def staff_edit(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        staff_form = StaffForm2(request.POST, instance=request.user.staff)
        if user_form.is_valid() and staff_form.is_valid():
            user_form.save()
            staff_form.save()
            current_user = request.user
            staff = Staff.objects.get(user_id=current_user.id)
            return render(request, 'staff/staff_account.html', {'staff': staff})
    else:
        user_form = UserForm(instance=request.user)
        staff_form = StaffForm2(instance=request.user.staff)
    return render(request, 'staff/staff_account_edit.html', {'user_form': user_form, 'staff_form': staff_form})


# search----------------------------------------------------------------------
def victim_search(request):
    if request.method == "POST":
        search = request.POST['search']
        victims = Victim.objects.filter(created_date__lte=timezone.now(), first_name__contains=search)
        page = request.GET.get('page', 1)
        paginator = Paginator(victims, 6)
        try:
            victims = paginator.page(page)
        except PageNotAnInteger:
            victims = paginator.page(1)
        except EmptyPage:
            victims = paginator.page(paginator.num_pages)
        return render(request, 'staff/victim_list.html', {'victims': victims})
    else:
        return redirect('staff:victim_list')


def activity_search(request):
    if request.method == "POST":
        search = request.POST['search']
        activity = Activity.objects.filter(created_date__lte=timezone.now(), name__contains=search)
        return render(request, 'staff/activity_list.html', {'activity': activity})
    else:
        return redirect('staff:activity_list')


def volunteer_search(request):
    if request.method == "POST":
        search = request.POST['search']
        user = User.objects.filter(is_volunteer=True)
        if user:
            volunteers_list = Volunteer.objects.select_related('user'). filter(user__username__contains=search)
            return render(request, 'staff/volunteer_list.html', {'volunteer_info': volunteers_list})
        else:
            return redirect('staff:volunteer_list')
    else:
        return redirect('staff:volunteer_list')


def location_search(request):
    if request.method == "POST":
        search = request.POST['search']
        location = Location.objects.filter(created_date__lte=timezone.now(), name__contains=search)
        return render(request, 'staff/location_list.html', {'location': location})
    else:
        return redirect('staff:location_list')
# --------------------------------------------------------------------------------------------------------


@login_required
def show_notification(request):
    if User.is_staff:
        loggedin_staff = request.user.id 
        staff_activity_list = Activity.objects.filter(name__isnull=False)

        for activity_list in staff_activity_list:
            staff_activity_list1 = get_object_or_404(Activity, pk=activity_list.pk)
            notes_list = Notes.objects.filter(created_date__lte=timezone.now(),volunteer__isnull=False).order_by('updated_date').reverse()

        return render(request, 'staff/notification.html', {'notes_list': notes_list})

def Count_Notifications(request):
    count_notifications=0
    staff_activity_list = Activity.objects.filter(name__isnull=False)
    for activity_list in staff_activity_list:
     staff_activity_list1 = get_object_or_404(Activity, pk=activity_list.pk)
     count_notifications = Notes.objects.filter(created_date__lte=timezone.now(), volunteer__isnull=False,is_seen=False).count()
    return {'count_notifications': count_notifications}

def notes_details(request,pk):
    model = Notes
    notes = get_object_or_404(Notes, pk=pk)
    Activity.objects.filter(name__isnull=False)
    Notes.objects.filter(pk=pk, is_seen=False).update(is_seen=True)
    return render(request, 'staff/notes_detail.html', {'notes': notes})
