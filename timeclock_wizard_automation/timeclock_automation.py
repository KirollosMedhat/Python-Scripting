import os
import time
import re
import sys
import argparse
import getpass
from datetime import datetime
from playwright.sync_api import sync_playwright, Playwright, Page, TimeoutError as PlaywrightTimeoutError

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

Acceptable_Notes = {
    "WFH",
    "NASA",
    "APJ",
    "Public Holiday Worked",
}


def normalize(text: str) -> str:
    return text.upper().replace("_", "").replace(" ", "")

def open_timeclock_wizard_and_log_in(username: str, password: str, p: Playwright) -> Page:
    #browser = p.chromium.launch(headless=False, slow_mo=500)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://apps.timeclockwizard.com/Login?subDomain=Siliconegypt")
    page.get_by_placeholder("UserName").first.fill(username)
    page.get_by_placeholder("Password").first.fill(password)
    page.wait_for_load_state("networkidle")       #This line because the script broke when i removed slow_mo(the login button click wasn't acutally clicked, probably too fast for the website.)
    page.get_by_role("button", name="Log In").click()
    try:
        page.locator("#jError").wait_for(state="visible", timeout=5000)
        error_text = page.locator("#jError").inner_text()
        print(f"Login failed: {error_text}")
        browser.close()
        sys.exit(1)
    except PlaywrightTimeoutError:
        pass
    return page

def clock_in(username:str, password:str, note: str):
    with sync_playwright() as p:
        page = open_timeclock_wizard_and_log_in(username, password, p)
        page.get_by_text("Clock In", exact=True).click()
        page.locator("#txtClockInNote").click()
        page.locator("#txtClockInNote").fill(note)
        #page.get_by_role("button", name="Clock In").click()    #commented for safety.

def clock_out(username:str, password:str, note: str):
    with sync_playwright() as p:
        page = open_timeclock_wizard_and_log_in(username, password, p)
        page.get_by_text("Clock Out", exact=True).click()
        page.locator("#txtClockInNote").click()
        page.locator("#txtClockInNote").fill(note)
        #page.get_by_role("button", name="Clock Out").click()   #commented for safety.

def start_break(username:str, password:str):
    with sync_playwright() as p:
        page = open_timeclock_wizard_and_log_in(username, password, p)
        #page.get_by_text("Start Break").click()    #commented for safety.

def end_break(username:str, password:str):
    with sync_playwright() as p:
        page = open_timeclock_wizard_and_log_in(username, password, p)
        #page.get_by_text("End Break").click()      #commented for safety.

def adjust_period_of_time(page: Page,
                        daysfilterinput, 
                        clock_in_time, 
                        clock_out_time, 
                        start_break_time, 
                        end_break_time, 
                        note):
    
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
            #page.pause()
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
            #page.pause()

def adjust(username: str,
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

def valid_time(value):
    datetime.strptime(value, "%I:%M%p")  # raises ValueError if invalid
    return value



if __name__ == "__main__":

    # # print(sys.argv[0])
    # # print(sys.argv[1])
    # # print(sys.argv[2])
    # # print(sys.argv[3])
    # parser = argparse.ArgumentParser()
    # subparsers = parser.add_subparsers(dest="command", required=True)

    # clockin_parser = subparsers.add_parser("clockin")
    # clockin_parser.add_argument("username")
    # clockin_parser.add_argument("--note", default="WFH", choices=Acceptable_Notes)

    # clockout_parser = subparsers.add_parser("clockout")
    # clockout_parser.add_argument("username")
    # clockout_parser.add_argument("--note", default="WFH", choices=Acceptable_Notes)



    # breakin_parser = subparsers.add_parser("breakin")
    # breakin_parser.add_argument("username")

    # breakout_parser = subparsers.add_parser("breakout")
    # breakout_parser.add_argument("username")

    # #daysfilterinput, clock_in_time, clock_out_time, start_break_time, end_break_time, note
    # adjust_parser = subparsers.add_parser("adjust")
    # adjust_parser.add_argument("username")
    # adjust_parser.add_argument("daysfilterinput", choices=DAYS_FILTERS)
    # adjust_parser.add_argument("-cit", "--clock_in_time", default="9:00AM", type=valid_time)
    # adjust_parser.add_argument("-cot", "--clock_out_time", default="6:00PM", type=valid_time)
    # adjust_parser.add_argument("-bit", "--break_in_time", default="3:00PM", type=valid_time)
    # adjust_parser.add_argument("-bot", "--break_out_time", default="4:00PM", type=valid_time)
    # adjust_parser.add_argument("-n", "--note", default="WFH", choices=Acceptable_Notes)


    

    # args = parser.parse_args()

    # # x = datetime.strptime("9:00AM", "%I:%M%p")
    # # y = datetime.strptime("09:00AM", "%I:%M%p")
    # # E = datetime.strptime("19:00AM", "%I:%M%p")

    # # print(f"this should be okay: {x}")
    # # print(f"this should be okay: {y}")
    # # print(f"this should be an error: {E}")





    # print(args.username)
    # print(args.clock_in_time)
    # print(args.clock_out_time)
    # print(args.break_in_time)
    # print(args.break_out_time)
    # print(args.note)

    # password = getpass.getpass("Password: ")





    daysfilterinput = normalize(sys.argv[3])
    if daysfilterinput not in DAYS_FILTERS:
        print(f"'{daysfilterinput}' is not valid. Choose from: {DAYS_FILTERS}")
        sys.exit(1)


    start_time = time.perf_counter()
    #main(sys.argv[1],sys.argv[2],daysfilterinput)
    #clock_in(sys.argv[1],sys.argv[2],daysfilterinput)
    end_time = time.perf_counter()

    execution_time = end_time - start_time
    print(f"\n\nExecuted in {execution_time:.4f} seconds.\n\n")

