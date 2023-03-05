from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone


# TODO create a custom user
class CustomUser(UserManager):
    def _create_user_(self, email, password, **extra_fields):
        if not email:
            raise ValueError("please provide a valid email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user_(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user_(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUser()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        if self.name:
            return self.name
        else:
            return self.email.split('@')[0]


class Task(models.Model):
    class State(models.TextChoices):
        INCOMPLETE = "INCOMPLETE"
        PENDING = 'PENDING'
        COMPLETED = "COMPLETED"

    name = models.TextField(null=True, blank=True, )
    updated = models.DateTimeField(auto_now=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    description = models.TextField()
    priority = models.IntegerField()
    status = models.CharField(
        max_length=15, choices=State.choices, default=State.INCOMPLETE)

    def __str__(self):
        return self.name


class Reminder(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='reminders')
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=200)


class Notification(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    sent_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)


class TimeTracking(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='time_trackings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_time = models.FloatField()
