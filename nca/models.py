from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.dispatch import receiver


class Choices(models.Model):
    ActivityType_CHOICES = (
        ("One-on-One Activity", "One-on-One Activity"),
        ("Group Activity", "Group Activity"),
        ("Public Activity", "Public Activity"),
        ("Virtual Activity", "Virtual Activity"),
    )

    LocationType_CHOICES = (
        ("Indoor", "Indoor"),
        ("Outdoor", "Outdoor"),
        ("Virtual", "Virtual"),
    )


# Create your models here.
class User(AbstractUser):
    is_staffs = models.BooleanField(default=False)
    is_volunteer = models.BooleanField(default=False)


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.user.username


class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    experience = models.CharField(max_length=200)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(default=timezone.now)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    # @receiver(post_save, sender=User)
    # def first_mail(sender, instance, **kwargs):
    #     if kwargs['created']:
    #         #user_email = instance.Volunteer.email
    #         user_email = 'jpailla@unomaha.edu'
    #         subject, from_email, to = 'New Post', 'mswproject.uno@gmail.com', 'jpailla@unomaha.edu'
    #
    #         text_content = "A new volunteer has been inserted"
    #         # html_content = render_to_string('post/mail_post.html')
    #
    #         # create the email, and attach the HTML version as well.
    #         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #         # msg.attach_alternative(html_content, "text/html")
    #         msg.send()

    def __str__(self):
        return self.user.username


