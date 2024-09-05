import random
import requests
import datetime
import calendar
import re
from .utils import send_email_to_client
from bs4 import BeautifulSoup
from newsapi.newsapi_client import NewsApiClient
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import Settings
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib import messages
from django.db.models import Q
from .forms import *
from application.models import *
from .models import Collegee
from .models import Appointment

from itertools import chain
import os
import json
import pytz
import datetime
from datetime import date


# Create your views here.


def EntryPage(request):
    if request.method == 'POST':
        name = request.POST.get('button_name')
        if name == 'signup':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('pswd')
            form = RegisterForm(request.POST)
            if form.is_valid():
                my_usr = User.objects.create_user(
                    username, email, password)
                my_usr.save()
                user = authenticate(request, username=username,
                                    password=password, email=email)
                login(request, user)
                return redirect('RegistrationFormPage')
        elif name == 'login':
            username = request.POST.get('username')
            password = request.POST.get('pswd')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(HomePage)
            else:
                messages.error(
                    request, ' The username or password you entered is incorrect')
        elif name == 'Guest':
            username = '1234'
            email = '1234@uap-bd.edu'
            password = 'AYONGHOSHAJOYGHOSH'
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(HomePage)
    request.session.clear()
    return render(request, 'EntryPage.html')


@login_required
def RegistrationFormPage(request):
    if request.method == 'POST':
        UserID = request.user.username
        UserEmail = request.user.email
        UserFullName = request.POST.get('full_name')
        UserGender = request.POST.get('gender')
        UserOccupation = request.POST.get('occupation')
        UserDateOfBirth = request.POST.get('date_of_birth')
        UserMobileNum = request.POST.get('mobile_number')
        UserPoints = 1000
        UserImageFilename = request.FILES.get('image')
        UserRole = request.POST.get('role')
        name = request.POST.get('save')
        birthday = date.fromisoformat(UserDateOfBirth)
        today = date.today()
        UserAge = today.year - birthday.year - \
            ((today.month, today.day) < (birthday.month, birthday.day))
        if UserImageFilename:
            UserImageFilename.name = f'{UserID}.jpg'
            with open(f'media', 'wb') as f:
                f.write(UserImageFilename.read())
        if name == 'confirm':
            user_details = UsersPrimaryDetails(UserID, UserEmail, UserFullName, UserGender, UserOccupation,
                                               UserDateOfBirth, UserRole, UserMobileNum, UserPoints, UserImageFilename, UserAge)
            user_details.save()
            userocp = str(UserOccupation)
            if userocp.__contains__("Politician"):
                print(UserID)
                politician_details = PoliticiansPrimaryDetails(
                    UserID, UserRole, UserFullName, 0, 0, 0, UserID, False, False)
                politician_details.save()
            return redirect(HomePage)
    return render(request, 'RegistrationFormPage.html')


@login_required
def HomePage(request):
    UserID = request.user.username
    user = UsersPrimaryDetails.objects.get(UserID=UserID)
    host = user.UserImageFilename.url
    host = "http://127.0.0.1:8000/"+host
    context = {
        'user': user,
    }
    return render(request, 'HomePage.html', context)


