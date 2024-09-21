from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view()),
    path('login/', views.Login.as_view()),
    path('import_from_csv/', views.ImportCsvView.as_view()),
    path('verify_cnic/', views.FindCnicView.as_view()),
    path('delete_user/', views.DeleteUser.as_view()),
    # path('refreshToken/', views.RefreshTokenView.as_view()),
]
