from django.shortcuts import render
from django.http import HttpResponse
from .models import Hexagram
from random import randint



def index(request):
    return render(request, 'index.html')

#
# def toss_coins(request):
#     return render(request, 'toss_coins.html')

def toss():
    result = "Heads" if randint(0, 1) == 0 else "Tails"
    return result

def generate_results():
    results = []
    for i in range(3):
        results.append(toss())
    return results


def toss_coins(request):
    print("Inside toss_coins view")
    if request.method == "POST":
        results = generate_results()
    else:
        results = []

    context = {
        'toss_results': results,
    }
    return render(request, "toss_coins.html", context=context)