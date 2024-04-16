from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    # Thêm related_name cho các trường groups và user_permissions
    groups = models.ManyToManyField(Group, related_name='bus_users')
    user_permissions = models.ManyToManyField(Permission, related_name='bus_users')

class BusCompany(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_companies')
    approved = models.BooleanField(default=False)

class Route(models.Model):
    company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, related_name='routes')
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    paid_online = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class Delivery(models.Model):
    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=20)
    sender_email = models.EmailField()
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20)
    receiver_email = models.EmailField()
    delivery_time = models.DateTimeField()
    pickup_time = models.DateTimeField()
    completed = models.BooleanField(default=False)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(BusCompany, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

class BlockedCompany(models.Model):
    company = models.OneToOneField(BusCompany, on_delete=models.CASCADE)

class RealTimeChat(models.Model):
    # Define your Firebase integration here
    pass

class RevenueStatistic(models.Model):
    company = models.ForeignKey(BusCompany, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    # You can add more fields for detailed statistics if needed
