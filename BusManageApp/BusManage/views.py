from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import perms
from .models import *
from .perms import *
from .serializer import *
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from datetime import datetime, date
from django.utils import timezone


class BusCompanyViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView,
                        generics.RetrieveAPIView):
    queryset = BusCompany.objects.filter(active=True)
    serializer_class = BusCompanySerializer

    permission_classes_by_action = {
        'create': [IsBusCompany],  # Chỉ cần phải là BusCompany mới có thể tạo
        'list': [AllowAny],  # Mọi người đều có thể xem danh sách
        'retrieve': [IsBusCompany]  # Chỉ có BusCompany mới có thể xem chi tiết
    }

    def get_permissions(self):
        # Lấy danh sách các lớp phân quyền tương ứng với hành động hiện tại
        try:
            # Lấy danh sách phân quyền cho hành động hiện tại
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # Nếu không có phân quyền được định nghĩa cho hành động này, trả về phân quyền mặc định
            return [permission() for permission in self.permission_classes]
    @action(methods=['post'], url_path='comments', detail=True, permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk):
        bus_company = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, bus_company=bus_company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], url_path='like', detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        bus_company = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, bus_company=bus_company)
        like.active = not like.active
        like.save()

        # Serialize lại đối tượng BusCompany
        serializer = self.get_serializer(instance=bus_company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def get_comments(self, request, pk):
        bus_company = self.get_object()
        comments = Comments.objects.filter(bus_company=bus_company, active=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def get_likes(self, request, pk):
        bus_company = self.get_object()
        likes = Like.objects.filter(bus_company=bus_company, active=True)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    @action(methods=['post'], url_path='reviews', detail=True, permission_classes=[IsAuthenticated])
    def add_review(self, request, pk):
        bus_company = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            # Lưu đánh giá với thông tin user và bus_company
            serializer.save(user=request.user, bus_company=bus_company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True)
    def get_reviews(self, request, pk):
        bus_company = self.get_object()
        reviews = Review.objects.filter(bus_company=bus_company, active=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

        # API sửa và xóa cho like, comment và review

    @action(methods=['patch'], url_path='comments/(?P<comment_id>[^/.]+)/update', detail=True,
            permission_classes=[IsAuthenticated])
    def update_comment(self, request, pk, comment_id):
        comment = get_object_or_404(Comments, pk=comment_id)

        if comment.user != request.user:
            return Response({"message": "Bạn không có quyền cập nhật bình luận này."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(methods=['delete'], url_path='comments/(?P<comment_id>[^/.]+)', detail=True,
            permission_classes=[IsAuthenticated])
    def delete_comment(self, request, pk, comment_id):
        comment = get_object_or_404(Comments, pk=comment_id)
        if comment.user == request.user:
            comment.active = False
            comment.save()
            return Response({"message": "Bình luận đã được đánh dấu không hoạt động."},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Bạn không có quyền xóa bình luận này."}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['patch'], url_path='reviews/(?P<review_id>[^/.]+)/update', detail=True,
            permission_classes=[IsAuthenticated])
    def update_review(self, request, pk, review_id):
        review = get_object_or_404(Review, pk=review_id)

        if review.user != request.user:
            return Response({"message": "Bạn không có quyền cập nhật đánh giá này."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='reviews/(?P<review_id>[^/.]+)', detail=True, permission_classes=[IsAuthenticated])
    def delete_review(self, request, pk, review_id):
        review = get_object_or_404(Review, pk=review_id)
        if review.user == request.user:
            review.active = False
            review.save()
            return Response({"message": "Đánh giá đã được đánh dấu không hoạt động."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "Bạn không có quyền xóa đánh giá này."}, status=status.HTTP_403_FORBIDDEN)

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated()]

        return [AllowAny()]

    # user/current_user/
    @action(methods=['get'], url_name='current', detail=False, url_path='current-user')
    def current_user(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response({'error': 'Vui lòng đăng nhập để xem thông tin!'}, status=status.HTTP_401_UNAUTHORIZED)


    # user/change_password/
    @action(methods=['post'], url_name='change_password', detail=False, url_path='change-password')
    def change_password(self, request):
        user = request.user

        # Kiểm tra mật khẩu cũ
        old_password = request.data.get('old_password')
        if not old_password or not check_password(old_password, user.password):
            return Response({'error': 'Mật khẩu cũ không chính xác!'}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra và cập nhật mật khẩu mới
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if new_password != confirm_password:
            return Response({'error': 'Mật khẩu mới và mật khẩu xác nhận không khớp!'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'success': 'Mật khẩu đã được thay đổi thành công!'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='change-profile')
    def change_profile(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = Delivery.objects.filter(active=True)
    serializer_class = DeliverySerializer
    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated],
        'retrieve': [permissions.IsAuthenticated],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set, return default permission_classes
            return [permission() for permission in self.permission_classes]

    def create(self, request):
        user = request.user
        request.data['user'] = user.id
        serializer = DeliverySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def retrieve(self, request, pk):
        user = request.user

        try:
            delivery = Delivery.objects.get(pk=pk)
        except Delivery.DoesNotExist:
            return Response({"message": "Gói hàng không tồn tại."},
                            status=status.HTTP_404_NOT_FOUND)

        if user.id != delivery.user_id:
            return Response({"message": "Bạn không có quyền truy cập gói hàng này."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)

    @action(methods=['patch'], detail=False, url_path='update/(?P<delivery_id>[^/.]+)',
            permission_classes=[permissions.IsAuthenticated, IsBusCompany])
    def update_delivery(self, request, delivery_id=None):
        try:
            delivery = Delivery.objects.get(pk=delivery_id)
        except Delivery.DoesNotExist:
            return Response({"message": "Gói hàng không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        if not delivery.bus_company.admin_user == request.user:
            return Response({"message": "Bạn không có quyền sửa gói hàng này."}, status=status.HTTP_403_FORBIDDEN)

        active = request.data.get('active', delivery.active)
        delivery_status = request.data.get('delivery_status', delivery.delivery_status)

        delivery.active = active
        delivery.delivery_status = delivery_status
        delivery.save()

        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)
class RevenueStatisticsViewSet(viewsets.ModelViewSet):
    queryset = RevenueStatistics.objects.all()
    serializer_class = RevenueStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]

class BusRouteViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView,
                      generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = BusRoute.objects.filter(active=True)
    serializer_class = BusRouteSerializer
    permission_classes = [permissions.IsAuthenticated, IsBusCompany]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsBusCompany]
        elif self.action == 'update':
            permission_classes = [permissions.IsAuthenticated, EditPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if EditPermission().has_object_permission(request, self, instance):
            instance.active = False
            instance.save()
            return Response({"message": "Xóa tuyến xe thành công."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Bạn không có quyền xóa tuyến xe."}, status=status.HTTP_403_FORBIDDEN)

class TripViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView,
                      generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Trip.objects.filter(active=True)
    serializer_class = TripSerializer
    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated, IsBusCompany],
        'update': [permissions.IsAuthenticated, IsBusCompany, EditPermission],
        'partial_update': [permissions.IsAuthenticated, IsBusCompany, EditPermission],
        'destroy': [permissions.IsAuthenticated, IsBusCompany, EditPermission],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set, return default permission_classes
            return [permission() for permission in self.permission_classes]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Lấy danh sách tuyến xe và nhà xe mà người dùng đăng nhập quản lý
        user = request.user
        bus_routes = BusRoute.objects.filter(bus_company__admin_user=user)
        bus_companies = BusCompany.objects.filter(admin_user=user)

        # Truyền danh sách tuyến xe và nhà xe vào serializer
        serializer = self.serializer_class(data=request.data,
                                           context={'bus_routes': bus_routes, 'bus_companies': bus_companies})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Chuyến xe đã được tạo thành công."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        trip = self.queryset.filter(pk=pk).first()
        if trip:
            serializer = self.serializer_class(trip)
            return Response(serializer.data)
        return Response({"message": "Không tìm thấy chuyến xe."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        trip = self.queryset.filter(pk=pk).first()
        if trip:
            if request.user != trip.bus_company.admin_user:
                return Response({"message": "Bạn không có quyền cập nhật chuyến xe này."},
                                status=status.HTTP_403_FORBIDDEN)
            bus_companies = BusCompany.objects.filter(admin_user=request.user)
            serializer = self.serializer_class(trip, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Chuyến xe đã được cập nhật thành công."})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Cập nhật chuyến xe thất bại!"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        trip = self.queryset.filter(pk=pk).first()
        if trip:
            if request.user != trip.bus_company.admin_user:
                return Response({"message": "Bạn không có quyền cập nhật chuyến xe này."},
                                status=status.HTTP_403_FORBIDDEN)
            bus_companies = BusCompany.objects.filter(admin_user=request.user)
            serializer = self.serializer_class(trip, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Chuyến xe đã được cập nhật thành công."})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Cập nhật chuyến xe thất bại!"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        trip = self.queryset.filter(pk=pk).first()
        if trip:
            if request.user != trip.bus_company.admin_user:
                return Response({"message": "Bạn không có quyền cập nhật chuyến xe này."},
                                status=status.HTTP_403_FORBIDDEN)
            trip.active=False
            trip.save()
            return Response({"message": "Chuyến xe đã được xóa thành công."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Xóa chuyến xe thất bại!"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, url_path='search-trip')
    def search_trip(self, request):
        departure_location = request.query_params.get('departure_location', None)
        arrival_location = request.query_params.get('arrival_location', None)
        departure_date = request.query_params.get('departure_date', None)

        queryset = self.queryset

        if departure_location:
            queryset = queryset.filter(bus_route__start_location__icontains=departure_location)
        if arrival_location:
            queryset = queryset.filter(bus_route__end_location__icontains=arrival_location)

        if departure_date:
            try:
                # Chuyển đổi chuỗi ngày thành đối tượng datetime
                departure_date = datetime.strptime(departure_date, '%Y-%m-%d')
                # Tạo đối tượng datetime bắt đầu và kết thúc cho ngày được chỉ định
                start_datetime = timezone.make_aware(datetime.combine(departure_date, datetime.min.time()))
                end_datetime = timezone.make_aware(datetime.combine(departure_date, datetime.max.time()))
                # Lọc các chuyến xe trong phạm vi thời gian từ start_datetime đến end_datetime
                queryset = queryset.filter(departure_time__range=(start_datetime, end_datetime))
            except ValueError:
                pass  # Xử lý lỗi nếu định dạng không đúng

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class TicketViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView,
                      generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Ticket.objects.filter(active=True)
    serializer_class = TicketSerializer
    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated, IsBusCompany],
        'update': [permissions.IsAuthenticated, IsBusCompany, EditTicketPermission],
        'partial_update': [permissions.IsAuthenticated, IsBusCompany, EditTicketPermission],
        'destroy': [permissions.IsAuthenticated, IsBusCompany, EditTicketPermission],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set, return default permission_classes
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        # Create a mutable copy of request.data
        mutable_data = request.data.copy()
        # Set active to True in the mutable copy
        mutable_data['active'] = True
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, pk=None):
        ticket = self.queryset.filter(pk=pk).first()
        if ticket:
            if request.user != ticket.trip.bus_company.admin_user:
                return Response({"message": "Bạn không có quyền cập nhật vé xe này."},
                                status=status.HTTP_403_FORBIDDEN)
            ticket.active=False
            ticket.save()
            return Response({"message": "Vé xe đã được xóa thành công."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Xóa vé xe thất bại!"}, status=status.HTTP_404_NOT_FOUND)
class UserTicketViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = UserTicket.objects.all()
    serializer_class = UserTicketSerializer

    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated],
        'retrieve': [permissions.IsAuthenticated],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set, return default permission_classes
            return [permission() for permission in self.permission_classes]
    def create(self, request):
        user = request.user
        ticket_id = request.data.get('ticket_id')
        if not ticket_id:
            return Response({'error': 'Ticket ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({'error': 'Vé không tồn tại!'}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity', 1)
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError("Số lượng vé phải từ 1 trờ lên.")
        except ValueError:
            raise ValidationError("Số lượng vé phải là số nguyên hợp lệ!")

        if ticket.remaining_seats < quantity:
            return Response({'error': 'Không đủ vé để mua!'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already has a ticket for this trip
        existing_ticket = UserTicket.objects.filter(user=user, ticket=ticket).first()
        if existing_ticket:
            existing_ticket.quantity += quantity
            existing_ticket.save()

            ticket.remaining_seats -= quantity
            ticket.save()
            serializer = UserTicketSerializer(existing_ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user_ticket_data = {
                'user': user.id,
                'ticket': ticket_id,
                'payment_status': False,
                'is_online_booking': request.data.get('is_online_booking'),
                'quantity': quantity,
            }
            serializer = UserTicketSerializer(data=user_ticket_data)
            serializer.is_valid(raise_exception=True)
            user_ticket = serializer.save()
            # Update remaining seats
            ticket.remaining_seats -= quantity
            ticket.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], url_name='list', detail=False, url_path='list')
    def list_ticket(self, request):
        user = request.user
        user_tickets = UserTicket.objects.filter(user=user)
        serializer = UserTicketSerializer(user_tickets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        user = request.user

        try:
            user_ticket = UserTicket.objects.get(pk=pk)
        except UserTicket.DoesNotExist:
            return Response({"message": "Vé không tồn tại."},
                            status=status.HTTP_404_NOT_FOUND)

        if user.id != user_ticket.user_id:
            return Response({"message": "Bạn không có quyền cập nhật vé xe này."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = UserTicketSerializer(user_ticket)
        return Response(serializer.data)

    @action(methods=['patch'], detail=False, url_path='update/(?P<user_ticket_id>[^/.]+)', permission_classes=[permissions.IsAuthenticated, IsBusCompany])
    def update_ticket(self, request, user_ticket_id=None):
        try:
            user_ticket = UserTicket.objects.get(pk=user_ticket_id)
        except UserTicket.DoesNotExist:
            return Response({"message": "Vé không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        if not user_ticket.ticket.trip.bus_company.admin_user == request.user:
            return Response({"message": "Bạn không có quyền sửa vé này."}, status=status.HTTP_403_FORBIDDEN)

        active = request.data.get('active', user_ticket.active)
        payment_status = request.data.get('payment_status', user_ticket.payment_status)

        user_ticket.active = active
        user_ticket.payment_status = payment_status
        user_ticket.save()

        serializer = UserTicketSerializer(user_ticket)
        return Response(serializer.data)

