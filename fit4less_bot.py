from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import smtplib
import os
from time import time, sleep
from datetime import datetime
from termcolor import colored
import csv
import numpy as np
from tkinter import *
from tkcalendar import *

def startService(emailEntryBox, passwordEntryBox, date, time, window):

    if( len(emailEntryBox.get()) > 0 and len(passwordEntryBox.get()) > 0 and len(date) > 0 and time != "SELECT TIME"):

        # emailEntryBox.config(state="readonly")
        # passwordEntryBox.config(state="readonly")
        validLogin = False
        windowOpen = False
        service = True

        featureNames = np.array([])
        importData = np.empty(shape = (1,11))

        with open ("data.csv") as file:

                reader = csv.reader(file, delimiter = ',')
                featureNames = next(reader)

                for row in reader:
                    importData = np.vstack([importData, row])

                importData = np.delete(importData, (0), axis=0)
                importData = np.array(importData)

        # sender_email = importData[0,0]
        # receiver_emails = importData[:,1]
        # cred = importData[0,2]
        url = importData[0,3]
        xPathLoginButton = importData[0,4]
        loginEmail = emailEntryBox.get()
        loginPassword = passwordEntryBox.get()
        xPathLoginEmailTextbox = importData[0,7]
        xPathLoginPasswordTextbox = importData[0,8]
        xPathSelectDayButton = importData[0,9]
        xPathYesButton = importData[0,10]
        xPathPreferredDate = '//*[@id="date_{}"]'.format(date)
        preferredTime = time
        preferredTimeToMatch = ""
        preferredTimeArray = ["at 7:00 AM", "at 8:00 AM", "at 9:00 AM", "at 10:00 AM", "at 11:00 AM", "at 12:00 PM", "at 1:00 PM", "at 2:00 PM", "at 3:00 PM", "at 4:00 PM", "at 5:00 PM", "at 6:00 PM", "at 7:00 PM", "at 8:00 PM", "at 9:00 PM"]
        preferedTimeIndex = 0
        window.destroy()

        if(preferredTime == "7AM"):
            preferedTimeIndex = 0
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "8AM"):
            preferedTimeIndex = 1
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "9AM"):
            preferedTimeIndex = 2
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "10AM"):
            preferedTimeIndex = 3
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "11AM"):
            preferedTimeIndex = 4
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "12PM"):
            preferedTimeIndex = 5
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "1PM"):
            preferedTimeIndex = 6
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "2PM"):
            preferedTimeIndex = 7
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "3PM"):
            preferedTimeIndex = 8
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "4PM"):
            preferedTimeIndex = 9
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "5PM"):
            preferedTimeIndex = 10
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "6PM"):
            preferedTimeIndex = 11
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "7PM"):
            preferedTimeIndex = 12
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "8PM"):
            preferedTimeIndex = 13
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        elif(preferredTime == "9PM"):
            preferedTimeIndex = 14
            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]

        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        windowOpen = True

        windowClosedErrorMessage_01 = "Unable to evaluate script: no such window: target window already closed\nfrom unknown error: web view not found\n"
        windowClosedErrorMessage_02 = "Unable to evaluate script: disconnected: not connected to DevTools\n"

        driver.get(url)

        while(service == True):

            try:
                loginEmailTextbox = driver.find_element_by_xpath(xPathLoginEmailTextbox)
                loginPasswordTextbox = driver.find_element_by_xpath(xPathLoginPasswordTextbox)
                loginButton = driver.find_element_by_xpath(xPathLoginButton)
                loginEmailTextbox.send_keys(loginEmail)
                loginPasswordTextbox.send_keys(loginPassword)
                loginButton.click()

                foundLatestDate = False

                os.system('cls')
                print(colored("Fit4Less Auto-Booking Service", "yellow"))
                print(f"Booking for {loginEmail} on {date} {preferredTimeToMatch}")
                
                print(colored("Searching for preferred date...", "cyan"))

                while(foundLatestDate == False):

                    try:

                        if(driver.get_log('driver')[-1]['message'] == windowClosedErrorMessage_01):
                            os.system('cls')
                            print(colored("Fit4Less Auto-Booking Service", "yellow"))
                            print(colored("Window closed by user.", "red"))
                            windowOpen = False
                            foundLatestDate = False

                        elif(driver.get_log('driver')[-1]['message'] == windowClosedErrorMessage_02): 
                            os.system('cls')
                            print(colored("Fit4Less Auto-Booking Service", "yellow"))
                            print(colored("Cannot connect to devtools.", "red"))
                            windowOpen = False
                        
                        validInput = False

                        while(validInput == False):

                            userInput = input("Would you like to restart the service?(Y/N): ")
                            print("Executing...")

                            if(userInput == "y" or userInput == "Y"):
                                validInput = True
                                startService()

                            elif(userInput == "n" or userInput == "N"):
                                validInput = True
                                #foundLatestDate = True
                                service = False
                                windowOpen = False
                                os.system('cls')
                                print(colored("Fit4Less Auto-Booking Service", "yellow"))
                                print("Shutting down Fit4Less Auto-Booking Service...")
                                exit()
                            else:
                                print(colored("Invalid input.", "red"))

                    except Exception as e:
                        #Throws list index out of range error if program is running normally.
                        pass

                    try:
                        html = driver.find_element_by_tag_name('html')
                        html.send_keys(Keys.END)
                        selectDayButton = driver.find_element_by_xpath(xPathSelectDayButton)
                        selectDayButton.click()
                        preferredDate = driver.find_element_by_xpath(xPathPreferredDate)
                        preferredDate.click()
                        validLogin = True

                        try:
                            #print(colored("Found preferred date. Attempting to book...", "green"))
                            availableTimeSlots = driver.find_elements_by_class_name("time-slot")

                            if(len(availableTimeSlots) > 0):
                                
                                timeslotNotFound = True

                                while(timeslotNotFound):

                                    for timeslot in availableTimeSlots:
                                        if(preferredTimeToMatch in timeslot.text):
                                            timeslot.click()
                                            timeslotNotFound = False

                                    if(timeslotNotFound == True):
                                        if(preferedTimeIndex < 14):
                                            preferedTimeIndex += 1
                                            preferredTimeToMatch = preferredTimeArray[preferedTimeIndex]
                                        else:
                                            print("Unable to additional timeslots.")
                                            print("Shutting down Fit4Less Auto-Booking Service...")
                                            exit()
                                    
                                yesButton = driver.find_element_by_xpath(xPathYesButton)
                                yesButton.click()

                                foundLatestDate = True
                                service = False

                        except:
                            pass
                        
                    except Exception as e:
                        #print("meow")
                        #print(e)

                        try:
                            checkFailure = driver.find_element_by_tag_name("h1")
                            if(checkFailure.text == "LOG IN FAILED"):
                                validLogin = False
                                break

                        except:
                            pass

                        if(service == True and windowOpen == True):
                            
                            driver.refresh()

                            #Fit4Less website will attempt to log you out if you refresh too many times.
                            #This Try/Catch block will log you back in if they try to pull that shit again.
                            try:
                                loginEmailTextbox = driver.find_element_by_xpath(xPathLoginEmailTextbox)
                                loginPasswordTextbox = driver.find_element_by_xpath(xPathLoginPasswordTextbox)
                                loginButton = driver.find_element_by_xpath(xPathLoginButton)
                                loginEmailTextbox.send_keys(loginEmail)
                                loginPasswordTextbox.send_keys(loginPassword)
                                loginButton.click()
                            except:
                                pass
                            
                        else:
                            pass

                if(foundLatestDate == True):
                    os.system('cls')
                    print(colored("Fit4Less Auto-Booking Service", "yellow"))
                    print(colored("Successfully booked for {} at {}!".format(importData[0,10], preferredTime), "green"))

                print("\nFit4Less Auto-Booking Service ended.")

            except:
                if(validLogin == True):
                    driver.refresh()
                    os.system('cls')
                    print(colored("Fit4Less Auto-Booking Service", "yellow"))
                    print("Fit4Less appears to be adding new timeslots. Continuing to monitor...")

                elif(validLogin == False):
                    os.system('cls')
                    print(colored("Fit4Less Auto-Booking Service", "yellow"))
                    print("Invalid username or password.")
                    exit()
    else:
        alertWindow = Toplevel(window)
        Label(alertWindow, text="Please fill out all required fields.", font="none 12 bold").pack()
        alertOKButton = Button(alertWindow, text="OK", command=lambda: close_window(alertWindow)).pack()

