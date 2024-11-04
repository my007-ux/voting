import traceback
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import status,viewsets
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
from .blockchain import Blockchain  # Assume this is your blockchain interface


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
                serializer = VoterUserSerializer(all_users, context={'request': request}, many=True)
                data_send={
                    "count":len(serializer.data),
                   "data":serializer.data,
                }
                return ok(data=data_send)
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



# Create your views here.
class ManageProvince(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
                try: 
                    payload_dict = request.data
                    provience_serializer = ProvinceSerializer(data=payload_dict)
                    if provience_serializer.is_valid():
                        provience_serializer.save()
                        message = f"{provience_serializer.validated_data.get('name')} created Successfully "
                    return created(message=message)

                except Exception as err:
                    print(traceback.format_exc())
                    return internal_server_error(message='Failed to create')

    def get(self, request):
        try: 
            all_province = Province.objects.order_by('name')
            resultdata=[]
            if all_province.exists():
                serializer = ProvinceSerializer(all_province, many=True)
                return ok(data=serializer.data)
            else:
                return ok(data=resultdata)
            
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get room list')

    def delete(self, request):
        try: 
            Pid= request.GET.get('id', None)
            try:
                province = Province.objects.filter(id=Pid).first()
            except Province.DoesNotExist:
                # Handle the case where the object is not found
                messageData="Province not found with id : ".format(Pid)
                return bad_request(message=messageData)
            else:
                # Object was found, do something with it
                province.delete()
                return ok(message='Successfully deleted')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete')


class ManageDistrict(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            payload_dict = request.data
            district_serializer = DistrictSerializer(data=payload_dict)
            if district_serializer.is_valid():
                district_serializer.save()
                message = f"{district_serializer.validated_data.get('name')} created successfully"
                return created(message=message)
            return bad_request(message="Invalid data")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create district')

    def get(self, request, id=None):
        try:
            if id is None:
                return bad_request(message="Province is missing")
            else:
                all_districts = District.objects.filter(province=id).order_by('name')
                resultdata = []
                if all_districts.exists():
                    serializer = DistrictSerializer(all_districts, many=True)
                    return ok(data=serializer.data)
                else:
                    return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get district list')

    def delete(self, request, id:None):
        try:
            district = District.objects.filter(id=id).first()
            if district:
                district.delete()
                return ok(message='Successfully deleted')
            return bad_request(message=f"District not found with id: {id}")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete district')


class ManageTehsil(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        try:
            payload_dict = request.data
            tehsil_serializer = TehsilSerializer(data=payload_dict)
            if tehsil_serializer.is_valid():
                tehsil_serializer.save()
                message = f"{tehsil_serializer.validated_data.get('name')} created successfully"
                return created(message=message)
            return bad_request(message="Invalid data")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create tehsil')

    def get(self, request, id=None):
        try:
            if id is None:
                return bad_request(message="District is missing")
            else:
                all_tehsils = Tehsil.objects.filter(district=id).order_by('name')
                resultdata = []
                if all_tehsils.exists():
                    serializer = TehsilSerializer(all_tehsils, many=True)
                    return ok(data=serializer.data)
                else:
                    return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get tehsil list')

    def delete(self, request, id=None):
        try:
            tehsil = Tehsil.objects.filter(id=id).first()
            if tehsil:
                tehsil.delete()
                return ok(message='Successfully deleted')
            return bad_request(message=f"Tehsil not found with id: {id}")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete tehsil')

class ManageArea(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        try:
            payload_dict = request.data
            area_serializer = AreaSerializer(data=payload_dict)
            if area_serializer.is_valid():
                area_serializer.save()
                message = f"{area_serializer.validated_data.get('name')} created successfully"
                return created(message=message)
            return bad_request(message="Invalid data")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create area')

    def get(self, request):
        try:
            all_areas = Area.objects.order_by('-modified_datetime')
            resultdata = []
            if all_areas.exists():
                serializer = AreaSerializer(all_tehsils, many=True)
                return ok(data=serializer.data)
            else:
                return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get area list')

    def delete(self, request, id=None):
        try:
            area = Area.objects.filter(id=id).first()
            if area:
                area.delete()
                return ok(message='Successfully deleted')
            return bad_request(message=f"Area not found with id: {id}")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete Area')



class ManageCouncil(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        try:
            payload_dict = request.data
            council_serializer = CouncilSerializer(data=payload_dict)
            if council_serializer.is_valid():
                council_serializer.save()
                message = f"{council_serializer.validated_data.get('name')} created successfully"
                return created(message=message)
            return bad_request(message="Invalid data")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create tehsil')

    def get(self, request, id=None):
        try:
            if id is None:
                return bad_request(message="Tehsil is missing")
            else:
                all_councils = Council.objects.filter(tehsil=id).order_by('-name')
                resultdata = []
                if all_councils.exists():
                    serializer = CouncilSerializer(all_councils, many=True)
                    return ok(data=serializer.data)
                else:
                    return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get tehsil list')

    def delete(self, request, id=None):
        try:
            council = Council.objects.filter(id=id).first()
            if council:
                council.delete()
                return ok(message='Successfully deleted')
            return bad_request(message=f"Council not found with id: {id}")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete Council')


class ManagePollingStation(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        try:
            payload_dict = request.data
            polling_station_serializer = PollingStationSerializer(data=payload_dict)
            if polling_station_serializer.is_valid():
                polling_station_serializer.save()
                message = f"{polling_station_serializer.validated_data.get('name')} created successfully"
                return created(message=message)
            return bad_request(message="Invalid data")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create polling station')

    def get(self, request, id=None):
        try:
            if id is None:
                return bad_request(message="Tehsil is missing")
            else:
                all_polling_stations = PollingStation.objects.order_by('name')
                resultdata = []
                if all_polling_stations.exists():
                    serializer = PollingStationSerializer(all_polling_stations, many=True)
                    return ok(data=serializer.data)
                else:
                    return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get polling station list')

    def delete(self, request, id=None):
        try:
            polling_station = PollingStation.objects.filter(id=id).first()
            if polling_station:
                polling_station.delete()
                return ok(message='Successfully deleted')
            return bad_request(message=f"Polling station not found with id: {id}")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete polling station')


class ManageCandidate(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        try:
            payload_dict = request.data
            candidate_serializer = CandidateSerializer(data=payload_dict)
            if candidate_serializer.is_valid():
                candidate_serializer.save()
                message = f"{candidate_serializer.validated_data.get('name')} created successfully"
                return created(message=message)
            return bad_request(message="Invalid data")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create polling station')

    def get(self, request, id=None):
        try:
            if id is None:
                return bad_request(message='Polling Station ID is missing')
            else:
                all_candiates = Candidate.objects.filter(polling_station=id).order_by('-modified_datetime')
                resultdata = []
                if all_candiates.exists():
                    serializer = CandidateSerializer(all_candiates, many=True)
                    return ok(data=serializer.data)
                else:
                    return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get candidate list')

    def delete(self, request, id=None):
        try:
            candidate = Candidate.objects.filter(id=id).first()
            if candidate:
                candidate.delete()
                return ok(message='Successfully deleted')
            return bad_request(message=f"Candidate not found with id: {id}")

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete Candidate')


class VoterViewSet(viewsets.ViewSet):

    def list_voters(self, request):
        # Filter by province, district, tehsil, etc.
        filters = {
            'province': request.query_params.get('province'),
            'district': request.query_params.get('district'),
            'tehsil': request.query_params.get('tehsil'),
            'council': request.query_params.get('council'),
            'polling_station': request.query_params.get('polling_station'),
        }
        voters = VoterTable.objects.filter(**{k: v for k, v in filters.items() if v is not None})
        serializer = VoterUserSerializer(voters, many=True)
        return ok(data=serializer.data)

    def get_candidate_list(self, request):
        # Filter candidates by the same parameters
        filters = {
            'province': request.query_params.get('province'),
            'district': request.query_params.get('district'),
            'tehsil': request.query_params.get('tehsil'),
            'council': request.query_params.get('council'),
            'polling_station': request.query_params.get('polling_station'),
        }
        candidates = Candidate.objects.filter(**{k: v for k, v in filters.items() if v is not None})
        serializer = CandidateSerializer(candidates, many=True)
        return ok(data=serializer.data)

    def voter_statistics(self, request):
        # Compare registered and casted voters in polling stations
        polling_station_id = request.query_params.get('polling_station_id')
        polling_station = PollingStation.objects.get(id=polling_station_id)
        registered_voters = VoterTable.objects.filter(polling_station=polling_station).count()
        casted_voters = Vote.objects.filter(candidate__polling_station=polling_station).values('voter').distinct().count()

        data = {
            'registered_voters': registered_voters,
            'casted_voters': casted_voters,
        }
        return ok(data=data)

    def candidate_details(self, request, pk=None):
        # Get candidate profile detail and votes
        candidate = Candidate.objects.get(pk=pk)
        votes = Vote.objects.filter(candidate=candidate).count()
        total_votes = Vote.objects.count()
        percentage = (votes / total_votes) * 100 if total_votes > 0 else 0

        data = {
            'candidate': CandidateSerializer(candidate).data,
            'total_votes': votes,
            'percentage': percentage,
        }
        return ok(data=data)

class CastVote(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            voter = serializer.validated_data['voter']
            candidate = serializer.validated_data['candidate']
            
            # Check if the voter has already voted
            voter_instance = VoterTable.objects.get(id=voter.id)
            if voter_instance.is_voted:
                return Response({"message": "You have already voted."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create a blockchain transaction (this is a placeholder for actual implementation)
            blockchain = Blockchain()  # Instantiate your blockchain interface
            transaction_id = blockchain.create_transaction(voter.id, candidate.id)  # Implement this method in your blockchain logic
            print(transaction_id)
            # Save the vote with transaction details
            # vote = Vote(
            #     voter=voter_instance,
            #     candidate=candidate,
            #     transaction_id=transaction_id
            # )
            # vote.save()
            
            # # Set is_vote to True in the VoterTable
            # voter_instance.is_voted = True
            # voter_instance.save()

            return created(message= "Vote cast successfully", data={"transaction_id": transaction_id})
        return bad_request(data=serializer.errors)

    def get(self, request, id=None):
        try:
            # Retrieve votes for the specific candidate
            votes = Vote.objects.filter(candidate__id=id)

            # Count the number of votes for this candidate
            vote_count = votes.count()

            # Retrieve transaction details
            transaction_details = [
                {
                    "voter_id": vote.voter.id,
                    "transaction_id": vote.transaction_id,
                    "candidate": vote.candidate.name,
                }
                for vote in votes
            ]

            return ok(data={
                "candidate_id": candidate_id,
                "vote_count": vote_count,
                "transactions": transaction_details
            })

        except Candidate.DoesNotExist:
            return not_found(message= "Candidate not found.")
        except Exception as e:
            return internal_server_error(message=str(e))