from django.shortcuts import render
from django.http import JsonResponse
import urllib.request
import json



def index(request):
    return render(request, 'index.html')

con = ['INDIA', 'AUSTRALIA', 'CHINA', 'JAPAN']

st = ['PUNJAB', 'HARYANA']

ct = ['AMBALA','JALANDHAR','MOHALI']


def chatbot_view(request):
    # Check if a country has been provided in the session
    if 'country' not in request.session:
        message = 'Please enter your country:'
        request.session['prompt'] = 'state'
    elif 'state' not in request.session:
        request.session['country'] = request.POST.get('message', '').strip()
        message = 'Please enter your state:'
        request.session['prompt'] = 'city'
    elif 'city' not in request.session:
        request.session['state'] = request.POST.get('message', '').strip()
        city = request.POST.get('message', '').strip()
        country = request.session['country']
        state = request.session['state']
        source = urllib.request.urlopen('http://api.weatherstack.com/current?access_key=499926bcaf71ac88510480a752017b9b&query={},{},{}'.format(city, state, country)).read()
        list_of_data = json.loads(source)
        data = {
                    "country_code": str(list_of_data['location']['country']),
                    "city_name": str(list_of_data['location']['name']),
                    "coordinate": str(list_of_data['location']['lon']) + ', ' + str(list_of_data['location']['lat']),
                    "temp": str(list_of_data['current']['temperature']) + ' °C',
                    "pressure": str(list_of_data['current']['pressure']),
                    "humidity": str(list_of_data['current']['humidity']),
                }
        # Reset the session variables for the next use
        request.session.flush()
        # Return the weather information as a JSON response
        return JsonResponse({'message': 'Weather information for {} {}: {}'.format(country, state, data)})
    else:
        # This case should never happen if the previous elif statements are correct
        message = 'Unexpected error. Please try again.'
        request.session.flush()
        
    # If a prompt is required, save the user's input in the session and ask the next question
    if request.method == 'POST':
        user_input = request.POST.get('message', '').strip()
        if 'country' not in request.session:
            request.session['prompt'] = 'Please enter a state:'
            request.session['country'] = user_input
        elif 'state' not in request.session:
            request.session['prompt'] = 'Please enter a city:'
            request.session['state'] = user_input

    # Get the prompt from the session and return it as JSON
    prompt = request.session.get('prompt', 'Please enter a country:')
    return JsonResponse({'message': prompt})






