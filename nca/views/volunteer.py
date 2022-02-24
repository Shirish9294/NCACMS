from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView
from ..forms import *
from ..models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

now = timezone.now()


class VolunteerSignUpView(CreateView):
    model = User
    form_class = VolunteerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'volunteer'
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


class volunteer_home(ListView):
    model = Volunteer
    template_name = 'volunteer/volunteer.html'


# from django.views.generic.edit import CreateView, DeleteView, UpdateView
# class VolunteerActivityForm(CreateView):
#     model = Activity
#     fields = ['volunteer', 'victim', 'location', 'name', 'description', 'type', 'start_date', 'end_date',
#             'created_date', 'updated_date', 'notes']
#
#     def get_form(self, *args, **kwargs):
#         form = super(VolunteerActivityForm, self).get_form(*args, **kwargs)
#         form.fields['volunteer'].queryset = self.request.user.a_set.all()
#
#         return form

@login_required
def volunteer_activity_list(request):
    if User.is_volunteer:
        loggedin_volunteer = request.user.id  # matching names is kind of difficult,since activity.volunteer is returning "id" but not the name.So,matching Ids instead of names
        volunteer_activity_list = Activity.objects.filter(created_date__lte=timezone.now(),
                                                          volunteer=loggedin_volunteer)
        list = [0,1,2,3,4,5,6,7,8]
        """page = request.GET.get('page', 2)
                paginator = Paginator(volunteer_activity_list, 6)
                try:
                    volunteer_activity_list = paginator.page(page)
                except PageNotAnInteger:
                    volunteer_activity_list = paginator.page(1)
                except EmptyPage:
                    volunteer_activity_list = paginator.page(paginator.num_pages)"""
    return render(request, 'volunteer/volunteer_activity_list.html', {'activity': volunteer_activity_list,'list': list})


@login_required
def volunteer_activity_detail(request, pk):
    model = Activity
    volunteer_activity_detail = get_object_or_404(Activity, pk=pk)
    print('detail', volunteer_activity_detail.victim.id)
    context = {'activity': volunteer_activity_detail}
    return render(request, 'volunteer/volunteer_activity_detail.html', {'activity': volunteer_activity_detail})


from django.contrib import messages


@login_required
def volunteer_activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    print(activity.staff)
    if activity.staff == None:
        if request.method == "POST":
            # update
            form = VolunteerActivityForm(request.user.id, request.POST, instance=activity)
            if form.is_valid():
                activity = form.save(commit=False)
                activity.updated_date = timezone.now()
                activity.save()
                activity = Activity.objects.filter(created_date__lte=timezone.now(), volunteer=request.user.id)
                return render(request, 'volunteer/volunteer_activity_list.html',
                              {'activity': activity})
        else:
            # edit
            form = VolunteerActivityForm(request.user.id, instance=activity)
        return render(request, 'volunteer/volunteer_activity_edit.html', {'form': form})
    else:
        print("Not editable")
        messages.warning(request,
                         'Sorry, you do not have permission to edit this activity since it was created by a Staff Member.')
        model = Activity
        volunteer_activity_detail = get_object_or_404(Activity, pk=pk)
        print('detail', volunteer_activity_detail.victim.id)
        context = {'activity': volunteer_activity_detail}
        return render(request, 'volunteer/volunteer_activity_detail.html', {'activity': volunteer_activity_detail})


@login_required
def volunteer_activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    print(activity.staff)
    if activity.staff == None:
        activity = get_object_or_404(Activity, pk=pk)
        activity.delete()
        return redirect('nca:volunteer_activity_list')
    else:
        messages.warning(request,
                         'Sorry, you do not have permission to Delete this activity since it was created by a Staff Member.')
        return redirect('nca:volunteer_activity_list')


@login_required
def volunteer_activity_new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VolunteerActivityForm(request.user.id, request.POST)
        # check whether it's valid:
        if form.is_valid():
            activity = form.save()
            activity.created_date = timezone.now()
            activity.save()
            activity = Activity.objects.filter(created_date__lte=timezone.now(), volunteer=request.user.id)
            return render(request, 'volunteer/volunteer_activity_list.html', {'activity': activity})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VolunteerActivityForm(request.user.id)

    return render(request, 'volunteer/volunteer_activity_new.html', {'form': form})


@login_required
def volunteer_notes_list(request, pk1):
    volunteer_activity_detail = get_object_or_404(Activity, pk=pk1)
    notes_list = Notes.objects.filter(created_date__lte=timezone.now(), victim=volunteer_activity_detail.victim.id,
                                      activity=volunteer_activity_detail.id)
    return render(request, 'volunteer/volunteer_notes_list.html', {'notes_list': notes_list})


