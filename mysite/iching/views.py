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

def cast_results(results):
    if results in [["Heads", "Heads", "Tails"], ["Heads", "Tails", "Heads"], ["Tails", "Heads", "Heads"]]:
        return ("HHT")
    elif results in [["Tails", "Tails", "Heads"], ["Tails", "Heads", "Tails"], ["Heads", "Tails", "Tails"]]:
        return ("TTH")
    elif results == ["Heads", "Heads", "Heads"]:
        return ("HHH.")
    else:
        return ("TTT.")

def toss_coins(request):
    if request.method == "POST":
        results = generate_results()
        casted_results = cast_results(results)
    else:
        results = []
        casted_results = []

    context = {
        'toss_results': results,
        'casted_results': casted_results
    }
    return render(request, "toss_coins.html", context=context)
