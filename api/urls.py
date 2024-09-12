from django.urls import path
from .views import (StaffListCreateView, StaffDetailView, 
                    PositionListCreateView, PositionDetailView, 
                    ShiftListCreateView, ShiftDetailView, 
                    StaffShiftListCreateView, StaffShiftDetailView, 
                    StaffAttendanceListCreateView, StaffAttendanceDetailView, CustomAuthToken)

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api_login'),

    path('staff/', StaffListCreateView.as_view(), name='staff-list-create'),
    path('staff/<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
    
    path('position/', PositionListCreateView.as_view(), name='position-list-create'),
    path('position/<int:pk>/', PositionDetailView.as_view(), name='position-detail'),
    
    path('shift/', ShiftListCreateView.as_view(), name='shift-list-create'),
    path('shift/<int:pk>/', ShiftDetailView.as_view(), name='shift-detail'),
    
    path('staffshift/', StaffShiftListCreateView.as_view(), name='staffshift-list-create'),
    path('staffshift/<int:pk>/', StaffShiftDetailView.as_view(), name='staffshift-detail'),
    
    path('attendance/', StaffAttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('attendance/<int:pk>/', StaffAttendanceDetailView.as_view(), name='attendance-detail'),
]
