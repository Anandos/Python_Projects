import time
import requests
import datetime
import config
import smtplib

# get lat long from iss
# get sunrisesunset from api
# work out if night or day
# is night find out if iss is above, within 5 degrees
# send email if true

# API's have required and optional parameters, like arguments for functions/objects
def iss_near():
    # ISS
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(f"ISS lat, long: {iss_latitude}, {iss_longitude}\n")

    if 15 >= iss_latitude - config.MY_LAT >= -15:
        if 15 >= iss_longitude - config.MY_LONG >= -15:
            print("The ISS is flying past now!")
            return True

    print("The ISS is somewhere else on the planet")
    return False

def is_night():
    parameters = {
        "lat": config.MY_LAT,
        "lng": config.MY_LONG,
        "formatted": config.FORMAT, }

    # Sunrise Sunset
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Time
    time_now = int(str(datetime.datetime.now()).split(" ")[1].split(":")[0])
    print("\nTime is: " + str(datetime.datetime.now().time()).split(".")[0] +
          ", sunrise is: " + data["results"]["sunrise"].split("T")[1].split("+")[0] +
          ", sunset is: " + data["results"]["sunset"].split("T")[1].split("+")[0]
          )

    if time_now <= sunrise or time_now >= sunset:
        print("It's night time")
        return True
    else:
        print("It's still day time")
        return False


while True:
    if is_night():
        if iss_near():
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=config.EMAIL, password=config.PASSWORD)
                connection.sendmail(from_addr=config.EMAIL, to_addrs=config.TO_EMAIL, msg=config.MSG)
            pass

    time.sleep(60)
