from rest_framework import serializers
from .models import MyUser, AccountVerification
from .utils import send_verification_email
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from .models import DepositPayment


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("The user with this email already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = MyUser.objects.create_user(**validated_data)

        code = AccountVerification.generate_code()
        AccountVerification.objects.create(user=user, code=code)
        send_verification_email(user)
        return user



class AccountVerificationSerializer(serializers.Serializer):
    code = serializers.SlugField(max_length=32)

    def validate(self, data):
        code = data['code']

        verification = AccountVerification.objects.filter(code=code).first()
        if not verification:
            raise serializers.ValidationError('Code not found')

        user = verification.user
        if not user:
            raise serializers.ValidationError('Code is invalid')

        if not user.email:
            raise serializers.ValidationError('Unknown error')

        if verification.is_expired():
            raise serializers.ValidationError('Code is expired')

        verification.delete()

        data['user'] = user
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        user = MyUser.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError('User not found')

        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password')

        if not user.is_active:
            raise serializers.ValidationError('User is not active')

        if not user.is_verified:
            raise serializers.ValidationError('User is not verified')

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }




class DepositBalanceSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    card_number = serializers.CharField(write_only=True, max_length=16)
    card_expiry = serializers.CharField(write_only=True, max_length=5)
    card_cvv = serializers.CharField(write_only=True, max_length=4, required=False)
    otp_code = serializers.CharField(read_only=True, max_length=6)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The amount should be positive.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        amount = validated_data['amount']
        otp_code = DepositPayment.generate_code()
        deposit = DepositPayment.objects.create(user=user, otp_code=otp_code, amount=amount)
        deposit.save()
        data = {
            'amount': amount,
            'otp_code': otp_code,
            'message': 'OTP-код сгенерирован. Подтвердите пополнение.'

        }
        return data


class ConfirmDepositSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)

    def validate(self, data):
        otp_code = data['otp_code']
        verification = DepositPayment.objects.filter(otp_code=otp_code).first()
        if not verification:
            raise serializers.ValidationError("Otp code not found")

        user = verification.user
        if not user:
            raise serializers.ValidationError("Code is invalid")

        if verification.is_expired():
            verification.delete()
            raise serializers.ValidationError("Otp code is expired")

        self.verification = verification
        return data

    def save(self, **kwargs):
        verification = self.verification
        user = verification.user
        amount = verification.amount

        user.balance += amount
        user.save()
        data = {
            "message": "Deposit confirmed successfully.",
            'balance': user.balance
        }

        verification.delete()

        return data