@login_required
def VotingPage(request):
    if request.method == 'POST':
        UserID = request.user.username
        vote_setup = request.POST.get('save')
        now = datetime.datetime.now(pytz.timezone('UTC'))
        if vote_setup == 'setup':
            return redirect(ElectionSetupPage)
        Election = MPElection.objects.filter(EndTime__gte=now)
        for voteo in Election:
            one = json.loads(voteo.VoteDoneList)
            if str(UserID) not in one:
                if vote_setup == 'Cd1v':
                    voteo.Candidate1Vote += 1
                    one += str(UserID)
                    one = json.dumps(one, separators=(",", ","))
                    voteo.VoteDoneList = one
                if vote_setup == 'Cd2v':
                    voteo.Candidate2Vote += 1
                    one += str(UserID)
                    one = json.dumps(one, separators=(",", ","))
                    voteo.VoteDoneList = one
                voteo.save()
            else:
                messages.error(
                    request, 'You have already voted in this election.')
    timenow = datetime.datetime.now(pytz.timezone('UTC'))
    voting = MPElection.objects.filter(EndTime__lte=timenow)
    elc = MPElection.objects.filter(EndTime__gte=timenow)
    check = elc.exists()
    userid = int(request.user.username)
    ss = 00000000
    vc1 = 1
    vc2 = 1
    for vote in voting:
        vote.ElectionStatus = False
        vote.save()
        vc1 = 1
        vc2 = 1
    for vote in elc:
        vc1 = vote.Candidate1Vote
        vc2 = vote.Candidate2Vote
        vc3 = vc1+vc2
        if vc3 != 0:
            vc1 = vc1*100/vc3

            vc2 = vc2*100/vc3
            vc1 = round(vc1, 2)
            vc2 = round(vc2, 2)
    context = {
        'Elections': elc,
        'UserID': userid,
        'Check': check,
        'President': ss,
        'vc1': vc1,
        'vc2': vc2,
    }
    return render(request, 'VotingPage.html', context)


@login_required
def MinistryPage(request):
    if request.method == 'POST':
        minister_setup = request.POST.get('save')
        if minister_setup == 'setup':
            return redirect(MinistrySetupPage)
    UserID = int(request.user.username)
    objMinisterList = CountryMinistries.objects.exclude(MinisterName='1')
    ministerids = []
    for mid in objMinisterList:
        ministerids.append(mid.MinisterID)
    objUserPrimaryDetails = []
    objMinisterPrimaryDetails = []
    for id in ministerids:
        objUserPrimaryDetails += (UsersPrimaryDetails.objects.filter(UserID=id))
        objUserPrimaryDetails = list(objUserPrimaryDetails)
        objMinisterPrimaryDetails += (
            MinisterPrimaryDetails.objects.filter(MinisterNumberID=id))
        objMinisterPrimaryDetails = list(objMinisterPrimaryDetails)
    ss = 00000000
    context = {
        'UserID': UserID,
        'President': ss,
        'MinisterList': objMinisterPrimaryDetails,
        'MinisterDetails': objUserPrimaryDetails,
    }
    return render(request, 'MinistryPage.html', context)


@login_required
def ElectionSetupPage(request):
    if request.method == 'POST':
        Candidate1 = request.POST.get('Candidate1')
        Candidate2 = request.POST.get('Candidate2')
        Constituency = request.POST.get('Constituency')
        name = request.POST.get('save')
        Cd1 = int(Candidate1)
        Cd2 = int(Candidate2)
        findCandidate = PoliticiansPrimaryDetails.objects.filter(
            PoliticianID=Cd1)
        findCandidate1 = findCandidate.exists()
        findCandidate = PoliticiansPrimaryDetails.objects.filter(
            PoliticianID=Cd2)
        findCandidate2 = findCandidate.exists()
        findconstituency = CountryConstituency.objects.filter(
            ConstituencyName=Constituency)
        findconstituency0 = findconstituency.exists()
        print(findconstituency0, findCandidate1, findCandidate2)
        if (findCandidate1 is False or findCandidate2 is False or findconstituency0 is False):
            messages.error(
                request, 'could not find any matches for your input')
        elif Cd1 == Cd2:
            messages.error(
                request, 'Please select two different candidates.')
        else:
            time = datetime.datetime.now(pytz.timezone('UTC'))
            starttime = time
            time = increase_hour(time)
            endtime = time
            votedonelist = json.dumps("", separators=(",", ","))
            if name == "confirm":
                Election = MPElection(Candidate1, Candidate2,
                                      0, 0, True, starttime, endtime, Constituency, Cd1, Cd2, votedonelist)
                Election.save()
            return redirect(VotingPage)
    AfterElection = MPElection.objects.filter(ElectionStatus=False)
    for Ae in AfterElection:
        Constituency = Ae.Constituency
        Ca1 = Ae.Candidate1Vote
        Ca2 = Ae.Candidate2Vote
        Cd1 = Ae.Cd1
        Cd2 = Ae.Cd2
        if Ca1 > Ca2:
            WinnerID = Cd1
        elif Ca1 < Ca2:
            WinnerID = Cd2
        else:
            WinnerID = -800
            AePPd1 = PoliticiansPrimaryDetails.objects.get(Pid=Ae.Cd1)
            AePPd2 = PoliticiansPrimaryDetails.objects.get(Pid=Ae.Cd2)
            AePPd1.ElectionRun += 1
            AePPd2.ElectionRun += 1
            AePPd1.save()
            AePPd2.save()
        if Cd1 < Cd2 or Cd1 > Cd2:
            AePPd = PoliticiansPrimaryDetails.objects.get(Pid=WinnerID)
            AePPd.TimeLeft = 1
            AePPd.ElectionRun += 1
            AePPd.ElectionWon += 1
            AePPd.PoliticianRole = f'MP({Constituency})'
            AePPd.IsMP = True
            AePPd.save()
            AeUpd = UsersPrimaryDetails.objects.get(UserID=WinnerID)
            AeUpd.UserRole = f'MP({Constituency})'
            AeUpd.UserPoints += 1000
            AeUpd.save()
            obj_constituency = CountryConstituency.objects.get(
                ConstituencyName=Constituency)
            obj_constituency.TimeLeft = 1
            obj_constituency.save()
            Ae.ElectionStatus = True
            Ae.save()
    ConstituencyList = CountryConstituency.objects.filter(TimeLeft='0')
    PoliticiansList = PoliticiansPrimaryDetails.objects.filter(TimeLeft='0')
    context = {}
    context.update({"ConstituencyList": ConstituencyList})
    context.update({"PoliticiansList": PoliticiansList})
    return render(request, 'ElectionSetupPage.html', context)


