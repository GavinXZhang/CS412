from django.shortcuts import render

# Create your views he
from django.http import JsonResponse

import random 

def index(request):
    if 'currency' not in request.session:
        request.session['currency'] = 100 # Starting currency
    return render(request, 'gacha/index.html', {'currency': request.session['currency']})
def spin(request):
    if request.method == 'POST':
        spin_cost = 10
        currency = request.session.get('currency', 0)

        if currency < spin_cost:
            return JsonResponse({'error':'not enough currency to spin!'}, status = 400)
        
        currency -= spin_cost
        request.session['currency'] = currency

        rewards = [
            ('Common', .7),
            ('Rare', .25),
            ('Epic', .04),
            ('Legendary', .01)
        ]

        random_value = random.random()
        cumulative = 0
        result = 'Common'
        for reward, probability in rewards:
            cumulative += probability
            if random_value < cumulative:
                result = reward 
                break 

        return JsonResponse({'result':result, 'currency':currency})
    else:
        return JsonResponse({'error':'Invalid request method'}, status = 405)