window = Tk()
newWindow = Toplevel(window)
newWindow.destroy()

alertWindow = Toplevel(window)
alertWindow.destroy()

calendarHidden = True

def close_window(alertWindow): 
    alertWindow.destroy()

def penis(date, window):
    
    global calendarHidden
    calendarHidden = True
    window.destroy()
    datePickedTextbox.config(state="normal")
    datePickedTextbox.delete(0,END)
    datePickedTextbox.insert(INSERT,date)
    datePickedTextbox.config(state="readonly")

def pickDate():

    global calendarHidden
    global newWindow

    if(calendarHidden == True):
        calendarHidden = False
        newWindow = Toplevel(window)
        calendar = Calendar(newWindow, selectmode="day", year=2021, month=3, day=8, date_pattern="yyyy-mm-dd")
        calendar.pack()
        calendarOKButton = Button(newWindow, text="OK", command= lambda: penis(calendar.get_date(), newWindow))
        calendarOKButton.pack()

    elif(calendarHidden == False):
        newWindow.destroy()
        calendarHidden = True

def handle_click(event):

    pickDate()

clicked = StringVar()
clicked.set("SELECT TIME")

window.title("F4L Auto-Booking Service")
window.configure(background="#F6B221")
Label(window, text="F4L Auto-Booking Service", bg="#F6B221", fg="black", font="none 12 bold").grid(row=1, column=0, columnspan=4)
Label(window, text="", bg="#F6B221", fg="black", font="none 12 bold").grid(row=2, column=0, sticky=W)