@login_required
def MinistrySetupPage(request):
    if request.method == 'POST':
        MinistryName = request.POST.get('Ministry')
        MinisterName = request.POST.get('MP')
        name = request.POST.get('save')
        MinisterID = get_number_from_string(MinisterName)
        MinisterName = get_text_from_string(MinisterName)
        if name == 'confirm':
            ObjCountryMinistry = CountryMinistries.objects.get(
                MinistryName=MinistryName)
            ObjCountryMinistry.MinisterName = MinisterName
            ObjCountryMinistry.MinisterID = MinisterID
            objPoliticianPrimaryDetails = PoliticiansPrimaryDetails.objects.get(
                PoliticianID=MinisterID)
            objPoliticianPrimaryDetails.IsMinister = True
            tmpConstitutionName = extract_district_from_mp(
                objPoliticianPrimaryDetails.PoliticianRole)
            objMinisterPrimaryDetails = MinisterPrimaryDetails(
                MinistryName, MinisterID, tmpConstitutionName, MinisterID)
            objMinisterPrimaryDetails.save()
            objPoliticianPrimaryDetails.save()
            ObjCountryMinistry.save()
            return redirect(MinistryPage)

    PoliticiansList = PoliticiansPrimaryDetails.objects.filter(
        Q(IsMP=True) & Q(IsMinister=False))
    MinistriesList = CountryMinistries.objects.filter(MinisterName='1')
    context = {}
    context.update({"MpList": PoliticiansList})
    context.update({'MinistryList': MinistriesList})
    return render(request, 'MinistrySetupPage.html', context)


@login_required
def TransportationMain(request):
    return render(request, 'Transportation/TransportationMain.html')


def homebus(request):
    if request.user.is_authenticated:
        return render(request, 'Transportation/Bus/homebus.html')
    else:
        return render(request, 'Transportation/Bus/signin.html')


def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        bus_list = Bus.objects.filter(
            source=source_r, dest=dest_r, date=date_r)
        if bus_list:
            return render(request, 'Transportation/Bus/list.html', locals())
        else:
            context["error"] = "Sorry no buses available"
            return render(request, 'Transportation/Bus/findbus.html', context)
    else:
        return render(request, 'Transportation/Bus/findbus.html')


