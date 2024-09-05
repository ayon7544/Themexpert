from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete


class UsersPrimaryDetails(models.Model):
    UserID = models.IntegerField(primary_key=True)
    UserEmail = models.EmailField(max_length=254)
    UserFullName = models.CharField(max_length=255)
    UserGender = models.CharField(max_length=255)
    UserOccupation = models.CharField(max_length=255)
    UserDateOfBirth = models.DateField()
    UserRole = models.CharField(max_length=255)
    UserMobileNum = models.CharField(max_length=255)
    UserPoints = models.IntegerField()
    UserImageFilename = models.ImageField()
    UserAge = models.IntegerField()

    def __str__(self):
        return str(self.UserID)


class PoliticiansPrimaryDetails(models.Model):
    PoliticianID = models.OneToOneField(
        UsersPrimaryDetails, on_delete=models.CASCADE, primary_key=True)
    PoliticianRole = models.CharField(max_length=255)
    PoliticianName = models.CharField(max_length=256)
    TimeLeft = models.IntegerField()
    ElectionRun = models.IntegerField()
    ElectionWon = models.IntegerField()
    Pid = models.IntegerField()
    IsMP = models.BooleanField()
    IsMinister = models.BooleanField()

    def __str__(self):
        return str(self.PoliticianName)


class CountryConstituency(models.Model):
    ConstituencyName = models.CharField(max_length=255)
    TimeLeft = models.IntegerField()

    def __str__(self):
        return str(self.ConstituencyName)


class MPElection(models.Model):
    Candidate1ID = models.ForeignKey(
        UsersPrimaryDetails, on_delete=models.CASCADE, related_name="Candidate1ID")
    Candidate2ID = models.ForeignKey(
        UsersPrimaryDetails, on_delete=models.CASCADE, related_name="Candidate2ID")
    Candidate1Vote = models.IntegerField()
    Candidate2Vote = models.IntegerField()
    ElectionStatus = models.BooleanField()
    StartTime = models.DateTimeField(primary_key=True)
    EndTime = models.DateTimeField()
    Constituency = models.CharField(max_length=254)
    Cd1 = models.IntegerField()
    Cd2 = models.IntegerField()
    VoteDoneList = models.JSONField()

    def __str__(self):
        return str(self.StartTime)


class CountryMinistries(models.Model):
    MinistryName = models.CharField(max_length=300, primary_key=True)
    MinisterName = models.CharField(max_length=255)
    MinisterID = models.IntegerField()

    def __str__(self):
        return str(self.MinistryName)


class MinisterPrimaryDetails(models.Model):
    MinistryName = models.OneToOneField(
        CountryMinistries, on_delete=models.CASCADE)
    MinisterID = models.OneToOneField(
        PoliticiansPrimaryDetails, on_delete=models.CASCADE, primary_key=True)
    MinisterConstituency = models.CharField(max_length=254)
    MinisterNumberID = models.IntegerField()

    def __str__(self):
        return str(self.MinisterID)


class PublicOpinions(models.Model):
    UserID = models.IntegerField()
    Opinion = models.TextField(primary_key=True)

    def __str__(self):
        return str(self.Opinion)


# entertainment/Sports


class Sport(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class SportVenue(models.Model):
    Sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class SportDate(models.Model):
    SportVenue = models.ForeignKey(SportVenue, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SportSeatType(models.Model):
    SportDate = models.ForeignKey(SportDate, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SportTickets(models.Model):
    SportName = models.CharField(max_length=500)
    SportVenue = models.CharField(max_length=1000)
    SportDate = models.CharField(max_length=100)
    SportSeatType = models.CharField(max_length=100)
    SportSeatNumber = models.CharField(max_length=500)
    SportTicketPrice = models.CharField(max_length=500)
    UserID = models.ForeignKey(UsersPrimaryDetails, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)


class Bus(models.Model):
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.bus_name


class UserB(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES,
                              default=BOOKED, max_length=2)

    def __str__(self):
        return self.email


class Train(models.Model):
    train_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.train_name


class UserB(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class BookTrain(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    train_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES,
                              default=BOOKED, max_length=2)

    def __str__(self):
        return self.email


class Plane(models.Model):
    plane_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.plane_name


class UserB(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class BookPlane(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    plane_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES,
                              default=BOOKED, max_length=2)

    def __str__(self):
        return self.email


class Collegee(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Honourss(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Masterss(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CollegeSubject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CollegeApplicant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255)
    school_name = models.CharField(max_length=255)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    subject = models.ForeignKey(CollegeSubject, on_delete=models.CASCADE)
    college = models.ForeignKey(Collegee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HonoursSubject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HonoursApplicant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255)
    collage_name = models.CharField(max_length=255)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    subject = models.ForeignKey(HonoursSubject, on_delete=models.CASCADE)
    institute_name = models.ForeignKey(Honourss, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MastersSubject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MastersApplicant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255)
    honours_from = models.CharField(max_length=255)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    subject = models.ForeignKey(CollegeSubject, on_delete=models.CASCADE)
    institute_name = models.ForeignKey(Masterss, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    facility = models.CharField(max_length=255)
    date = models.DateField()
    description = models.CharField(max_length=255)
