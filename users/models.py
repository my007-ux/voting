from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from utils.enum import Types

type_obj = Types()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        print(**extra_fields)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=True, blank=True,unique=True)
    first_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=60, null=True, blank=True)
    full_name = models.CharField(max_length=120, null=True, blank=True)
    username = models.CharField(max_length=254, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    role =  models.CharField(max_length=100, blank=True, null=True)
    user_image = models.ImageField(upload_to='assets/', default='assets/no_image.png', null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('User', null=True, blank=True, related_name="user_created_by_fk",
                                   on_delete=models.CASCADE)
    modified_by = models.ForeignKey('User', blank=True, related_name="user_modified_by_fk",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s' % self.full_name
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self):
        return self.email

    def get_type(self):
        """Returns User Type."""
        return type_obj.get_user_type(self.type)

    def __str__(self):
        try:
            return self.email
        except:
            return "User"


class UserPermissions(models.Model):
    user = models.ForeignKey(User, related_name='user_permission_fk', null=True, blank=True, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, null=True, blank=True,
                                   related_name="%(app_label)s_%(class)s_created_by", on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, blank=True, related_name="%(app_label)s_%(class)s_modified_by",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'user_permission'
        verbose_name_plural = 'user_permissions'

    def __str__(self):
        return self.user.first_name + '-' + self.user.last_name


class Province(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey('User', null=True, blank=True, related_name="user_voter_created_by_province",
                                   on_delete=models.CASCADE)
    modified_by = models.ForeignKey('User', blank=True, related_name="user_voter_modified_by_province",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(auto_now_add=True)


class Division(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    created_by = models.ForeignKey('User', null=True, blank=True, related_name="user_voter_created_by_division",
                                   on_delete=models.CASCADE)
    modified_by = models.ForeignKey('User', blank=True, related_name="user_voter_modified_by_division",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(auto_now_add=True)
class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    created_by = models.ForeignKey('User', null=True, blank=True, related_name="user_voter_created_by_district",
                                   on_delete=models.CASCADE)
    modified_by = models.ForeignKey('User', blank=True, related_name="user_voter_modified_by_district",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(auto_now_add=True)

class Tehsil(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    created_by = models.ForeignKey('User', null=True, blank=True, related_name="user_voter_created_by_tehsil",
                                   on_delete=models.CASCADE)
    modified_by = models.ForeignKey('User', blank=True, related_name="user_voter_modified_by_tehsil",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(auto_now_add=True)

class Council(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    tehsil = models.ForeignKey(Tehsil, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    created_by = models.ForeignKey('User', null=True, blank=True, related_name="user_voter_created_by_council",
                                   on_delete=models.CASCADE)
    modified_by = models.ForeignKey('User', blank=True, related_name="user_voter_modified_by_council",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(auto_now_add=True)


class PollingStation(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    tehsil = models.ForeignKey(Tehsil, on_delete=models.CASCADE)
    council = models.ForeignKey(Council, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    created_by = models.ForeignKey('User', null=True, blank=True, related_name="user_voter_created_by_pollingstation",
                                   on_delete=models.CASCADE)
    modified_by = models.ForeignKey('User', blank=True, related_name="user_voter_modified_by_pollingstation",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(auto_now_add=True)

class PollingBooth(models.Model):
    name = models.CharField(max_length=100)
    polling_station = models.ForeignKey(PollingStation, on_delete=models.CASCADE)
    gender=models.CharField(max_length=60, null=True, blank=True)
    created_by = models.ForeignKey('User', null=True, blank=True, related_name="user_voter_created_by_pollingbooth",
                                   on_delete=models.CASCADE)
    modified_by = models.ForeignKey('User', blank=True, related_name="user_voter_modified_by_pollingbooth",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(auto_now_add=True)


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    gender=models.CharField(max_length=60, null=True, blank=True)
    father_name = models.CharField(max_length=60)
    date_of_birth = models.CharField(max_length=60)
    cnic = models.CharField(max_length=120)
    type=models.CharField(max_length=60, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    tehsil = models.ForeignKey(Tehsil, on_delete=models.CASCADE)
    council = models.ForeignKey(Council, on_delete=models.CASCADE)
    polling_station = models.ForeignKey(PollingStation, on_delete=models.CASCADE)
    polling_booth = models.ForeignKey(PollingBooth, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('User', null=True, blank=True, related_name="user_voter_created_by_candidate",
                                   on_delete=models.CASCADE)
    modified_by = models.ForeignKey('User', blank=True, related_name="user_voter_modified_by_candidate",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(auto_now_add=True)
    
class VoterTable(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    father_name = models.CharField(max_length=60, null=True, blank=True)
    cnic = models.CharField(max_length=120, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    tehsil = models.ForeignKey(Tehsil, on_delete=models.CASCADE)
    council = models.ForeignKey(Council, on_delete=models.CASCADE)
    polling_station = models.ForeignKey(PollingStation, on_delete=models.CASCADE)
    polling_booth = models.ForeignKey(PollingBooth, on_delete=models.CASCADE)
    uc_id = models.IntegerField(null=True, blank=True, default=0)
    address = models.CharField(max_length=250, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    gender=models.CharField(max_length=60, null=True, blank=True)
    is_voted = models.BooleanField(default=False)
    fingerprint = models.CharField(max_length=200)
    created_by = models.ForeignKey('User', null=True, blank=True, related_name="user_voter_created_by_fk",
                                   on_delete=models.CASCADE)
    modified_by = models.ForeignKey('User', blank=True, related_name="user_voter_modified_by_fk",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    voter = models.ForeignKey(VoterTable, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    gender=models.CharField(max_length=60, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    council = models.ForeignKey(Council, on_delete=models.CASCADE)
    polling_station = models.ForeignKey(PollingStation, on_delete=models.CASCADE)
    polling_booth = models.ForeignKey(PollingBooth, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['candidate', 'voter']  # Ensure each candidate-voter combination is unique


class CatsedVote(models.Model):
    transaction_id = models.CharField(max_length=255, null=True, blank=True)  # To store the blockchain transaction ID

class TransactionPart1(models.Model):
    part = models.CharField(max_length=255)

class TransactionPart2(models.Model):
    part = models.CharField(max_length=255)

class TransactionPart3(models.Model):
    part = models.CharField(max_length=255)