from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import datetime, date, time
from dirtyfields import DirtyFieldsMixin
import random
import string
from django.db import models

class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True, folder="avatars")

    def __str__(self):
        return self.username


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class Customer(DirtyFieldsMixin, BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)  # Không bắt buộc
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Không bắt buộc
    email = models.EmailField(unique=True)  # Bắt buộc
    address = models.CharField(max_length=255, null=True, blank=True)  # Không bắt buộc
    avatar = CloudinaryField('avatar', null=True, blank=True, folder="CustomerAvatars")  # Không bắt buộc
    password = models.CharField(max_length=255, validators=[MinLengthValidator(8)])  # Bắt buộc
    def __str__(self):
        return f"{self.name} - {self.phone_number}"

    # def save(self, *args, **kwargs):
    #     # Băm mật khẩu trước khi lưu
    #     if not self.pk or 'password' in self.get_dirty_fields():
    #         self.password = make_password(self.password)
    #     super().save(*args, **kwargs)

class Bus(BaseModel):
    license_plate = models.CharField(max_length=20)
    total_seats = models.IntegerField()
    driver = models.CharField(max_length=50)

    def __str__(self):
        return self.license_plate
class BusRoute(BaseModel):
    route_name = models.CharField(max_length=100)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    distance = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.route_name


class Trip(BaseModel):
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)  # Thêm giá trị mặc định

    def save(self, *args, **kwargs):
        if isinstance(self.departure_time, datetime):
            # Loại bỏ milliseconds
            self.departure_time = self.departure_time.replace(microsecond=0)
        if isinstance(self.arrival_time, datetime):
            self.arrival_time = self.arrival_time.replace(microsecond=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bus_route.route_name} - {self.departure_time}"

class Seat(BaseModel):
    name = models.CharField(max_length=5, unique=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TripStatistics(BaseModel):
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE)  # Mỗi chuyến xe chỉ có 1 bản thống kê
    total_tickets = models.IntegerField(default=0)  # Tổng số vé
    booked_tickets = models.IntegerField(default=0)  # Số vé người dùng đã đặt
    total_payment = models.DecimalField(max_digits=12, decimal_places=0, default=0)  # Tổng số tiền thanh toán

    def __str__(self):
        return f"Statistics for Trip: {self.trip.bus_route.route_name} - {self.trip.departure_time}"

class Booking(BaseModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=10)
    booking_time = models.DateTimeField(auto_now_add=True, null=True)
    ticket_code = models.CharField(max_length=6, unique=True, blank=True)  # Thêm trường mã vé

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['trip', 'seat', 'customer_email'],
                name='unique_trip_seat_email'
            )
        ]

    def save(self, *args, **kwargs):
        if not self.ticket_code:  # Kiểm tra nếu mã vé chưa có
            self.ticket_code = self.generate_ticket_code()  # Tạo mã vé ngẫu nhiên
        super().save(*args, **kwargs)

        # Cập nhật thông tin thống kê của chuyến xe
        trip_stats, created = TripStatistics.objects.get_or_create(trip=self.trip)
        trip_stats.booked_tickets += 1  # Tăng số lượng vé đã đặt
        trip_stats.total_payment += self.trip.ticket_price  # Tăng tổng số tiền thanh toán
        trip_stats.save()

    def generate_ticket_code(self):
        """Hàm tạo mã vé ngẫu nhiên gồm 6 ký tự chữ và số"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Booking.objects.filter(ticket_code=code).exists():
                return code

    def __str__(self):
        return f"Booking for {self.customer_name} - Seat {self.seat.name} ({self.trip.bus_route.route_name})"

class Review(BaseModel):
    title = models.CharField(max_length=255, default=None)  # Giới hạn độ dài tiêu đề
    content = models.TextField(default="No content")  # Dùng TextField để lưu nội dung dài
    customer_email = models.EmailField(default=None)  # Bắt buộc email của khách hàng
    name = models.CharField(max_length=50, default=None)  # Bắt buộc tên
    phone_number = models.CharField(max_length=10, default=None)  # Bắt buộc số điện thoại

    def __str__(self):
        return self.title



class RevenueStatistics(BaseModel):
    month = models.IntegerField(default=1)  # Thêm giá trị mặc định
    year = models.IntegerField(default=2024)  # Thêm giá trị mặc định
    revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Thêm giá trị mặc định
    frequency = models.IntegerField(default=0)  # Thêm giá trị mặc định
