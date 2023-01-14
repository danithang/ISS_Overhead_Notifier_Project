import requests
from datetime import datetime
import smtplib
import time

# My latitude
MY_LAT = 37.028271
# My longitude
MY_LONG = -76.342339

my_email = "pythontestberry@gmail.com"
# password from app generator on gmail
password = "dluhzayjhamxzxbj"
other_email = "berrypythontest@yahoo.com"


# function to check if iss position is within range of my current position and if it is then return true
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    # saying if iss latitude and iss longitude is greater than MY_LAT and MY_LONG-5 and less than MY_LAT and
    # MY_LONG +5 then it will show
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


# function determining if it is nighttime then return true
def is_nighttime():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    # getting the sunset and sunrise api data and turning it to a json file and pulling certain results
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    # if the current time is greater than sunset(after sun goes down) or current time is before sunrise then it means
    # it's still dark
    if time_now >= sunset or time_now <= sunrise:
        return True

# putting this in a while loop to check every 60 secs with time.sleep...if the iss is overhead and it is nighttime
# then I will get an email telling me so
while True:
    time.sleep(60)
    if is_iss_overhead() and is_nighttime():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            # start transport layer security to secure the connection to the email server
            connection.starttls()
            # login process
            connection.login(user=my_email, password=password)
            # sending the email from one address to the other with message...adding subject and /n to make
            # sure it doesn't go into spam box
            connection.sendmail(from_addr=my_email, to_addrs=other_email,
                                msg=f"Subject:Look Up!\n\nThe ISS is above you right now!")
