from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.core.checks import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from .serializer import *
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
import qrcode
from django.core.mail import send_mail
from .forms import CustomerProfileForm, PasswordChangeForm
from django.shortcuts import render, get_object_or_404
from .models import Trip, Seat
from django.shortcuts import redirect
from datetime import datetime
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os
import json
import uuid
import hmac
import hashlib
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def search_trip(request):
    departure = request.GET.get('departure')
    destination = request.GET.get('destination')
    date_input = request.GET.get('date')

    now = timezone.now()

    queryset = Trip.objects.filter(active=True, departure_time__gt=now)

    if departure:
        queryset = queryset.filter(bus_route__start_location__icontains=departure)
    if destination:
        queryset = queryset.filter(bus_route__end_location__icontains=destination)

    if date_input:
        try:
            departure_date = datetime.strptime(date_input, '%d/%m/%Y').date()
            start_datetime = timezone.make_aware(datetime.combine(departure_date, datetime.min.time()))
            end_datetime = timezone.make_aware(datetime.combine(departure_date, datetime.max.time()))
            queryset = queryset.filter(departure_time__range=(start_datetime, end_datetime))
        except ValueError:
            return HttpResponse("<h1>Định dạng ngày không hợp lệ!</h1><a href='/'>Quay về trang chủ</a>")

    trips = []
    for trip in queryset:
        duration = trip.arrival_time - trip.departure_time
        total_seconds = duration.total_seconds()

        # Tính số giờ và phút
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # Chuyển đổi sang số nguyên cho giờ và phút
        hours = int(hours)
        minutes = int(minutes)

        # Thêm thông tin thời gian vào trip
        setattr(trip, 'duration_str', f"{hours} giờ {minutes} phút")
        trips.append(trip)

    context = {
        'trips': trips,
        'departure': departure,
        'destination': destination,
        'date': date_input
    }

    return render(request, 'website/trip_search_results.html', context)



