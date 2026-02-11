from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.
class CustomUserManager(BaseUserManager): #custom user model since intended to use email and password only
    def create_user(self, email, password=None, **extra_fields):
        if not email: #proper email validation
            raise ValueError('The Email field must be set')
        if not password: #proper password validation
            raise ValueError('The Password field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields): #super user linte wala ko ni gyapon kabalo ano ni pulos
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True: 
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True: 
            raise ValueError('Superuser must have is_superuser=True.')
        
        user = self.create_user(email=email, password=password, **extra_fields)
        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=150, blank=True, default="")
    avatar_url = models.URLField(blank=True, default="")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def role(self) -> str:
        # Keep role logic centralized for API serialization.
        # "admin" covers staff and superusers.
        return "admin" if (self.is_staff or getattr(self, "is_superuser", False)) else "student"

    @property
    def name(self) -> str | None:
        return self.full_name or None

    @property
    def avatar(self) -> str | None:
        return self.avatar_url or None

    def __str__(self):
        return self.email