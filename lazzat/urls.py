from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('generate-fake-data/', views.generate_fake_data, name='generate-fake-data'),
    
    # Position
    path('position/create/', views.create_position, name='create_position'),
    path('position/list/', views.position_list, name='position_list'),
    path('position/update/<int:pk>/', views.update_position, name='update_position'),
    path('position/delete/<int:pk>/', views.delete_position, name='delete_position'),

    # Staff
    path('staff/create/', views.create_staff, name='create_staff'),
    path('staff/list/', views.staff_list, name='staff_list'),
    path('staff/update/<int:pk>/', views.update_staff, name='update_staff'),
    path('staff/delete/<int:pk>/', views.delete_staff, name='delete_staff'),

    # Shift
    path('shifts/', views.shift_list, name='shift_list'),
    path('shifts/create/', views.shift_create, name='shift_create'),
    path('shifts/edit/<int:pk>/', views.shift_update, name='shift_update'),
    path('shifts/delete/<int:pk>/', views.shift_delete, name='shift_delete'),

    # StaffShift
    path('staffshifts/', views.staffshift_list, name='staffshift_list'),
    path('staffshifts/create/', views.staffshift_create, name='staffshift_create'),
    path('staffshifts/edit/<int:pk>/', views.staffshift_update, name='staffshift_update'),
    path('staffshifts/delete/<int:pk>/', views.staffshift_delete, name='staffshift_delete'),

    # StaffAttendance
     path('attendances/', views.attendance_list, name='attendance_list'),

    # Search
    path('search/', views.search, name='search'),
]