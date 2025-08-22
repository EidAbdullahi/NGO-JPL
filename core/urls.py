# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ---------- Auth ----------
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("", views.redirect_after_login, name="redirect_after_login"),

    # ---------- Dashboards ----------
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/ngo/", views.ngo_dashboard, name="ngo_dashboard"),
    path("dashboard/labour/", views.labour_dashboard, name="labour_dashboard"),
    path("dashboard/migration/", views.migration_dashboard, name="migration_dashboard"),

    # ---------- NGO: Project CRUD ----------
    path("projects/", views.project_list, name="project_list"),
    path("projects/create/", views.project_create, name="project_create"),
    path("projects/<int:pk>/update/", views.project_update, name="project_update"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),

    # ---------- Labour: Workforce ----------
    path("workforce/", views.workforce_list, name="workforce_list"),
    path("workforce/<int:pk>/edit/", views.workforce_edit, name="workforce_edit"),

    # ---------- Migration: Permit ----------
    path("permits/", views.permit_list, name="permit_list"),
    path("permits/create/", views.permit_create, name="permit_create"),
    path("permits/<int:pk>/update/", views.permit_update, name="permit_update"),
    path("permits/<int:pk>/delete/", views.permit_delete, name="permit_delete"),
]