class Victim(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    zipcode = models.CharField(max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True)
    disease_type = models.CharField(max_length=50)
    notes = models.CharField(max_length=500, blank=True)
    created_date = models.DateField(default=timezone.now, blank=True)
    updated_date = models.DateField(default=timezone.now, blank=True)

    def __str__(self):
        return self.first_name

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()


class Location(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=Choices.LocationType_CHOICES,
                            default=Choices.LocationType_CHOICES[0][1])
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    created_date = models.DateField(default=timezone.now, blank=True)
    updated_date = models.DateField(default=timezone.now, blank=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.name)


class Activity(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='activities')
    volunteer = models.ForeignKey(Volunteer, on_delete=models.DO_NOTHING, related_name='activities')
    staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, related_name='activities', null=True)
    victim = models.ForeignKey(Victim, on_delete=models.DO_NOTHING, related_name='activities')
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=Choices.ActivityType_CHOICES,
                            default=Choices.ActivityType_CHOICES[0][1])
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateField(default=timezone.now, blank=True)
    updated_date = models.DateField(default=timezone.now, blank=True)
    notes = models.TextField(max_length=200, blank=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Activities"


############ sending email upon change in Activity ##############
from django.db.models import signals
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.mail import send_mail
from datetime import date
import pytz

# signal used for is_active=False to is_active=True
# @receiver(pre_save, sender=Activity, dispatch_uid='active')
# def active(sender, instance, **kwargs):
#     subject = 'Activity added'
#     mesagge = 'A new activity has been added'
#     from_email = settings.EMAIL_HOST_USER
#     to_email = ['jpailla@unomaha.edu','sindhurapailla14@gmail.com']
#     #to_email = Victim.email
#     send_mail(subject, mesagge, from_email, to_email, fail_silently=False)

############ @receiver pre_save is working for both insert and update, post_save functionality is overriden by pre-save ##########
"""@receiver(post_save, sender=Activity)
def first_mail(sender, instance, **kwargs):
    if kwargs['created']:
        user_email = [instance.victim.email,instance.volunteer.user.email]
        #user_email = ['jpailla@unomaha.edu','smoorthi@unomaha.edu']
        subject, from_email, to = 'NCACMS Activity', 'mswproject.uno@gmail.com', user_email#'jpailla@unomaha.edu'

        text_content = "Hello," + "\n" + \
                       "A new activity has been created for you. Please find the details of it below :" + "\n" + "\n" +  "\n" +  "\n" +\
                       "activity_name : " + instance.name + "\n" + \
                       "Location : "+ instance.location.name + "\n" +\
                       "Volunteer : " + instance.volunteer.user.first_name + "\n" +\
                        "Victim : " + instance.victim.first_name + "\n" + \
                       "Activity start date : "+ str(instance.start_date) + "\n" +  \
                       "Activity End date : " + str(instance.end_date) + "\n" + \
                       "Thanks," + "\n" + \
                       "NCACMS Team"
            # html_content = render_to_string('post/mail_post.html')

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        # msg.attach_alternative(html_content, "text/html")
        msg.send()"""


@receiver(pre_save, sender=Activity)
def first_mail(sender, instance, **kwargs):
    user_email = [instance.victim.email, instance.volunteer.user.email]
    # user_email =  instance.volunteer.user.email
    # user_email = ['jpailla@unomaha.edu','smoorthi@unomaha.edu']
    subject, from_email, to = 'NCACMS Activity', 'mswproject.uno@gmail.com', user_email  # 'jpailla@unomaha.edu'
    text_content = "Hello," + "\n" + \
                   "An activity has been scheduled for you. Please find the details of it below :" + "\n" + "\n" + \
                   "Activity Name : " + instance.name + "\n" + \
                   "Location : " + instance.location.name + "\n" + \
                   "Volunteer : " + instance.volunteer.user.first_name + "\n" + \
                   "Victim : " + instance.victim.first_name + "\n" + \
                   "Activity Start date : " + str(
        instance.start_date.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%m/%d/%Y, %H:%M")) + ' ' + '\n' + \
                   "Activity End date : " + str(
        instance.end_date.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%m/%d/%Y, %H:%M")) + ' ' + "\n" + "\n" \
                                                                                                                    "Thanks," + "\n" + \
                   "NCACMS Team"
    # html_content = render_to_string('post/mail_post.html')
    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    # msg.attach_alternative(html_content, "text/html")
    msg.send()


# @receiver(pre_save, sender=Activity)
# def first_mail(sender, instance, **kwargs):
#     user_email = [instance.victim.email,instance.volunteer.user.email]
#     #user_email =  instance.volunteer.user.email
#     #user_email = ['jpailla@unomaha.edu','smoorthi@unomaha.edu']
#     subject, from_email, to = 'NCACMS Activity', 'mswproject.uno@gmail.com', user_email#'jpailla@unomaha.edu'
#
#     text_content = "Hello," + "\n" + \
#                    "An already scheduled activity has been modified. Please find the details of it below :" + "\n" +  "\n" +  "\n" +\
#                    "activity_name : " + instance.name + "\n" + \
#                    "Location : " + instance.location.name + "\n" + \
#                    "Volunteer : " + instance.volunteer.user.first_name + "\n" + \
#                    "Victim : " + instance.victim.first_name + "\n" + \
#                    "Activity start date : " + str(instance.start_date) + "\n" + \
#                    "Activity End date : " + str(instance.end_date) + "\n" + \
#                    "Thanks," + "\n" + \
#                    "NCACMS Team"
#     # html_content = render_to_string('post/mail_post.html')
#     # create the email, and attach the HTML version as well.
#     msg = EmailMultiAlternatives(subject, text_content, from_email, to)
#     # msg.attach_alternative(html_content, "text/html")
#     msg.send()


class Notes(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='note', null=True)
    victim = models.ForeignKey(Victim, on_delete=models.CASCADE, related_name='note')
    # name = models.CharField(max_length=50)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='note')
    notes = models.TextField(max_length=200, blank=True)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    is_seen = models.BooleanField(default=False)




    def created(self):
        print("Notes Creatednnn1")
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        print("Notes Creatednnn1")
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "Notes"


choice = (
    ('pending', 'PENDING'),
    ('approved', 'APPROVED'),
)




class Volunteerinfo(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    address = models.CharField(max_length=200, blank=False)
    city = models.CharField(max_length=30, blank=False)
    state = models.CharField(max_length=30, blank=False)
    phone = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=False)
    zipcode = models.CharField(max_length=5, blank=False)
    Experience = models.CharField(max_length=50, blank=False)
    created_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=30, default='pending', choices=choice, null=False)

    def __str__(self):
        return str(self.first_name)

    def created(self):
        self.created_date = timezone.now()
        self.save()
