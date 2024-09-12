from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout 
from django.contrib.auth.decorators import login_required
from .models import Position, Staff, Shift, StaffShift, StaffAttendance
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse
import datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from faker import Faker
from .models import Position, Shift, Staff, StaffShift, StaffAttendance
from faker import Faker
from random import choice
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse


def generate_fake_data(request):
    fake = Faker()

    for _ in range(10):
        staff_member = Staff.objects.create(
            full_name=fake.name(),
            phone_number=fake.phone_number(),
            address=fake.address(),
            email=fake.email(),
        )

        position = Position.objects.create(
            title=fake.job(),
            description=fake.text(),
            staff=staff_member
        )

        start_time = timezone.now() + timedelta(days=fake.random_int(min=1, max=10))
        end_time = start_time + timedelta(hours=fake.random_int(min=4, max=8))
        shift = Shift.objects.create(
            start_time=start_time,
            end_time=end_time
        )

        StaffShift.objects.create(
            staff=staff_member,
            shift=shift,
            position=position
        )

        StaffAttendance.objects.create(
            staff=staff_member,
            shift=shift,
            date=shift.start_time.date(),
            status=choice(['Present', 'Absent', 'Late'])
        )

    return HttpResponse("Yolgon malumtolar yaratildi!")



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(reverse('index'))  # 'index' o'rniga haqiqiy view nomi
        else:
            error = "Foydalanuvchi nomi yoki parol noto'g'ri."
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')


