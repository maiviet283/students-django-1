from .models import *
from .serializers import *
from django.contrib.auth.hashers import make_password,check_password
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterStudents(APIView):
    permission_classes = [AllowAny]    

    def post(self,request):
        serializers = StudentsSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(password=make_password(request.data.get('password')))
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginStudent(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = Students.objects.get(username=username)
            
            if check_password(password,user.password):
                refresh_token = RefreshToken()
                refresh_token["id"] = user.pk
                refresh_token["username"] = user.username
                access_token = refresh_token.access_token

                return Response({
                    'access':str(access_token),
                    'refresh':str(refresh_token)
                })
            
            else: 
                return Response({'error':'Tên đăng nhập hoặc mật khẩu không đúng'},status=status.HTTP_400_BAD_REQUEST)
            
        except Students.DoesNotExist:
            return Response({'error':'Tên đăng nhập hoặc mật khẩu không đúng'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get('id')
            if not user_id:
                raise InvalidToken("Token does not contain user ID")
            
            user = Students.objects.get(id=user_id)
            return user
        except Students.DoesNotExist:
            raise InvalidToken("User not found")

        

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = StudentsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            new_access_token = token.access_token

            return Response({
                'access': str(new_access_token),
                'refresh': str(token),
            })
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def update_user(self,user,data):
        serializer = StudentsSerializer(instance=user,data=data,partial=True)

        if not serializer.is_valid():
            return {'error': serializer.errors}, status.HTTP_400_BAD_REQUEST

        
        if 'username' in data:
            if Students.objects.filter(username=data['username']).exclude(pk=user.pk).exists():
                return {'error': 'Username đã tồn tại'}, status.HTTP_400_BAD_REQUEST
            
        if 'email' in data:
            if Students.objects.filter(email=data['email']).exclude(pk=user.pk).exists():
                return {'error': 'Email đã tồn tại'}, status.HTTP_400_BAD_REQUEST
            
        if 'password' in data and data['password']:
            data['password'] = make_password(data['password'])

        serializer.save()
        return serializer.data, status.HTTP_200_OK
    

    def put(self,request):
        response,status_code = self.update_user(request.user,request.data)
        return Response(response,status_code)

    def patch(self, request):
        response, status_code = self.update_user(request.user, request.data)
        return Response(response, status=status_code)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Đưa Refresh Token vào danh sách đen

            return Response({'message': 'Đăng xuất thành công'}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
