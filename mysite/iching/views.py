from django.shortcuts import render
from django.http import HttpResponse
from .models import Hexagram, CastedResult, Coin, UserProfile
from random import randint
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

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

                    # Save the hexagrams to the user's profile
                    # user_profile = UserProfile.objects.get(user=request.user)
                    # user_profile.saved_hexagrams.add(hexagram_number)
                    #
                    # if modified_hexagram_number:
                    #     user_profile.saved_hexagrams.add(modified_hexagram_number)
                    #
                    # user_profile.save()

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


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} is already taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with email address {email} is already registered!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    UserProfile.objects.create(user=user)

                    messages.info(request, f'User {username} has been registered sucessfully!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'registration/register.html')

@login_required
def my_iching(request):
    user_profile = UserProfile.objects.get(user=request.user)
    saved_hexagrams = user_profile.saved_hexagrams.all()
    context = {
        'saved_hexagrams': saved_hexagrams
    }
    return render(request, 'my_iching.html', context=context)