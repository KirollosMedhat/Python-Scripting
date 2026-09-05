import time
import sys
import argparse
import getpass
import subprocess
import os
from datetime import datetime
from playwright.sync_api import sync_playwright, Error, Playwright, Page, TimeoutError as PlaywrightTimeoutError

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
    # try:
    #     browser = p.chromium.launch(headless=False)
    # except Error as e:
    #     if "Executable doesn't exist" in str(e):
    #         print("Setting up browser for first use, please wait...")
    #         #subprocess.run(["playwright", "install", "chromium"], check=True)
    #         subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    #         browser = p.chromium.launch(headless=False)
    #     else:
    #         raise

    try:
        browser = p.chromium.launch(headless=False)
    except Error as e:
        if "Executable doesn't exist" in str(e):
            print("Setting up browser for first use, please wait...")
            from playwright.__main__ import main as playwright_main
            sys.argv = ["playwright", "install", "chromium"]
            try:
                playwright_main()
            except SystemExit:
                pass
            browser = p.chromium.launch(headless=False)
        else:
            raise

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

        # adjust_period_of_time(page, daysfilterinput, clock_in_time, clock_out_time, start_break_time, end_break_time, note)

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

def valid_time(value):
    datetime.strptime(value, "%I:%M%p")  # raises ValueError if invalid
    return value



if __name__ == "__main__":

    if getattr(sys, "frozen", False):
        #print("DEBUG: frozen detected, setting browsers path")
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(os.environ["LOCALAPPDATA"], "ms-playwright")

    parser = argparse.ArgumentParser(description="Automates TimeClock Wizard actions: clock in/out, start/end break, or bulk-correct entries for a date range.")
    parser.add_argument("-v", "--version", action="version", version="v1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    clockin_parser = subparsers.add_parser("clockin", help="Clock in for the day")
    clockin_parser.add_argument("username", help="Your TimeClock Wizard username")
    clockin_parser.add_argument(
        "-n", "--note", default="WFH", choices=Acceptable_Notes,
        help="Note attached to the clock-in entry (default: WFH)"
    )

    clockout_parser = subparsers.add_parser("clockout", help="Clock out for the day")
    clockout_parser.add_argument("username", help="Your TimeClock Wizard username")
    clockout_parser.add_argument(
        "-n", "--note", default="WFH", choices=Acceptable_Notes,
        help="Note attached to the clock-out entry (default: WFH)"
    )

    breakin_parser = subparsers.add_parser("breakin", help="Start a break")
    breakin_parser.add_argument("username", help="Your TimeClock Wizard username")

    breakout_parser = subparsers.add_parser("breakout", help="End a break")
    breakout_parser.add_argument("username", help="Your TimeClock Wizard username")

    adjust_parser = subparsers.add_parser(
        "adjust", help="Bulk-correct clock and break entries for a date range")
    adjust_parser.add_argument("username", help="Your TimeClock Wizard username")

    adjust_parser.add_argument(
    "daysfilterinput", choices=DAYS_FILTERS,
    help=(
        "Date range whose entries will be corrected. Options: TODAY, YESTERDAY, "
        "CURRENTWEEK, PREVIOUSWEEK, CURRENTMONTH, PREVIOUSMONTH, LAST30DAYS, "
        "LAST60DAYS, LAST90DAYS, CURRENTYEAR, PREVIOUSYEAR")
    )
    adjust_parser.add_argument(
        "-cit", "--clock_in_time", default="9:00AM", type=valid_time,
        help="Clock-in time to be set for every entry in chosen range, 12-hour format e.g. 9:00AM (default: 9:00AM)"
    )
    adjust_parser.add_argument(
        "-cot", "--clock_out_time", default="6:00PM", type=valid_time,
        help="Clock-out time to be set for every entry in chosen range, 12-hour format e.g. 6:00PM (default: 6:00PM)"
    )
    adjust_parser.add_argument(
        "-bit", "--break_in_time", default="3:00PM", type=valid_time,
        help="Break-start time to be set for every entry in chosen range, 12-hour format e.g. 3:00PM (default: 3:00PM)"
    )
    adjust_parser.add_argument(
        "-bot", "--break_out_time", default="4:00PM", type=valid_time,
        help="Break-end time to be set for every entry in chosen range, 12-hour format e.g. 4:00PM (default: 4:00PM)"
    )
    adjust_parser.add_argument(
        "-n", "--note", default="WFH", choices=Acceptable_Notes,
        help=(
            "Note attached to each corrected clock entry."
            "Options: WFH, NASA, APJ, Public Holiday Worked (default: WFH)"
        )
    )

    args = parser.parse_args()

    password = getpass.getpass("Password: ")


    start_time = time.perf_counter()

    if args.command == "clockin":
        clock_in(args.username, password, args.note)
    elif args.command == "clockout":
        clock_out(args.username, password, args.note)
    elif args.command == "breakin":
        start_break(args.username, password)
    elif args.command == "breakout":
        end_break(args.username, password)
    elif args.command == "adjust":
        adjust(args.username, password, args.daysfilterinput,
           args.clock_in_time, args.clock_out_time,
           args.break_in_time, args.break_out_time, args.note)

    end_time = time.perf_counter()
    execution_time = end_time - start_time    
    print(f"\n\nExecuted in {execution_time:.4f} seconds.\n\n")

