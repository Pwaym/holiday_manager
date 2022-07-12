from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import config


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
      
    def __init__(self,name, date):
        self.name = name
        self.date = date        
    
    def __str__ (self):
        return f"{self.name} ({self.date})"
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
        self.innerHolidays = []
   
    def addHoliday(self,holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
        objtype = type(holidayObj)
        if objtype == "__main__.Holiday":
            self.innerHolidays.append(holidayObj)
            print(f"Success:\r\n{holidayObj} has been added to the holiday list.")
        else:
            print("Invalid input.\r\n")

    def findHoliday(self,HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday
        for holiday in self.innerHolidays:
            if holiday["name"] == HolidayName and holiday["date"] == Date:
                return holiday
            else:
                pass
        return False

    def removeHoliday(self,HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        delete = HolidayList.findHoliday(HolidayName, Date)
        if delete == False:
            return print("Error:\r\nHoliday not found.")
        else:
            self.innerHolidays.remove(delete)
            print(f"Success:\r\n{delete} has been removed from the holiday list.")


    def read_json(self,filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
        file = open(filelocation)
        jsonfile = json.loads(file.read())
        for holiday in jsonfile["holidays"]:
            HolidayList.addHoliday(holiday)

    def save_to_json(self,filelocation):
        # Write out json file to selected file.
        file = open(filelocation, "w")
        json.dump(self.innerHolidays,file)
        
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions. 
        html = ""
        holidaylist = []
        years = ["2020","2021","2022","2023","2024"]
        for year in years:
            response = requests.get(f"https://www.timeanddate.com/holidays/us/{year}?hol=33554809")
            html = response.text

            soup = BeautifulSoup(html,"html.parser")
            table = soup.find("table",attrs = {"id":"holidays-table"})

            for row in table.find_all("tr",attrs = {"class":"showrow"}):
                holidays = row.find_all("td")
                holidaydict = {}
                holidaydict["name"] = holidays[1].string
                dates = row.find("th")
                holidaydict["date"] = year + " " + dates.string
                holidaylist.append(holidaydict)

        for x in holidaylist:
            x["date"] = datetime.strptime(x["date"],"%Y %b %d")
            x["date"] = datetime.strftime(x["date"],"%Y-%m-%d")
            
            for item in self.innerHolidays:
                if x["name"] == item["name"] and x["date"] == item["date"]:
                    holidaylist.remove(x)
                else:
                    self.innerHolidays.append(x)
            

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)
    
    def filter_holidays_by_week(self,year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays


    def displayHolidaysInWeek(self,holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    # def getWeather(self,weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

def exit():
    print("\r\nExit\r\n====")
    exitchoice = input("Would you like to exit? [y/n]:")
    if exitchoice == "y":
        print("Goodbye!")
        return False
    elif exitchoice == "n":
        return True
    else:
        print("Invalid choice.")

def adding():
    print("\r\nAdd a Holiday")
    print("=============")
    name = input("Holiday:")
    date = input("Date (yyyy-mm-dd):")
    checking = True
    while checking == True:
        if len(date) == 10:
            newholiday = Holiday(name,date)
            HolidayList.addHoliday(newholiday)
            checking = False
        else:
            print("Invalid date. Please try again.")
            date = input(f"Date for {name} (yyyy-mm-dd):")

def saving():
    print("\r\nSaving Holiday List")
    print("===================")
    choice = input("Would you like to save your changes? [y/n]:")
    if choice == "y":
        HolidayList.save_to_json(config.jsonsavedestination)
        print("Success:\r\nYour changes have been saved.")
        return False
    elif choice == "n":
        print("Canceled:\r\nHoliday list file save cancelled.")
        return True
    else:
        print("Invalid choice.")



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
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program. 
    #    If they do wish to continue, keep the program going. 
    
    
    inapp = True
    print(f"Holiday Management\r\n==================\r\nThere are {HolidayList.numHolidays()} holidays stored in the system.")
    while inapp:
        print("\r\nHoliday Menu\r\n============\r\n1. Add a Holiday\r\n2. Remove a Holiday\r\n3. Save Holiday List\r\n4. View Holidays\r\n5. Exit")
        menuchoice = input("Please enter your choice [1-5]:")
        if menuchoice == "1": # Add a Holiday
            adding()
            unsaved = True
        elif menuchoice == "2": # Remove a Holiday
            print("Remove a Holiday")
            print("================")
            name = input("Holiday:")
            date = input("Date (yyyy-mm-dd):")
            HolidayList.removeHoliday(name,date)
            unsaved = True
        elif menuchoice == "3": # Save Holiday list
            unsaved = saving()
        elif menuchoice == "4": # View Holidays
            print("4 picked")
        elif menuchoice == "5": # Exit
            if unsaved:
                print("Your changes will be lost.")
                inapp = exit()
            else:
                inapp = exit()
        else:
            print("Invalid input. Enter a number 1-5\r\n")



if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





