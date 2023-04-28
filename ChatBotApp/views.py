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
    if request.method == 'POST':
        message = ''
        user_input = request.POST.get('message').upper()

        if user_input in con:
            message = {'message': 'Please enter your state:'}
            request.session['prompt'] = 'state'
            request.session['state'] = user_input
        else:
            print("not in country")
            if user_input not in con:
                message = {'message': 'Welcome to the weather information chatbot! Please enter your country:'}
                request.session['prompt'] = 'country'
                print("country saved")
                print(request.session['country'])
            elif 'country' in request.session and 'state' not in request.session:
                message = {'message': 'Please enter your state:'}
                request.session['prompt'] = 'state'
                request.session['country'] = user_input
                print("country saved")
                print(request.session['country'])

            elif 'state' in request.session and 'city' not in request.session:
                message = {'message': 'Please enter your city:'}
                request.session['prompt'] = 'city'
                request.session['state'] = user_input
                print(request.session['city'])
                print("state saved")
            else:
                # Retrieve weather information using the entered country, state, and city
                country = request.session['country']
                state = request.session['state']
                city = request.POST['message']
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
                message = {'message': 'Weather information for {} {}, {}: {}'.format(city, state, country, data)}

                return JsonResponse(message)


        






    return JsonResponse(message)


    
    #     # If country, state, and city have not been entered yet, prompt the user for them
    #     if 'country' not in request.session:
    #         message = 'Please enter your country:'
    #         request.session['prompt'] = 'state'
    #     elif 'state' not in request.session:
    #         request.session['country'] = request.POST['message']
    #         message = 'Please enter your state:'
    #         request.session['prompt'] = 'city'
    #     elif 'city' not in request.session:
    #         request.session['state'] = request.POST['message']
    #         message = 'Please enter your city:'
    #         request.session['prompt'] = 'get_weather'
    #     else:
    #         # Retrieve weather information using the entered country, state, and city
    #         country = request.session['country']
    #         state = request.session['state']
    #         city = request.session['city']
    #         source = urllib.request.urlopen('http://api.weatherstack.com/current?access_key=499926bcaf71ac88510480a752017b9b&query={},{},{}'.format(city, state, country)).read()
    #         list_of_data = json.loads(source)
    #         data = {
    #             "country_code": str(list_of_data['location']['country']),
    #             "city_name": str(list_of_data['location']['name']),
    #             "coordinate": str(list_of_data['location']['lon']) + ', ' + str(list_of_data['location']['lat']),
    #             "temp": str(list_of_data['current']['temperature']) + ' °C',
    #             "pressure": str(list_of_data['current']['pressure']),
    #             "humidity": str(list_of_data['current']['humidity']),
    #         }
    #         # Reset the session variables for the next use
    #         request.session.flush()
    #         message = 'Weather information for {} {}, {}: {}'.format(city, state, country, data)
    #         response = {'message': message}
    #         return JsonResponse(response)

    # # If the request method is not POST or there are no session variables yet, prompt the user for their country
    # if 'chat_log' not in request.session:
    #     request.session['chat_log'] = ''
    # if 'prompt' not in request.session:
    #     request.session['prompt'] = 'country'

    # if request.session['prompt'] == 'country':
    #     response = {'message': 'Welcome to the weather information chatbot! Please enter your country:'}
    # elif request.session['prompt'] == 'state':
    #     request.session['country'] = request.POST['message']
    #     response = {'message': 'Please enter your state:'}
    # elif request.session['prompt'] == 'city':
    #     request.session['state'] = request.POST['message']
    #     response = {'message': 'Please enter your city:'}

    # print(request.POST['message'],"HERE")

    # # Append the new message to the existing content of the chat log
    # request.session['chat_log'] += "hh"
    # # request.session['chat_log'] += 'Bot: ' + response['message'] + '\n'

    # response = {"test":"k"}

    # return JsonResponse(response)



