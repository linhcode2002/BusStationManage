from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField
from .models import *

class BusCompanySerializer(ModelSerializer):
    class Meta:
        model = BusCompany
        fields = ['id', 'name', 'description', 'avatar']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'read_only': True}
        }
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('username', None)  # Xóa trường 'username' khỏi validated_data để đảm bảo không thay đổi
        return super().update(instance, validated_data)

class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class DeliverySerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'created_date', 'updated_date']

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'comment', 'created_date', 'updated_date']

class RevenueStatisticsSerializer(ModelSerializer):
    class Meta:
        model = RevenueStatistics
        fields = '__all__'


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserRoleSerializer(ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class BusRouteSerializer(ModelSerializer):
    bus_company = PrimaryKeyRelatedField(source='bus_company.id', read_only=True)
    class Meta:
        model = BusRoute
        fields = ['id', 'bus_company', 'route_name', 'start_location', 'end_location']

    def create(self, validated_data):
        user = self.context['request'].user
        if user.groups.filter(name='bus_company').exists():
            return super().create(validated_data)
        else:
            raise ValidationError("Bạn không có quyền tạo tuyến xe.")

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.groups.filter(name='bus_company').exists() and instance.bus_company.admin_user == user:
            return super().update(instance, validated_data)
        else:
            raise ValidationError("Bạn không có quyền sửa tuyến xe.")


class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'