from django.shortcuts import render
from django.http import HttpResponse
from .models import Hexagram
from random import randint



def index(request):
    return render(request, 'index.html')


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
        return "_____"
    elif results in [["Tails", "Tails", "Heads"], ["Tails", "Heads", "Tails"], ["Heads", "Tails", "Tails"]]:
        return "__ __"
    elif results == ["Heads", "Heads", "Heads"]:
        return "__ __."
    else:
        return "_____."


def toss_coins(request):
    if request.method == "POST":
        casted_results = request.session.get('casted_results', [])
        results = generate_results()
        casted_results.append(cast_results(results))
        request.session['casted_results'] = casted_results
    else:
        request.session['casted_results'] = []

    context = {
        'toss_results': generate_results(),
        'casted_results': request.session['casted_results'],
    }
    return render(request, "toss_coins.html", context=context)