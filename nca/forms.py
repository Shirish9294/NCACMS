from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms.widgets import DateInput, DateTimeInput
from django.utils import timezone
from nca.models import (User, Staff, Volunteer, Activity, Victim, Location, Notes, Volunteerinfo)


class StaffsSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staffs = True
        if commit:
            user.save()
            staff = Staff.objects.create(user=user)
        return user


class VolunteerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_volunteer = True
        user.save()
        volunteer = Volunteer.objects.create(user=user)
        return user


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


"""ActivityType_CHOICES =(
    ("Group Activity (In-person)", "Group Activity (In-person)"),
    ("One-One (In-person)", "One-One (In-person)"),
    ("Group Activity (Virtual)", "Group Activity (Virtual)"),
    ("One-One (Virtual)", "One-One (Virtual)"),
)"""


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            'staff', 'volunteer', 'victim', 'location', 'name', 'description', 'type', 'start_date', 'end_date',
            'created_date', 'updated_date', 'notes')
        widgets = {
            # 'type': forms.Select(choices=ActivityType_CHOICES),
            'start_date': DateTimeInput(),
            'end_date': DateTimeInput(),
            'created_date': DateInput(attrs={'type': 'date'}),
            'updated_date': DateInput(attrs={'type': 'date'}),
        }
        # widgets = {
        #     'start_date_time': DateTimeInput(),
        #     'end_date_time': DateTimeInput(),
        #     'description': forms.Textarea(attrs={'placeholder': 'Add description..', })
        # }

    def clean(self):
        cleaned_data = super(ActivityForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise forms.ValidationError('End date should be greater than Startdate.')



class VolunteerActivityForm(forms.ModelForm):

    def __init__(self,user, *args, **kwargs):
        super(VolunteerActivityForm, self).__init__(*args, **kwargs)
        self.fields['volunteer'].queryset = Volunteer.objects.filter(user=user)  #user=request.user.id passed while calling from views
        victim_activity = Activity.objects.values_list('victim',flat=True).filter(created_date__lte=timezone.now(), volunteer=user)
        self.fields['victim'].queryset = Victim.objects.filter(pk__in=set(victim_activity)) #after getting the list of victims associated to the logged in volunteer,just pulling the first_name which is the primary key in the victim table

    class Meta:
        model = Activity
        fields = (
            'volunteer', 'victim', 'location', 'name', 'description', 'type', 'start_date', 'end_date',
            'created_date', 'updated_date', 'notes')
        widgets = {
            # 'type': forms.Select(choices=ActivityType_CHOICES),
            'start_date': DateTimeInput(),
            'end_date': DateTimeInput(),
            'created_date': DateInput(attrs={'type': 'date'}),
            'updated_date': DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super(VolunteerActivityForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise forms.ValidationError('End date should be greater than Startdate.')


"""LocationType_CHOICES =(
    ("Outdoor", "Outdoor"),
    ("Indoor", "Indoor"),
    ("Virtual", "Virtual"),
)"""


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'address', 'type', 'city', 'state', 'zipcode', 'created_date', 'updated_date')
        widgets = {
            # 'type': forms.Select(choices=LocationType_CHOICES),
            'created_date': DateInput(attrs={'type': 'date'}),
            'updated_date': DateInput(attrs={'type': 'date'}),
        }

class LocationForm2(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'address', 'type', 'city', 'state', 'zipcode')


class VictimForm(forms.ModelForm):
    class Meta:
        model = Victim
        fields = (
            'first_name', 'last_name', 'address', 'city', 'state', 'zipcode', 'phone', 'email', 'disease_type',
            'notes',)


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ('phone', 'experience', 'created_date', 'updated_date')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('phone', 'created_date', 'updated_date')


class VolunteerNotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        # fields = ('volunteer','victim',  'name', 'notes')
        fields = ('notes',)


class StaffForm2(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('phone',)


class VolunteerForm2(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ('phone', 'experience',)


class VolunteerRequestForm(forms.ModelForm):
    class Meta:
        model = Volunteerinfo
        fields = ('first_name', 'last_name', 'address', 'city', 'state', 'phone', 'email', 'zipcode', 'Experience')
