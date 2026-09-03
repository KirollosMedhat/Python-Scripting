import os
import time
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    page.goto("https://apps.timeclockwizard.com/Login?subDomain=Siliconegypt")
    print(page.title())

    # username = os.environ.get("MY_APP_USER", "your_username")
    # password = os.environ.get("MY_APP_PASS", "your_password")
    username = ""
    password = ""
    page.get_by_placeholder("UserName").first.fill(username)
    page.get_by_placeholder("Password").first.fill(password)
    page.get_by_role("button", name="Log In").click()

    page.locator("#sidebar a").filter(has_text="Timesheet").click()
    



    page.locator("#ddlDays").select_option(label="Previous Month")
    
    page.get_by_text("Search", exact=True).click()
    print(page.get_by_text("102550100 User/Day Type Time"))
    page.pause()

