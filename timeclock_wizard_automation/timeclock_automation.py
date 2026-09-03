import os
import time
import re
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    page.goto("https://apps.timeclockwizard.com/Login?subDomain=Siliconegypt")

    # username = os.environ.get("MY_APP_USER", "your_username")
    # password = os.environ.get("MY_APP_PASS", "your_password")
    username = ""
    password = ""
    page.get_by_placeholder("UserName").first.fill(username)
    page.get_by_placeholder("Password").first.fill(password)
    page.get_by_role("button", name="Log In").click()
    page.locator("#sidebar a").filter(has_text="Timesheet").click()
    #page.locator("#ddlDays").select_option(label="Previous Month")
    page.locator("#ddlDays").select_option(label="Current Month")
    page.get_by_text("Search", exact=True).click()
    #cell = page.get_by_role("gridcell", name="Mon").first
    rows = page.get_by_role("row").all()
    # print(len(rows))

    # target_row = rows[3]  
    # print(target_row.inner_text())
    # target_row.get_by_text("Edit").click()
    count = 0
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
            page.get_by_role("button", name="Edit Time Request").click()
            #page.get_by_role("button", name="Edit Time Request").click()
        else:
            print("break in/out entry")
            row.get_by_text("Edit").click()
            page.locator("#txtStartTimeBreak").click()
            page.locator("#txtStartTimeBreak").press("ControlOrMeta+a")
            page.locator("#txtStartTimeBreak").fill("4:00AM")
            page.locator("#txtEndTimeBreak").click()
            page.locator("#txtEndTimeBreak").press("ControlOrMeta+a")
            page.locator("#txtEndTimeBreak").fill("5:00AM")
            page.get_by_role("button", name="Edit Time Request").click()
            #page.get_by_role("button").filter(has_text=re.compile(r"^$")).click()
            #page.pause()
            

            

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

