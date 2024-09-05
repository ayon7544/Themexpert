from django.contrib import admin
from application.models import *


# Register your models here.
admin.site.register(UsersPrimaryDetails)
admin.site.register(PoliticiansPrimaryDetails)
admin.site.register(CountryConstituency)
admin.site.register(MPElection)
admin.site.register(MinisterPrimaryDetails)
admin.site.register(CountryMinistries)
admin.site.register(PublicOpinions)
#entertainment/sports
admin.site.register(Sport)
admin.site.register(SportVenue)
admin.site.register(SportDate)
admin.site.register(SportSeatType)
admin.site.register(SportTickets)

admin.site.register(Bus)
admin.site.register(Book)
admin.site.register(Train)
admin.site.register(BookTrain)
admin.site.register(Plane)
admin.site.register(BookPlane)

admin.site.register(Collegee)
admin.site.register(Honourss)
admin.site.register(Masterss)
admin.site.register(CollegeSubject)
admin.site.register(CollegeApplicant)
admin.site.register(HonoursSubject)
admin.site.register(HonoursApplicant)
admin.site.register(MastersSubject)
admin.site.register(MastersApplicant)

admin.site.register(Appointment)