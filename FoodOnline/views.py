from django.shortcuts import HttpResponse, redirect, render


def HomeView(request):
    return render(request,'home.html')