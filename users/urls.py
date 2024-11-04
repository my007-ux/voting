from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view()),
    path('login/', views.Login.as_view()),
    path('import_from_csv/', views.ImportCsvView.as_view()),
    path('verify_cnic/', views.FindCnicView.as_view()),
    path('delete_user/', views.DeleteUser.as_view()),
    path('province/', views.ManageProvince.as_view(), name='manage_province'),
    path('province/<int:id>/', views.ManageProvince.as_view(), name='manage_province'),
    path('district/', views.ManageDistrict.as_view(), name='manage_district'),
    path('district/<int:id>/', views.ManageDistrict.as_view(), name='manage_district'),
    path('tehsil/', views.ManageTehsil.as_view(), name='manage_tehsil'),
    path('tehsil/<int:id>/', views.ManageTehsil.as_view(), name='manage_tehsil'),
    path('area/', views.ManageArea.as_view(), name='manage_tehsil'),
    path('area/<int:id>/', views.ManageArea.as_view(), name='manage_tehsil'),
    path('council/', views.ManageCouncil.as_view(), name='manage_council'),
    path('council/<int:id>/', views.ManageCouncil.as_view(), name='manage_council'),
    path('polling_station/', views.ManagePollingStation.as_view(), name='manage_polling_station'),
    path('polling_station/<int:id>/', views.ManagePollingStation.as_view(), name='manage_polling_station'),
    path('candidate/', views.ManageCandidate.as_view(), name='manage_candidate'),
    path('candidate/<int:id>/', views.ManageCandidate.as_view(), name='manage_candidate'),
    path('voters/', views.VoterViewSet.as_view({'get': 'list_voters'}), name='list_voters'),
    path('voters/candidates/', views.VoterViewSet.as_view({'get': 'get_candidate_list'}), name='get_candidate_list'),
    path('voters/statistics/', views.VoterViewSet.as_view({'get': 'voter_statistics'}), name='voter_statistics'),
    path('candidates/<int:pk>/', views.VoterViewSet.as_view({'get': 'candidate_details'}), name='candidate_details'),
    path('cast_vote/', views.CastVote.as_view(), name='cast_vote'),

    # path('refreshToken/', views.RefreshTokenView.as_view()),
]
