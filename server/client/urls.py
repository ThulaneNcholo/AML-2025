
from django.urls import path
from .import views

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('login', views.LoginPage, name='login'),
    path('register/', views.RegisterView, name='Register'),
    path('exhibit/', views.ExhibitView, name='Exhibit'),
    path('sponsor/', views.SponsorView, name='Sponsor'),
    path('sponsor-benefits/', views.SponsorBenefitsView, name='Sponsor-benefits'),
    path('submit-form/', views.SubmitFormView, name='submit-form'),
    path('register-another/', views.RegisterAnotherPost, name='register-another'),
    path('dashboard/', views.AdminDashboardView, name='dashboard'),
    path('download-csv/', views.download_csv, name='download-csv'),
]
