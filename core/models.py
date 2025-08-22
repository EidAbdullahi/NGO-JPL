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
from django.db import models

# -------------------------
# NGO
# -------------------------
class NGO(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    
    # New fields
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    area_manager = models.CharField(max_length=200, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='ngo_profiles/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # tracks changes

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
from django.db import models

# -------------------------
# Worker
# -------------------------
class Worker(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # New field

    def __str__(self):
        return self.name

# -------------------------
# Permit
# -------------------------
class Permit(models.Model):
    PERMIT_TYPE_CHOICES = [
        ("NGO", "NGO Permit"),
        ("FOREIGN_WORKER", "Foreign Worker Permit"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="permits")
    permit_number = models.CharField(max_length=100, unique=True)
    permit_type = models.CharField(max_length=20, choices=PERMIT_TYPE_CHOICES, default="NGO")
    issue_date = models.DateField()
    expiry_date = models.DateField()
    workers = models.ManyToManyField(Worker, blank=True, related_name="permits")  # only for FOREIGN_WORKER

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def status(self):
        from django.utils.timezone import now
        return "expired" if self.expiry_date < now().date() else "valid"

    def __str__(self):
        return f"{self.permit_number} ({self.get_permit_type_display()})"



    @property
    def status(self):
        from django.utils.timezone import now
        today = now().date()
        return "expired" if self.expiry_date < today else "valid"

