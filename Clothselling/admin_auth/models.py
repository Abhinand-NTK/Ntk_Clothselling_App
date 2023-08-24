from django.db import models
from django.contrib.auth.models import  BaseUserManager,AbstractUser, Group, Permission
from django.utils import timezone


class Brand(models.Model):
    name=models.CharField(max_length=10)
    image=models.ImageField(upload_to='brand',blank=True)

    def __str__(self):
        return self.name
class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    active=models.BooleanField(default=True,null=True,blank=True)
    
    def __str__(self):
        return self.name

class  Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    active=models.BooleanField(default=True,null=True,blank=True)


    def __str__(self):
        return self.name

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()
    active = models.BooleanField(default=True,null=True,blank=True)

    def __str__(self):
        return self.code

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/banners')
    link = models.URLField()
    active = models.BooleanField(default=True,null=True,blank=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='photos/products',blank=True)
    # coupons = models.ManyToManyField(Coupon, blank=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_avaliable=models.BooleanField(default=True,null=True,blank=True)
    rating = models.FloatField(default=0)

class CustomUserManager(BaseUserManager):

    """Define a model manager for User model with no username field."""
    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

   

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

 

class CustomUser(AbstractUser):

    username = None
    is_verified=models.BooleanField(default=False)
    
    email = models.EmailField(unique=True)  # Email becomes the primary identifier
    is_blocked = models.BooleanField(default=False)

    otp = models.CharField(max_length=6, null=True, blank=True)

    
    # required
    created_at = models.DateTimeField(default=timezone.now,null=True,blank=True)


    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email



   







































# class CustomUserManager(BaseUserManager):
#     def create_user(self,email=None,password=None):
#         if not email:
#             raise ValueError('User must have either an email address or a phone number')
      
        
#         user = self.model(
#             email=self.normalize_email(email),
#         )
#         user.set_password(password)
#         user.save()
#         return user
    
#     def create_superuser(self, email, password):

#         user=self.create_user(email=self.normalize_email(email))
#         user.is_admin=True
#         user.is_active=True
#         user.is_staff=True
#         user.is_superadmin=True
#         user.save()
#         return user
        
# class CustomUser(AbstractBaseUser):
#     test=models.CharField(max_length=10,blank=True  )
#     email = models.EmailField(max_length=50, unique=True, blank=True, null=True)
#     phone = models.CharField(max_length=40, unique=True, blank=True, null=True)
#     otp=models.CharField(max_length=6, null=True, blank=True)

#     # Required fields
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)
#     is_superadmin = models.BooleanField(default=False)

#     is_email_verified=models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'  # You can change this to 'phone' if desired
#     REQUIRED_FIELDS = ['']  # Either email or phone is required for registration

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email or self.phone
    
#     def has_perm(self, perm, obj=None):
#         return self.is_admin
    
#     def has_module_perms(self, app_label):
#         return True

  