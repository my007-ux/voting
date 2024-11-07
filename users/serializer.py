from rest_framework.authtoken.models import Token
from rest_framework.serializers import (ModelSerializer, DateField, ValidationError,
                                        SerializerMethodField, ImageField, CharField, EmailField, IntegerField,Serializer,PrimaryKeyRelatedField, BooleanField )
from .models import User, VoterTable,Province, District, Tehsil, Division, Council, PollingBooth,PollingStation, Candidate, Vote
from utils.enum import Types
from django.contrib.auth.models import Group

type_obj = Types()


class UserSerializer(ModelSerializer):
    username = CharField(max_length=120, required=True, allow_null=False)
    first_name = CharField(max_length=60, required=True, allow_null=False)
    last_name = CharField(max_length=60, required=True, allow_null=False)
    full_name = CharField(max_length=120, required=True, allow_null=False)
    role = CharField(max_length=100, required=True, allow_null=False)
    email = EmailField(required=True, allow_null=False)
    date_of_birth = DateField(required=False, allow_null=True)
    user_image = ImageField(required=False, allow_null=True)
    created_by_id = IntegerField(required=False, allow_null=True)
    
    def validate_type(self, value):
        type_value = type_obj.get_user_type(value)
        if type_value == 0:
            raise ValidationError("Invalid Type.")
        return type_value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        # Assign the user to the corresponding group
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'username', 'date_of_birth',
                  'user_image', 'password', 'created_by_id', 'role']


class GetUserSerializer(ModelSerializer):
    user_image = SerializerMethodField('get_user_image', required=False)
    full_name = SerializerMethodField('get_name', required=False)
    api_token = SerializerMethodField('get_api_token', required=False)

    def get_user_image(self, obj):
        try:
            photo_url = obj.user_image.url
            # print("PHOTO URL: ", photo_url)
            return self.context['request'].build_absolute_uri(photo_url)
        except Exception as e:
            # print(e)
            return None

    def get_name(self, obj):
        return str(obj.full_name)

    def get_api_token(self, obj):
        # Try to get an existing token for the user
        token, created = Token.objects.get_or_create(user=obj)

        return token.key

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'username', 'date_of_birth', 'user_image',
                  'role','api_token',
                  'created_by_id', 'date_joined']


class UpdateUserSerializer(ModelSerializer):
    os = CharField(max_length=10, required=True, allow_null=False)
    modified_by_id = IntegerField(required=True, allow_null=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'username', 'date_of_birth',
                  'user_image', 'role', 'modified_by_id',
                  'modified_datetime', 'date_joined']


class FilterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'username', 'date_of_birth', 'user_image',
                  'role',
                  'modified_by_id',
                  'modified_datetime', 'date_joined']

class ProvinceSerializer(ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

class DistrictSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class TehsilSerializer(ModelSerializer):
    class Meta:
        model = Tehsil
        fields = '__all__'

class DivisionSerializer(ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'

class CouncilSerializer(ModelSerializer):
    class Meta:
        model = Council
        fields = '__all__'

class PollingStationSerializer(ModelSerializer):
    class Meta:
        model = PollingStation
        fields = '__all__'

class PollingBoothSerializer(ModelSerializer):
    class Meta:
        model = PollingBooth
        fields = '__all__'


class PollingStationGetterSerializer(ModelSerializer):
    class Meta:
        model = PollingStation
        fields = ['id', 'name']

class ProvinceGetterSerializer(ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name']

class DivisionGetterSerializer(ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'name']

class DistrcitGetterSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']

class TehsilGetterSerializer(ModelSerializer):
    class Meta:
        model = Tehsil
        fields = ['id', 'name']

class CouncilGetterSerializer(ModelSerializer):
    class Meta:
        model = Council
        fields = ['id', 'name']

class PollingBoothGetterSerializer(ModelSerializer):
    class Meta:
        model = PollingBooth
        fields = ['id', 'name', 'gender']


class CandidateSerializer(ModelSerializer):
    province = ProvinceGetterSerializer()
    division = DivisionGetterSerializer()
    district = DistrcitGetterSerializer()
    tehsil = TehsilGetterSerializer()
    council = CouncilGetterSerializer()
    polling_station = PollingStationGetterSerializer()
    polling_booth = PollingBoothGetterSerializer()

    class Meta:
        model = Candidate
        fields = '__all__'


class CandidateGetSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name']

class VoterUserSerializer(ModelSerializer):
    polling_station = PollingStationGetterSerializer()
    polling_booth = PollingBoothGetterSerializer()
    class Meta:
        model = VoterTable
        fields = '__all__'

class VoterGetterUserSerializer(ModelSerializer):
    class Meta:
        model = VoterTable
        fields = ['id', 'name', 'gender']

class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class VoteGetterSerializer(ModelSerializer):
    voter=VoterGetterUserSerializer()
    candidate=CandidateGetSerializer()
    council = CouncilGetterSerializer()
    polling_station = PollingStationGetterSerializer()
    polling_booth = PollingBoothGetterSerializer()
    class Meta:
        model = Vote
        fields = '__all__'

