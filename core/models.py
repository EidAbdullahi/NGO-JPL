from django.db import models
from django.contrib.auth.models import AbstractUser


# -------------------------
# Custom User
# -------------------------
class User(AbstractUser):
    NGO = "NGO"
    LABOUR = "LABOUR"
    MIGRATION = "MIGRATION"
    ADMIN = "ADMIN"

    ROLE_CHOICES = [
        (NGO, "NGO"),
        (LABOUR, "Labour"),
        (MIGRATION, "Migration"),
        (ADMIN, "Admin"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=NGO)

    def __str__(self):
        return f"{self.username} ({self.role})"


# -------------------------
# NGO
# -------------------------
class NGO(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -------------------------
# Project
# -------------------------
# Project
# -------------------------
class Project(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.ngo.name})"



# -------------------------
# Workforce
# -------------------------
class Workforce(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="workforce")

    # Replacing old broken fields: foreign_staff, local_staff
    local_workers = models.PositiveIntegerField(default=0)
    foreign_workers = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def total(self):
        return self.local_workers + self.foreign_workers

    def __str__(self):
        return f"Workforce for {self.project.title}"


# -------------------------
# -------------------------
# Permit
# -------------------------
class Permit(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="permits")
    permit_number = models.CharField(max_length=100, unique=True)
    issue_date = models.DateField()
    expiry_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Permit {self.permit_number} for {self.project.title}"

    @property
    def status(self):
        from django.utils.timezone import now
        today = now().date()
        return "expired" if self.expiry_date < today else "valid"

