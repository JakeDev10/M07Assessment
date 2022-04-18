import datetime as dt
import json
from unicodedata import name
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import calendar

class Holiday:

    def __init__(self, name, date):
        self.name = name
        self.date = date            #I assume this is a date object
    
    def __str__(self):
        return f"{self.name} ({self.date})"

    def getValues(self):
        returnList = [self.name, self.date]
        return returnList

class HolidayList:                  #controller/wrapper

    def __init__(self):
        self.innerHolidays = []
        self.unsavedStuff = True        #this is used to see if there are changes to be saved
    
    def unsavedChanges(self):               #returns true if unsaved changes, else false
        if self.unsavedStuff == True:
            return True
        else:
            return False

    def makeDate(self, date, year):   #gets input in format 'Jan 1', 2022 and returns date object
        dateStr = date.split(" ")
        monthNum = list(calendar.month_abbr).index(dateStr[0])  #converts 'Apr' to 4
        day = int(dateStr[1])
        dateObject = dt.date(int(year), monthNum, day)
        return dateObject
    
    def getDateInput(self):     #get date input, return datetime object
        while 1:                #keep going until valid input is recieved
            userInput = input("Enter a date [YYYY-MM-DD]: ")
            try:
                inputList = [int(x) for x in list(userInput.split("-"))]
                myDate = dt.date(inputList[0], inputList[1], inputList[2])
                return myDate
            except:
                print("Invalid input, please try again")
    
    def getWeekInput(self):     #get week input in range 1-53, return integer (0 for current week)
        while 1:
            week = input("What week? #[1-53, leave blank for current week]: ")
            if week == '':
                return 0
            else:
                try:
                    week = int(week)
                    if week in range(1,54):
                        return week
                    else:
                        print("Week out of range.")
                except:
                    print("Invalid input, integers only.")

    def getYearInput(self):     #get year input in range 2020-2024, return integer
        while 1:
            year = input("What year? [2020-2024]:")
            try:
                year = int(year)
            except:
                print("Invalid input, year must be an integer")
            else:
                if year in range(2020,2025):
                    return year
                else:
                    print("Invalid year, format must be YYYY in range 2020-2024")
    
    def getBoolInput(self):     #get y/n response
        while 1:
            choice = input("[y/n] ")
            if choice == 'y' or choice == 'n':
                return choice
            else:
                print("Invalid input, 'y' or 'n' only.")

    def mainMenu(self):     #print main menu, get valid user input
        print('''
Holiday Menu
============
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit
        ''')
        while 1:        #keep going until valid input is recieved
            try:
                userInput = int(input("What would you like to do? [1-5] "))
                if userInput in range(1,6):
                    return userInput
                else:
                    print("That number is out of range")
            except:
                print("Invalid input, please enter an integer")

    def addHoliday(self, holidayObj):
        if type(holidayObj) == Holiday:         # Make sure holidayObj is an Holiday Object by checking the type
            self.innerHolidays.append(holidayObj)
            print(f"{holidayObj} was successfully added")
            self.unsavedStuff = True
        else:
            print("Error, holiday not added, that wasn't a holiday object")   #Used for debugging

    def removeHoliday(self, HolidayName, Date):
        myHoliday = Holiday(HolidayName, Date)
        deleteSuccess = False

        for x in self.innerHolidays:
            if vars(x) == vars(myHoliday):      #remove holiday from list if date and name match input
                self.innerHolidays.remove(x)
                print("Holiday successfully removed")
                deleteSuccess = True
                self.unsavedStuff = True
        
        if not deleteSuccess:
            print("That holiday wasn't in the list.")

    def readJson(self, filelocation):           #read in json from file, populate innerHolidays
        with open(filelocation, 'r') as file:
            dict = json.load(file)
        dictList = dict['holidays']
        for holiday in dictList:
            strDate = holiday['date'].split('-')
            intDate = [int(x) for x in strDate]
            dateObj = dt.date(intDate[0], intDate[1], intDate[2])
            self.innerHolidays.append(Holiday(holiday['name'], dateObj))    #I didn't use addHoliday method because of "You added x holiday" spam

    def saveJson(self, filelocation):           #write json to filelocation
        file = open(filelocation, 'w')
        aList = []
        dictionary = {'holidays': aList}
        for x in self.innerHolidays:
            nameDate = x.getValues()
            aList.append({'name': nameDate[0], 'date': str(nameDate[1])})
        json.dump(dictionary, file, indent = 4)
        file.close()
        print("Success, your changes were saved to myHolidays.json")
        self.unsavedStuff = False
        
    def scrapeHolidays(self):
        years = [2020, 2021, 2022, 2023, 2024]
        for year in years:
            html = requests.get(f"https://www.timeanddate.com/holidays/us/{year}?hol=33554809")
            soup = BeautifulSoup(html.text, 'html.parser')
            table = soup.find('tbody')
            rows = table.find_all(attrs = {'class':'showrow'})
            
            for row in rows:
                date = self.makeDate(row.find('th').text, year)
                name = row.find('a').text
                aHoliday = Holiday(name, date)
                self.innerHolidays.append(aHoliday)

    def numHolidays(self):
        print('''
Holiday Management
==================
        ''')
        print(f"The number of holidays in the system is {len(self.innerHolidays)}.")
        
    
    def filterHolidaysByWeek(self, year, week_number):
        filteredList = list(filter(lambda x: x.getValues()[1].isocalendar()[1] == week_number 
            and x.getValues()[1].isocalendar()[0] == year, self.innerHolidays))

        return filteredList

    def displayHolidaysInWeek(self, holidayList):
        for x in holidayList:
            print(x)

    #The free option for this API only gives weather for the next 5 days,
    #and I'm assuming we're not interested in weather for previous days
    #based on the assignment saying this function is for planning purposes.
    def getWeather(self):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast"
        querystring = {"q":"minneapolis,us"}
        headers = {
	        "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
	        "X-RapidAPI-Key": "032495499cmsh87a7f851860036ap143e00jsn16c55b0cdc5f"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()

        weatherList = []
        for i in range(5):
            weatherList.append(data['list'][8*i]['weather'][0]['description'])    #gives weather for the next 5 days
        
        return weatherList


    def viewCurrentWeek(self):
        now = dt.datetime.now()
        weekNum = now.isocalendar()[1]
        year = now.year
        day = now.day
        validInput = 0
        filteredList = self.filterHolidaysByWeek(year, weekNum)

        
        print("Would you like to see the weather?")
        response = self.getBoolInput()
        if response == 'n':
            self.displayHolidaysInWeek(filteredList)
        else:
            weatherList = self.getWeather()     #weather from today for 5 days
            for x in filteredList:
                if x.getValues()[1].day in range(day, day+5):
                    print(f"{x} {weatherList[x.getValues()[1].day - day]}")   #calculates index for weatherList
                else:
                    print(x)

def main():
    quitProgram = False

    myList = HolidayList()
    myList.readJson("holidays.json")
    myList.scrapeHolidays()
    myList.numHolidays()
    
    while not quitProgram:
        userInput = myList.mainMenu()
        validInput = 0

        if userInput == 1:
            print('''
Adding Holiday
==============''')
            name = input("What is the Holiday called? ")
            date = myList.getDateInput()
            myList.addHoliday(Holiday(name, date))

        elif userInput == 2:
            print('''
Remove a Holiday
================''')
            name = input("What is the Holiday called? ")
            date = myList.getDateInput()
            myList.removeHoliday(name, date)

        elif userInput == 3:
            print('''
Saving Holiday List
===================''')
            print("Are you sure you want to save your changes?")
            choice = myList.getBoolInput()
            if choice == 'y':
                myList.saveJson('myHolidays.json')
            else:
                print("Saving cancelled.")

        elif userInput == 4:
            print('''
View Holidays
=============''')
            year = myList.getYearInput()
            weekNum = myList.getWeekInput()
            now = dt.datetime.now()
            if weekNum == 0:            #This means the user left week input blank
                weekNum = now.isocalendar()[1]
            if weekNum == now.isocalendar()[1] and year == now.year:
                myList.viewCurrentWeek()
            else:
                tempList = myList.filterHolidaysByWeek(year, weekNum)
                myList.displayHolidaysInWeek(tempList)

        else:
            print("""
Exit
====""")
            if myList.unsavedChanges():
                print("Are you sure you want to exit? You have unsaved changes.")
                choice = myList.getBoolInput()
                if choice == 'y':
                    print("Goodbye!")
                    quitProgram = True
            else:
                print("Are you sure you want to exit?")
                choice = myList.getBoolInput()
                if choice == 'y':
                    print("Goodbye!")
                    quitProgram = True


main()