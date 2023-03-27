import requests
import csv
import datetime as dt
import schedule
from pathlib import Path
import time as tm


fieldnames = ['name', 'description', 'temp', 'tempf', 'humidity', 'visibility', 'windspeed', 'clouds', 'time', 'sunrise', 'sunset']

f = open(Path("location1/coords.txt"), "r")

url1 = "https://api.openweathermap.org/data/2.5/weather?"

api = open(Path("api.txt"), "r").read()
city = "London"
coord1 = [(f.readline()).replace("\n", ""), f.readline()]
coord2 = ["53.588158451515596", "-0.3430739111539013"]
coord3 = ["52.78131814913128", "-1.4026796887844883"]
coord4 = ["52.36503955211087", "-3.3115721290012825"]
coord5 = ["54.35979232999362", "-1.8179171446502072"]

coordlist = [coord1,coord2,coord3,coord4,coord5]

urllist = []

responses = []

for i in range(len(coordlist)):
    url = url1+"lat=" + coordlist[i][0] + "&lon=" + coordlist[i][1] + "&appid=" + api + "&units=metric"

    urllist.append(url)


def job():
    responses=[]
    for url in urllist:
        response1 = requests.get(url).json()

        responses.append(response1)


    for response in responses:
        name=response["name"]
        description = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        tempf = response["main"]["feels_like"]
        humidity = response["main"]["humidity"]
        visibility = response["visibility"]
        windspeed = response["wind"]["speed"]
        clouds = response["clouds"]["all"]
        time = dt.datetime.utcfromtimestamp((response["dt"]+response["timezone"])).strftime('%m-%d-%Y %H:%M')
        sunrise = dt.datetime.utcfromtimestamp(response["sys"]["sunrise"]+response["timezone"]).strftime('%H:%M:%S')
        sunset = dt.datetime.utcfromtimestamp(response["sys"]["sunset"]+response["timezone"]).strftime('%H:%M:%S')

        values = [name, description, temp, tempf, humidity, visibility, windspeed, clouds, time, sunrise, sunset]


        stringe = str(response["coord"]["lon"]) + str(response["coord"]["lat"])

        
        with open("weather"+ str(stringe) +".csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=",")

            res = {fieldnames[i]: values[i] for i in range(len(fieldnames))}

            #writer.writeheader()
            
            writer.writerow(res)

      
    abc = dt.datetime.now()
    abc = abc.strftime('%H:%M:%S')
    print(abc)


schedule.every().hour.at(":00").do(job)
schedule.every().hour.at(":30").do(job)

#job()

while True:
    schedule.run_pending()
    tm.sleep(1)

#print(f"Town name: {name}\nDescription: {description}\nTemperature: {temp}°c\nFeels Like Temperature: {tempf}°c\nHumidity: {humidity}%\n\
#Visibility: {visibility} metres\nWind Speed: {windspeed} m/s\nCloud Percentage: {clouds}%\nTime: {time}\nSunrise: {sunrise}\nSunset: {sunset}")





