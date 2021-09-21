from time import sleep
import functions as foo

def code():
    Table = foo.timeTable()
    className = foo.getClass(Table)
    if className == " ":
        print("No class Right Now")
        sleep_min = 15  # Set this in minutes to wait for the next iteration (15 preferable)
        # Checks for the class 'sleep_min' minutes once, 15 minutes once here
        sleep(sleep_min*60)
        code()
    if(className in Table):  
        foo.login()
        class_link = foo.getGCRlink(className)
        foo.joinClass(class_link, className)
        code()
    else:
        print(className)

if __name__ == "__main__":
    code()