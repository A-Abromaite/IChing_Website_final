from django.shortcuts import render
from django.http import HttpResponse
from .models import Hexagram
from random import randint



def index(request):
    num_hexagrams = Hexagram.objects.all().count()

    context = {
        'num_hexagrams': num_hexagrams,
    }
    return render(request, 'index.html', context=context)

#
# def toss_coins(request):
#     return render(request, 'toss_coins.html')

def toss_coins(request):
    if request.method == "POST":
        result = "Heads" if randint(0, 1) == 0 else "Tails"
    else:
        result = ""
    return render(request, "toss_coins.html", {"toss_result": result})