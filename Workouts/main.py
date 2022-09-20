import requests
from datetime import datetime
import os

# Nutrix
nutri_headers = {
    "x-app-id": "213462c2",
    "x-app-key": "9ebc3a2cdf4a69833f5af9cb89159044",
}
user_input = input("Which exercise did you do today, and for how long? \n")
exercise_params = {
    "query": user_input,
    "gender": "male",
    "weight_kg": 55,
    "height_cm": 167,
    "age": 33
}
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_response = requests.post(url=exercise_endpoint, json=exercise_params, headers=nutri_headers)
print(exercise_response.json())
json_response = exercise_response.json()


# Sheety
username = "ABC"
password = "123"
today_date = datetime.now().date().strftime("%d/%m/%Y")
time_now = datetime.now().time().strftime("%I:%M:%S %p")
new_exercise = {
    "workout": {
        "date": today_date,
        "time": time_now,
        "exercise": json_response['exercises'][0]['user_input'].title(),
        "duration": json_response['exercises'][0]['duration_min'],
        "calories": json_response['exercises'][0]['nf_calories'],
    }
}
headers = (username, password)
sheety_endpoint = "https://api.sheety.co/75cbb32bf67ecf85caa147710ebffa86/workoutTracking/workouts"
sheety_response = requests.post(url=sheety_endpoint, json=new_exercise, auth=headers)
print(sheety_response.json())
