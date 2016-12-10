# -*- coding: UTF-8 -*- 
import csv
import requests, json

api = 'AIzaSyAfUUFjCsoPzW9nqx5H8Qus-eqPvo2CA7o'


url = 'https://maps.googleapis.com/maps/api/geocode/json?address="'
url2 = '"&key=' + str(api)


r =  ""
final = []
with open('latlong.csv' ,'rb') as f:    
    csvw = csv.reader(f)
    
    for i in csvw:
         
        try:
            r = requests.get(url + i[1].replace(" ","+")+"+"+i[2]+",+"+i[3] + url2)
            final.append(i + [r.json()['results'][0]['geometry']['location']['lat'],r.json()['results'][0]['geometry']['location']['lng']])
        except Exception as e:
            print e, i

with open('missed.csv','wb') as f:
    csvw = csv.writer(f)

    csvw.writerows(final)
        
        
    
    
    