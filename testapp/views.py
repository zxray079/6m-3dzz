from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import CustomTokenObtainPairSerializer


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Вы успешно вышли из системы"},
                status=status.HTTP_200_OK,
            )
        except TokenError:
            return Response(
                {"error": "Недействительный или отозванный токен"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "email": user.email,
            "role": user.role,
            "is_staff": user.is_staff,
            "date_joined": user.date_joined,
        })