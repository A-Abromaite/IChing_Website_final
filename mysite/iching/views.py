from django.shortcuts import render
from django.http import HttpResponse
from .models import Hexagram, CastedResult, Coin, CoinTossCombination
from random import randint



def index(request):
    return render(request, 'index.html')

Heads = Coin.objects.get(side="Heads")
Tails = Coin.objects.get(side="Tails")


def toss():
    result = Heads if randint(0, 1) == 0 else Tails
    return result

def generate_results():
    results = []
    for i in range(3):
        results.append(toss())
    return results

def cast_results(results):
    if results in [[Heads, Heads, Tails], [Heads, Tails, Heads], [Tails, Heads, Heads]]:
        casted_result = CastedResult.objects.get(name="HHT")
        return {"name": casted_result.name, "line": casted_result.line.line}
    elif results in [[Tails, Tails, Heads], [Tails, Heads, Tails], [Heads, Tails, Tails]]:
        casted_result = CastedResult.objects.get(name="TTH")
        return {"name": casted_result.name, "line": casted_result.line.line}
    elif results == [Heads, Heads, Heads]:
        casted_result = CastedResult.objects.get(name="HHH")
        return {"name": casted_result.name, "line": casted_result.line.line}
    else:
        casted_result = CastedResult.objects.get(name="TTT")
        return {"name": casted_result.name, "line": casted_result.line.line}


def toss_coins(request):
    new_toss = False
    hexagram_number = ""

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
            print(session_results)

            if button_clicks == 6:
                # Retrieve hexagram number from the database based on the casted results
                # session_results = request.session.get('casted_results', [])
                # hexagram_number = "Hexagram"
                hexagram_number = Hexagram.objects.filter(
                line1__line=session_results[0]["line"],
                line2__line=session_results[1]["line"],
                line3__line=session_results[2]["line"],
                line4__line=session_results[3]["line"],
                line5__line=session_results[4]["line"],
                line6__line=session_results[5]["line"],
                ).first()
                # request.session['hexagram_number'] = hexagram_number
                print(session_results)
                new_toss = True

        else:
            results = []
            casted_results = []
            # hexagram_number = request.session.get('hexagram_number')
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
        'hexagram_number': hexagram_number,
        'new_toss': new_toss,
    }
    return render(request, "toss_coins.html", context=context)



