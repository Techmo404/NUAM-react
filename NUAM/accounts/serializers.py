from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


# ============================
# LOGIN SERIALIZER
# ============================
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # puede ser username o email
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get("username")
        password = data.get("password")

        # 🔎 Detectar si es email
        if "@" in identifier:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                username = user_obj.username
            except User.DoesNotExist:
                raise serializers.ValidationError("Credenciales incorrectas.")
        else:
            username = identifier

        # 🔐 Autenticación real
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Credenciales incorrectas.")

        # 👤 Guardamos el user (lo usas en views para auditoría)
        self.user = user

        # 🔑 JWT
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
        }


# ============================
# USER SERIALIZER
# ============================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role"]