def volunteer_notes_new(request, pk2):
    # if this is a POST request we need to process the form data
    volunteer_activity_detail2 = get_object_or_404(Activity, pk=pk2)
    print(volunteer_activity_detail2.name)
    # notes = get_object_or_404(Notes, victim=volunteer_activity_detail2.victim.id,name=volunteer_activity_detail2.id)
    volunteer = volunteer_activity_detail2.volunteer
    victim = volunteer_activity_detail2.victim
    activity = get_object_or_404(Activity, pk=pk2)
    if request.method == 'POST':
        print("m here1")
        # create a form instance and populate it with data from the request:
        form = VolunteerNotesForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            notes_form = form.save(commit=False)
            notes_form.created_date = timezone.now()
            notes_form.volunteer = volunteer_activity_detail2.volunteer
            notes_form.victim = volunteer_activity_detail2.victim
            notes_form.activity = get_object_or_404(Activity, pk=pk2)
            notes_form.save()
            notes_list = Notes.objects.filter(created_date__lte=timezone.now(),
                                              victim=volunteer_activity_detail2.victim.id,
                                              activity=volunteer_activity_detail2.id)
            return render(request, 'volunteer/volunteer_notes_list.html', {'notes_list': notes_list})
    else:
        form = VolunteerNotesForm()
    return render(request, 'volunteer/volunteer_notes_new.html',
                  {'form': form, 'volunteer': volunteer, 'victim': victim, 'activity': activity})


@login_required
def volunteer_notes_edit(request, pk):
    notes = get_object_or_404(Notes, pk=pk)
    if request.method == "POST":
        # update
        form = VolunteerNotesForm(request.POST, instance=notes)
        if form.is_valid():
            notes_form = form.save(commit=False)
            notes_form.updated_date = timezone.now()
            notes_form.save()
            notes_list = Notes.objects.filter(created_date__lte=timezone.now(), volunteer=notes.volunteer.user.id,
                                              victim=notes.victim.id, activity=notes.activity.id)
            Notes.objects.filter(pk=pk, is_seen=True).update(is_seen=False)
            return render(request, 'volunteer/volunteer_notes_list.html',
                          {'notes_list': notes_list})
    else:
        # edit
        form = VolunteerNotesForm(instance=notes)
    return render(request, 'volunteer/volunteer_notes_edit.html', {'form': form})


@login_required
def volunteer_notes_delete(request, pk):
    notes_list = get_object_or_404(Notes, pk=pk)
    notes_list.delete()
    pk1 = notes_list.activity.id  # primary key of Activity table,need be passed to "volunteer_notes_list" function,otherwise it will throw errors
    return redirect('volunteer:volunteer_notes_list', pk1)


def volunteer_details(request):
    current_user = request.user
    volunteer = Volunteer.objects.get(user_id=current_user.id)
    return render(request, 'volunteer/volunteer_account.html', {'volunteer': volunteer})


def volunteer_edit(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        volunteer_form = VolunteerForm2(request.POST, instance=request.user.volunteer)
        if user_form.is_valid() and volunteer_form.is_valid():
            user_form.save()
            volunteer_form.save()
            current_user = request.user
            volunteer = Volunteer.objects.get(user_id=current_user.id)
            return render(request, 'volunteer/volunteer_account.html', {'volunteer': volunteer})
    else:
        user_form = UserForm(instance=request.user)
        volunteer_form = VolunteerForm2(instance=request.user.volunteer)
    return render(request, 'volunteer/volunteer_account_edit.html',
                  {'user_form': user_form, 'volunteer_form': volunteer_form})


@login_required
def volunteer_victim_list(request):
    if User.is_volunteer:
        loggedin_volunteer = request.user.id  # matching names is kind of difficult,since activity.volunteer is returning "id" but not the name.So,matching Ids instead of names
        volunteer_associated_victim_list = Activity.objects.values_list('victim', flat=True).filter(
            created_date__lte=timezone.now(),
            volunteer=loggedin_volunteer)
        victim_details = Victim.objects.filter(pk__in=set(volunteer_associated_victim_list))
        # victim_details = Victim.objects.filter(created_date__lte=timezone.now(), pk__in=victim)
        # print(volunteer_activity_list.name)
    return render(request, 'volunteer/volunteer_victim_list.html', {'victim': victim_details})


@login_required
def volunteer_victim_detail(request, pk):
    model = Victim
    volunteer_victim_detail = get_object_or_404(Victim, pk=pk)
    # print('detail', volunteer_activity_detail.victim.id)
    context = {'victim': volunteer_victim_detail}
    return render(request, 'volunteer/volunteer_victim_detail.html', {'victim': volunteer_victim_detail})


# Search ----------------------------------------------------------------------------------------------------


def volunteer_victim_search(request):
    if request.method == "POST":
        search = request.POST['search']
        if User.is_volunteer:
            loggedin_volunteer = request.user.id
            volunteer_associated_victim_list = Activity.objects.values_list('victim', flat=True).filter(
                created_date__lte=timezone.now(),
                volunteer=loggedin_volunteer)
            victim_details = Victim.objects.filter(pk__in=set(volunteer_associated_victim_list),
                                                   first_name__contains=search)
            return render(request, 'volunteer/volunteer_victim_list.html', {'victim': victim_details})
    else:
        return redirect('volunteer: volunteer_victim_list')


def volunteer_activity_search(request):
    if User.is_volunteer:
        loggedin_volunteer = request.user.id
        if request.method == "POST":
            search = request.POST['search']
            volunteer_activity_list = Activity.objects.filter(created_date__lte=timezone.now(), volunteer=loggedin_volunteer, name__contains=search)
            return render(request, 'volunteer/volunteer_activity_list.html', {'activity': volunteer_activity_list})
        else:
            return redirect('volunteer:volunteer_activity_list')

# ------------------------------------------------------------------------------------------------------------------------
