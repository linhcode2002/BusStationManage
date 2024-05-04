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

    @action(methods=['put'], url_path='comments/(?P<comment_id>[^/.]+)/update', detail=True,
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

    @action(methods=['put'], url_path='reviews/(?P<review_id>[^/.]+)/update', detail=True,
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

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return [permissions.IsAuthenticated]
    #
    #     return [permissions.AllowAny]

    #user/current_user/
    @action(methods=['get'], url_name='current', detail=False)
    def current_user(self, request):
        return Response(UserSerializer(request.user).data)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]

class RevenueStatisticsViewSet(viewsets.ModelViewSet):
    queryset = RevenueStatistics.objects.all()
    serializer_class = RevenueStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]

class BusRouteViewSet(viewsets.ModelViewSet):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
    permission_classes = [permissions.IsAuthenticated]


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]