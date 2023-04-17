from django.shortcuts import render
from django.http import HttpResponse

 
def login_score(request):
    return render(request, "base.html")

def game(request):
    return render(request, "index.html")