# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from .models import NGO, Project, Workforce, Permit, User
from .forms import ProjectForm, WorkforceForm, PermitForm
from .utils import require_role

User = get_user_model()

# ---------- Auth ----------
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("redirect_after_login")
        else:
            return render(request, "core/login.html", {"error": "Invalid credentials"})
    return render(request, "core/login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def redirect_after_login(request):
    if request.user.role == User.NGO:
        return redirect("ngo_dashboard")
    elif request.user.role == User.LABOUR:
        return redirect("labour_dashboard")
    elif request.user.role == User.MIGRATION:
        return redirect("migration_dashboard")
    elif request.user.role == User.ADMIN:
        return redirect("admin_dashboard")
    return redirect("login")


# ---------- Dashboards ----------
@login_required
def admin_dashboard(request):
    require_role(request.user, User.ADMIN)
    stats = {
        "ngos": NGO.objects.count(),
        "projects": Project.objects.count(),
        "users": User.objects.count(),
        "permits": Permit.objects.count(),
    }
    users = User.objects.all().order_by("username")
    return render(request, "core/admin_dashboard.html", {"stats": stats, "users": users})


@login_required
def ngo_dashboard(request):
    require_role(request.user, User.NGO, User.ADMIN)

    if request.user.role == User.NGO and hasattr(request.user, "ngo"):
        projects = Project.objects.filter(ngo=request.user.ngo).order_by("-start_date")
    else:
        projects = Project.objects.select_related("ngo").all().order_by("-start_date")

    stats = {
        "projects": projects.count(),
        "active_projects": projects.filter(status="active").count(),
        "ngos": NGO.objects.count(),
    }

    return render(request, "core/ngo_dashboard.html", {"projects": projects, "stats": stats})


from django.contrib.auth.decorators import login_required
from .models import Workforce, User
from .utils import require_role

@login_required
def labour_dashboard(request):
    require_role(request.user, User.LABOUR, User.ADMIN)
    workforce = Workforce.objects.select_related("project", "project__ngo").all()

    # Add a total attribute to each object
    for wf in workforce:
        wf.total_workers_count = wf.local_workers + wf.foreign_workers

    total_workforce = sum([wf.total_workers_count for wf in workforce])
    total_projects = workforce.count()

    context = {
        "workforce": workforce,
        "total_workforce": total_workforce,
        "total_projects": total_projects,
    }
    return render(request, "core/labour_dashboard.html", context)


from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Permit, User
from .utils import require_role

from django.shortcuts import render
from .models import Permit

def migration_dashboard(request):
    today = timezone.now().date()
    ngo_permits = Permit.objects.filter(permit_type="NGO")
    foreign_worker_permits = Permit.objects.filter(permit_type="FOREIGN_WORKER")
    context = {
        "today": today,
        "ngo_permits": ngo_permits,
        "foreign_worker_permits": foreign_worker_permits,
    }
    return render(request, "core/migration_dashboard.html", context)

@login_required
def migration_dashboard(request):
    require_role(request.user, User.MIGRATION, User.ADMIN)

    permits = Permit.objects.select_related("project").all().order_by("-issue_date")

    today = timezone.now().date()
    stats = {
        "permits": permits.count(),
        "valid": sum(1 for p in permits if p.expiry_date >= today),
        "expired": sum(1 for p in permits if p.expiry_date < today),
    }

    return render(request, "core/migration_dashboard.html", {"permits": permits, "stats": stats, "today": today})

# ---------- NGO: Project CRUD ----------
@login_required
def project_list(request):
    require_role(request.user, User.NGO, User.ADMIN)
    if request.user.role == User.NGO and hasattr(request.user, "ngo"):
        projects = Project.objects.filter(ngo=request.user.ngo).order_by("-start_date")
    else:
        projects = Project.objects.select_related("ngo").all().order_by("-start_date")
    return render(request, "core/projects/project_list.html", {"projects": projects})


@login_required
def project_create(request):
    require_role(request.user, User.NGO, User.ADMIN)
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        if request.user.role == User.NGO and hasattr(request.user, "ngo"):
            project.ngo = request.user.ngo
        project.created_by = request.user
        project.save()
        messages.success(request, "Project created successfully.")
        return redirect("project_list")
    return render(request, "core/projects/project_form.html", {"form": form, "title": "Create Project"})


@login_required
def project_update(request, pk):
    require_role(request.user, User.NGO, User.ADMIN)
    project = get_object_or_404(Project, pk=pk)
    if request.user.role == User.NGO and project.ngo != request.user.ngo:
        messages.error(request, "You cannot edit this project.")
        return redirect("project_list")
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        messages.success(request, "Project updated successfully.")
        return redirect("project_list")
    return render(request, "core/projects/project_form.html", {"form": form, "title": "Update Project"})


@login_required
def project_delete(request, pk):
    require_role(request.user, User.NGO, User.ADMIN)
    project = get_object_or_404(Project, pk=pk)
    if request.user.role == User.NGO and project.ngo != request.user.ngo:
        messages.error(request, "You cannot delete this project.")
        return redirect("project_list")
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted.")
        return redirect("project_list")
    return render(request, "core/projects/project_confirm_delete.html", {"project": project})


# ---------- Labour: Workforce CRUD ----------
@login_required
def workforce_list(request):
    require_role(request.user, User.LABOUR, User.ADMIN)
    rows = Workforce.objects.select_related("project", "project__ngo").all()
    return render(request, "core/workforce/workforce_list.html", {"rows": rows})


@login_required
def workforce_edit(request, pk):
    require_role(request.user, User.LABOUR, User.ADMIN)
    wf = get_object_or_404(Workforce, pk=pk)
    form = WorkforceForm(request.POST or None, instance=wf)
    if form.is_valid():
        form.save()
        messages.success(request, "Workforce updated.")
        return redirect("workforce_list")
    return render(request, "core/workforce/workforce_form.html", {"form": form, "title": f"Edit Workforce for {wf.project.title}"})


# ---------- Migration: Permit CRUD ----------
@login_required
def permit_list(request):
    require_role(request.user, User.MIGRATION, User.ADMIN)
    permits = Permit.objects.select_related("project", "project__ngo").all().order_by("expiry_date")
    today = timezone.now().date()
    return render(request, "core/permits/permit_list.html", {"permits": permits, "today": today})


@login_required
def permit_create(request):
    require_role(request.user, User.MIGRATION, User.ADMIN)
    form = PermitForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Permit created.")
        return redirect("permit_list")
    return render(request, "core/permits/permit_form.html", {"form": form, "title": "Create Permit"})


@login_required
def permit_update(request, pk):
    require_role(request.user, User.MIGRATION, User.ADMIN)
    obj = get_object_or_404(Permit, pk=pk)
    form = PermitForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Permit updated.")
        return redirect("permit_list")
    return render(request, "core/permits/permit_form.html", {"form": form, "title": "Update Permit"})


@login_required
def permit_delete(request, pk):
    require_role(request.user, User.MIGRATION, User.ADMIN)
    obj = get_object_or_404(Permit, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Permit deleted.")
        return redirect("permit_list")
    return render(request, "core/permits/permit_confirm_delete.html", {"permit": obj})
