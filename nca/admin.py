from django.contrib import admin
from .models import User, Staff, Volunteer, Victim, Location, Activity,Notes
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import csv


class ActivityExportCsvMixin:
    def export_as_csv(self, request, queryset):
        activities = Activity.objects.all().only("id", "location", "volunteer", "staff", "victim", "name",
                                                 "description", "type", "start_date", "end_date", "created_date",
                                                 "updated_date", "notes")
        formatted_field_names = ['Activity ID', 'Location', 'Volunteer', 'Staff', "Victim", "Activity Name",
                                 "Description", "Type", "Start Date", "End Date", "Created Date", "Updated Date",
                                 "Notes"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Activities_report.csv'
        writer = csv.writer(response)
        writer.writerow(formatted_field_names)

        for activity in queryset:
            writer.writerow([activity.id, activity.location, activity.volunteer, activity.staff, activity.victim,
                             activity.name, activity.description, activity.type, activity.start_date, activity.end_date,
                             activity.created_date, activity.updated_date, activity.notes])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class UsersExportCsvMixin:
    def export_as_csv(self, request, queryset):
        # users = Users.objects.all().only("id", "username", "first_name", "last_name", "email", "is_active",
        #                                          "is_superuser", "is_staffs", "is_volunteer")
        formatted_field_names = ['User ID', 'Username', 'First Name', 'Last Name', "Email ID", "Active User",
                                 "Super User", "Staff", "Volunteer"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Users_report.csv'
        writer = csv.writer(response)
        writer.writerow(formatted_field_names)

        for user in queryset:
            writer.writerow([user.id, user.username, user.first_name, user.last_name, user.email,
                             user.is_active, user.is_superuser, user.is_staffs, user.is_volunteer])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class VolunteersExportCsvMixin:
    def export_as_csv(self, request, queryset):
        # volunteers = Volunteers.objects.all().only("id", "username", "first_name", "last_name", "email", "is_active",
        #                                          "phone", "experience", "created_date", "updated_date")
        formatted_field_names = ['Username', 'First Name', 'Last Name', "Email ID", "Active User",
                                 "Phone", "Experience", "Created Date", "Updated Date"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Volunteers_report.csv'
        writer = csv.writer(response)
        writer.writerow(formatted_field_names)

        for volunteer in queryset:
            writer.writerow([volunteer.user.username, volunteer.user.first_name, volunteer.user.last_name,
                             volunteer.user.email, volunteer.user.is_active, volunteer.phone, volunteer.experience,
                             volunteer.created_date, volunteer.updated_date])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class StaffsExportCsvMixin:
    def export_as_csv(self, request, queryset):
        # staffs = Staffs.objects.all().only("id", "username", "first_name", "last_name", "email", "is_active",
        #                                          "phone", "created_date", "updated_date")
        formatted_field_names = ['Username', 'First Name', 'Last Name', "Email ID", "Active User",
                                 "Phone", "Created Date", "Updated Date"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Staffs_report.csv'
        writer = csv.writer(response)
        writer.writerow(formatted_field_names)

        for staff in queryset:
            writer.writerow([staff.user.username, staff.user.first_name, staff.user.last_name, staff.user.email,
                             staff.user.is_active, staff.phone, staff.created_date, staff.updated_date])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class LocationExportCsvMixin:
    def export_as_csv(self, request, queryset):
        # locations = Location.objects.all().only("id", "name", "type", "address", "city", "state",
        #                                         "zipcode", "created_date", "updated_date")
        formatted_field_names = ['Location ID', 'Location Name', 'Type', 'Address', "City", "State",
                                 "Zipcode", "Created Date", "Updated Date"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Locations_report.csv'
        writer = csv.writer(response)
        writer.writerow(formatted_field_names)

        for location in queryset:
            writer.writerow([location.id, location.name, location.type, location.address, location.city,
                             location.state, location.zipcode, location.created_date, location.updated_date])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class VictimsExportCsvMixin:
    def export_as_csv(self, request, queryset):
        # victims = Victims.objects.all().only("id", "first_name", "last_name", "address", "city", "state",
        #                                          "zipcode", "phone", "email", "disease_type", "notes", "created_date",
        #                                          "updated_date")
        formatted_field_names = ['Victim ID', 'First Name', 'Last Name', "Address", "City", "State", "Zipcode",
                                 "Phone", "Email ID", "Disease Type", "Notes", "Created Date", "Updated Date"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Victims_report.csv'
        writer = csv.writer(response)
        writer.writerow(formatted_field_names)

        for victim in queryset:
            writer.writerow([victim.id, victim.first_name, victim.last_name, victim.address, victim.city, victim.state,
                             victim.zipcode, victim.phone, victim.email, victim.disease_type, victim.notes,
                             victim.created_date, victim.updated_date])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


def username(instance):  # name of the method should be same as the field given in `list_display`
    try:
        return instance.user.username
    except ObjectDoesNotExist:
        return 'ERROR!!'


class UserList(admin.ModelAdmin, UsersExportCsvMixin):
    list_display = ('username', 'get_full_name', 'email', 'is_staffs', 'is_volunteer', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ['username', 'is_staffs', 'is_volunteer', 'is_superuser']
    ordering = ['username', 'is_staffs', 'is_volunteer', 'is_superuser']
    actions = ["export_as_csv"]


class StaffList(admin.ModelAdmin, StaffsExportCsvMixin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone')
    search_fields = ('username', 'email')
    actions = ["export_as_csv"]

    def username(self, instance):
        try:
            return instance.user.username
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def first_name(self, instance):
        try:
            return instance.user.first_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def last_name(self, instance):
        try:
            return instance.user.last_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def email(self, instance):
        try:
            return instance.user.email
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def phone(self, instance):
        try:
            return instance.phone
        except ObjectDoesNotExist:
            return 'ERROR!!'


class VolunteerList(admin.ModelAdmin, VolunteersExportCsvMixin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone', 'experience')
    search_fields = ('username', 'email')
    actions = ["export_as_csv"]

    def username(self, instance):
        try:
            return instance.user.username
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def first_name(self, instance):
        try:
            return instance.user.first_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def last_name(self, instance):
        try:
            return instance.user.last_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def email(self, instance):
        try:
            return instance.user.email
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def phone(self, instance):
        try:
            return instance.phone
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def experience(self, instance):
        try:
            return instance.experience
        except ObjectDoesNotExist:
            return 'ERROR!!'


class VictimList(admin.ModelAdmin, VictimsExportCsvMixin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'disease_type', 'notes')
    list_filter = ('first_name', 'disease_type', 'notes')
    search_fields = ('first_name', 'disease_type', 'notes')
    actions = ["export_as_csv"]


class LocationList(admin.ModelAdmin, LocationExportCsvMixin):
    list_display = ('name', 'address', 'type', 'city', 'state', 'zipcode')
    list_filter = ('type', 'city')
    search_fields = ('type', 'city')
    actions = ["export_as_csv"]


class ActivityList(admin.ModelAdmin, ActivityExportCsvMixin):
    list_display = ('name', 'description', 'type', 'start_date', 'end_date', 'notes')
    list_filter = ('name', 'type')
    search_fields = ('name', 'type')
    actions = ["export_as_csv"]

class NotesList(admin.ModelAdmin):
    list_display = ('volunteer', 'victim','activity', 'notes')
    list_filter = ('victim', 'activity')
    search_fields = ('victim', 'activity')

admin.site.register(User, UserList)
admin.site.register(Staff, StaffList)
admin.site.register(Volunteer, VolunteerList)
admin.site.register(Victim, VictimList)
admin.site.register(Location, LocationList)
admin.site.register(Activity, ActivityList)
admin.site.register(Notes,NotesList)
