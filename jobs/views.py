from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib import messages
from .forms import RegistrationForm, JobForm, ApplicationForm
from .models import Job, Application, Profile

def home(request):
    return render(request, "home.html")


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("post_login_redirect")
        messages.error(request, "Invalid credentials")
    return render(request, "login.html")


@login_required
def post_login_redirect(request):
    role = request.user.profile.role
    if role == "EMPLOYER":
        return redirect("employer_dashboard")
    return redirect("applicant_dashboard")


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")

# --- Dashboards ---

@login_required
def employer_dashboard(request):
    if request.user.profile.role != "EMPLOYER":
        return redirect("applicant_dashboard")
    jobs = Job.objects.filter(posted_by=request.user).order_by("-created_at")
    return render(request, "dashboard_employer.html", {"jobs": jobs})


@login_required
def applicant_dashboard(request):
    if request.user.profile.role != "APPLICANT":
        return redirect("employer_dashboard")
    return render(request, "dashboard_applicant.html")

# --- Employer: CRUD-like ---

@login_required
def job_create(request):
    if request.user.profile.role != "EMPLOYER":
        return redirect("home")
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posted!")
            return redirect("employer_dashboard")
    else:
        form = JobForm()
    return render(request, "job_form.html", {"form": form})


@login_required
def job_applicants(request, pk):
    if request.user.profile.role != "EMPLOYER":
        return redirect("home")

    job = get_object_or_404(Job, pk=pk, posted_by=request.user)

    if request.method == "POST":
        app_id = request.POST.get("application_id")
        new_status = request.POST.get("status")
        application = get_object_or_404(Application, pk=app_id, job=job)
        if new_status in ["APPROVED", "REJECTED"]:
            application.status = new_status
            application.save()
            messages.success(request, f"Application {new_status.lower()}.")

    applicants = job.applications.select_related("applicant").order_by("-applied_at")
    return render(request, "job_applicants.html", {"job": job, "applicants": applicants})


# --- Applicant: list, detail, apply, my applications ---

def job_list(request):
    query = request.GET.get("q", "").strip()
    jobs = Job.objects.all().order_by("-created_at")
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(location__icontains=query)
        )
    return render(request, "job_list.html", {"jobs": jobs, "query": query})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    can_apply = request.user.is_authenticated and request.user.profile.role == "APPLICANT"
    already_applied = False
    if can_apply:
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    return render(request, "job_detail.html", {
        "job": job,
        "can_apply": can_apply and not already_applied,
        "already_applied": already_applied
    })


@login_required
def apply_job(request, pk):
    if request.user.profile.role != "APPLICANT":
        return redirect("home")
    job = get_object_or_404(Job, pk=pk)
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, "You already applied to this job.")
        return redirect("job_detail", pk=pk)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            messages.success(request, "Application submitted!")
            return redirect("my_applications")
    else:
        form = ApplicationForm()
    return render(request, "application_form.html", {"form": form, "job": job})


@login_required
def my_applications(request):
    if request.user.profile.role != "APPLICANT":
        return redirect("home")
    
    status_filter = request.GET.get("status")
    apps = Application.objects.filter(applicant=request.user).select_related("job").order_by("-applied_at")
    if status_filter in ["PENDING", "APPROVED", "REJECTED"]:
        apps = apps.filter(status=status_filter)

    return render(request, "my_applications.html", {"applications": apps, "status_filter": status_filter})
