import random
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.forms import forms
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import datetime
from django.core.exceptions import ValidationError
import re

from .models import *
from .models import Appointment


from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Collegee, Honourss, Masterss,CollegeSubject,CollegeApplicant,HonoursSubject,HonoursApplicant,MastersSubject,MastersApplicant


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username has already been taken.')
        return username


def increase_hour(time):
    new_time = time + datetime.timedelta(hours=1)
    if new_time.minute < time.minute:
        new_time += datetime.timedelta(minutes=60)
    return new_time


def get_number_from_string(string):
    """Extracts the only number value from a string.

    Args:
      string: A string.

    Returns:
      A string containing the only number value in the string, or an empty string
      if no number value is found.
    """

    pattern = r'\d+'
    match = re.search(pattern, string)
    if match:
        return match.group()
    else:
        return ''


def get_text_from_string(string):
    """Extracts the text from a string, excluding any numbers.

    Args:
      string: A string.

    Returns:
      A string containing the text from the string, excluding any numbers, or an
      empty string if no text is found.
    """

    pattern = r'[^\d]+'
    match = re.search(pattern, string)
    if match:
        return match.group()
    else:
        return ''


def extract_district_from_mp(mp_string):
    """Extracts the district name from inside the brackets of a given MP string.

    Args:
      mp_string: A string representing the MP's name and district.

    Returns:
      A string representing the district name, or None if the MP's district cannot be extracted.
    """

    district_pattern = re.compile(r'\(([^)]+)\)', re.IGNORECASE)
    match = district_pattern.search(mp_string)
    if match:
        return match.group(1)
    else:
        return None

class CollegeApplicantForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=CollegeSubject.objects.all())
    college = forms.ModelChoiceField(queryset=Collegee.objects.all())
    class Meta:
        model = CollegeApplicant
        fields = '__all__'
class HonoursApplicantForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=HonoursSubject.objects.all())
    honours = forms.ModelChoiceField(queryset=Honourss.objects.all())
    class Meta:
        model = HonoursApplicant
        fields = '__all__'
class MastersApplicantForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=MastersSubject.objects.all())
    masters = forms.ModelChoiceField(queryset=Masterss.objects.all())
    class Meta:
        model = MastersApplicant
        fields = '__all__'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'facility', 'date', 'description']