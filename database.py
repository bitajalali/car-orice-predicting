import re
import requests
from bs4 import BeautifulSoup
import numpy as np
import mysql.connector
import re
import time
session = requests.Session()
session.proxies = {
   'http': 'http://10.10.10.10:8000',
   'https': 'http://10.10.10.10:8000',
}




cnx=mysql.connector.connect(user='bita',password='******',host='127.0.0.1')
mycursor=cnx.cursor(buffered=True)
carname=input('insert model: ')

table_name=str(carname)+'_table'

mycursor.execute('SHOW DATABASES')
output=mycursor.fetchall()
print(output)
mycursor.execute('USE cardatabase1')

mycursor.execute("create table if not exists %s (model_names varchar(255) ,prices varchar(255) ,miles varchar(255) ,years varchar(255))" % table_name)
mycursor.execute('show tables')


pattern=str(carname)+'/'
headers = {"Content-Type": "application/json; charset=utf-8"}
proxies = {
  'http': '10.10.10.10:3128',
  'https': '10.10.10.10:3128',
}
#headers=headers,proxies
#/?page=7
#Honda Civic

model_lists=[]
prices=[]
miles=[]
years=[]
for t in range(301,333):
    time.sleep(5)
    print(t)
    #response = session.get('https://www.truecar.com/used-cars-for-sale/listings/'+str(pattern)+'?page='+str(t))
    response=requests.get('https://www.truecar.com/used-cars-for-sale/listings/'+str(pattern)+'?page='+str(t),proxies,verify=False)
    print(response.status_code)
    soup=BeautifulSoup(response.text,'html.parser')

    y=soup.findAll('span',{'class':"vehicle-card-year text-xs"})

    p=soup.findAll('div',{'data-test':"vehicleCardPricingBlockPrice"})
    for item in p:
       new_string = re.sub(r"\$", "", item.text)
       prices.append(new_string)


    m=soup.findAll('div',{'data-test':"vehicleMileage"})
    for item in y:

        years.append(item.text)
    for item in m:

        new_string = re.sub(r"miles", "", item.text)

        miles.append(new_string)

    first=soup.findAll('div',{'data-test':"vehicleCardYearMakeModel"})
    for item in first:

        for i in item.findAll('span',{'class':"truncate"}):
            # if (i.text==specific_model):
            #     print(i.text)

            model_lists.append((i.text))


for i in range(len(years)):
    mycursor.execute('insert into %s values (\'%s\',\'%s\',\'%s\',\'%s\')' % (table_name, model_lists[i], prices[i], miles[i], years[i]))


cnx.commit()
cnx.close()
