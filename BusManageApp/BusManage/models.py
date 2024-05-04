from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from ckeditor.fields import RichTextField

class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True, folder="avatars")

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-id']

class Role(BaseModel):
    name = models.CharField(max_length=50)


class UserRole(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


class BusCompany(BaseModel):
    name = models.CharField(max_length=100)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_of_company')
    avatar = CloudinaryField('avatar', null=True, folder="BusAvatars")
    description = RichTextField()



class BusRoute(BaseModel):
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE)
    route_name = models.CharField(max_length=100)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='route_avatars/', null=True, blank=True)


class Trip(BaseModel):
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)


class Ticket(BaseModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_status = models.BooleanField(default=False)
    is_online_booking = models.BooleanField(default=False)


class Delivery(BaseModel):
    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=20)
    sender_email = models.EmailField()
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20)
    receiver_email = models.EmailField()
    delivery_time = models.DateTimeField()
    pickup_time = models.DateTimeField()
    delivery_status = models.CharField(max_length=50)
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE)

class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)

    class Meta:
        unique_together = ('user', 'bus_company')

class Comments(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE)
    comment = models.TextField()


class RevenueStatistics(BaseModel):
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    frequency = models.IntegerField()

class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    bus_company = models.ForeignKey(BusCompany, on_delete=models.RESTRICT, null=False)
    active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'bus_company')
