from django.conf.urls import url
from . import views
from django.urls import path, re_path, include
from .views import nca, staff, volunteer, admin
from nca.views import *

urlpatterns = [
    path('', nca.home, name='home'),
    path('VolunteerRequest/', nca.volunteer_request, name='volunteer_request'),
    path('VolunteerRequest/Sent/', nca.request_sent, name='request_sent'),

    path('Admins/', include(([
                                 path('', nca.SignUpView.as_view(), name='signup'),
                                 path('staffsignup/', staff.StaffSignUpView.as_view(), name='staff_signup'),
                                 path('volunteersignup/', volunteer.VolunteerSignUpView.as_view(),
                                      name='volunteer_signup'),
                                 path('staff_list', admin.staff_list, name='staff_list'),
                                 path('staff/<int:pk>/detail/', admin.staff_detail, name='staff_detail'),
                                 path('staff/<int:pk>/edit/', admin.staff_edit, name='staff_edit'),
                                 path('staff/<int:pk>/delete/', admin.staff_delete, name='staff_delete'),
                                 path('volunteersignupList', admin.volunteersignup_list, name='volunteersignup_list'),
                                 path('volunteersignupList/<int:pk>/detail/', admin.volunteersignup_detail,
                                      name='volunteersignup_detail'),
                                 path('volunteersignupList/<int:pk>/approved/', admin.volunteersignup_approve,
                                      name='volunteersignup_approve'),
                                 path('volunteersignupList/<int:pk>/delete/', admin.volunteersignup_delete,
                                      name='volunteersignup_delete'),
                                 path('volunteerapprovedList', admin.volunteerapproved_list,
                                      name='volunteerapproved_list'),
                                 path('volunteerapprovedList/<int:pk>/detail/', admin.volunteersignup_adetail,
                                      name='volunteerapproved_adetail'),
                                 path('volunteerapprovedList/<int:pk>/delete/', admin.volunteersignup_delete,
                                      name='volunteersignup_delete'),
                                 path('staff_list/search/', admin.staff_search, name='staff_search'),
                             ], 'nca'), namespace='admins')),
    path('Staff/', include(([
                                path('', staff.staff_home.as_view(), name='staff_home'),
                                path('account', staff.staff_details, name='staff_details'),
                                path('account/edit/', staff.staff_edit, name='staff_edit'),
                                path('activity_list', staff.activity_list, name='activity_list'),
                                path('activity/<int:pk>/detail/', staff.activity_detail, name='activity_detail'),
                                path('activity/<int:pk>/edit/', staff.activity_edit, name='activity_edit'),
                                path('activity/<int:pk>/delete/', staff.activity_delete, name='activity_delete'),
                                path('activity/new/', staff.activity_new, name='activity_new'),
                                path('activity/<int:pk>/notes/', staff.activity_notes_list, name='activity_notes_list'),
                                path('activity_list/search/', staff.activity_search, name='ac_search'),
                                # -------------------------------------------------------------------------------------
                                path('victim_list', staff.victim_list, name='victim_list'),
                                path('victim/<int:pk>/detail/', staff.victim_detail, name='victim_detail'),
                                path('victim/<int:pk>/edit/', staff.victim_edit, name='victim_edit'),
                                path('victim/<int:pk>/delete/', staff.victim_delete, name='victim_delete'),
                                path('victim/new/', staff.victim_new, name='victim_new'),
                                path('victim_list/search/', staff.victim_search, name='vi_search'),
                                # -------------------------------------------------------------------------------------
                                path('location_list', staff.location_list, name='location_list'),
                                path('location/<int:pk>/detail/', staff.location_detail, name='location_detail'),
                                path('location/<int:pk>/edit/', staff.location_edit, name='location_edit'),
                                path('location/<int:pk>/delete/', staff.location_delete, name='location_delete'),
                                path('location/new/', staff.location_new, name='location_new'),
                                path('location/<int:pk>/notes/', staff.location_notes, name='location_notes'),
                                path('location_list/search/', staff.location_search, name='lo_search'),
                                # -------------------------------------------------------------------------------------
                                path('volunteer_list', staff.volunteer_list, name='volunteer_list'),
                                path('volunteer/<int:pk>/detail/', staff.volunteer_detail, name='volunteer_detail'),
                                path('volunteer/<int:pk>/edit/', staff.volunteer_edit, name='volunteer_edit'),
                                path('volunteer/<int:pk>/delete/', staff.volunteer_delete, name='volunteer_delete'),
                                path('notification', staff.show_notification, name='show-notifications'),
                                path('notes_detail/<int:pk>/detail/', staff.notes_details, name='notes_details'),
                                path('volunteer_list/search/', staff.volunteer_search, name='vo_search'),
                            ], 'nca'), namespace='staff')),

    path('Volunteer/', include(([
                                    path('', volunteer.volunteer_home.as_view(), name='volunteer_home'),
                                    path('account', volunteer.volunteer_details, name='volunteer_details'),
                                    path('account/edit/', volunteer.volunteer_edit, name='volunteer_edit'),
                                    path('activity_list', volunteer.volunteer_activity_list,
                                         name='volunteer_activity_list'),
                                    path('activity/<int:pk>/detail/', volunteer.volunteer_activity_detail,
                                         name='volunteer_activity_detail'),
                                    path('activity/<int:pk>/edit/', volunteer.volunteer_activity_edit,
                                         name='volunteer_activity_edit'),
                                    path('activity/<int:pk>/delete/', volunteer.volunteer_activity_delete,
                                         name='volunteer_activity_delete'),
                                    path('activity/new/', volunteer.volunteer_activity_new,
                                         name='volunteer_activity_new'),
                                    path('notes/<int:pk1>/', volunteer.volunteer_notes_list,
                                         name='volunteer_notes_list'),
                                    path('notes/<int:pk2>/new/', volunteer.volunteer_notes_new,
                                         name='volunteer_notes_new'),
                                    path('notes/<int:pk>/edit/', volunteer.volunteer_notes_edit,
                                         name='volunteer_notes_edit'),
                                    path('notes/<int:pk>/delete/', volunteer.volunteer_notes_delete,
                                         name='volunteer_notes_delete'),
                                    path('victim_list', volunteer.volunteer_victim_list,
                                         name='volunteer_victim_list'),
                                    path('victim_list/search', volunteer.volunteer_victim_search,
                                         name='volunteer_victim_search'),
                                    path('victim/<int:pk>/detail/', volunteer.volunteer_victim_detail,
                                         name='volunteer_victim_detail'),
                                    path('activity_list/search', volunteer.volunteer_activity_search,
                                         name='volunteer_activity_search'),
                                ], 'nca'), namespace='volunteer')),

    # path('activity_list', views.activity_list, name='activity_list'),
    # path('activity/<int:pk>/detail/', views.activity_detail, name='activity_detail'),
    # path('activity/<int:pk>/edit/', views.activity_edit, name='activity_edit'),
    # path('activity/<int:pk>/delete/', views.activity_delete, name='activity_delete'),
    # path('activity/new/', views.activity_new, name='activity_new'),
    # path('activity/<int:pk>/notes/', views.activity_notes, name='activity_notes'),

]
