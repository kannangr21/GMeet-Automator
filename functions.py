from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from decouple import config  # Remove this import if email and password are configured
from time import sleep
from datetime import datetime
import os
import re
from selenium.webdriver.chrome.options import Options

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

DIR = os.getcwd()

driver = ""

def login():         # Login to google account and redirects to GMail
    global driver
    driver = webdriver.Chrome(options = opt, executable_path = DIR + "/chromedriver.exe")
    driver.get("https://www.gmail.com")
    eMail = driver.find_element_by_tag_name('input')
    eMail.send_keys(config('EMAIL_ID')) # Enter the email id as .send_keys("example@example.com"), remove config('EMAIL_ID')
    eMail.send_keys(Keys.RETURN)
    sleep(3)
    eMail = driver.find_element_by_name('password')
    eMail.send_keys(config('PASSWORD')) # Enter the password as .send_keys("password"), remove config('PASSWORD')
    eMail.send_keys(Keys.RETURN)

def buttonControl(): # Turns off Camera, Mic and joins / leaves
    # Mutes Microphone
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[1]/div[1]/div/div[4]/div[1]').click() 
    sleep(1)
    # Turns off Camera
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[1]/div[1]/div/div[4]/div[2]').click() 
    sleep(5) 
    # Joins the Meet 
    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/span').click()
    sleep(3600) # Stays in the meet for 1 hour (Update needed)
    # Leaves the meet
    driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[2]/div/div[7]/span/button').click()
    sleep(3)

def joinClass(link): # Looks For GMeet Link and redirects to it
    sleep(5)
    driver.get(link)
    sleep(5)
    try: # Searches for the link posted as hyperlink in stream / dashboard
            element = driver.find_element_by_partial_link_text("meet.google")
            driver.get(element.text)
    except: 
        try:    # Searches for the link posted in GCR stream as 'meet.google.com/{code}' 
            element = driver.find_elements_by_css_selector('div.pco8Kc')
            sleep(5)
            for i in range(0, 10): # Checks last 10 posts in GCR stream and gets the link 
                regex = r"meet.google.com/"
                meetCode = re.findall(regex, element[i].text)
                if meetCode:
                    driver.get("https://" + element[i].text)
                    break
        except: # Joins the meet if the class is added as an event in Google calendar
            driver.get("https://meet.google.com")
            sleep(1)
            # Joins the event added through Google Calendar
            driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[2]/c-wiz/c-wiz/div[1]/div[1]/div/div[5]/c-wiz/div/c-wiz/div').click()    
    sleep(3)
    buttonControl()
    return driver.close()

def timeTable():   # Gets the time table from the local storage and returns current day's schedule
    # Make sure that no whitespaces are present in the shortcodes and time is in 24 hr format
    # Days has '$' notation
    # Eg : Computer Science at 1.30 PM => "13.30 CS" in TimeTable.txt
    f = open(DIR + "/TimeTable.txt", "r")
    content = f.read()
    day = datetime.now().strftime('%A') # Get current day
    content = content.split()
    Table = []
    flag = 0
    for line in range(0,len(content)):
        if content[line] == '$' + day:
            flag = 1
            Table.append(content[line])
            continue
        elif('$' in content[line]):
            flag = 0
            continue
        elif(flag == 1):
            Table.append(content[line])
    return Table

  
def getClass(Table): # Searches for the live class and joins between (time - 5) mins and (time + 15) mins, !! 24 hrs format
    # Eg: for 12:00 hr class, you may join between 11:55 hr and 12:15 hr, Modify the time if needed 
    currentTime = float(datetime.now().strftime("%H.%M"))
    if Table == []:
        return "No classes Today!!" # Customized message, Terminates the program
    for i in range(1, len(Table), 2):
        if (
            currentTime <= float(Table[i]) + 0.15 and  # within 15 mins from the start of the class
            currentTime >= float(Table[i]) - 0.05      # Before 5 mins of the class
            ):
            return Table[i+1]
    if (currentTime > float(Table[-2])): # All the classes for the day has ended
            return "Chill!! That's all for today" # Customized message, Terminates the program
    else: # No class Currently
        return " "

def getGCRlink(className): # Returns the live class GCR link
    # Use the Short codes given in the time table
    # Paste the GCR links respective to the shortcodes of the classes

    if className == "DS":
        class_link = "https://classroom.google.com/u/0/c/" # Paste GCR link
    if className == "DSD":
        class_link = "https://classroom.google.com/u/0/c/" # Paste GCR link
    if className == "MAT":
        class_link = "https://classroom.google.com/u/0/c/" # Paste GCR link
    if className == "CO":
        class_link = "https://classroom.google.com/u/0/c/" # Paste GCR link
    if className == "JAVA":
        class_link = "https://classroom.google.com/u/0/c/" # Paste GCR link
    if className == "DSD(LAB)":
        class_link = "https://classroom.google.com/u/0/c/" # Paste GCR link
    if class_link == "DS(LAB)":
        class_link = "https://classroom.google.com/u/0/c/" # Paste GCR link

    # Add classes in the same format or remove if not needed
    return class_link