def is_admin(user):
    return user.is_authenticated and user.is_staff


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if is_admin(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper

fake = Faker()

@api_view(['POST'])
def generate_fake_data(request):
    for _ in range(10):
        Position.objects.create(name=fake.job())

    shift_list = []
    for _ in range(15):
        shift = Shift(
            time=fake.time_object(),
            end_time=fake.time_object()
        )
        shift_list.append(shift)
    Shift.objects.bulk_create(shift_list)

    staff_list = []
    for _ in range(15):
        staff_member = Staff(
            full_name=fake.name(),
            phone=fake.phone_number(),
            email=fake.email(),
            position=Position.objects.order_by('?').first(),
            start_date=fake.date_this_decade(),
            is_active=fake.boolean()
        )
        staff_list.append(staff_member)
    Staff.objects.bulk_create(staff_list)

    staff_shift_list = []
    staff_attendance_list = []
    
    all_staff = Staff.objects.all()
    all_shifts = Shift.objects.all()

    for staff_member in all_staff:
        for _ in range(3):
            staff_shift_list.append(
                StaffShift(
                    staff=staff_member,
                    shift=all_shifts.order_by('?').first(),
                    date=fake.date_this_month()
                )
            )
        
        for _ in range(15):
            staff_attendance_list.append(
                StaffAttendance(
                    staff=staff_member,
                    date=fake.date_this_month(),
                    present=fake.boolean()
                )
            )
    
    StaffShift.objects.bulk_create(staff_shift_list)
    StaffAttendance.objects.bulk_create(staff_attendance_list)

    return redirect('')



@login_required(login_url='login')
@admin_required
def index(request):
    return render(request, 'base.html')


# Read
@login_required(login_url='login')
@admin_required
def position_list(request):
    positions = Position.objects.all()
    return render(request, 'position/list.html', {'positions': positions})


@login_required(login_url='login')
@admin_required
def create_position(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description') 
        Position.objects.create(
            name=name, 
            description=description
            ) 
        return redirect('position_list')
    return render(request, 'position/create.html')


# Update
@login_required(login_url='login')
@admin_required
def update_position(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        position.title = request.POST.get('title')
        position.description = request.POST.get('description')
        position.save()
        return redirect('position_list')
    return render(request, 'position/update.html', {'position': position})


# Delete
@login_required(login_url='login')
@admin_required
def delete_position(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        position.delete()
        return redirect('position_list')
    return render(request, 'position/delete.html', {'position': position})


# Staff CRUD
@login_required(login_url='login')
@admin_required
def staff_list(request):
    staff = Staff.objects.all()
    staff_count = Staff.objects.count()
    new_staff_count = Staff.objects.filter(hire_date__gte=timezone.now() - timezone.timedelta(days=30)).count()
    context = {
        'staff': staff,
        'staff_count': staff_count,
        'new_staff_count': new_staff_count
    }
    return render(request, 'staff/list.html', context)


@login_required(login_url='login')
@admin_required
def create_staff(request):
    if request.method == 'POST':
        position = Position.objects.get(pk=request.POST.get('position'))
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        hire_date = request.POST.get('hire_date')
        
        Staff.objects.create(
            position=position, 
            first_name=first_name,  
            last_name=last_name,  
            phone_number=phone_number,
            hire_date=hire_date
        ) 
        return redirect('staff_list')
    
    positions = Position.objects.all() 
    return render(request, 'staff/create.html', {'positions': positions})


@login_required(login_url='login')
@admin_required
def update_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.first_name = request.POST.get('first_name')
        staff.last_name = request.POST.get('last_name')
        staff.phone_number = request.POST.get('phone_number')
        staff.hire_date = request.POST.get('hire_date')
        staff.save()
        return redirect('staff_list')
    return render(request, 'staff/update.html', {'staff': staff})


@login_required(login_url='login')
@admin_required
def delete_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff_list')
    return render(request, 'staff/delete.html', {'staff': staff})


# Shift CRUD
@login_required(login_url='login')
@admin_required
def shift_list(request):
    shifts = Shift.objects.all()
    
    # Filtrlash
    name_filter = request.GET.get('name', '')
    if name_filter:
        shifts = shifts.filter(name__icontains=name_filter)
    
    context = {
        'shifts': shifts,
        'name_filter': name_filter,
    }
    return render(request, 'shift/list.html', context)


@login_required(login_url='login')
@admin_required
def shift_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if name and start_time and end_time:
            Shift.objects.create(
                name=name,
                start_time=start_time,
                end_time=end_time
            )
            return redirect('shift_list')
        else:
            return HttpResponse("Invalid input", status=400)

    return render(request, 'shift/create.html')


@login_required(login_url='login')
@admin_required
def shift_update(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if name and start_time and end_time:
            shift.name = name
            shift.start_time = start_time
            shift.end_time = end_time
            shift.save()
            return redirect('shift_list')
        else:
            return HttpResponse("Invalid input", status=400)
    
    return render(request, 'shift/update.html', {
        'action': 'Smenni',
    })


@login_required(login_url='login')
@admin_required
def shift_delete(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    
    if request.method == 'POST':
        shift.delete()
        return redirect('shift_list')
    
    return render(request, 'shift/delete.html', {'object': shift})


# StaffShift CRUD
@login_required(login_url='login')
@admin_required
def staffshift_list(request):
    staff_shifts = StaffShift.objects.all()
    return render(request, 'staffshift/list.html', {'staff_shifts': staff_shifts})


@login_required(login_url='login')
@admin_required
def staffshift_create(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        shift_id = request.POST.get('shift')
        date = request.POST.get('date')

        if staff_id and shift_id and date:
            staff = get_object_or_404(Staff, pk=staff_id)
            shift = get_object_or_404(Shift, pk=shift_id)
            StaffShift.objects.create(staff=staff, shift=shift, date=date)
            return redirect('staffshift_list')
        else:
            return HttpResponse("Invalid input", status=400)

    staffs = Staff.objects.all()
    shifts = Shift.objects.all()
    return render(request, 'staffshift/create.html', {'staffs': staffs, 'shifts': shifts})


@login_required(login_url='login')
@admin_required
def staffshift_update(request, pk):
    staffshift = get_object_or_404(StaffShift, pk=pk)
    
    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        shift_id = request.POST.get('shift')
        date = request.POST.get('date')

        if staff_id and shift_id and date:
            staffshift.staff = get_object_or_404(Staff, pk=staff_id)
            staffshift.shift = get_object_or_404(Shift, pk=shift_id)
            staffshift.date = date
            staffshift.save()
            return redirect('staffshift_detail', pk=pk)
        else:
            return HttpResponse("Invalid input", status=400)
    
    staffs = Staff.objects.all()
    shifts = Shift.objects.all()
    return render(request, 'staffshift/update.html', {
        'staffshift': staffshift,
        'staffs': staffs,
        'shifts': shifts,
        'action': 'Edit'
    })


@login_required(login_url='login')
@admin_required
def staffshift_delete(request, pk):
    staff_shift = get_object_or_404(StaffShift, pk=pk)
    if request.method == 'POST':
        staff_shift.delete()
        return redirect('staffshift_list')
    return render(request, 'staffshift/delete.html', {'object': staff_shift})


# StaffAttendance
@login_required(login_url='login')
@admin_required
def attendance_list(request):
    attendances = StaffAttendance.objects.all()
    return render(request, 'staffattendance/list.html', {'attendances': attendances})

# Search
@login_required(login_url='login')
@admin_required
def search(request):
    query = request.GET.get('q')
    staff_results = Staff.objects.none()
    position_results = Position.objects.none()
    shift_results = Shift.objects.none()
    
    if query:
        staff_results = Staff.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(phone_number__icontains=query)
        )
        position_results = Position.objects.filter(name__icontains=query)
        shift_results = Shift.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'staff_results': staff_results,
        'position_results': position_results,
        'shift_results': shift_results,
    }
    
    return render(request, 'search_results.html', context)
