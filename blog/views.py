from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, AccountVerificationSerializer, LoginSerializer, DepositBalanceSerializer
from rest_framework import status as Status


@api_view(['POST'])
def register(request):
    register_serializer = RegisterSerializer(data=request.data)
    if register_serializer.is_valid():
        register_serializer.save()
        return Response({'message': 'User is successfully created'}, status=Status.HTTP_201_CREATED)
    else:
        return Response(register_serializer.errors, status=Status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def AccountVerificationView(request):
    verify_serializer = AccountVerificationSerializer(data=request.data)
    if verify_serializer.is_valid():
        user = verify_serializer.validated_data['user']
        user.is_verified = True
        user.is_active = True
        user.save()
        return Response({'message': 'Account is successfully confirmed'}, status=Status.HTTP_200_OK)
    return Response(verify_serializer.errors, status=Status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def LoginView(request):
    login_serializer = LoginSerializer(data=request.data)
    if login_serializer.is_valid():
        return Response(login_serializer.validated_data, status=Status.HTTP_200_OK)
    return Response(login_serializer.errors,  status=Status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def DepositBalanceView(request):
    deposit_serializer = DepositBalanceSerializer(data=request.data)
    if deposit_serializer.is_valid():
        return Response(deposit_serializer.validated_data, status=Status.HTTP_201_CREATED)
    return Response(deposit_serializer.errors, status=Status.HTTP_400_BAD_REQUEST)