def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=id_r)  # Corrected the field name to 'id'
        if bus:
            if bus.rem > int(seats_r):
                name_r = bus.bus_name
                cost = int(seats_r) * bus.price
                source_r = bus.source
                dest_r = bus.dest
                nos_r = (bus.nos)
                price_r = bus.price
                date_r = bus.date
                time_r = bus.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = bus.rem - seats_r
                Bus.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(name=username_r, email=email_r, bus_name=name_r, source=source_r,
                                           dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                # book.save()
                return render(request, 'Transportation/Bus/bookings.html', locals())
            else:
                context["error"] = "Sorry, select fewer number of seats"
                return render(request, 'Transportation/Bus/findbus.html', context)

    else:
        return render(request, 'Transportation/Bus/findbus.html')


def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        # seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            # nos_r = book.nos - seats_r
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'Transportation/Bus/error.html', context)
    else:
        return render(request, 'Transportation/Bus/findbus.html')


def seebookings(request, new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(id=id_r)
    if book_list:
        return render(request, 'Transportation/Bus/booklist.html', locals())
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'Transportation/Bus/findbus.html', context)


def hometrain(request):
    if request.user.is_authenticated:
        return render(request, 'Transportation/Train/hometrain.html')
    else:
        return render(request, 'Transportatio/Train/signin.html')


