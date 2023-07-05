from .models import CustomUser  # Import the CustomUser model
from .forms import DepartmentForm
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
import requests
from django.conf import settings
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from hubspot.crm.contacts import SimplePublicObjectInputForCreate, ApiException
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
# Create your views here.
from django.contrib.auth import authenticate, login, logout


from .models import CustomUser
from django.db.models import Q

from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
# import hubspot
from pprint import pprint
# from hubspot.crm.contacts import ApiException
# from hubspot.crm.contacts import SimplePublicObjectInput, SimplePublicObjectInputForCreate, ApiException
from .models import Ticket
from .forms import TicketForm
# from hubspot import HubSpot

from .models import Department
from hubspot.crm.tickets import SimplePublicObjectInputForCreate, ApiException
import requests
from django.shortcuts import render, get_object_or_404, redirect

from django.shortcuts import render
from .models import Ticket







import json

from django.views.decorators.csrf import csrf_exempt
from .models import Ticket

import requests
from django.http import JsonResponse

def authenticate(request, email_or_phone_number=None, password=None):
    # UserModel = get_user_model()
    if email_or_phone_number is None or password is None:
        return None
    try:
        user = CustomUser.objects.get(
            Q(email=email_or_phone_number) | Q(phone_number=email_or_phone_number))
        if user.check_password(password):
            return user
    except CustomUser.DoesNotExist:
        return None


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email_or_phone_number = request.POST.get('email_or_phone_number')
        password = request.POST.get('password')

        user = authenticate(
            request, email_or_phone_number=email_or_phone_number, password=password)
        if user is not None:
            # The user's credentials are correct, so log them in
            login(request, user)
            # if user.is_superuser:
            #     # If the user is an admin, redirect to the ticket page
            #     return redirect('ticket_page')
            # else:
            # If the user is a regular user, redirect to the home page
            return redirect('Accounts:home')
        else:
            # The user's credentials are incorrect, so return an error message
            return JsonResponse({'success': False, 'message': 'Invalid login credentials'})
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user  # Get the logged-in user
    # Filter tickets based on the logged-in user
    tickets = Ticket.objects.filter(ticket_email=user)
    context = {'tickets': tickets}
    return render(request, 'home.html', context)


@login_required(login_url='Accounts:login')
def logout_view(request):
    logout(request)
    return redirect('Accounts:login')





def admin_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('home')  # Redirect to home page if not an admin
        return function(request, *args, **kwargs)
    return wrap


# Redirects non-admin users to home page
@staff_member_required(login_url='Accounts:home')
# Redirects non-logged-in users to login page
@login_required(login_url='Accounts:login')
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.created_by = request.user
            department.save()
            # Replace with your department list URL
            return redirect('Accounts:home')
    else:
        form = DepartmentForm()
    return render(request, 'department_create.html', {'form': form})


# Redirects non-admin users to home page
@staff_member_required(login_url='home')
# Redirects non-logged-in users to login page
@login_required(login_url='login')
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace with your department list URL
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'department_edit.html', {'form': form, 'department': department})


@login_required
# Redirects non-admin users to home page
@staff_member_required(login_url='Accounts:home')
@login_required(login_url='Accounts:login')
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    # Check if the current user is an admin
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Only admin users can delete departments.'}, status=403)

    # Check if the department is assigned to any user
    if CustomUser.objects.filter(department=department).exists():
        return JsonResponse({'error': 'The department is assigned to one or more users and cannot be deleted.'}, status=400)

    # Delete the department
    department.delete()
    return JsonResponse({'message': 'Department deleted successfully.'})


# Redirects non-admin users to home page
@staff_member_required(login_url='Accounts:home')
@login_required(login_url='Accounts:login')
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            role = form.cleaned_data['role']
            department = form.cleaned_data['department']

            # Create contact in HubSpot

            # Check if contact already exists in Django model
            if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(phone_number=phone_number).exists():
                pprint("Contact already exists in Django model.")
            else:
                # Save contact to Django model
                try:
                    user = CustomUser(
                        email=email,
                        phone_number=phone_number,
                        department=department,  # Set the department accordingly if available
                        role=role,  # Set the role accordingly if available
                        created_by=None,  # Set the created_by accordingly if available
                        is_active=True,  # Set the active status accordingly if available
                        is_staff=False,  # Set the staff status accordingly if available
                    )
                    user.set_password(password1)
                    user.save()
                    return redirect('home')
                except Exception as e:
                    # Handle the error if the contact already exists in Django model
                    pprint(f"Error saving contact to Django model: {e}")

    else:
        form = CustomUserCreationForm()

    return render(request, 'create-user.html', {'form': form})


@staff_member_required(login_url='Accounts:home')
@login_required(login_url='Accounts:home')
def view_all_users(request):
    if not request.user.is_staff:
        return redirect('Accounts:home')

    users = CustomUser.objects.all()
    return render(request, 'users.html', {'users': users})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='Accounts:home')
def view_departments(request):
    departments = Department.objects.all()
    return render(request, 'departments.html', {'departments': departments})


PRIORITY_MAPPING = {
    'low': 1,
    'medium': 2,
    'high': 3,
}



