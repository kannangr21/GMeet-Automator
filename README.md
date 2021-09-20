# GMeet-Automator
This is an Automator developed using Python's Selenium framework. This works effectively with Google Class Room

## Prerequisites
- Python 3.5 or above installed in the machine
- ChromeDriver.exe (has been added to this repository for ease of use)
- Good Internet Connection
- Google Account (Mostly G-suite for schools and colleges, but yeah! personal accounts also works well)
## Running the bot
1. Clone this repository.
2. Run the command `pip install -r requirements.txt` in the command prompt / terminal.
3. Configure the `TimeTale.txt`, login credentials, GCR links, Sleep time based on internet connection / Class timings.  
    In `functions.py` check the lines,  
        - `30`,`34` for login credentials  
        - `46` for class duration (Default - 1 hour)  
        - `116`-`136` for GCR links  
        - `104`,`112` for customized messages  
      The conventions in `TimeTable.txt` are to be followed to avoid errors!
4. After configuring, save the files and run `python main.py` in command prompt and `python3 main.py` in linux

