import os
import time
import re
from playwright.sync_api import sync_playwright
from typing import Literal


DAYS_FILTERS = {
    "TODAY",
    "YESTERDAY",
    "CURRENTWEEK",
    "PREVIOUSWEEK",
    "CURRENTMONTH",
    "PREVIOUSMONTH",
    "LAST30DAYS",
    "LAST60DAYS",
    "LAST90DAYS",
    "CURRENTYEAR",
    "PREVIOUSYEAR",
    }

def normalize(text: str):
    return text.upper().replace("_", "").replace(" ", "")

def clock_in(page, note: str):
    page.get_by_text("Clock In", exact=True).click()
    page.locator("#txtClockInNote").click()
    page.locator("#txtClockInNote").fill(note)
    page.get_by_role("button", name="Clock In").click()

def clock_out(page, note: str):
    page.get_by_text("Clock Out", exact=True).click()
    page.locator("#txtClockInNote").click()
    page.locator("#txtClockInNote").fill(note)
    page.get_by_role("button", name="Clock Out").click()    

def start_break(page):
    page.get_by_text("Start Break").click()

def end_break(page):
    page.get_by_text("End Break").click()



# clock_in_time:str = "12:00AM"
# clock_out_time:str = "9:00AM"
# start_break_time:str = "4:00AM"
# start_break_time:str = "5:00AM"


# username = "170600"
# password = "123456"





with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    while True:
        daysfilterinput = normalize(input("Enter a date filter: "))
        if daysfilterinput in DAYS_FILTERS:
            break
        print(f"'{daysfilterinput}' is not valid. Choose from: {DAYS_FILTERS}")

    page.goto("https://apps.timeclockwizard.com/Login?subDomain=Siliconegypt")

    # username = os.environ.get("MY_APP_USER", "your_username")
    # password = os.environ.get("MY_APP_PASS", "your_password")

    # adjusting_period = Literal["Today","Yesterday","Current Week","","","","","","","","","","","","",""]
    




    page.get_by_placeholder("UserName").first.fill(username)
    page.get_by_placeholder("Password").first.fill(password)
    page.get_by_role("button", name="Log In").click()
    page.locator("#sidebar a").filter(has_text="Timesheet").click()
    #page.locator("#ddlDays").select_option(label="Previous Month")

    

    page.locator("#ddlDays").select_option(daysfilterinput)


    #page.locator("#ddlDays").select_option(label="Current Month")
    page.get_by_text("Search", exact=True).click()

    rows = page.get_by_role("row").all()

    options = page.locator("#ddlDays option").all()
    for opt in options:
        print(opt.get_attribute("value"))

    for row in rows[3:]:
        if "Notes" in row.inner_text():
            print("clock in/out entry")
            row.get_by_text("Edit").click()
            page.locator("#txtstartTimeClock").click()
            page.locator("#txtstartTimeClock").press("ControlOrMeta+a")
            page.locator("#txtstartTimeClock").fill("12:00AM")
            page.locator("#txtEndTimeClock").click()
            page.locator("#txtEndTimeClock").press("ControlOrMeta+a")
            page.locator("#txtEndTimeClock").fill("9:00AM")
            page.locator("#txtNoteClocked").click()
            page.locator("#txtNoteClocked").fill("APJ")
            #page.get_by_role("button", name="Edit Time Request").click() #commented for safety.
            page.pause()

        else:
            print("break in/out entry")
            row.get_by_text("Edit").click()
            page.locator("#txtStartTimeBreak").click()
            page.locator("#txtStartTimeBreak").press("ControlOrMeta+a")
            page.locator("#txtStartTimeBreak").fill("4:00AM")
            page.locator("#txtEndTimeBreak").click()
            page.locator("#txtEndTimeBreak").press("ControlOrMeta+a")
            page.locator("#txtEndTimeBreak").fill("5:00AM")
            #page.get_by_role("button", name="Edit Time Request").click() #commented for safety.
            page.pause()


            
    #########################################################
    #for clocking in:
    # page.get_by_text("Clock In", exact=True).click()
    # page.locator("#txtClockInNote").click()
    # page.locator("#txtClockInNote").fill("APJ")
    # page.get_by_role("button", name="Clock In").click()
    #########################################################

    #########################################################
    #for clocking out:
    # page.get_by_text("Clock Out", exact=True).click()
    # page.locator("#txtClockInNote").click()
    # page.locator("#txtClockInNote").fill("APJ")
    # page.get_by_role("button", name="Clock Out").click()
    #########################################################

    #########################################################
    #for starting break:
    # page.get_by_text("Start Break").click()
    #########################################################

    #########################################################
    #for ending break:
    # page.get_by_text("End Break").click()
    #########################################################

    







    # For information: this is the layout of the table rows[0]=header, rows[1]=summary, data starts at rows[2] For information.
    # Row 0: User/Day        Type    Time In Time Out        Duration(Hours : Minutes)       Payable Job     Location        Action
    # ---
    # Row 1: Kirollos Medhat Hanna 2701
    # Regular Hours:180:00
    # Break Hours:19:51
    # Absences Hours:00:00


    # print(rows[0].inner_text())
    # print("---")
    # print(rows[1].inner_text())
    # print("---")
    # print(rows[2].inner_text())
    # print(rows[3].inner_text())
    # print(rows[4].inner_text())

    page.pause()



if __name__ == "__main__":
    print("hi")