from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Hexagram, CastedResult, Coin, UserProfile, HexagramInstance
from random import randint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import datetime


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

                request.session['hexagram_number'] = hexagram_number.id

                print(session_results)
                print(hexagram_number)
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

                    request.session['modified_hexagram_number'] = modified_hexagram_number.id

                    print(modified_results)
                    print(modified_hexagram_number)


        else:
            results = []
            casted_results = []
            request.session['casted_results'] = []
            request.session['button_clicks'] = 0
            request.session['hexagram_number'] = None
            request.session['modified_hexagram_number'] = None

    else:
        results = []
        casted_results = []
        request.session['casted_results'] = []
        request.session['button_clicks'] = 0
        request.session['hexagram_number'] = None
        request.session['modified_hexagram_number'] = None

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

        if not username:
            messages.error(request, 'Username is required!')
            return redirect('register')
        if not email:
            messages.error(request, 'Email is required!')
            return redirect('register')
        if not password:
            messages.error(request, 'Password is required!')
            return redirect('register')
        if not password2:
            messages.error(request, 'Confirm password is required!')
            return redirect('register')

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


def save_hexagram(request):
    hexagram_id = request.session.get('hexagram_number')
    modified_hexagram_id = request.session.get('modified_hexagram_number')
    note = request.POST.get('note')

    hexagram_number = Hexagram.objects.get(id=hexagram_id)
    modified_hexagram_number = None

    if modified_hexagram_id:
        modified_hexagram_number = Hexagram.objects.get(id=modified_hexagram_id)

    timestamp = datetime.datetime.now()

    if request.method == 'POST' and hexagram_number:
        # Create a new HexagramInstance object and save it
        hexagram_instance = HexagramInstance(
            user_profile=request.user.userprofile,
            hexagram_number=hexagram_number,
            modified_hexagram_number=modified_hexagram_number,
            date_saved=timestamp,
            note=note
        )
        hexagram_instance.save()

        return redirect('my_iching')

    context = {
        'hexagram_number': hexagram_number,
        'modified_hexagram_number': modified_hexagram_number,
        'timestamp': timestamp,
        'note': note,
    }

    return render(request, 'save_hexagram.html', context)


@login_required
def my_iching(request):
    user_profile = UserProfile.objects.get(user=request.user)
    saved_hexagrams = HexagramInstance.objects.filter(user_profile=user_profile).order_by("-date_saved")

    context = {
        'saved_hexagrams': saved_hexagrams
    }
    return render(request, 'my_iching.html', context=context)
