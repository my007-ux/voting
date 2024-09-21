import traceback
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from utils.responses import internal_server_error, bad_request, created, not_found, ok
from .models import *
from .serializer import *
import csv


User = get_user_model()

# Create your views here.
class SignUp(APIView):
    def post(self, request):
        try: 
            payload = request.data
            serializer = UserSerializer(data=payload)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return created(message='User Created successfully')                                   
          
        except ValidationError as err:
            error_message = err.get_full_details()
            print(traceback.format_exc())
            return internal_server_error(message=error_message)
class Login(APIView):
    def post(self, request):
        try:
            print(request.data)
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')
            user = authenticate(request=request, email=email, password=password)
            
            if not user:
                return bad_request(message='Invalid credentials')

            if not user.is_active:
                return bad_request(message='User account is disabled')

            refresh = RefreshToken.for_user(user)
            serializer = GetUserSerializer(user)

        
            return ok(data={'user': serializer.data, 'access_token': str(refresh.access_token), 'refresh_token': str(refresh)},message='Login successfully successfully')                                   
          
        except ValidationError as err:
            error_message = err.get_full_details()
            print(traceback.format_exc())
            return internal_server_error(message=error_message)

class ImportCsvView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        csv_file = request.FILES['csv_file']
        print(csv_file)
        # Read and parse the CSV file
        if csv_file:
            file_data = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(file_data)
            for row in csv_reader:
                try:
                    name = row[0]
                    father_name = row[1]
                    cnic = row[2]
                    address = row[3]
                    division = row[4]
                    province = row[5]
                    tehsil = row[6]
                    district = row[7]
                    uc_id = row[8]  # Assuming this is an integer in your CSV

                    # Ensure uc_id is an integer
                    uc_id = int(uc_id) if uc_id.isdigit() else None

                    # Use get_or_create with cnic as the unique identifier
                    voter, created = VoterTable.objects.get_or_create(
                        cnic=cnic,  # Ensuring uniqueness on the CNIC field
                        defaults={
                            'name': name,
                            'father_name': father_name,
                            'address': address,
                            'division': division,
                            'province': province,
                            'tehsil': tehsil,
                            'district': district,
                            'uc_id': uc_id
                        }
                    )

                    if created:
                        print(f'New voter created: {name}')
                    else:
                        print(f'Existing voter found: {name}')

                except Exception as e:
                    print(f'Error processing row {row}: {e}')
                    continue

            return Response({'data': 'null', 'message': 'Data Saved Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try: 
            all_users = VoterTable.objects.filter().order_by('-date_joined')
            resultdata=[]
            if all_users.exists():
                paginator = PageNumberPagination()
                paginator.page_size = 10
                result_page = paginator.paginate_queryset(all_users, request)
                serializer = VoterUserSerializer(result_page, context={'request': request}, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return ok(data=resultdata)
        
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get voter')


class FindCnicView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data
        cnic = data.get('cnic')  # Get 'cnic' from the POST request body
        # Read and parse the CSV file
        if cnic:
            # Retrieve voter data based on the provided CNIC
            voter_data = VoterTable.objects.filter(cnic=cnic).first()

            if voter_data:
                # Serialize the voter data
                serializer = VoterUserSerializer(voter_data)

                # Return the serialized data
                return ok(data= serializer.data)
            else:
                return bad_request(message= "CNIC does not exist")
        else:
            return bad_request(message= "CNIC Required")



class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'message': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user_instance = User.objects.filter(email=email).first()
        if user_instance:
            user_instance.set_password(password)
            user_instance.is_first_time_login = False
            user_instance.reset_token = None
            user_instance.save()
            return Response({'data': 'null', 'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

        return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class GetUsers(APIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try: 
            all_users = User.objects.filter().order_by('-date_joined')
            resultdata=[]
            if all_users.exists():
                paginator = PageNumberPagination()
                paginator.page_size = 10
                result_page = paginator.paginate_queryset(all_users, request)
                serializer = GetUserSerializer(result_page, context={'request': request}, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return ok(data=resultdata)
        
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get news')


class DeleteUser(APIView):
    def post(self, request):
        try:
            userId = request.data.get('userId')
            user=User.objects.filter(id=userId)
            if not user:
                return not_found(message='Invalid user')
            else:
                user.delete()
                return ok(message='User deleted successfully')                                   
          
        except ValidationError as err:
            error_message = err.get_full_details()
            print(traceback.format_exc())
            return internal_server_error(message=error_message)


