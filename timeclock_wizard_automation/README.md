# TimeClock Wizard Automation

A command-line tool that automates repetitive [TimeClock Wizard] actions — clocking in/out, starting/ending a break, and bulk-correcting existing timesheet entries for a date range — using [Playwright](https://playwright.dev/python/) browser automation.

## What it does

TimeClock Wizard has no public API for these actions, so this tool drives a real Chromium browser to log in and perform them exactly as a human would, but scriptable from the command line.

Five commands are supported:

| Command    | What it does                                                        |
|------------|----------------------------------------------------------------------|
| `clockin`  | Clocks you in for the day, with a note                              |
| `clockout` | Clocks you out for the day, with a note                             |
| `breakin`  | Starts a break                                                       |
| `breakout` | Ends a break                                                         |
| `adjust`   | Bulk-corrects every clock and break entry within a chosen date range |

## Who this is for

Anyone who submits TimeClock Wizard entries and wants to automate the repetitive parts — clocking in/out daily, or correcting a batch of entries at once instead of editing each one by hand in the browser. This isn't tied to any specific company's TimeClock Wizard account — see the subdomain setup step below.

## Before you run it: set your TimeClock Wizard subdomain

TimeClock Wizard logs each company in through a subdomain-specific URL, e.g.:

```
https://apps.timeclockwizard.com/Login?subDomain=<YourCompanySubdomain>
```

This is **left blank in the source** on purpose, so this tool isn't tied to any one company's account. Before running it, open `timeclock_automation.py` and find:

```python
    page = browser.new_page()
    # TODO: Left blank intentionally. Fill in your own TimeClock Wizard login URL here.
    # Format: https://apps.timeclockwizard.com/Login?subDomain=<YourCompanySubdomain>
    # Example: https://apps.timeclockwizard.com/Login?subDomain=xyzcompany
    page.goto("")
```

Fill in the blank `page.goto("")` with your own company's login URL, using your own subdomain in place of `<YourCompanySubdomain>`. You can find your subdomain by checking the URL you normally use to log into TimeClock Wizard in your browser.

> If you're using the packaged `.exe` (Option A below) rather than building from source yourself, this step needs to already be done in whatever build you were given — check with whoever built it for you if you're unsure which company's subdomain it points to.

## Two ways to run this

### Option A — Run the standalone `.exe` (no Python needed)

If you were given a built `timeclock_automation.exe` (or a folder containing one), you don't need Python, `uv`, or Playwright installed at all. Just run it from a terminal:

```
.\timeclock_automation.exe clockin <username> -n WFH
```

**The first time you run any command**, the tool will automatically download the Chromium browser it needs — you'll see:

```
Setting up browser for first use, please wait...
```

This only happens once; it downloads to your Windows user profile (`%LOCALAPPDATA%\ms-playwright`) and is reused on every run after that. It requires an internet connection the first time.

You will be prompted for your TimeClock Wizard password on every run — it is never shown on screen and never stored anywhere.

### Option B — Run from source (for development)

If you're working on the script itself, or don't have a built `.exe`:

**1. Install [`uv`](https://docs.astral.sh/uv/)** (this project's Python package/environment manager), if you don't already have it.

**2. Clone the repo and install dependencies:**
```
git clone https://github.com/KirollosMedhat/Python-Scripting.git
cd Python-Scripting
uv sync
```

**3. Set your subdomain** — see "Before you run it" above.

**4. Install the Playwright browser** (one-time step, only needed when running from source):
```
uv run playwright install chromium
```

**5. Run the script:**
```
uv run timeclock_wizard_automation/timeclock_automation.py clockin <username> -n WFH
```

> Note: step 4 is **not** needed when using the packaged `.exe` (Option A) — the `.exe` handles that automatically on first run.

## Commands and arguments

Run `--help` on the tool itself or any subcommand for the full, always-up-to-date list of arguments and their defaults:

```
timeclock_automation.exe -h
timeclock_automation.exe adjust -h
```

### `clockin` / `clockout`

```
timeclock_automation.exe clockin <username> [-n NOTE]
timeclock_automation.exe clockout <username> [-n NOTE]
```

- `username` — your TimeClock Wizard username
- `-n`, `--note` — note attached to the entry. Run `--help` for the current list of accepted values for your setup.

### `breakin` / `breakout`

```
timeclock_automation.exe breakin <username>
timeclock_automation.exe breakout <username>
```

- `username` — your TimeClock Wizard username

### `adjust`

Bulk-corrects **every** clock entry and **every** break entry within a chosen date range to the same set of times and note. Useful for fixing a batch of wrong entries in one go rather than editing each individually.

```
timeclock_automation.exe adjust <username> <daysfilterinput> [options]
```

- `username` — your TimeClock Wizard username
- `daysfilterinput` — the date range to search and correct. One of:
  `TODAY`, `YESTERDAY`, `CURRENTWEEK`, `PREVIOUSWEEK`, `CURRENTMONTH`, `PREVIOUSMONTH`, `LAST30DAYS`, `LAST60DAYS`, `LAST90DAYS`, `CURRENTYEAR`, `PREVIOUSYEAR`
- `-cit`, `--clock_in_time` — new clock-in time for every clock entry in range, 12-hour format e.g. `9:00AM` (default: `9:00AM`)
- `-cot`, `--clock_out_time` — new clock-out time for every clock entry in range (default: `6:00PM`)
- `-bit`, `--break_in_time` — new break-start time for every break entry in range (default: `3:00PM`)
- `-bot`, `--break_out_time` — new break-end time for every break entry in range (default: `4:00PM`)
- `-n`, `--note` — note attached to each corrected entry. Run `--help` for the current list of accepted values for your setup.

**Example** — set every entry in the current month to a standard 9–6 schedule with a 3–4 break:
```
timeclock_automation.exe adjust <username> CURRENTMONTH -cit 9:00AM -cot 6:00PM -bit 3:00PM -bot 4:00PM -n <Note>
```

## Other flags

- `-h`, `--help` — show help for the tool or any subcommand
- `-v`, `--version` — show the tool's version

## Security notes

- Your password is requested interactively on every run and is never echoed to the screen, never stored, and never written to disk.
- Your username is currently passed as a plain command-line argument. This means it can end up in your shell history. This is a known, accepted limitation for now — do not pass your password this way (it isn't possible to; the tool always prompts for it separately).

## Known limitations / current status

This is the first working version of the tool. A few things are intentionally simple for now:

- `adjust` sets the **same** times/note across every entry in the chosen range — it does not yet support correcting individual entries to different values each. Per-entry correction (e.g. from a CSV file) is a planned future feature.
- The TimeClock Wizard login URL/subdomain must be manually set in the source before use (see "Before you run it" above) — it isn't yet a command-line argument.
- The final "submit" step for some actions may be disabled in certain builds while under active testing — check the script/build notes if an action appears to run but doesn't submit.

## Troubleshooting

- **"Login failed: Username/Email and password do not match."** — the credentials entered were rejected by TimeClock Wizard itself. Double check your username and password.
- **Login page doesn't load / times out** — check that the subdomain has been set correctly (see "Before you run it").
- **Script seems stuck after "Setting up browser for first use..."** — this is downloading Chromium and requires an internet connection; on a slow connection this can take a minute or two. Let it finish.
- **Nothing happens / wrong entries get changed** — always double check the `daysfilterinput` range and the time values before running `adjust`, since it affects every entry in that range at once.
