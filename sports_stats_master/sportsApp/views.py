from django.shortcuts import render
from django.http import HttpResponse

#function that handles the traffic from the host page of the SportsApp
def home(request):
    return HttpResponse('<h1>Sports App Home</h1>')
