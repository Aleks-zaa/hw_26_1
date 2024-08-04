from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from materials.models import Course
from users.models import User, Payment
from users.serializers import UserSerializer, CreateUserSerializer, PaymentSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_product


class UserRegisterView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()


class UserRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


# class PaymentViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
#     ordering_fields = ('payment_date',)

class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['paid_lesson', 'paid_course', 'payment_method']
    ordering_fields = ['-payment_date']


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_stripe_product(payment)
        price = create_stripe_price(product_id, payment)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

