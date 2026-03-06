from django.urls import path
from .views import (
    gym_members_list, gym_add_member, gym_renew_member, 
    gym_edit_member, gym_delete_member,
    gym_membership_types, gym_add_membership_type, 
    gym_edit_membership_type, gym_delete_membership_type
)

urlpatterns = [
    path('', gym_members_list, name='gym_members_list'),
    path('add/', gym_add_member, name='gym_add_member'),
    path('edit/<int:member_id>/', gym_edit_member, name='gym_edit_member'),
    path('delete/<int:member_id>/', gym_delete_member, name='gym_delete_member'),
    path('renew/<int:member_id>/', gym_renew_member, name='gym_renew_member'),
    
    # Types
    path('types/', gym_membership_types, name='gym_membership_types'),
    path('types/add/', gym_add_membership_type, name='gym_add_membership_type'),
    path('types/edit/<int:type_id>/', gym_edit_membership_type, name='gym_edit_membership_type'),
    path('types/delete/<int:type_id>/', gym_delete_membership_type, name='gym_delete_membership_type'),
]