Label(window, text="Email",  bg="#F6B221", fg="black", font="none 12 bold", justify="right").grid(row=3, column=0, sticky=E)
emailEntryBox = Entry(window, width=30, bg="white")
emailEntryBox.grid(row=3, column=2, sticky=W)

Label(window, text="Password",  bg="#F6B221", fg="black", font="none 12 bold", justify="right").grid(row=4, column=0, sticky=E)
passwordEntryBox = Entry(window, show="*", width=30, bg="white")
passwordEntryBox.grid(row=4, column=2, sticky=W)

Label(window, text="Preferred Date", bg="#F6B221", fg="black", font="none 12 bold").grid(row=5, column=0, sticky=W)
#pickDateButton = Button(window, text="SELECT DATE", command=pickDate).grid(row=5, column=3, sticky=W)
datePickedTextbox = Entry(window, width=30, bg="white", state='readonly')



datePickedTextbox.bind("<1>", handle_click)

datePickedTextbox.grid(row=5, column=2, sticky=W)


#
#

# Label(window, text="", bg="#F6B221", fg="black", font="none 12 bold").grid(row=6, column=0, sticky=W)

Label(window, text="Preferred Time", bg="#F6B221", fg="black", font="none 12 bold").grid(row=7, column=0, sticky=W)
# timeEntryTextbox = Entry(window, width=30, bg="white", state='readonly')
# timeEntryTextbox.grid(row=7, column=2, sticky=W)
timeDropdown = OptionMenu(window, clicked, "7AM", "8AM", "9AM", "10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM", "7PM", "8PM", "9PM")
timeDropdown.grid(row=7, column=2, sticky=W)

Label(window, text="", bg="#F6B221", fg="black", font="none 12 bold").grid(row=8, column=0, sticky=W)

Button(window, text="Run", command=lambda: startService(emailEntryBox, passwordEntryBox, datePickedTextbox.get(), clicked.get(), window)).grid(row=9, column=0, columnspan=4, sticky=E)


window.mainloop()