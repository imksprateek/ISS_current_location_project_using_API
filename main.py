import requests
import datetime
import smtplib
import time

def iss_is_near():
    global MY_LAT, MY_LONG, iss_longitude, iss_latitude
    if iss_latitude>MY_LAT-5 and iss_latitude<MY_LAT+5 and iss_longitude>MY_LONG-5 and iss_latitude<MY_LONG+5:
        return True
    else:
        return False

#CONSTANTS
MY_LAT = 13.100370
MY_LONG = 77.596268

#ISS
iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_response.raise_for_status()
iss_longitude = float(iss_response.json()["iss_position"]["longitude"])
iss_latitude = float(iss_response.json()["iss_position"]["latitude"])
iss_position = (iss_latitude, iss_longitude)

#SUN
parameters = {
    "lat":MY_LAT,
    "lng":MY_LONG,
    "formatted": 0
}
sun_response = requests.get(url=" https://api.sunrise-sunset.org/json", params=parameters)
sun_response.raise_for_status()
data = sun_response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.datetime.now().time().hour

while True:
    time.sleep(60)
    if iss_is_near() and time_now>sunset and time_now < sunrise:
        connection = smtplib.SMTP()
        connection.starttls()
        with open("credentials.txt") as credential_file:
            content = credential_file.readlines()
            user_id = content[0][:-1]
            user_password = content[1]
        connection.login(user=user_id, password=user_password)
        connection.sendmail(from_addr=user_id, to_addrs="ksprateek7@yahoo.com", msg="Subject:Look Up👆 \n\nISS is visible in the sky right now. Look Up!")

    else:
        pass