@csrf_exempt
# def create_ticket(request):
#     if request.method == 'POST':
#         # Extract the data from the request
#         subject = request.POST.get('subject')
#         body = request.POST.get('body')
#         priority = request.POST.get('priority')
#         ticket_email = request.POST.get('ticket_email')
#         ticket_phone_number = request.POST.get('ticket_phone_number')

#         # Map priority value to numeric value
#         priority_mapping = {
#             'low': 1,
#             'medium': 2,
#             'high': 3,
#         }
#         # Default to 1 if priority is not found
#         priority = priority_mapping.get(priority, 1)

#         # Create the ticket in Freshdesk
#         url = 'https://acme8306.freshdesk.com/api/v2/tickets'
#         headers = {'Content-Type': 'application/json'}
#         auth = ('1DTPsoWBTnqpLENEEWf', 'X')
#         data = {
#             'description': body,
#             'subject': subject,
#             'email': ticket_email,
#             'priority': priority,  # Use the mapped numeric value
#             'status': 2,
#         }
#         response = requests.post(url, headers=headers, auth=auth, json=data)
#         if response.status_code == 201:
#             # Ticket created successfully in Freshdesk, save it in the Django database
#             user = CustomUser.objects.get(email=ticket_email)
#             freshdesk_ticket_id = response.json().get(
#                 'id')  # Retrieve the CustomUser instance
#             ticket = Ticket.objects.create(
#                 subject=subject,
#                 body=body,
#                 priority=str(priority),  # Save the priority as a string
#                 ticket_email=user,  # Assign the CustomUser instance to ticket_email field
#                 ticket_phone_number=ticket_phone_number,
#                 freshdesk_ticket_id=freshdesk_ticket_id
#             )
#             return JsonResponse({'success': True, 'ticket_id': ticket.id})
#         else:
#             return JsonResponse({'success': False, 'error_message': response.json()})

#     # GET request, render the form
#     return render(request, 'create-ticket.html')
def create_ticket(request):
    if request.method == 'POST':
        # Extract the data from the request
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        priority = request.POST.get('priority')
        ticket_email = request.POST.get('ticket_email')
        ticket_phone_number = request.POST.get('ticket_phone_number')

        # Map priority value to numeric value
        priority_mapping = {
            'low': 1,
            'medium': 2,
            'high': 3,
        }
        # Default to 1 if priority is not found
        priority = priority_mapping.get(priority, 1)

        # Create the ticket in Freshdesk
        url = 'https://acme8306.freshdesk.com/api/v2/tickets'
        headers = {'Content-Type': 'application/json'}
        auth = ('1DTPsoWBTnqpLENEEWf', 'X')
        data = {
            'description': body,
            'subject': subject,
            'priority': priority,
            'status': 2,
        }
        
        # Check if email is provided and add it to the data
        if ticket_email:
            data['email'] = ticket_email

        response = requests.post(url, headers=headers, auth=auth, json=data)
        if response.status_code == 201:
            # Ticket created successfully in Freshdesk, save it in the Django database
            user = CustomUser.objects.get(email=ticket_email)
            freshdesk_ticket_id = response.json().get('id')
            ticket = Ticket.objects.create(
                subject=subject,
                body=body,
                priority=str(priority),
                ticket_email=user,
                ticket_phone_number=ticket_phone_number,
                freshdesk_ticket_id=freshdesk_ticket_id
            )
            return redirect('Accounts:home')
            # return JsonResponse({'success': True, 'ticket_id': ticket.id})
        else:
            return JsonResponse({'success': False, 'error_message': response.json()})

    # GET request, render the form
    return render(request, 'create-ticket.html')

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='Accounts:home')
@csrf_exempt
def retrieve_all_tickets(request):
    api_url = 'https://acme8306.freshdesk.com/api/v2/tickets'
    auth = ('1DTPsoWBTnqpLENEEWf', 'X')

    try:
        response = requests.get(api_url, auth=auth)
        if response.status_code == 200:
            tickets = response.json()
            return render(request, 'all_user_ticket.html', {'tickets': tickets})
        else:
            error_message = response.json()
            return render(request, 'all_user_ticket.html', {'error_message': error_message})
    except requests.exceptions.RequestException as e:
        return render(request, 'all_user_ticket.html', {'error_message': str(e)})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='Accounts:home')
def delete_ticket(request, ticket_id):
    freshdesk_domain = 'your_freshdesk_domain'
    api_key = '1DTPsoWBTnqpLENEEWf'
    
    # Construct the Freshdesk API endpoint URL
    url = f'https://acme8306.freshdesk.com/api/v2/tickets/{ticket_id}'
    
    # Set the headers and authentication
    headers = {
        'Content-Type': 'application/json'
    }
    auth = (api_key, 'X')
    
    # Send the DELETE request to the Freshdesk API
    response = requests.delete(url, headers=headers, auth=auth)
    
    if response.status_code == 204:
        return redirect('Accounts:retrieve_all_tickets')
        print(".......tikcet deleted successfully......")
        # return HttpResponse('Ticket deleted successfully')
    else:
        return redirect("Accounts:retrieve_all_tickets")
        print(".......failed to delete ticket........")