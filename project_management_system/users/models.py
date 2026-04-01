from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('ProjectManager', 'Project Manager'),
        ('TeamMember', 'Team Member'),
        ('Viewer', 'Viewer'),
    ]

    DEPARTMENT_CHOICES = [
        ('IT', 'Information Technology'),
        ('HR', 'Human Resources'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Operations', 'Operations'),
        ('Engineering', 'Engineering'),
        ('Sales', 'Sales'),
        ('Other', 'Other'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='TeamMember'
    )

    department = models.CharField(
        max_length=20,
        choices=DEPARTMENT_CHOICES,
        default='Other'
    )

    # Additional fields
    phone = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role}) - {self.department}"

    class Meta:
        ordering = ['username']
        verbose_name = "User"
        verbose_name_plural = "Users"