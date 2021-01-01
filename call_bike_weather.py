# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 14:28:08 2020

@author: hanna
"""
import time
import datetime
import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account


## Big IoT


# lat and long for each weather zone 
w_list = [[51.46,-0.10],[51.46,-0.15],[51.46,-0.20],[51.48,-0.00],[51.48,-0.10],
          [51.48,-0.15],[51.48,-0.20],[51.48,-0.25],[51.50,-0.00],[51.50,-0.05],
          [51.50,-0.10],[51.50,-0.15],[51.50,-0.20],[51.50,-0.25],[51.52,-0.00],
          [51.52,-0.05],[51.52,-0.10],[51.52,-0.15],[51.52,-0.20],[51.52,-0.25], 
          [51.54,-0.00],[51.54,-0.05],[51.54,-0.10],[51.54,-0.15],[51.54,-0.20]]

timeout = time.time() + 60 * 60 * 24 * 10 #running for 10 days worth of data collection


def main():
    count = 0
    while True:
        if time.time() > timeout: #if it goes beyond this 10 day time, break the while true loop
            break
        elif time.time() < timeout: 
            count = count+1
            print (count)
            #every loop
            start = time.time()
            now = datetime.datetime.now()
            print ('Calling APIs...')
            
            #get data using API
            #My_key = 'e2f4519ee0864e1dabb44966c68e28fc'
            r = requests.get('https://api.tfl.gov.uk/BikePoint')
            b_data = r.json()
            print ('Bike Data Received...')
            
            w_data = []
            for i in w_list:
                lat = i[0]
                lon = i[1]
                        
                my_key = '755c70082a775db26c20327b0310c542' # API Key for OpenWeatherMap
                r = requests.get('http://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid='+str(my_key)+'&units=metric')
                temp_data = r.json()
                w_data.append(temp_data)
            
            print ('Weather Data Received...')    
            #sort data
            
            time_row = [now.strftime("%m/%d/%Y"),now.strftime("%H:%M:%S")]
            bike_list = []
            empty_list = []
            weather_list = []
            wind_list = []
            temp_list = []
            feels_list = []
            visibility_list = []
            humidity_list = []
            
        
            for i in range (790):
                bike_list.append(b_data[i]['additionalProperties'][6]['value'])
                empty_list.append(b_data[i]['additionalProperties'][7]['value'])
            
            for i in range(25):
                weather_list.append(w_data[i]['weather'][0]['description'])
                wind_list.append(w_data[i]['wind']['speed'])
                temp_list.append(w_data[i]['main']['temp'])
                feels_list.append(w_data[i]['main']['feels_like'])
                visibility_list.append(w_data[i]['visibility'])
                humidity_list.append(w_data[i]['main']['humidity']) 
               
            print ('Data in list from...') 
            
            main_list = time_row + bike_list + empty_list + weather_list + wind_list + temp_list + feels_list + visibility_list + humidity_list
            print (main_list)
            print ('add [] for some reason so it runs...')
            
            main_list = [main_list]
            
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            SERVICE_ACCOUNT_FILE = 'client_secret.json'
            credentials = None
            credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            sheet_id = '1MTQkEZ0E7yrDvRC4wEic582OWDqVriE5qxww9LU5FdQ'
            service = build('sheets', 'v4', credentials=credentials)
            sheet = service.spreadsheets()
            print ('Opened workbook...') 
            
            print (time_row)
            request_instance = sheet.values().append(spreadsheetId=sheet_id, 
                                range="Instance!A2", valueInputOption="RAW",
                                insertDataOption="INSERT_ROWS", body={"values":main_list}) 
            
            
            
            request_instance.execute()
            
        
            print ('Done...') 
            timer = time.time() - start
            print(timer)
            time.sleep(300-round(timer)) 
            
            
main()