class LoginView(APIView):
    def post(self, request):
        # Xử lý đăng nhập bằng email và mật khẩu
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            try:
                user = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return Response({"message": "Email không đúng."}, status=status.HTTP_400_BAD_REQUEST)

            # Kiểm tra mật khẩu đã băm
            if check_password(password, user.password):
                # Lưu thông tin người dùng vào session
                request.session['customer_id'] = user.id
                request.session['is_customer_authenticated'] = True
                request.session['customer_email'] = user.email

                return Response({"message": "Đăng nhập thành công!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Mật khẩu không đúng."}, status=status.HTTP_400_BAD_REQUEST)

        # Xử lý đăng nhập bằng Google
        token = request.data.get('token')  # Nhận token từ Google
        if token:
            try:
                # Xác thực token từ Google
                idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)

                # Lấy thông tin người dùng
                email = idinfo['email']
                user, created = Customer.objects.get_or_create(email=email)

                if created:
                    # Nếu người dùng mới, bạn có thể thiết lập thêm thông tin
                    user.username = email.split('@')[0]  # Tạo username từ email
                    user.is_active = True  # Kích hoạt người dùng
                    user.save()

                # Lưu thông tin người dùng vào session
                request.session['customer_id'] = user.id
                request.session['is_customer_authenticated'] = True
                request.session['customer_email'] = user.email

                return Response({"message": "Đăng nhập bằng Google thành công!"}, status=status.HTTP_200_OK)

            except ValueError:
                return Response({"message": "Token không hợp lệ."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"message": f"Có lỗi xảy ra: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Vui lòng cung cấp email và mật khẩu hoặc token Google."}, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    def post(self, request):
        # Lấy dữ liệu từ yêu cầu POST
        email = request.data.get('email')
        password = request.data.get('password')

        # Kiểm tra xem tất cả các trường đều có giá trị
        if not email or not password:
            return Response({"message": "Vui lòng nhập đầy đủ thông tin."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra xem email có tồn tại không
        if Customer.objects.filter(email=email).exists():
            return Response({"message": "Email này đã được đăng ký."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Tạo người dùng mới
            customer = Customer(
                email=email,
                password=make_password(password)  # Băm mật khẩu trước khi lưu
            )
            customer.full_clean()  # Kiểm tra tính hợp lệ của dữ liệu
            customer.save()

            return Response({"message": "Đăng ký thành công!"}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # Xử lý các lỗi validation
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Xử lý các lỗi khác
            return Response({"message": "Có lỗi xảy ra. Vui lòng thử lại sau."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@login_required
def profile_view(request):
    is_authenticated = request.session.get('is_customer_authenticated', False)
    customer_email = request.session.get('customer_email')
    print("Customer session:", request.session.get('customer_id'), request.session.get('customer_email'))

    try:
        customer = Customer.objects.get(email=customer_email)
    except Customer.DoesNotExist:
        return redirect('login')

    # Khởi tạo biến form và password_form
    form = CustomerProfileForm(instance=customer)
    password_form = PasswordChangeForm(initial={'email': customer_email})

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            # Xử lý cập nhật thông tin cá nhân
            form = CustomerProfileForm(request.POST, request.FILES, instance=customer)
            if form.is_valid():
                form.save()
                return redirect('profile')  # Thay đổi này nếu bạn đã định nghĩa trong urls.py
        elif 'change_password' in request.POST:
            # Xử lý đổi mật khẩu
            password_form = PasswordChangeForm(request.POST, initial={'email': customer_email})
            if password_form.is_valid():
                # Kiểm tra mật khẩu cũ
                if check_password(password_form.cleaned_data['old_password'], customer.password):
                    # Kiểm tra mật khẩu mới và xác nhận
                    new_password = password_form.cleaned_data['new_password']
                    confirm_password = password_form.cleaned_data['confirm_password']
                    if new_password == confirm_password:
                        # Băm mật khẩu mới và lưu vào customer
                        customer.password = make_password(new_password)
                        customer.save()
                        return redirect('profile')  # Thay đổi này nếu bạn đã định nghĩa trong urls.py
                    else:
                        password_form.add_error('confirm_password', "Mật khẩu mới và xác nhận không khớp.")
                else:
                    password_form.add_error('old_password', "Mật khẩu cũ không chính xác.")

    return render(request, 'website/profile.html', {
        'is_authenticated': is_authenticated,
        'customer_email': customer_email,
        'form': form,
        'password_form': password_form,
    })


def submit_review(request):
    is_authenticated = request.session.get('is_customer_authenticated', False)
    customer_email = request.session.get('customer_email')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Kiểm tra các trường bắt buộc
        if not all([name, email, phone_number, title, content]):
            messages.error(request, "Vui lòng điền đầy đủ các thông tin.")
            return redirect('contact')  # Quay lại trang liên hệ nếu có lỗi

        # Lưu đánh giá vào database
        Review.objects.create(
            name=name,
            customer_email=email,
            phone_number=phone_number,
            title=title,
            content=content
        )

        messages.success(request, "Đánh giá của bạn đã được gửi thành công!")
        return redirect('contact')  # Quay lại trang liên hệ sau khi gửi thành công

    return render(request, 'website/contact.html', {
        'is_authenticated': is_authenticated,
        'customer_email': customer_email,
    })


def home(request):
    is_authenticated = request.session.get('is_customer_authenticated', False)
    customer_email = request.session.get('customer_email')

    return render(request, 'website/home.html', {
        'is_authenticated': is_authenticated,
        'customer_email': customer_email,
    })


def logout_view(request):
    auth_logout(request)  # Gọi hàm logout của Django
    request.session.flush()  # Xóa tất cả dữ liệu session
    return redirect('home')  # Chuyển hướng về trang chính

def generate_signature(raw_data, secret_key):
    """Generate HMAC SHA256 signature"""
    return hmac.new(bytes(secret_key, 'utf-8'), bytes(raw_data, 'utf-8'), hashlib.sha256).hexdigest()


def booking(request, trip_id):
    is_authenticated = request.session.get('is_customer_authenticated', False)
    customer_email = request.session.get('customer_email')
    trip = get_object_or_404(Trip, id=trip_id)
    seats = list(Seat.objects.filter(bus=trip.bus_route.bus))
    booked_seats = Booking.objects.filter(trip=trip).values_list('seat__name', flat=True)
    seats.reverse()

    total_price = 0  # Giá trị mặc định nếu không có POST request

    if request.method == 'POST':
        data = json.loads(request.body)
        selected_seats = data['selected_seats']
        customer_name = data['name']
        customer_phone = data['phone']
        customer_email = data['email']
        total_price = data.get('total_price', 0)

        if len(selected_seats) == 0:
            messages.error(request, "Vui lòng chọn ít nhất một ghế.")
            return JsonResponse({'error': 'No seats selected'})

        booking_ids = []  # Danh sách lưu ID của tất cả booking

        for seat_name in selected_seats:
            if seat_name in booked_seats:
                messages.error(request, f"Ghế {seat_name} đã được đặt.")
                return JsonResponse({'error': f'Seat {seat_name} unavailable'})

            seat = get_object_or_404(Seat, name=seat_name)

            # Tạo booking và thêm vào danh sách booking_ids
            booking = Booking.objects.create(
                trip=trip,
                seat=seat,
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_email=customer_email
            )
            booking_ids.append(booking.id)  # Thêm booking ID vào danh sách

        request.session['booking_ids'] = booking_ids  # Lưu danh sách booking_id vào session
        request.session['total_price'] = total_price  # Lưu tổng giá tiền vào session
        request.session['booking_name'] = customer_name

        payment_url = reverse('payment_success')  # URL thanh toán
        return JsonResponse({'payment_url': payment_url})

    return render(request, 'website/booking.html', {
        'trip': trip,
        'seats': seats,
        'booked_seats': booked_seats,
        'is_authenticated': is_authenticated,
        'customer_email': customer_email,
        'amount': total_price  # Sử dụng giá trị mặc định
    })

import logging

logger = logging.getLogger(__name__)

# def zalo_payment(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         customer_name = data['name']
#         customer_phone = data['phone']
#         customer_email = data['email']
#         total_amount = data['amount']  # Số tiền thanh toán (tính theo đơn vị VNĐ)
#         logger.info("Customer Name: %s", customer_name)
#         logger.info("Customer Phone: %s", customer_phone)
#         logger.info("Customer Email: %s", customer_email)
#         logger.info("Total Amount: %s", total_amount)
#         # ZaloPay endpoint và thông tin tích hợp
#         endpoint = "https://sandbox.zalopay.com.vn/v001/tpe/createorder"  # Dùng môi trường test của ZaloPay
#         app_id = settings.ZALOPAY_APP_ID
#         key1 = settings.ZALOPAY_KEY1
#         key2 = settings.ZALOPAY_KEY2
#         order_info = "Thanh toán vé xe"
#         redirect_url = "https://127.0.0.1:8000/thanh-toan-thanh-cong"
#         ipn_url = "https://127.0.0.1:8000/ayment-ipn"
#         amount = str(total_amount)
#         order_id = str(int(datetime.timestamp(datetime.now())))  # ID đơn hàng duy nhất
#         app_trans_id = f"{datetime.now():%y%m%d}_{order_id}"  # Mã giao dịch ứng dụng
#         embed_data = ""
#         item = json.dumps([{'name': 'Vé xe', 'amount': total_amount}])
#
#         # Tạo chữ ký (signature) cho ZaloPay
#         raw_data = f"{app_id}|{app_trans_id}|{amount}|{ipn_url}|{key1}"
#         signature = hmac.new(bytes(key1, 'utf-8'), bytes(raw_data, 'utf-8'), hashlib.sha256).hexdigest()
#
#         # Payload gửi tới ZaloPay
#         payload = {
#             'app_id': app_id,
#             'app_trans_id': app_trans_id,
#             'app_user': customer_email,  # Email của người dùng
#             'amount': amount,
#             'app_time': int(datetime.now().timestamp() * 1000),  # Thời gian tạo đơn hàng
#             'item': item,
#             'embed_data': embed_data,
#             'description': order_info,
#             'bank_code': '',  # Mã ngân hàng nếu có (có thể để trống)
#             'mac': signature,  # Chữ ký
#             'callback_url': ipn_url  # URL để ZaloPay gửi thông báo
#         }
#
#         # Gửi yêu cầu POST tới ZaloPay
#         response = requests.post(endpoint, json=payload)
#         response_data = response.json()
#
#         # Kiểm tra phản hồi từ ZaloPay
#         if response_data.get('order_url'):
#             return JsonResponse({'payUrl': response_data['order_url']})
#         else:
#             return JsonResponse({'error': response_data.get('message', 'Could not create payment request')})
#
#     return JsonResponse({'error': 'Invalid request method'})

def zalo_payment(request):
    total_amount = 50000  # 50,000 VND
    customer_email = 'test@example.com'  # Customer email

    endpoint = "https://sandbox.zalopay.com.vn/v001/tpe/createorder"
    app_id = settings.ZALOPAY_APP_ID
    key1 = settings.ZALOPAY_KEY1
    key2 = settings.ZALOPAY_KEY2
    order_info = "Thanh toán vé xe"
    redirect_url = "https://127.0.0.1:8000/thanh-toan-thanh-cong"
    amount = str(total_amount)
    order_id = str(int(datetime.timestamp(datetime.now())))
    app_trans_id = f"{datetime.now():%y%m%d}_{order_id}"
    item = json.dumps([{'name': 'Vé xe', 'amount': total_amount}])

    # Create signature
    raw_data = f"{app_id}|{app_trans_id}|{amount}|{redirect_url}|{key1}"
    signature = hmac.new(bytes(key1, 'utf-8'), bytes(raw_data, 'utf-8'), hashlib.sha256).hexdigest()

    # Print for debugging
    print("Raw data for signature:", raw_data)
    print("Signature:", signature)

    # Payload sent to ZaloPay
    payload = {
        'app_id': app_id,
        'app_trans_id': app_trans_id,
        'app_user': customer_email,
        'amount': amount,
        'app_time': int(datetime.now().timestamp() * 1000),
        'item': item,
        'embed_data': json.dumps({}),
        'description': order_info,
        'mac': signature  # Signature
    }

    print("Payload:", payload)

    # Send POST request to ZaloPay
    response = requests.post(endpoint, json=payload)

    # Print HTTP status code and response text
    print("HTTP Status Code:", response.status_code)
    print("Raw Response Text:", response.text)

    # Check if response is JSON
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Response is not JSON', 'raw_response': response.text})

    # Check response from ZaloPay
    if response_data.get('returncode') == 0:
        return JsonResponse({'payUrl': response_data['orderurl']})
    else:
        error_message = response_data.get('returnmessage', 'Could not create payment request')
        return JsonResponse({'error': error_message})



@csrf_exempt
def momo_payment(request):
    # Kiểm tra xem thông tin đặt vé đã có trong session chưa
    total_price = request.session.get('total_price')
    if total_price is None:
        return JsonResponse({'error': 'No booking information available'}, status=400)

    # parameters send to MoMo get payUrl
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    orderInfo = "pay with MoMo"
    # Thay đổi redirectUrl để điều hướng đến trang payment_success của bạn
    redirectUrl = "http://127.0.0.1:8000/thanh-toan-thanh-cong/"  # Thay bằng URL thật của bạn
    ipnUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
    amount = str(total_price)  # Sử dụng tổng giá tiền đã lưu trong session
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    requestType = "captureWallet"
    extraData = ""  # pass empty value or Encode base64 JsonString

    # before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl
    # &orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId
    # &requestType=$requestType
    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType

    # puts raw signature
    print("--------------------RAW SIGNATURE----------------")
    print(rawSignature)
    # signature
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()
    print("--------------------SIGNATURE----------------")
    print(signature)

    # json object send to MoMo endpoint
    data = {
        'partnerCode': partnerCode,
        'partnerName': "Test",
        'storeId': "MomoTestStore",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    print("--------------------JSON REQUEST----------------\n")
    data = json.dumps(data)
    print(data)

    clen = len(data)
    response = requests.post(endpoint, data=data,
                             headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

    # In kết quả trả về
    print("--------------------JSON response----------------\n")
    print(response.json())

    # Lấy URL thanh toán từ phản hồi
    payment_url = response.json().get('payUrl')
    print(payment_url)
    # Chuyển hướng đến payment_url
    return HttpResponseRedirect(payment_url)

def payment_success(request):
    is_authenticated = request.session.get('is_customer_authenticated', False)
    customer_email = request.session.get('customer_email')
    booking_ids = request.session.get('booking_ids')
    booking_name = request.session.get('booking_name')

    if not booking_ids:
        return redirect('some_error_page')  # Chuyển hướng nếu không có booking_ids

    bookings = Booking.objects.filter(id__in=booking_ids)  # Lấy tất cả booking theo ID

    # Tạo dữ liệu QR cho từng booking
    qr_code_paths = []
    messages = []

    for booking in bookings:
        seat = booking.seat
        qr_data = f"Booking ID: {booking.id}, Trip: {booking.trip.id}, Seat: {seat.name}, Customer: {booking.customer_name}"

        qr_code_dir = 'media/qr_codes/'
        os.makedirs(qr_code_dir, exist_ok=True)

        qr_image_path = f"{qr_code_dir}booking_{booking.id}.png"
        qr_img = qrcode.make(qr_data)
        qr_img.save(qr_image_path)

        qr_code_paths.append(qr_image_path)  # Thêm đường dẫn mã QR vào danh sách

        # Tạo nội dung email cho mỗi booking
        subject = "Thông tin đặt vé xe"
        message = f"""
        Xin chào {booking.customer_name},

        Cảm ơn bạn đã đặt vé. Dưới đây là thông tin đặt vé của bạn:

        - Mã vé: {booking.ticket_code}
        - Chuyến đi: {booking.trip.bus_route.route_name}
        - Thời gian khởi hành: {booking.trip.departure_time}
        - Ghế đã đặt: {seat.name}
        - Tên khách hàng: {booking.customer_name}
        - Số điện thoại: {booking.customer_phone}
        - Thời gian đặt vé: {booking.booking_time.strftime('%Y-%m-%d %H:%M:%S')}

        Vui lòng giữ thông tin này để xác nhận đặt vé của bạn. Nếu bạn có bất kỳ câu hỏi nào, đừng ngần ngại liên hệ với chúng tôi.

        Trân trọng,
        Đội ngũ hỗ trợ khách hàng
        """

        # Gửi email cho mỗi booking
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [booking.customer_email],
            fail_silently=False,
        )

    return render(request, 'website/payment_success.html', {
        'is_authenticated': is_authenticated,
        'customer_email': customer_email,
        'booking_name': booking_name,
        'bookings': bookings,
        # 'qr_code_paths': qr_code_paths,  # Truyền đường dẫn mã QR vào template
    })

def some_error_page(request):
    is_authenticated = request.session.get('is_customer_authenticated', False)
    customer_email = request.session.get('customer_email')

    return render(request, 'website/some_error_page.html', {
        'is_authenticated': is_authenticated,
        'customer_email': customer_email,
    })
def schedule(request):
    is_authenticated = request.session.get('is_customer_authenticated', False)
    customer_email = request.session.get('customer_email')

    active_trips = Trip.objects.filter(active=True)

    return render(request, 'website/schedule.html', {
        'is_authenticated': is_authenticated,
        'customer_email': customer_email,
        'active_trips': active_trips,
    })


def ticket_search(request):
    is_authenticated = request.session.get('is_customer_authenticated', False)
    customer_email = request.session.get('customer_email')

    bookings = []
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        bookings = Booking.objects.filter(customer_email=email, customer_phone=phone_number).order_by('-booking_time')

    return render(request, 'website/ticket-search.html', {
        'is_authenticated': is_authenticated,
        'customer_email': customer_email,
        'bookings': bookings
    })


def contact(request):
    is_authenticated = request.session.get('is_customer_authenticated', False)
    customer_email = request.session.get('customer_email')

    return render(request, 'website/contact.html', {
        'is_authenticated': is_authenticated,
        'customer_email': customer_email,
    })


def about(request):
    is_authenticated = request.session.get('is_customer_authenticated', False)
    customer_email = request.session.get('customer_email')

    return render(request, 'website/about.html', {
        'is_authenticated': is_authenticated,
        'customer_email': customer_email,
    })

# class BusCompanyViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView,
#                         generics.RetrieveAPIView):
#     queryset = BusCompany.objects.filter(active=True)
#     serializer_class = BusCompanySerializer
#
#     permission_classes_by_action = {
#         'create': [IsBusCompany],  # Chỉ cần phải là BusCompany mới có thể tạo
#         'list': [AllowAny],  # Mọi người đều có thể xem danh sách
#         'retrieve': [IsBusCompany]  # Chỉ có BusCompany mới có thể xem chi tiết
#     }
#
#     def get_permissions(self):
#         # Lấy danh sách các lớp phân quyền tương ứng với hành động hiện tại
#         try:
#             # Lấy danh sách phân quyền cho hành động hiện tại
#             return [permission() for permission in self.permission_classes_by_action[self.action]]
#         except KeyError:
#             # Nếu không có phân quyền được định nghĩa cho hành động này, trả về phân quyền mặc định
#             return [permission() for permission in self.permission_classes]
#
#     @action(methods=['post'], url_path='comments', detail=True, permission_classes=[IsAuthenticated])
#     def add_comment(self, request, pk):
#         bus_company = self.get_object()
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user, bus_company=bus_company)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['post'], url_path='like', detail=True, permission_classes=[IsAuthenticated])
#     def like(self, request, pk):
#         bus_company = self.get_object()
#         like, created = Like.objects.get_or_create(user=request.user, bus_company=bus_company)
#         like.active = not like.active
#         like.save()
#
#         # Serialize lại đối tượng BusCompany
#         serializer = self.get_serializer(instance=bus_company)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     @action(methods=['get'], detail=True)
#     def get_comments(self, request, pk):
#         bus_company = self.get_object()
#         comments = Comments.objects.filter(bus_company=bus_company, active=True)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
#
#     @action(methods=['get'], detail=True)
#     def get_likes(self, request, pk):
#         bus_company = self.get_object()
#         likes = Like.objects.filter(bus_company=bus_company, active=True)
#         serializer = LikeSerializer(likes, many=True)
#         return Response(serializer.data)
#
#     @action(methods=['post'], url_path='reviews', detail=True, permission_classes=[IsAuthenticated])
#     def add_review(self, request, pk):
#         bus_company = self.get_object()
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             # Lưu đánh giá với thông tin user và bus_company
#             serializer.save(user=request.user, bus_company=bus_company)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['get'], detail=True)
#     def get_reviews(self, request, pk):
#         bus_company = self.get_object()
#         reviews = Review.objects.filter(bus_company=bus_company, active=True)
#         serializer = ReviewSerializer(reviews, many=True)
#         return Response(serializer.data)
#
#         # API sửa và xóa cho like, comment và review
#
#     @action(methods=['patch'], url_path='comments/(?P<comment_id>[^/.]+)/update', detail=True,
#             permission_classes=[IsAuthenticated])
#     def update_comment(self, request, pk, comment_id):
#         comment = get_object_or_404(Comments, pk=comment_id)
#
#         if comment.user != request.user:
#             return Response({"message": "Bạn không có quyền cập nhật bình luận này."}, status=status.HTTP_403_FORBIDDEN)
#
#         serializer = CommentSerializer(comment, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['delete'], url_path='comments/(?P<comment_id>[^/.]+)', detail=True,
#             permission_classes=[IsAuthenticated])
#     def delete_comment(self, request, pk, comment_id):
#         comment = get_object_or_404(Comments, pk=comment_id)
#         if comment.user == request.user:
#             comment.active = False
#             comment.save()
#             return Response({"message": "Bình luận đã được đánh dấu không hoạt động."},
#                             status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({"message": "Bạn không có quyền xóa bình luận này."}, status=status.HTTP_403_FORBIDDEN)
#
#     @action(methods=['patch'], url_path='reviews/(?P<review_id>[^/.]+)/update', detail=True,
#             permission_classes=[IsAuthenticated])
#     def update_review(self, request, pk, review_id):
#         review = get_object_or_404(Review, pk=review_id)
#
#         if review.user != request.user:
#             return Response({"message": "Bạn không có quyền cập nhật đánh giá này."}, status=status.HTTP_403_FORBIDDEN)
#
#         serializer = ReviewSerializer(review, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['delete'], url_path='reviews/(?P<review_id>[^/.]+)', detail=True,
#             permission_classes=[IsAuthenticated])
#     def delete_review(self, request, pk, review_id):
#         review = get_object_or_404(Review, pk=review_id)
#         if review.user == request.user:
#             review.active = False
#             review.save()
#             return Response({"message": "Đánh giá đã được đánh dấu không hoạt động."},
#                             status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "Bạn không có quyền xóa đánh giá này."}, status=status.HTTP_403_FORBIDDEN)
#
#     # Chú ý truyền theo params
#     @action(methods=['get'], url_path='search', detail=False)
#     def search_bus_companies(self, request):
#         # Lấy từ khóa tìm kiếm từ tham số truy vấn
#         keyword = request.GET.get('keyword', '')
#
#         # Tìm kiếm tất cả các nhà xe có tên gần giống với từ khóa
#         bus_companies = BusCompany.objects.filter(
#             Q(name__icontains=keyword) |  # Tìm theo tên nhà xe
#             Q(description__icontains=keyword)  # Tìm theo mô tả
#         ).distinct()  # Lọc bỏ các bản ghi trùng lặp
#
#         serializer = BusCompanySerializer(bus_companies, many=True)
#         return Response(serializer.data)
#
#
# class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView, generics.RetrieveAPIView):
#     queryset = User.objects.filter(is_active=True)
#     serializer_class = UserSerializer
#     parser_classes = [MultiPartParser]
#
#     def get_permissions(self):
#         if self.action == 'retrieve':
#             return [IsAuthenticated()]
#
#         return [AllowAny()]
#
#     # user/current_user/
#     @action(methods=['get'], url_name='current', detail=False, url_path='current-user')
#     def current_user(self, request):
#         if request.user.is_authenticated:
#             serializer = UserSerializer(request.user)
#             return Response(serializer.data)
#         else:
#             return Response({'error': 'Vui lòng đăng nhập để xem thông tin!'}, status=status.HTTP_401_UNAUTHORIZED)
#
#     # user/change_password/
#     @action(methods=['post'], url_name='change_password', detail=False, url_path='change-password')
#     def change_password(self, request):
#         user = request.user
#
#         # Kiểm tra mật khẩu cũ
#         old_password = request.data.get('old_password')
#         if not old_password or not check_password(old_password, user.password):
#             return Response({'error': 'Mật khẩu cũ không chính xác!'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Kiểm tra và cập nhật mật khẩu mới
#         new_password = request.data.get('new_password')
#         confirm_password = request.data.get('confirm_password')
#         if new_password != confirm_password:
#             return Response({'error': 'Mật khẩu mới và mật khẩu xác nhận không khớp!'},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         user.set_password(new_password)
#         user.save()
#
#         return Response({'success': 'Mật khẩu đã được thay đổi thành công!'}, status=status.HTTP_200_OK)
#
#     @action(detail=False, methods=['patch'], url_path='change-profile')
#     def change_profile(self, request):
#         user = request.user
#         serializer = self.serializer_class(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class DeliveryViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
#     queryset = Delivery.objects.filter(active=True)
#     serializer_class = DeliverySerializer
#     permission_classes_by_action = {
#         'create': [permissions.IsAuthenticated],
#         'retrieve': [permissions.IsAuthenticated],
#     }
#
#     def get_permissions(self):
#         try:
#             # return permission_classes depending on `action`
#             return [permission() for permission in self.permission_classes_by_action[self.action]]
#         except KeyError:
#             # action is not set, return default permission_classes
#             return [permission() for permission in self.permission_classes]
#
#     def create(self, request):
#         user = request.user
#         request.data['user'] = user.id
#
#         # Lấy thời gian hiện tại
#         current_time = timezone.now()
#
#         # Thiết lập delivery_time và pickup_time
#         request.data['delivery_time'] = current_time
#
#         # Tính toán pickup_time
#         pickup_time = current_time + timedelta(days=10)
#         request.data['pickup_time'] = pickup_time
#
#         serializer = DeliverySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def retrieve(self, request, pk):
#         user = request.user
#
#         try:
#             delivery = Delivery.objects.get(pk=pk)
#         except Delivery.DoesNotExist:
#             return Response({"message": "Gói hàng không tồn tại."},
#                             status=status.HTTP_404_NOT_FOUND)
#
#         if user.id != delivery.user_id:
#             return Response({"message": "Bạn không có quyền truy cập gói hàng này."},
#                             status=status.HTTP_403_FORBIDDEN)
#
#         serializer = DeliverySerializer(delivery)
#         return Response(serializer.data)
#
#     @action(methods=['patch'], detail=False, url_path='update/(?P<delivery_id>[^/.]+)',
#             permission_classes=[permissions.IsAuthenticated, IsBusCompany])
#     def update_delivery(self, request, delivery_id=None):
#         try:
#             delivery = Delivery.objects.get(pk=delivery_id)
#         except Delivery.DoesNotExist:
#             return Response({"message": "Gói hàng không tồn tại."}, status=status.HTTP_404_NOT_FOUND)
#
#         if not delivery.bus_company.admin_user == request.user:
#             return Response({"message": "Bạn không có quyền sửa gói hàng này."}, status=status.HTTP_403_FORBIDDEN)
#
#         active = request.data.get('active', delivery.active)
#         delivery_status = request.data.get('delivery_status', delivery.delivery_status)
#
#         delivery.active = active
#         delivery.delivery_status = delivery_status
#         delivery.save()
#
#         serializer = DeliverySerializer(delivery)
#         return Response(serializer.data)
#
#
# class RevenueStatisticsViewSet(viewsets.ModelViewSet):
#     queryset = RevenueStatistics.objects.all()
#     serializer_class = RevenueStatisticsSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
# class BusRouteViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView,
#                       generics.UpdateAPIView, generics.DestroyAPIView):
#     queryset = BusRoute.objects.filter(active=True)
#     serializer_class = BusRouteSerializer
#     permission_classes = [permissions.IsAuthenticated, IsBusCompany]
#
#     def get_permissions(self):
#         if self.action == 'create':
#             permission_classes = [permissions.IsAuthenticated, IsBusCompany]
#         elif self.action == 'update':
#             permission_classes = [permissions.IsAuthenticated, EditPermission]
#         else:
#             permission_classes = [permissions.AllowAny]
#         return [permission() for permission in permission_classes]
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if EditPermission().has_object_permission(request, self, instance):
#             instance.active = False
#             instance.save()
#             return Response({"message": "Xóa tuyến xe thành công."}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "Bạn không có quyền xóa tuyến xe."}, status=status.HTTP_403_FORBIDDEN)
#
#
# class TripViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView,
#                   generics.UpdateAPIView, generics.DestroyAPIView):
#     queryset = Trip.objects.filter(active=True)
#     serializer_class = TripSerializer
#     permission_classes_by_action = {
#         'create': [permissions.IsAuthenticated, IsBusCompany],
#         'update': [permissions.IsAuthenticated, IsBusCompany, EditPermission],
#         'partial_update': [permissions.IsAuthenticated, IsBusCompany, EditPermission],
#         'destroy': [permissions.IsAuthenticated, IsBusCompany, EditPermission],
#     }
#
#     def get_permissions(self):
#         try:
#             # return permission_classes depending on `action`
#             return [permission() for permission in self.permission_classes_by_action[self.action]]
#         except KeyError:
#             # action is not set, return default permission_classes
#             return [permission() for permission in self.permission_classes]
#
#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request):
#         # Lấy danh sách tuyến xe và nhà xe mà người dùng đăng nhập quản lý
#         user = request.user
#         bus_routes = BusRoute.objects.filter(bus_company__admin_user=user)
#         bus_companies = BusCompany.objects.filter(admin_user=user)
#
#         # Truyền danh sách tuyến xe và nhà xe vào serializer
#         serializer = self.serializer_class(data=request.data,
#                                            context={'bus_routes': bus_routes, 'bus_companies': bus_companies})
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Chuyến xe đã được tạo thành công."}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self, request, pk=None):
#         trip = self.queryset.filter(pk=pk).first()
#         if trip:
#             serializer = self.serializer_class(trip)
#             return Response(serializer.data)
#         return Response({"message": "Không tìm thấy chuyến xe."}, status=status.HTTP_404_NOT_FOUND)
#
#     def update(self, request, pk=None):
#         trip = self.queryset.filter(pk=pk).first()
#         if trip:
#             if request.user != trip.bus_company.admin_user:
#                 return Response({"message": "Bạn không có quyền cập nhật chuyến xe này."},
#                                 status=status.HTTP_403_FORBIDDEN)
#             bus_companies = BusCompany.objects.filter(admin_user=request.user)
#             serializer = self.serializer_class(trip, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({"message": "Chuyến xe đã được cập nhật thành công."})
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response({"message": "Cập nhật chuyến xe thất bại!"}, status=status.HTTP_404_NOT_FOUND)
#
#     def partial_update(self, request, pk=None):
#         trip = self.queryset.filter(pk=pk).first()
#         if trip:
#             if request.user != trip.bus_company.admin_user:
#                 return Response({"message": "Bạn không có quyền cập nhật chuyến xe này."},
#                                 status=status.HTTP_403_FORBIDDEN)
#             bus_companies = BusCompany.objects.filter(admin_user=request.user)
#             serializer = self.serializer_class(trip, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({"message": "Chuyến xe đã được cập nhật thành công."})
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response({"message": "Cập nhật chuyến xe thất bại!"}, status=status.HTTP_404_NOT_FOUND)
#
#     def destroy(self, request, pk=None):
#         trip = self.queryset.filter(pk=pk).first()
#         if trip:
#             if request.user != trip.bus_company.admin_user:
#                 return Response({"message": "Bạn không có quyền cập nhật chuyến xe này."},
#                                 status=status.HTTP_403_FORBIDDEN)
#             trip.active = False
#             trip.save()
#             return Response({"message": "Chuyến xe đã được xóa thành công."}, status=status.HTTP_204_NO_CONTENT)
#         return Response({"message": "Xóa chuyến xe thất bại!"}, status=status.HTTP_404_NOT_FOUND)
#
#     @action(methods=['get'], detail=False, url_path='search-trip')
#     def search_trip(self, request):
#         departure_location = request.query_params.get('departure_location', None)
#         arrival_location = request.query_params.get('arrival_location', None)
#         departure_date = request.query_params.get('departure_date', None)
#
#         queryset = self.queryset
#
#         if departure_location:
#             queryset = queryset.filter(bus_route__start_location__icontains=departure_location)
#         if arrival_location:
#             queryset = queryset.filter(bus_route__end_location__icontains=arrival_location)
#
#         if departure_date:
#             try:
#                 # Chuyển đổi chuỗi ngày thành đối tượng datetime
#                 departure_date = datetime.strptime(departure_date, '%Y-%m-%d')
#                 # Tạo đối tượng datetime bắt đầu và kết thúc cho ngày được chỉ định
#                 start_datetime = timezone.make_aware(datetime.combine(departure_date, datetime.min.time()))
#                 end_datetime = timezone.make_aware(datetime.combine(departure_date, datetime.max.time()))
#                 # Lọc các chuyến xe trong phạm vi thời gian từ start_datetime đến end_datetime
#                 queryset = queryset.filter(departure_time__range=(start_datetime, end_datetime))
#             except ValueError:
#                 pass  # Xử lý lỗi nếu định dạng không đúng
#
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data)
#
#
# class TicketViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView,
#                     generics.UpdateAPIView, generics.DestroyAPIView):
#     queryset = Ticket.objects.filter(active=True)
#     serializer_class = TicketSerializer
#     permission_classes_by_action = {
#         'create': [permissions.IsAuthenticated, IsBusCompany],
#         'update': [permissions.IsAuthenticated, IsBusCompany, EditTicketPermission],
#         'partial_update': [permissions.IsAuthenticated, IsBusCompany, EditTicketPermission],
#         'destroy': [permissions.IsAuthenticated, IsBusCompany, EditTicketPermission],
#     }
#
#     def get_permissions(self):
#         try:
#             # return permission_classes depending on `action`
#             return [permission() for permission in self.permission_classes_by_action[self.action]]
#         except KeyError:
#             # action is not set, return default permission_classes
#             return [permission() for permission in self.permission_classes]
#
#     def create(self, request, *args, **kwargs):
#         # Create a mutable copy of request.data
#         mutable_data = request.data.copy()
#         # Set active to True in the mutable copy
#         mutable_data['active'] = True
#         serializer = self.get_serializer(data=mutable_data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#     def destroy(self, request, pk=None):
#         ticket = self.queryset.filter(pk=pk).first()
#         if ticket:
#             if request.user != ticket.trip.bus_company.admin_user:
#                 return Response({"message": "Bạn không có quyền cập nhật vé xe này."},
#                                 status=status.HTTP_403_FORBIDDEN)
#             ticket.active = False
#             ticket.save()
#             return Response({"message": "Vé xe đã được xóa thành công."}, status=status.HTTP_204_NO_CONTENT)
#         return Response({"message": "Xóa vé xe thất bại!"}, status=status.HTTP_404_NOT_FOUND)
#
#
# class UserTicketViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
#     queryset = UserTicket.objects.all()
#     serializer_class = UserTicketSerializer
#
#     permission_classes_by_action = {
#         'create': [permissions.IsAuthenticated],
#         'retrieve': [permissions.IsAuthenticated],
#     }
#
#     def get_permissions(self):
#         try:
#             # return permission_classes depending on `action`
#             return [permission() for permission in self.permission_classes_by_action[self.action]]
#         except KeyError:
#             # action is not set, return default permission_classes
#             return [permission() for permission in self.permission_classes]
#
#     def create(self, request):
#         user = request.user
#         ticket_id = request.data.get('ticket_id')
#         if not ticket_id:
#             return Response({'error': 'Ticket ID is required'}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             ticket = Ticket.objects.get(id=ticket_id)
#         except Ticket.DoesNotExist:
#             return Response({'error': 'Vé không tồn tại!'}, status=status.HTTP_404_NOT_FOUND)
#
#         quantity = request.data.get('quantity', 1)
#         try:
#             quantity = int(quantity)
#             if quantity < 1:
#                 raise ValueError("Số lượng vé phải từ 1 trờ lên.")
#         except ValueError:
#             raise ValidationError("Số lượng vé phải là số nguyên hợp lệ!")
#
#         if ticket.remaining_seats < quantity:
#             return Response({'error': 'Không đủ vé để mua!'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Check if the user already has a ticket for this trip
#         existing_ticket = UserTicket.objects.filter(user=user, ticket=ticket).first()
#         if existing_ticket:
#             existing_ticket.quantity += quantity
#             existing_ticket.save()
#
#             ticket.remaining_seats -= quantity
#             ticket.save()
#             serializer = UserTicketSerializer(existing_ticket)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             user_ticket_data = {
#                 'user': user.id,
#                 'ticket': ticket_id,
#                 'payment_status': False,
#                 'is_online_booking': request.data.get('is_online_booking'),
#                 'quantity': quantity,
#             }
#             serializer = UserTicketSerializer(data=user_ticket_data)
#             serializer.is_valid(raise_exception=True)
#             user_ticket = serializer.save()
#             # Update remaining seats
#             ticket.remaining_seats -= quantity
#             ticket.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     @action(methods=['get'], url_name='list', detail=False, url_path='list')
#     def list_ticket(self, request):
#         user = request.user
#         user_tickets = UserTicket.objects.filter(user=user)
#         serializer = UserTicketSerializer(user_tickets, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk):
#         user = request.user
#
#         try:
#             user_ticket = UserTicket.objects.get(pk=pk)
#         except UserTicket.DoesNotExist:
#             return Response({"message": "Vé không tồn tại."},
#                             status=status.HTTP_404_NOT_FOUND)
#
#         if user.id != user_ticket.user_id:
#             return Response({"message": "Bạn không có quyền cập nhật vé xe này."},
#                             status=status.HTTP_403_FORBIDDEN)
#
#         serializer = UserTicketSerializer(user_ticket)
#         return Response(serializer.data)
#
#     @action(methods=['patch'], detail=False, url_path='update/(?P<user_ticket_id>[^/.]+)',
#             permission_classes=[permissions.IsAuthenticated, IsBusCompany])
#     def update_ticket(self, request, user_ticket_id=None):
#         try:
#             user_ticket = UserTicket.objects.get(pk=user_ticket_id)
#         except UserTicket.DoesNotExist:
#             return Response({"message": "Vé không tồn tại."}, status=status.HTTP_404_NOT_FOUND)
#
#         if not user_ticket.ticket.trip.bus_company.admin_user == request.user:
#             return Response({"message": "Bạn không có quyền sửa vé này."}, status=status.HTTP_403_FORBIDDEN)
#
#         active = request.data.get('active', user_ticket.active)
#         payment_status = request.data.get('payment_status', user_ticket.payment_status)
#
#         user_ticket.active = active
#         user_ticket.payment_status = payment_status
#         user_ticket.save()
#
#         serializer = UserTicketSerializer(user_ticket)
#         return Response(serializer.data)
