from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ..forms import StaffForm, UserForm
from ..models import Staff, User
from django.db import transaction
from ..forms import *
from ..models import *

now = timezone.now()

@login_required
def staff_list(request):
    if request.user.is_superuser:
        staffs_list = Staff.objects.select_related('user')
        # staffs_list = User.objects.filter(is_staff=True)   #print(staffs_list1) #print(staffs_other_details.user.is_staff)
        """page = request.GET.get('page', 2)
        paginator = Paginator(staffs_list, 6)
        try:
            staffs_list = paginator.page(page)
        except PageNotAnInteger:
            staffs_list = paginator.page(1)
        except EmptyPage:
            staffs_list = paginator.page(paginator.num_pages)"""
        return render(request, 'admin/staff_list.html', {'staff_info': staffs_list})
    else:
        print("condition not satisfied")

@login_required
def staff_detail(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    user = get_object_or_404(User, pk=pk)
    return render(request, 'admin/staff_detail.html', {'staff': staff,'user': user})

@login_required
def staff_edit(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        # update
        form = StaffForm2(request.POST, instance=staff)
        form_user = UserForm(request.POST, instance=user)
        if form.is_valid() and form_user.is_valid():
            staff = form.save(commit=False)
            staff_user = form_user.save(commit=False)
            staff.updated_date = timezone.now()
            staff.save()
            staff_user.save()
            staffs = Staff.objects.filter(created_date__lte=timezone.now())
            #users = User.objects.filter(created_date__lte=timezone.now())
            staffs_list = Staff.objects.select_related('user') #giving this statement is important, since we have to return to staff_list page and the data in that page is viewable only when we pass the data again to that page
            return render(request, 'admin/staff_list.html',{'staffs': staffs,'staff_info': staffs_list})
    else:
        # edit
        form = StaffForm2(instance=staff)
        form_user = UserForm(instance=user)
    return render(request, 'admin/staff_edit.html', {'form': form,'form_user': form_user})

@login_required
def staff_delete(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    user = get_object_or_404(User, pk=pk)
    staff.delete()
    user.delete()
    return redirect('admins:staff_list')


@login_required
def staff_search(request):
    if request.user.is_superuser:
        if request.method == "POST":
            search = request.POST['search']
        staffs_list = Staff.objects.select_related('user').filter(user__username__contains=search)
        return render(request, 'admin/staff_list.html', {'staff_info': staffs_list})
    else:
        print("condition not satisfied")

# ----------------------------------------------------------------------------------------------------------------------


def volunteersignup_list(request):
    info = Volunteerinfo.objects.filter(created_date__lte=timezone.now(), status='pending')
    return render(request, 'admin/Volunteer_Signup_List.html', {'info': info})


def volunteerapproved_list(request):
    info = Volunteerinfo.objects.filter(created_date__lte=timezone.now(), status='approved')
    return render(request, 'admin/Volunteer_approved_List.html', {'info': info})


def volunteersignup_detail(request, pk):
    volunteer = get_object_or_404(Volunteerinfo, pk=pk)
    return render(request, 'admin/Volunteer_Signup_detail.html', {'volunteer': volunteer})


def volunteersignup_adetail(request, pk):
    volunteer = get_object_or_404(Volunteerinfo, pk=pk)
    return render(request, 'admin/Volunteer_Signup_adetail.html', {'volunteer': volunteer})


def volunteersignup_approve(request, pk):
    volunteer = get_object_or_404(Volunteerinfo, pk=pk)
    volunteer.status = 'approved'
    volunteer.save()
    return redirect('admins:volunteersignup_list')


def volunteersignup_delete(request, pk):
    volunteer = get_object_or_404(Volunteerinfo, pk=pk)
    if volunteer.status == 'pending':
        volunteer.delete()
        return redirect('admins:volunteersignup_list')
    else:
        volunteer.delete()
        return redirect('admins:volunteerapproved_list')

