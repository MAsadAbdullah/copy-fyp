from django.urls import path
from django.contrib import admin
from . import views
# from .views import SignUpView
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landingpage, name='landingpage'),
    path('admin/', admin.site.urls),
    path('aboutus/', aboutus, name='aboutus'),
    path('faqs/', faqs, name='faqs'),
    path('signup/', register_request, name='signup'),
    path('login/', doctor_login, name='login'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('dashboard/', dashboard, name='dashboard'),
    path('patient_personal_data/', patient_personal_data,
         name='patient_personal_data'),
    path('patient_medical_data/', patient_medical_data,
         name='patient_medical_data'),
    path("profile/", profile, name="profile"),
    path("logout/", logout, name="logout"),
    path("add_patient/", add_patient, name="add_patient"),
    path('patient_profile/<int:patient_id>/', patient_profile, name='patient_profile'),
    path("results/<int:patient_id>/", results, name="results"),
]
if settings.DEBUG:
     
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)