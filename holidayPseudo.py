import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import calendar

class Holiday:
      
    def __init__(self,name, date):
        #Your Code Here        
    
    def __str__ (self):
        # String output
        # Holiday output when printed.

    def getValues(self):
        #returns name and date obj
          

class HolidayList:
    def __init__(self):
       self.innerHolidays = []
    
    def unsavedChanges():
        #return true or false based on if there are unsaved changes

    def makeDate():
        #take abbreviated date format ex. ('Jan 1' 2022) and return date object
        #use calendar's built in list of abbreviated months for conversion

    def getDateInput():
        #get input for date in format YYYY-MM-DD
        #validate input, reprompt as needed
        #return datetime object
    
    def getWeekInput():
        #get input for week number
        #validate, reprompt
        #return int (0 for current week)

    def getYearInput():
        #get input for year number
        #check that it's an int and in range
        #return int
    
    def getBoolInput():
        #get y/n input
        #validate
        #return 'y' or 'n'
    
    def mainMenu():
        #print main menu
        #get input for menu selection
        #validate
        #return int 1-5

    def addHoliday(holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def removeHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def readJson(filelocation):
        # Read in things from json file location
        # split text into name and date
        # make date into ints
        # make date into datetime object
        # add entries to innerHolidays

    def saveJson(filelocation):
        # Write out json file to selected file.
        
    def scrapeHolidays():
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # scrape 5 times, for 2020-2024
        # iterate over table object, pull out name and date and make holiday object for each     

    def numHolidays():
        # Return the total number of holidays in innerHolidays
    
    def filter_holidays_by_week(year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    def displayHolidaysInWeek(holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 

    def getWeather(weekNum):
        # build weather query
        # get weather for 5 days from current day
        # filter to weather description
        # return list of weather descriptions

    def viewCurrentWeek():
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results



def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is

main()



