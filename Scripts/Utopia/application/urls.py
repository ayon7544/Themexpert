from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('EntryPage/', views.EntryPage, name='EntryPage'),
    path('RegistrationFormPage/',views.RegistrationFormPage,name='RegistrationFormPage'),
    path('',views.HomePage, name='HomePage'),
    path('VotingPage/',views.VotingPage,name='VotingPage'),
    path('ElectionSetupPage/',views.ElectionSetupPage,name='ElectionSetupPage'),
    path('MinistryPage/',views.MinistryPage,name='MinistryPage'),
    path('MinistySetupPage/',views.MinistrySetupPage,name='MinistrySetupPage'),

    path('EducationPage',views.EducationPage,name='EducationPage'),
    path('College',views.College,name='College'),
    path('Honours',views.Honours,name='Honours'),
    path('Masters',views.Masters,name='Masters'),
    path('Form',views.Form,name='Form'),
    path('collegeapply', views.Collegeapply, name='collegeapply'),
    path('honoursapply', views.Honoursapply, name='honoursapply'),
    path('mastersapply', views.Mastersapply, name='mastersapply'),
    path('success', views.success, name='success'),


    path('EntertainmentPage/',views.EntertainmentPage,name='EntertainmentPage'),
    path('Am_I_A_Citizen/',views.Am_I_A_CitizenPage,name='Am_I_A_CitizenPage'),
    path('NewsDetailsPage/<path:news>/',views.NewsDetailsPage, name='NewsDetailsPage'),
    path('AboutPage/',views.AboutPage,name='AboutPage'),
    path('ContactPage/',views.ContactPage,name='ContactPage'),
    path('HelpPage/',views.HelpPage,name='HelpPage'),
    path('TicketsPage/',views.TicketsPage,name='TicketsPage'),

    path('TransportationMain', views.TransportationMain, name='TransportationMain'),
    path('homebus', views.homebus, name="homebus"),
    path('findbus', views.findbus, name="findbus"),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
    path('hometrain', views.hometrain, name="hometrain"),
    path('find_train', views.find_train, name="find_train"),
    path('booking', views.booking, name="booking"),
    path('cancelling', views.cancelling, name="cancelling"),
    path('seebooking', views.seebooking, name="seebooking"),
    path('homeplane', views.homeplane, name="homeplane"),
    path('find_plane', views.find_plane, name="find_plane"),
    path('bookingp', views.bookingp, name="bookingp"),
    path('cancellingp', views.cancellingp, name="cancellingp"),
    path('seebookingp', views.seebookingp, name="seebookingp"),

    path('HealthcareMain',views.HealthcareMain,name='HealthcareMain'),
    path('Clinic',views.Clinic,name='Clinic'),
    path('Hospital',views.Hospital,name='Hospital'),
    path('Eyeclinic',views.Eyeclinic,name='Eyeclinic'),
    path('Diagnostic',views.Diagnostic,name='Diagnostic'),
    path('Pharmacy',views.Pharmacy,name='Pharmacy'),
    path('PrivateClinic', views.PrivateClinic, name='PrivateClinic'),
    path('PublicClinic', views.PublicClinic, name='PublicClinic'),
    path('PrivateHospital', views.PrivateHospital, name='PrivateHospital'),
    path('PublicHospital', views.PublicHospital, name='PublicHospital'),
    path('PrivateDiagnostic', views.PrivateDiagnostic, name='PrivateDiagnostic'),
    path('PublicDiagnostic', views.PublicDiagnostic, name='PublicDiagnostic'),
    path('PrivateEyeclinic', views.PrivateEyeclinic, name='PrivateEyeclinic'),
    path('PublicEyeclinic', views.PublicEyeclinic, name='PublicEyeclinic'),
    path('HospitalAppointmentPage', views.HospitalAppointmentPage, name='HospitalAppointmentPage'),
    path('PharmacyBookingPage', views.PharmacyBookingPage, name='PharmacyBookingPage'),
    path('DiagnosticAppointmentPage', views.DiagnosticAppointmentPage, name='DiagnosticAppointmentPage'),
    path('ClinicAppointmentPage', views.ClinicAppointmentPage, name='ClinicAppointmentPage'),
    path('EyeclinicAppointmentPage', views.EyeclinicAppointmentPage, name='EyeclinicAppointmentPage'),
    path('book_clinicappointment', views.book_clinicappointment, name='book_clinicappointment'),
    path('book_diagappointment', views.book_diagappointment, name='book_diagappointment'),
    path('book_eyeappointment', views.book_eyeappointment, name='book_eyeappointment'),
    path('book_hospitalappointment', views.book_hospitalappointment, name='book_hospitalappointment'),
    path('book_pharmacyappointment', views.book_pharmacyappointment, name='book_pharmacyappointment'),
    path('ThankYou', views.ThankYou, name='ThankYou'),

    #entertainment
    path('LoadVenues/', views.LoadVenues,name='ajax_load_Venues'),
    path('LoadDate/', views.LoadDate,name='ajax_load_Date'),
    path('LoadSeat/', views.LoadSeat,name='ajax_load_Seat'),
    path('<path:undefined_path>/', views.Undefine),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