def find_train(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        train_list = Train.objects.filter(
            source=source_r, dest=dest_r, date=date_r)
        if train_list:
            return render(request, 'Transportation/Train/list.html', locals())
        else:
            context["error"] = "Sorry no train available"
            return render(request, 'Transportation/Train/findtrain.html', context)
    else:
        return render(request, 'Transportation/Train/findtrain.html')


def booking(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('train_id')
        seats_r = int(request.POST.get('no_seats'))
        train = Train.objects.get(id=id_r)
        if train:
            if train.rem > int(seats_r):
                name_r = train.train_name
                cost = int(seats_r) * train.price
                source_r = train.source
                dest_r = train.dest
                nos_r = train.nos
                price_r = train.price
                date_r = train.date
                time_r = train.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = train.rem - seats_r
                Train.objects.filter(id=id_r).update(rem=rem_r)
                book = BookTrain.objects.create(name=username_r, email=email_r, train_name=name_r, source=source_r,
                                                dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                                status='BOOKED')
                print('------------book id-----------', book.id)
                # book.save()
                return render(request, 'Transportation/Train/bookings.html', locals())
            else:
                context["error"] = "Sorry, select fewer number of seats"
                return render(request, 'Transportation/Train/findtrain.html', context)

    else:
        return render(request, 'Transportation/Train/findtrain.html')


def cancelling(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('train_id')
        # seats_r = int(request.POST.get('no_seats'))

        try:
            book = BookTrain.objects.get(id=id_r)
            train = Train.objects.get(id=book.trainid)
            rem_r = train.rem + book.nos
            Train.objects.filter(id=book.trainid).update(rem=rem_r)
            # nos_r = book.nos - seats_r
            BookTrain.objects.filter(id=id_r).update(status='CANCELLED')
            BookTrain.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except BookTrain.DoesNotExist:
            context["error"] = "Sorry You have not booked that train"
            return render(request, 'Transportation/Train/error.html', context)
    else:
        return render(request, 'Transportation/Train/findtrain.html')


def seebooking(request, new={}):
    context = {}
    id_r = request.user.id
    book_list = BookTrain.objects.filter(id=id_r)
    if book_list:
        return render(request, 'Transportation/Train/booklist.html', locals())
    else:
        context["error"] = "Sorry no train booked"
        return render(request, 'Transportation/Train/findTrain.html', context)


def homeplane(request):
    if request.user.is_authenticated:
        return render(request, 'Transportation/Plane/homeplane.html')
    else:
        return render(request, 'Transportation/Plane/signin.html')


def find_plane(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        plane_list = Plane.objects.filter(
            source=source_r, dest=dest_r, date=date_r)
        if plane_list:
            return render(request, 'Transportation/Plane/list.html', locals())
        else:
            context["error"] = "Sorry no plane available"
            return render(request, 'Transportation/Plane/findplane.html', context)
    else:
        return render(request, 'Transportation/Plane/findplane.html')


def bookingp(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('plane_id')
        seats_r = int(request.POST.get('no_seats'))
        plane = Plane.objects.get(id=id_r)
        if plane:
            if plane.rem > int(seats_r):
                name_r = plane.plane_name
                cost = int(seats_r) * plane.price
                source_r = plane.source
                dest_r = plane.dest
                nos_r = plane.nos
                price_r = plane.price
                date_r = plane.date
                time_r = plane.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = plane.rem - seats_r
                Plane.objects.filter(id=id_r).update(rem=rem_r)
                book = BookPlane.objects.create(name=username_r, email=email_r, plane_name=name_r, source=source_r,
                                                dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                                status='BOOKED')
                print('------------book id-----------', book.id)
                # book.save()
                return render(request, 'Transportation/Plane/bookings.html', locals())
            else:
                context["error"] = "Sorry, select fewer number of seats"
                return render(request, 'Transportation/Plane/findplane.html', context)

    else:
        return render(request, 'Transportation/Plane/findplane.html')


def cancellingp(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('plane_id')
        # seats_r = int(request.POST.get('no_seats'))

        try:
            book = BookPlane.objects.get(id=id_r)
            plane = Plane.objects.get(id=book.planeid)
            rem_r = plane.rem + book.nos
            Plane.objects.filter(id=book.planeid).update(rem=rem_r)
            # nos_r = book.nos - seats_r
            BookPlane.objects.filter(id=id_r).update(status='CANCELLED')
            BookPlane.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except BookPlane.DoesNotExist:
            context["error"] = "Sorry You have not booked that plane"
            return render(request, 'Transportation/Plane/error.html', context)
    else:
        return render(request, 'Transportation/Plane/findplane.html')


def seebookingp(request, new={}):
    context = {}
    id_r = request.user.id
    book_list = BookPlane.objects.filter(id=id_r)
    if book_list:
        return render(request, 'Transportation/Plane/booklist.html', locals())
    else:
        context["error"] = "Sorry no plane booked"
        return render(request, 'Transportation/Plane/findplane.html', context)


@login_required
def HealthcareMain(request):
    return render(request, "Healthcare/HealthcareMain.html")


def Clinic(request):
    return render(request, "Healthcare/Category.html/Clinic.html")


def Hospital(request):
    return render(request, "Healthcare/Category.html/Hospital.html")


def Pharmacy(request):
    return render(request, "Healthcare/Category.html/Pharmacy.html")


def Diagnostic(request):
    return render(request, "Healthcare/Category.html/Diagnostic.html")


def Eyeclinic(request):
    return render(request, "Healthcare/Category.html/Eyeclinic.html")


def PublicClinic(request):
    return render(request, "Healthcare/Clinic.html/PublicClinic.html")


def PrivateClinic(request):
    return render(request, "Healthcare/Clinic.html/PrivateClinic.html")


def PublicHospital(request):
    return render(request, "Healthcare/Hospital.html/PublicHospital.html")


def PrivateHospital(request):
    return render(request, "Healthcare/Hospital.html/PrivateHospital.html")


def PrivateDiagnostic(request):
    return render(request, "Healthcare/Diagnostic.html/PrivateDiagnostic.html")


def PublicDiagnostic(request):
    return render(request, "Healthcare/Diagnostic.html/PublicDiagnostic.html")


def PrivateEyeclinic(request):
    return render(request, "Healthcare/Eyeclinic.html/PrivateEyeclinic.html")


def PublicEyeclinic(request):
    return render(request, "Healthcare/Eyeclinic.html/PublicEyeclinic.html")


def HospitalAppointmentPage(request):
    return render(request, "Healthcare/Hospital.html/HospitalAppointmentPage.html")


def PharmacyBookingPage(request):
    return render(request, "Healthcare/Pharmacy.html/PharmacyBookingPage.html")


def DiagnosticAppointmentPage(request):
    return render(request, "Healthcare/Diagnostic.html/DiagnosticAppointmentPage.html")


def ClinicAppointmentPage(request):
    return render(request, "Healthcare/Clinic.html/ClinicAppointmentPage.html")


def EyeclinicAppointmentPage(request):
    return render(request, "Healthcare/Eyeclinic.html/EyeclinicAppointmentPage.html")


def book_clinicappointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ThankYou')

    else:
        form = AppointmentForm()

    return render(request, 'Healthcare/Clinic.html/ClinicAppointmentPage.html', {'form': form})


def book_diagappointment(request):
    if request.method == 'POST':
        diaform = AppointmentForm(request.POST, request.FILES)
        if diaform.is_valid():
            diaform.save()
            return redirect('success')
    else:
        diaform = AppointmentForm()

    context = {
        'diaform': diaform,
    }
    return render(request, 'Healthcare/Diagnostic.html/DiagnosticAppointmentPage.html', context)


def book_hospitalappointment(request):
    if request.method == 'POST':
        hosform = AppointmentForm(request.POST)
        if hosform.is_valid():
            hosform.save()
            return redirect('ThankYou')

    else:
        hosform = AppointmentForm()

    return render(request, 'Healthcare/Hospital.html/HospitalAppointmentPage.html', {'hosform': hosform})


def book_pharmacyappointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ThankYou')

    else:
        form = AppointmentForm()

    return render(request, 'Healthcare/Pharmacy.html/PharmacyBookingPage.html', {'form': form})


def book_eyeappointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ThankYou')

    else:
        form = AppointmentForm()

    return render(request, 'Healthcare/Eyeclinic.html/EyeclinicAppointmentPage.html', {'form': form})


def ThankYou(request):
    return render(request, 'Healthcare/ThankYou.html')


@login_required
def EducationPage(request):
    return render(request, 'EducationPage.html')


def College(request):
    colleges = Collegee.objects.all()
    return render(request, 'Education/College.html', {'colleges': colleges})


def Honours(request):
    honours = Honourss.objects.all()
    return render(request, 'Education/Honours.html', {'honours': honours})


def Masters(request):
    masters = Masterss.objects.all()
    return render(request, 'Education/Masters.html', {'masters': masters})


def Form(request):
    return render(request, 'Education/Form.html')


def Collegeapply(request):
    if request.method == 'POST':
        collegeform = CollegeApplicantForm(request.POST, request.FILES)
        if collegeform.is_valid():
            collegeform.save()
            return redirect('success')
    else:
        collegeform = CollegeApplicantForm()

    context = {
        'collegeform': collegeform,
    }
    return render(request, 'Education/Collegeapply.html', context)


def Mastersapply(request):
    if request.method == 'POST':
        mastersform = MastersApplicantForm(request.POST, request.FILES)
        if mastersform.is_valid():
            mastersform.save()
            return redirect('success')
    else:
        mastersform = MastersApplicantForm()

    context = {
        'mastersform': mastersform,
    }
    return render(request, 'Education/Mastersapply.html', context)


def Honoursapply(request):
    if request.method == 'POST':
        honoursform = HonoursApplicantForm(request.POST, request.FILES)
        if honoursform.is_valid():
            honoursform.save()
            return redirect('success')
    else:
        honoursform = HonoursApplicantForm()

    context = {
        'honoursform': honoursform,
    }
    return render(request, 'Education/Honoursapply.html', context)


def success(request):
    return render(request, 'Education/success.html')


@login_required
def EntertainmentPage(request):
    if request.method == "POST":
        nameu = request.POST.get('save')
        SportName = request.POST.get('Sport')
        SportName = Sport.objects.get(id=SportName)
        Venue = request.POST.get('SportVenue')
        Venue = SportVenue.objects.get(id=Venue)
        Date = request.POST.get('SportDate')
        Date = SportDate.objects.get(id=Date)
        Date = str(Date)
        SeatType = request.POST.get('SportSeatType')
        SeatType = SportSeatType.objects.get(id=SeatType)
        SeatType = str(SeatType)
        TicketPrice = get_number_from_string(SeatType)
        TicketPrice = int(TicketPrice)
        SeatType = SeatType.split("(")[0]
        UserID = request.user.username
        UserMoney = UsersPrimaryDetails.objects.get(UserID=UserID)
        parts = Date.split("-")
        month, day = parts[1], parts[2]
        month_name = calendar.month_name[int(month)]
        DM = f"{month_name} {day}TH"
        Year = Date.split("-")[0]
        pattern = r"\d{4}-\d{2}-\d{2}"
        match = re.search(pattern, Date)
        year, month, day = int(match.group(0)[:4]), int(
            match.group(0)[5:7]), int(match.group(0)[8:])
        DayName = calendar.day_name[calendar.weekday(year, month, day)]
        text = str(Venue)
        parts = text.split(",")
        GroundName = parts[0]
        CityName = parts[1]
        if nameu == "confirm":
            if UserMoney.UserPoints > TicketPrice:
                UserMoney.UserPoints = UserMoney.UserPoints-TicketPrice
                UserMoney.save()
                SportSeatNumber = random.randrange(00000, 99999)
                SeatNumber = str(SportSeatNumber)
                objectU = SportTickets(
                    SportName, Venue, Date, SeatType, SeatNumber, TicketPrice, UserID)
                objectU.save()
                TicketData = {'Ticket': objectU, 'DM': DM, 'Year': Year,
                              'DayName': DayName, 'CityName': CityName, 'GroundName': GroundName}
                return render(request, 'SportTicket.html', TicketData)
            else:
                messages.error(
                    request, 'You do not have enough money to buy the ticket.')
    game = Sport.objects.all()
    d = {'Sport': game}
    return render(request, 'EntertainmentPage.html', d)


@login_required
def LoadVenues(request):
    gameid = request.GET.get('Sport')
    Venues = SportVenue.objects.filter(Sport=gameid).order_by('name')
    return render(request, 'Venue_dropdown_list_options.html', {'Venues': Venues})


@login_required
def LoadDate(request):
    Venueid = request.GET.get('SportVenue')
    Dates = SportDate.objects.filter(SportVenue=Venueid).order_by('name')
    return render(request, 'Date_dropdown_list_options.html', {'Dates': Dates})


@login_required
def LoadSeat(request):
    Dateid = request.GET.get('SportDate')
    Seates = SportSeatType.objects.filter(SportDate=Dateid).order_by('name')
    return render(request, 'Seat_dropdown_list_options.html', {'Seates': Seates})


@login_required
def SportTicket(request):
    return render(request, 'SportTicket.html')

# sports finish


@login_required
def Am_I_A_CitizenPage(request):
    if request.method == 'POST':
        news = request.POST.get('save')
        if news == "confirm":
            userOpinion = request.POST.get('Opinions')
            opinion = PublicOpinions(request.user.username, userOpinion)
            opinion.save()
        else:
            return redirect(NewsDetailsPage, news)
    opinions = PublicOpinions.objects.all()

    api_key = '392d7f4dc8c84340adfd4248a825e0e5'
    newsapi = NewsApiClient(api_key=api_key)

    # Specify your query parameters
    query_params = {
        'language': 'en',  # Language code (e.g., 'en' for English)
    }

    # Fetch news articles using the `get_top_headlines` method
    headlines = newsapi.get_top_headlines(**query_params)
    headlines = headlines['articles'][:10]
    context = {
        'NEWS': headlines,
        'PublicOpinion': opinions
    }
    return render(request, 'Am-I-A-CitizenPage.html', context)


@login_required
def NewsDetailsPage(request, news):
    response = requests.get(news)
    html_content = response.content

#   Remove any unnecessary elements from the HTML content.
    soup = BeautifulSoup(html_content, "html.parser")
    header = soup.find("header")
    footer = soup.find("footer")
    nav = soup.find("nav")
    if header is not None:
        header.extract()
    if footer is not None:
        footer.extract()
    if nav is not None:
        nav.extract()
    context = {
        "news": soup.prettify()
    }
    return render(request, 'NewsDetailsPage.html', context)


@login_required
def AboutPage(request):
    return render(request, 'AboutPage.html')


@login_required
def ContactPage(request):
    return render(request, 'ContactPage.html')


@login_required
def HelpPage(request):
    return render(request, 'HelpPage.html')


@login_required
def TicketsPage(request):
    user = request.user.username
    Tickets = SportTickets.objects.filter(UserID=user)
    return render(request, 'TicketsPage.html', {'Tickets': Tickets})


def Undefine(request, undefined_path):
    return redirect(HomePage)
