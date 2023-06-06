from django.shortcuts import render
from django.http import HttpResponse
from .models import Hexagram, CastedResult, Coin, CoinTossCombination
from random import randint


def index(request):
    return render(request, 'index.html')


Heads = Coin.objects.get(side="Heads")
Tails = Coin.objects.get(side="Tails")


# toss of 1 coin
def toss():
    result = Heads if randint(0, 1) == 0 else Tails
    return result


# tossing 3 coins
def generate_results():
    results = []
    for i in range(3):
        results.append(toss())
    return results


# assigning result to toss_combination
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


# assigning opposite value in case of HHH or TTT
def change(casted_result):
    if casted_result["name"] == "HHH":
        casted_result = CastedResult.objects.get(name="TTT")
        return {"name": casted_result.name, "line": casted_result.line.line}
    elif casted_result["name"] == "TTT":
        casted_result = CastedResult.objects.get(name="HHH")
        return {"name": casted_result.name, "line": casted_result.line.line}
    else:
        return casted_result


def toss_coins(request):
    new_toss = False
    situation_change = False
    hexagram_number = ""
    modified_hexagram_number = ""

    if request.method == "POST":
        button_clicks = request.session.get('button_clicks', 0)

        if button_clicks < 6:
            results = generate_results()
            casted_results = cast_results(results)
            session_results = request.session.get('casted_results', [])
            session_results.append(casted_results)
            request.session['casted_results'] = session_results[:6]  # Limit to 6 rows
            button_clicks += 1
            request.session['button_clicks'] = button_clicks
            print(session_results)

            if button_clicks == 6:
                hexagram_number = Hexagram.objects.get(
                    line1__line=session_results[0]["line"],
                    line2__line=session_results[1]["line"],
                    line3__line=session_results[2]["line"],
                    line4__line=session_results[3]["line"],
                    line5__line=session_results[4]["line"],
                    line6__line=session_results[5]["line"],
                )
                print(session_results)
                new_toss = True

                if any(result["name"] in ["HHH", "TTT"] for result in session_results):
                    situation_change = True
                    modified_results = []
                    for result in session_results:
                        modified_result = change(result)
                        modified_results.append(modified_result)
                    modified_hexagram_number = Hexagram.objects.get(
                        line1__line=modified_results[0]["line"],
                        line2__line=modified_results[1]["line"],
                        line3__line=modified_results[2]["line"],
                        line4__line=modified_results[3]["line"],
                        line5__line=modified_results[4]["line"],
                        line6__line=modified_results[5]["line"],
                    )
                    print(modified_hexagram_number)

        else:
            results = []
            casted_results = []
            request.session['casted_results'] = []
            request.session['button_clicks'] = 0
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
        'modified_hexagram_number': modified_hexagram_number,
        'new_toss': new_toss,
    }
    return render(request, "toss_coins.html", context=context)

