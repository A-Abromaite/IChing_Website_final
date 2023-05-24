from django.shortcuts import render
from django.http import HttpResponse
from .models import Hexagram

def index(request):
    num_hexagrams = Hexagram.objects.all().count()

    context = {
        'num_hexagrams': num_hexagrams,
    }
    return render(request, 'index.html', context=context)

def toss_coins(request):
    return render(request, 'toss_coins.html')