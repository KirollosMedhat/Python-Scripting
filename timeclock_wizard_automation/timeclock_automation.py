import os
import time
import re
import sys
from playwright.sync_api import sync_playwright

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

def open_timeclock_wizard_and_log_in(username: str, password: str, p):
    #browser = p.chromium.launch(headless=False, slow_mo=500)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://apps.timeclockwizard.com/Login?subDomain=Siliconegypt")
    page.get_by_placeholder("UserName").first.fill(username)
    page.get_by_placeholder("Password").first.fill(password)
    page.wait_for_load_state("networkidle")       #This line because the script broke when i removed slow_mo(the login button click wasn't acutally clicked, probably too fast for the website.)
    page.get_by_role("button", name="Log In").click()
    return page

def adjust_period_of_time(page, daysfilterinput, clock_in_time, clock_out_time, start_break_time, end_break_time, note):
    page.locator("#sidebar a").filter(has_text="Timesheet").click()
    page.locator("#ddlDays").select_option(daysfilterinput)
    
    page.get_by_text("Search", exact=True).click()
    
    rows = page.get_by_role("row").all()
    
    for row in rows[3:]:
        if "Notes" in row.inner_text():
            #print("clock in/out entry")
            row.get_by_text("Edit").click()
            page.locator("#txtstartTimeClock").click()
            page.locator("#txtstartTimeClock").press("ControlOrMeta+a")
            page.locator("#txtstartTimeClock").fill(clock_in_time)
            page.locator("#txtEndTimeClock").click()
            page.locator("#txtEndTimeClock").press("ControlOrMeta+a")
            page.locator("#txtEndTimeClock").fill(clock_out_time)
            page.locator("#txtNoteClocked").click()
            page.locator("#txtNoteClocked").fill(note)
            #page.get_by_role("button", name="Edit Time Request").click() #commented for safety.
            page.pause()

        else:
            #print("break in/out entry")
            row.get_by_text("Edit").click()
            page.locator("#txtStartTimeBreak").click()
            page.locator("#txtStartTimeBreak").press("ControlOrMeta+a")
            page.locator("#txtStartTimeBreak").fill(start_break_time)
            page.locator("#txtEndTimeBreak").click()
            page.locator("#txtEndTimeBreak").press("ControlOrMeta+a")
            page.locator("#txtEndTimeBreak").fill(end_break_time)
            #page.get_by_role("button", name="Edit Time Request").click() #commented for safety.
            page.pause()



def main(username: str,
        password: str, 
        daysfilterinput: str,
        clock_in_time:str = "12:00AM", 
        clock_out_time:str = "9:00AM", 
        start_break_time:str = "4:00AM", 
        end_break_time:str = "5:00AM", 
        note: str = "APJ"
        ):

    
    with sync_playwright() as p:
        page = open_timeclock_wizard_and_log_in(username, password, p)
        #clock_in(page, note) #SUCCEEDED
        adjust_period_of_time(page, daysfilterinput, clock_in_time, clock_out_time, start_break_time, end_break_time, note)
        page.pause()



if __name__ == "__main__":

    # print(sys.argv[0])
    # print(sys.argv[1])
    # print(sys.argv[2])
    # print(sys.argv[3])



    daysfilterinput = normalize(sys.argv[3])
    if daysfilterinput not in DAYS_FILTERS:
        print(f"'{daysfilterinput}' is not valid. Choose from: {DAYS_FILTERS}")
        sys.exit(1)


    start_time = time.perf_counter()
    main(sys.argv[1],sys.argv[2],daysfilterinput)
    end_time = time.perf_counter()

    execution_time = end_time - start_time
    print(f"Script took {execution_time:.4f} seconds to complete.\n\n")

