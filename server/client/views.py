from django.shortcuts import render, redirect
from django.utils.timezone import now
import csv
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# email imports start
from django.core.mail import send_mail
from django.conf import settings
# email imports end

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.models import User

from .models import *


# Create your views here.
def LoginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, "client/login.html")


def IndexView(request):
    proposal = Proposal.objects.first()

    context = {
        'proposal': proposal,
        "page": "client/index.html",
    }

    if request.htmx:
        return render(request, "client/index.html", context)
    return render(request, "client/base.html", context)


def RegisterView(request):
    proposal = Proposal.objects.first()

    context = {
        'proposal': proposal,
        'form_status': 'show_form',
        "page": "client/register.html",
    }

    if request.htmx:
        return render(request, "client/register.html", context)
    return render(request, "client/base.html", context)


def ExhibitView(request):
    context = {
        "page": "client/exhibit.html",
    }

    if request.htmx:
        return render(request, "client/exhibit.html", context)
    return render(request, "client/base.html", context)


def SponsorView(request):
    context = {
        "page": "client/sponsor.html",
    }

    if request.htmx:
        return render(request, "client/sponsor.html", context)
    return render(request, "client/base.html", context)


def SponsorBenefitsView(request):
    context = {
        "page": "client/benefits.html",
    }

    if request.htmx:
        return render(request, "client/benefits.html", context)
    return render(request, "client/base.html", context)


# Register View Start
def RegisterPartial(request, form_status):
    context = {
        'form_status': form_status,
        "page": "partials/register_form_partial.html",
    }

    if request.htmx:
        return render(request, "partials/register_form_partial.html", context)
    return render(request, "partials/base.html", context)


def SubmitFormView(request):

    if request.method == "POST":
        reference = f"{now().strftime('%Y%m%d%H%M%S')}"
        # Get just the path
        dashboard_path = reverse('dashboard')  # returns '/dashboard/'
        # Get the full domain
        domain = get_current_site(request).domain  # returns 'example.com'
        # Full URL
        full_dashboard_url = request.scheme + '://' + domain + dashboard_path

        RegistrationsModel.objects.create(
            reference=reference,
            plans=request.POST.get('plans'),
            FullName=request.POST.get('FullName'),
            contact=request.POST.get('contact'),
            email=request.POST.get('email'),
            company=request.POST.get('company'),
            position=request.POST.get('position'),
            dietary=request.POST.get('dietary'),
            other_diet=request.POST.get('other_diet'),
        )

        # Compose email message
        subject = "New Registration Submitted"
        message = f"""
        A new registration has been submitted:

        Reference: {reference}
        Name: {request.POST.get('FullName')}
        Email: {request.POST.get('email')}
        Contact: {request.POST.get('contact')}
        Company: {request.POST.get('company')}
        Position: {request.POST.get('position')}
        Dietary: {request.POST.get('dietary')}
        Other Diet: {request.POST.get('other_diet')}
        Admin Link: {full_dashboard_url}
                """

        # Step 2: try sending email
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['polite@ndebeleconsulting.co.za'],
                fail_silently=False,
            )
            form_status = 'success'  # Step 3a: success if no error
        except Exception as e:
            form_status = 'error'  # Step 3b: error if email fails

    return RegisterPartial(request, form_status)


def RegisterAnotherPost(request):
    if request.method == "POST":
        form_status = 'show_form'

    return RegisterPartial(request, form_status)


@login_required(login_url='index')  # Replace 'login' with your login URL name
def AdminDashboardView(request):
    users = RegistrationsModel.objects.all()
    users_count = RegistrationsModel.objects.all().count

    context = {
        'users': users,
        "users_count": users_count,
        "page": "client/dashboard.html",
    }

    if request.htmx:
        return render(request, "client/dashboard.html", context)
    return render(request, "client/base.html", context)

# ====== Download CSV ======


def download_csv(request):
    users = RegistrationsModel.objects.all()

    # Create the HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="AML2025.csv"'

    writer = csv.writer(response)

    # Write the header
    writer.writerow(['Full Name', 'Package', 'Contact', 'Email', 'Company',
                    'Position', 'Dietary', 'Dietary(Other)'])  # Replace with your fields

    # Write data rows
    for obj in users:
        writer.writerow([obj.FullName, obj.plans, obj.contact, obj.email, obj.company,
                        obj.position, obj.dietary, obj.other_diet])  # Adjust fields as needed

    return response
