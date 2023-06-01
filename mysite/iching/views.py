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
    new_toss = False

    if request.method == "POST":
        button_clicks = request.session.get('button_clicks', 0)

        if button_clicks < 6:
            results = generate_results()
            casted_results = cast_results(results)
            session_results = request.session.get('casted_results', [])
            session_results.insert(0, casted_results)
            request.session['casted_results'] = session_results[:6]  # Limit to 6 rows
            button_clicks += 1
            request.session['button_clicks'] = button_clicks

            if button_clicks == 6:
                # Retrieve hexagram number from the database based on the casted results
                hexagram_number = "Hexagram Number"
                request.session['hexagram_number'] = hexagram_number
                new_toss = True

        else:
            results = []
            casted_results = []
            hexagram_number = request.session.get('hexagram_number')
            # Reset values to start over
            request.session['button_clicks'] = 0
            request.session['casted_results'] = []
            request.session['hexagram_number'] = None

    else:
        results = []
        casted_results = []
        request.session['casted_results'] = []
        request.session['button_clicks'] = 0
        request.session['hexagram_number'] = None

    context = {
        'toss_results': results,
        'casted_results': request.session['casted_results'],
        'hexagram_number': request.session['hexagram_number'],
        'new_toss': new_toss,
    }
    return render(request, "toss_coins.html", context=context)



