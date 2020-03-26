#!/usr/bin/env python
# coding: utf-8
'''
covic19.py is a program written by Dr.Monchai Sopitkamon, a lecturer affiliated with the
 Computer Engineering Department, Kasetsart University, Bangkok. This program is written 
 to demonstrate the concepts of subroutine, list, array, and basic visualization as 
 taught in 01204111 Computers and Programming class during the second semester of 2019.
 Thanks to data from The Center for Systems Science and Engineering (CSSE) at Johns 
 Hopkins University and repository site at gitbub.com.
My contact email is monchai.so@ku.th. Any comments/feedbacks are much welcome. Thanks!
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.image as image
from urllib.request import urlopen
from datetime import datetime
np.seterr(divide='ignore', invalid='ignore')
with cbook.get_sample_data('copyright2.png') as imgfile:
    img = image.imread(imgfile)

file_path='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

#file_confirmed='time_series_19-covid-Confirmed.csv' #previously used file
file_confirmed='time_series_covid19_confirmed_global.csv' #newly released file
#file_deaths='time_series_19-covid-Deaths.csv' #previously used file
file_deaths='time_series_covid19_deaths_global.csv' #newly released file
file_recovered='time_series_covid19_recovered_global.csv'

    
confirmed_lines=[]
deaths_lines=[]
recovered_lines=[]
dates_List=[]
got_data_Confirmed = False
got_data_Active = False
got_data_Deaths = False
got_data_Recovered = False
printed_Dates = False

def get_Data_List(file_Name):
    file_List=[]; data=''
    print(f'Retrieving {file_Name} from web site...')
    data = urlopen(file_path+file_Name).read().decode('utf-8')
    data=data.splitlines()
    data=[x.split(',') for x in data]
    file_List = data
    return file_List

def get_Dates(file_List):
    dates=np.array(range(1,len(file_List[0])-3)) 
    return dates

def get_Index_by_Country(file,country):
    for i in range(len(file)):
        if file[i][1]==country:
            #print(f'index = {i}')
            return i
    print(f"Error can't find {country}")
    return -1

def several_country_entries(xList,country):
    count=0
    for i in range(len(xList)):
        if xList[i][1]==country:
            count+=1
    if count>1:
        return True

def get_Data_by_Country(fileList,country):
    country_List=[]
    if several_country_entries(fileList,country)==True: #check if country having multiple lines?
        for j in range(4,len(fileList[0])):
            temp=0
            for i in range(1,len(fileList)):
                if fileList[i][1]==country: #find just matching country
                    #print(f'file[{i}][{j}]: {fileList[i][j]}')
                    if fileList[i][j]!='':
                        temp += int(fileList[i][j])
                    else:
                        temp=0
            country_List.append(temp)
            temp=0
    else: #only country with single line
        index=get_Index_by_Country(fileList,country)
        if index!=-1:
            country_List=fileList[index][4:]
            country_List = [int(x) for x in country_List if x!='']
    data_Array=np.array(country_List)
    return data_Array

def gen_New_Cases_by_Country(file):
    #Th_Confirmed_List=[int(x) for x in Th_Confirmed_List]
    Country_New_Cases_List=[]
    for i in range(len(file)):
        if i<len(file)-1:
            new_cases=file[i+1]-file[i]
            Country_New_Cases_List.append(new_cases)
    Country_New_Cases = np.array(Country_New_Cases_List)
    return Country_New_Cases
            
def gen_Active_Data_by_Country(confirmed,deaths,recovered):
    if len(confirmed)==len(deaths) and len(confirmed)==len(recovered):
        Active = confirmed-deaths-recovered
        return Active
    else:
        confirmed=confirmed[0:len(confirmed)-1]
        deaths=deaths[0:len(deaths)-1]
        Active = confirmed-deaths-recovered
        
    return Active
        
def gen_Deaths_to_Confirmed_by_Country(deaths,confirmed):
    Deaths_to_Confirmed = deaths/confirmed
    return Deaths_to_Confirmed

def plot(dates,title, lgscale,*countries):
    fig, ax = plt.subplots(figsize=(7,4))
    fig.figimage(img, 40, 130, zorder=10, alpha=0.6,resize=False)
    now=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    fig.text(0.95, 0.05, now, fontfamily='monospace',
         fontsize=8, color='gray',
         ha='right', va='top', alpha=0.8)
    #if title=='# of New Cases':
    n = len(countries)//2
    if len(dates)!=len(countries[-1]):
            dates=dates[:-1] #taking the last element out
    for i in range(n):
        plt.plot(dates,countries[n+i],label=f'{countries[i]}')
    if lgscale == True:
        plt.yscale('log')
    plt.xlabel('day')
    plt.title(title,fontsize=12,fontweight='bold',loc='right')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=2, borderaxespad=0.)
    plt.grid()
    plt.show()
    
def print_Dates(dates,confirmed_lines):
    #confirmed_lines_List=confirmed_lines.splitlines()
    #confirmed_lines_List=confirmed_lines.split(',')
    print('\nDates:')
    for i in range(4,len(dates)+4):
        print(f'{confirmed_lines[i]} ', end='')
            
def showtable(dates,title, *countries):
    global printed_Dates
    if not printed_Dates:
        #print('Printing Dates')
        print_Dates(dates,confirmed_lines)
        printed_Dates=True
    n = len(countries)//2
    for i in range(n):
        #print('Printing Data')
        print(f'\n\n{countries[i]} {title} Cases')
        j = n+i
        print(f'{countries[j]} ', end='')
    print()

#main routine
confirmed_lines=get_Data_List(file_confirmed)
deaths_lines=get_Data_List(file_deaths)
recovered_lines=get_Data_List(file_recovered)

dates = get_Dates(confirmed_lines)


Ch_Confirmed = get_Data_by_Country(confirmed_lines,'China')
Th_Confirmed = get_Data_by_Country(confirmed_lines,'Thailand')
US_Confirmed = get_Data_by_Country(confirmed_lines,'US')
It_Confirmed = get_Data_by_Country(confirmed_lines,'Italy')
Gr_Confirmed = get_Data_by_Country(confirmed_lines,'Germany')
Sp_Confirmed = get_Data_by_Country(confirmed_lines,'Spain')
Jp_Confirmed = get_Data_by_Country(confirmed_lines,'Japan')
Sg_Confirmed = get_Data_by_Country(confirmed_lines,'Singapore')
Ta_Confirmed = get_Data_by_Country(confirmed_lines,'Taiwan*')

Ch_New_Cases = gen_New_Cases_by_Country(Ch_Confirmed)
Th_New_Cases = gen_New_Cases_by_Country(Th_Confirmed)
US_New_Cases = gen_New_Cases_by_Country(US_Confirmed)
It_New_Cases = gen_New_Cases_by_Country(It_Confirmed)
Gr_New_Cases = gen_New_Cases_by_Country(Gr_Confirmed)
Sp_New_Cases = gen_New_Cases_by_Country(Sp_Confirmed)
Jp_New_Cases = gen_New_Cases_by_Country(Jp_Confirmed)
Sg_New_Cases = gen_New_Cases_by_Country(Sg_Confirmed)
Ta_New_Cases = gen_New_Cases_by_Country(Ta_Confirmed)

Ch_Deaths = get_Data_by_Country(deaths_lines,'China')
Th_Deaths = get_Data_by_Country(deaths_lines,'Thailand')
US_Deaths = get_Data_by_Country(deaths_lines,'US')
It_Deaths = get_Data_by_Country(deaths_lines,'Italy')
Gr_Deaths = get_Data_by_Country(deaths_lines,'Germany')
Sp_Deaths = get_Data_by_Country(deaths_lines,'Spain')
Jp_Deaths = get_Data_by_Country(deaths_lines,'Japan')
Sg_Deaths = get_Data_by_Country(deaths_lines,'Singapore')
Ta_Deaths = get_Data_by_Country(deaths_lines,'Taiwan*')

Ch_New_Deaths = gen_New_Cases_by_Country(Ch_Deaths)
Th_New_Deaths = gen_New_Cases_by_Country(Th_Deaths)
US_New_Deaths = gen_New_Cases_by_Country(US_Deaths)
It_New_Deaths = gen_New_Cases_by_Country(It_Deaths)
Gr_New_Deaths = gen_New_Cases_by_Country(Gr_Deaths)
Sp_New_Deaths = gen_New_Cases_by_Country(Sp_Deaths)
Jp_New_Deaths = gen_New_Cases_by_Country(Jp_Deaths)
Sg_New_Deaths = gen_New_Cases_by_Country(Sg_Deaths)
Ta_New_Deaths = gen_New_Cases_by_Country(Ta_Deaths)

Ch_Recovered = get_Data_by_Country(recovered_lines,'China')
Th_Recovered = get_Data_by_Country(recovered_lines,'Thailand')
US_Recovered = get_Data_by_Country(recovered_lines,'US')
It_Recovered = get_Data_by_Country(recovered_lines,'Italy')
Gr_Recovered = get_Data_by_Country(recovered_lines,'Germany')
Sp_Recovered = get_Data_by_Country(recovered_lines,'Spain')
Jp_Recovered = get_Data_by_Country(recovered_lines,'Japan')
Sg_Recovered = get_Data_by_Country(recovered_lines,'Singapore')
Ta_Recovered = get_Data_by_Country(recovered_lines,'Taiwan*')

Ch_Deaths_to_Confirmed = gen_Deaths_to_Confirmed_by_Country(Ch_Deaths,Ch_Confirmed)
Th_Deaths_to_Confirmed = gen_Deaths_to_Confirmed_by_Country(Th_Deaths,Th_Confirmed)
US_Deaths_to_Confirmed = gen_Deaths_to_Confirmed_by_Country(US_Deaths,US_Confirmed)
It_Deaths_to_Confirmed = gen_Deaths_to_Confirmed_by_Country(It_Deaths,It_Confirmed)
Gr_Deaths_to_Confirmed = gen_Deaths_to_Confirmed_by_Country(Gr_Deaths,Gr_Confirmed)
Sp_Deaths_to_Confirmed = gen_Deaths_to_Confirmed_by_Country(Sp_Deaths,Sp_Confirmed)
Jp_Deaths_to_Confirmed = gen_Deaths_to_Confirmed_by_Country(Jp_Deaths,Jp_Confirmed)
Sg_Deaths_to_Confirmed = gen_Deaths_to_Confirmed_by_Country(Sg_Deaths,Sg_Confirmed)
Ta_Deaths_to_Confirmed = gen_Deaths_to_Confirmed_by_Country(Ta_Deaths,Ta_Confirmed)


Ch_Active = gen_Active_Data_by_Country(Ch_Confirmed,Ch_Deaths,Ch_Recovered)
Th_Active = gen_Active_Data_by_Country(Th_Confirmed,Th_Deaths,Th_Recovered)
US_Active = gen_Active_Data_by_Country(US_Confirmed,US_Deaths,US_Recovered)
It_Active = gen_Active_Data_by_Country(It_Confirmed,It_Deaths,It_Recovered)
Gr_Active = gen_Active_Data_by_Country(Gr_Confirmed,Gr_Deaths,Gr_Recovered)
Sp_Active = gen_Active_Data_by_Country(Sp_Confirmed,Sp_Deaths,Sp_Recovered)
Jp_Active = gen_Active_Data_by_Country(Jp_Confirmed,Jp_Deaths,Jp_Recovered)
Sg_Active = gen_Active_Data_by_Country(Sg_Confirmed,Sg_Deaths,Sg_Recovered)
Ta_Active = gen_Active_Data_by_Country(Ta_Confirmed,Ta_Deaths,Ta_Recovered)

if len(Th_Confirmed)==len(Th_Recovered):
    Ch_Recovered_to_Confirmed = Ch_Recovered/Ch_Confirmed
    Th_Recovered_to_Confirmed = Th_Recovered/Th_Confirmed
    US_Recovered_to_Confirmed = US_Recovered/US_Confirmed
    It_Recovered_to_Confirmed = It_Recovered/It_Confirmed
    Gr_Recovered_to_Confirmed = Gr_Recovered/Gr_Confirmed
    Sp_Recovered_to_Confirmed = Sp_Recovered/Sp_Confirmed
    Jp_Recovered_to_Confirmed = Jp_Recovered/Jp_Confirmed
    Sg_Recovered_to_Confirmed = Sg_Recovered/Sg_Confirmed
    Ta_Recovered_to_Confirmed = Ta_Recovered/Ta_Confirmed
else:
    Ch_Recovered_to_Confirmed = Ch_Recovered/Ch_Confirmed[0:len(Th_Confirmed)-1]
    Th_Recovered_to_Confirmed = Th_Recovered/Th_Confirmed[0:len(Th_Confirmed)-1]
    US_Recovered_to_Confirmed = US_Recovered/US_Confirmed[0:len(US_Confirmed)-1]
    It_Recovered_to_Confirmed = It_Recovered/It_Confirmed[0:len(It_Confirmed)-1]
    Gr_Recovered_to_Confirmed = Gr_Recovered/Gr_Confirmed[0:len(Gr_Confirmed)-1]
    Sp_Recovered_to_Confirmed = Sp_Recovered/Sp_Confirmed[0:len(Sp_Confirmed)-1]
    Jp_Recovered_to_Confirmed = Jp_Recovered/Jp_Confirmed[0:len(Jp_Confirmed)-1]
    Sg_Recovered_to_Confirmed = Sg_Recovered/Sg_Confirmed[0:len(Sp_Confirmed)-1]
    Ta_Recovered_to_Confirmed = Ta_Recovered/Ta_Confirmed[0:len(Sp_Confirmed)-1]
    
showtable(dates, 'Confirmed', *('Thailand','China','US','Italy','Germany','Spain',\
    'Japan','Singapore','Taiwan',Th_Confirmed,Ch_Confirmed,US_Confirmed,It_Confirmed,\
    Gr_Confirmed,Sp_Confirmed,Jp_Confirmed,Sg_Confirmed),Ta_Confirmed)

showtable(dates, 'New', *('Thailand','China','US','Italy','Germany','Spain',\
    'Japan','Singapore','Taiwan',Th_New_Cases,Ch_New_Cases,US_New_Cases,\
    It_New_Cases,Gr_New_Cases,Sp_New_Cases,Jp_New_Cases,Sg_New_Cases,Ta_New_Cases))

showtable(dates, 'Active', *('Thailand','China','US','Italy','Germany','Spain',\
    'Japan','Singapore','Taiwan',Th_Active,Ch_Active,US_Active,It_Active,\
    Gr_Active,Sp_Active,Jp_Active,Sg_Active,Ta_Active))

showtable(dates, 'Deaths', *('Thailand','China','US','Italy','Germany','Spain',\
    'Japan','Singapore','Taiwan',Th_Deaths,Ch_Deaths,US_Deaths,It_Deaths,\
    Gr_Deaths,Sp_Deaths,Jp_Deaths,Sg_Deaths,Ta_Deaths))

showtable(dates, 'Recovered', *('Thailand','US','Italy','Germany','Spain','Japan','Singapore', \
          Th_Recovered,US_Recovered,It_Recovered,Gr_Recovered,Sp_Recovered,Jp_Recovered,Sg_Recovered))

showtable(dates, 'Deaths to Confirmed', *('Thailand','US','Italy','Japan','Singapore', \
          Th_Deaths_to_Confirmed,US_Deaths_to_Confirmed,It_Deaths_to_Confirmed,\
              Jp_Deaths_to_Confirmed,Sg_Deaths_to_Confirmed))

showtable(dates, 'Recovered to Confirmed', \
          *('Thailand','China','US','Italy','Germany','Spain','Japan','Singapore', \
          Th_Recovered_to_Confirmed,Ch_Recovered_to_Confirmed,US_Recovered_to_Confirmed,It_Recovered_to_Confirmed,\
              Gr_Recovered_to_Confirmed,Sp_Recovered_to_Confirmed,Jp_Recovered_to_Confirmed,Sg_Recovered_to_Confirmed))

plot(dates,'# of Confirmed Cases',True,*('Thailand','China','US','Italy',\
        'Germany','Spain','Japan','Singapore','Taiwan', \
        Th_Confirmed,Ch_Confirmed,US_Confirmed,It_Confirmed,Gr_Confirmed,\
        Sp_Confirmed,Jp_Confirmed,Sg_Confirmed,Ta_Confirmed))

plot(dates,'# of New Cases',True,*('Thailand','China','US','Italy','Germany',\
        'Spain','Japan','Singapore','Taiwan', \
        Th_New_Cases,Ch_New_Cases,US_New_Cases,It_New_Cases,Gr_New_Cases,\
        Sp_New_Cases,Jp_New_Cases,Sg_New_Cases,Ta_New_Cases))

plot(dates,'# of Active Cases',True,*('Thailand','China','US','Italy','Germany',\
        'Spain','Japan','Singapore','Taiwan', \
        Th_Active,Ch_Active,US_Active,It_Active,Gr_Active,Sp_Active,Jp_Active,\
        Sg_Active,Ta_Active))   
    
plot(dates,'# of Deaths',True,*('Thailand','China','US','Italy','Germany',\
        'Spain','Japan','Singapore','Taiwan', \
        Th_Deaths,Ch_Deaths,US_Deaths,It_Deaths,Gr_Deaths,Sp_Deaths,Jp_Deaths,\
        Sg_Deaths,Ta_Deaths))

plot(dates,'# of New Deaths',True,*('Thailand','China','US','Italy','Germany',\
        'Spain','Japan','Singapore','Taiwan', \
        Th_New_Deaths,Ch_New_Deaths,US_New_Deaths,It_New_Deaths,Gr_New_Deaths,\
        Sp_New_Deaths,Jp_New_Deaths,Sg_New_Deaths,Ta_New_Deaths))
    
plot(dates,'# of Recovered Cases',True,*('Thailand','China','US','Italy','Germany',\
        'Spain','Japan','Singapore','Taiwan', \
        Th_Recovered,Ch_Recovered,US_Recovered,It_Recovered,Gr_Recovered,\
        Sp_Recovered,Jp_Recovered,Sg_Recovered,Ta_Recovered))
    
plot(dates,'Deaths-to-Confirmed Ratios',False,\
    *('Thailand','China','US','Italy','Germany','Spain','Japan','Singapore','Taiwan', \
    Th_Deaths_to_Confirmed,Ch_Deaths_to_Confirmed,US_Deaths_to_Confirmed,\
    It_Deaths_to_Confirmed,Gr_Deaths_to_Confirmed,Sp_Deaths_to_Confirmed,\
    Jp_Deaths_to_Confirmed,Sg_Deaths_to_Confirmed,Ta_Deaths_to_Confirmed))

plot(dates,'Recovered-to-Confirmed Ratios',False,\
    *('Thailand','China','US','Italy','Germany','Spain','Japan','Singapore','Taiwan', \
    Th_Recovered_to_Confirmed,Ch_Recovered_to_Confirmed,US_Recovered_to_Confirmed,\
    It_Recovered_to_Confirmed,Gr_Recovered_to_Confirmed,Sp_Recovered_to_Confirmed,\
    Jp_Recovered_to_Confirmed,Sg_Recovered_to_Confirmed,Ta_Recovered_to_Confirmed))

plot(dates,'China',True,*('Confirmed','New Cases','Active','Deaths','New Deaths',\
    'Recovered','Deaths-to-Confirmed','Recovered-to-Confirmed',Ch_Confirmed[:-1],\
    Ch_New_Cases,Ch_Active,Ch_Deaths[:-1],Ch_New_Deaths,Ch_Recovered,\
    Ch_Deaths_to_Confirmed[:-1],Ch_Recovered_to_Confirmed,Ta_Recovered_to_Confirmed))
    
plot(dates,'Thailand',False,*('Confirmed','New Cases','Active','Deaths','New Deaths',\
                          'Recovered','Deaths-to-Confirmed','Recovered-to-Confirmed',\
                        Th_Confirmed[:-1],Th_New_Cases,Th_Active,Th_Deaths[:-1],Th_New_Deaths,\
                        Th_Recovered,Th_Deaths_to_Confirmed[:-1],Th_Recovered_to_Confirmed))

plot(dates,'US',True,*('Confirmed','New Cases','Active','Deaths','New Deaths',\
                          'Recovered','Deaths-to-Confirmed','Recovered-to-Confirmed',\
                        US_Confirmed[:-1],US_New_Cases,US_Active,US_Deaths[:-1],US_New_Deaths,\
                        US_Recovered,US_Deaths_to_Confirmed[:-1],US_Recovered_to_Confirmed))

plot(dates,'Italy',True,*('Confirmed','New Cases','Active','Deaths','New Deaths',\
                          'Recovered','Deaths-to-Confirmed','Recovered-to-Confirmed',\
                        It_Confirmed[:-1],It_New_Cases,It_Active,US_Deaths[:-1],It_New_Deaths,\
                        It_Recovered,It_Deaths_to_Confirmed[:-1],It_Recovered_to_Confirmed))

plot(dates,'Germany',True,*('Confirmed','New Cases','Active','Deaths','New Deaths',\
                          'Recovered','Deaths-to-Confirmed','Recovered-to-Confirmed',\
                        Gr_Confirmed[:-1],Gr_New_Cases,Gr_Active,Gr_Deaths[:-1],Gr_New_Deaths,\
                        Gr_Recovered,Gr_Deaths_to_Confirmed[:-1],Gr_Recovered_to_Confirmed))

plot(dates,'Spain',True,*('Confirmed','New Cases','Active','Deaths','New Deaths',\
                          'Recovered','Deaths-to-Confirmed','Recovered-to-Confirmed',\
                        Sp_Confirmed[:-1],Sp_New_Cases,Sp_Active,Sp_Deaths[:-1],Sp_New_Deaths,\
                        Sp_Recovered,Sp_Deaths_to_Confirmed[:-1],Sp_Recovered_to_Confirmed))

plot(dates,'Japan',False,*('Confirmed','New Cases','Active','Deaths','New Deaths',\
                          'Recovered','Deaths-to-Confirmed','Recovered-to-Confirmed',\
                        Jp_Confirmed[:-1],Jp_New_Cases,Jp_Active,Jp_Deaths[:-1],Jp_New_Deaths,\
                        Jp_Recovered,Jp_Deaths_to_Confirmed[:-1],Jp_Recovered_to_Confirmed))

plot(dates,'Singapore',False,*('Confirmed','New Cases','Active','Deaths','New Deaths',\
                          'Recovered','Deaths-to-Confirmed','Recovered-to-Confirmed',\
                        Sg_Confirmed[:-1],Sg_New_Cases,Sg_Active,Sg_Deaths[:-1],Sg_New_Deaths,\
                        Sg_Recovered,Sg_Deaths_to_Confirmed[:-1],Sg_Recovered_to_Confirmed))

plot(dates,'Taiwan',False,*('Confirmed','New Cases','Active','Deaths','New Deaths',\
                          'Recovered','Deaths-to-Confirmed','Recovered-to-Confirmed',\
                        Ta_Confirmed[:-1],Ta_New_Cases,Ta_Active,Ta_Deaths[:-1],Ta_New_Deaths,\
                        Ta_Recovered,Ta_Deaths_to_Confirmed[:-1],Ta_Recovered_to_Confirmed))

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

