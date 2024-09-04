from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    FullName = models.CharField(max_length=70, blank=False)
    Username = models.CharField(max_length=70, unique=True)  # Username column matches SQL column name
    Email = models.CharField(max_length=50, unique=True)  # Shortened to match SQL definition
    UserPassword = models.CharField(max_length=255)  # Password column matches SQL definition
    UserRole = models.BooleanField(default=False)  # Matches BIT column (0 = user, 1 = admin)
    CreatedDate = models.DateTimeField(default=timezone.now, blank=False)
    EmailVerified = models.BooleanField(default=False)
    UpdatedDate = models.DateTimeField(default=timezone.now, blank=True, null=True)
    IsActive = models.BooleanField(default=False)
    Canlogin = models.BooleanField(default=True)  # Matches SQL column name

    def set_password(self, raw_password):
        self.UserPassword = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.UserPassword)

    def __str__(self):
        return self.Username
    
    class Meta:
        db_table = 'USER'  # Custom table name for SQL Server

class PasswordReset(models.Model):
    ResetID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    ResetToken = models.CharField(max_length=70)
    CreatedDate = models.DateTimeField(default=timezone.now)
    ExpireDate = models.DateTimeField()

    class Meta:
        db_table = 'users.PasswordResets'  # Custom table name for SQL Server

class LoginAttempt(models.Model):
    AttemptID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    AttemptTime = models.DateTimeField(default=timezone.now)
    Successful = models.BooleanField()  # Matches BIT column
    IpAddress = models.CharField(max_length=20)

    class Meta:
        db_table = 'users.LoginAttempts'  # Custom table name for SQL Server

class UserSession(models.Model):
    SessionID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    SessionToken = models.CharField(max_length=255, unique=True)
    CreatedDate = models.DateTimeField(default=timezone.now)
    ExpireDate = models.DateTimeField()
    IpAddress = models.CharField(max_length=45)
    UserAgent = models.TextField()

    class Meta:
        db_table = 'users.UserSessions'  # Custom table name for SQL Server
