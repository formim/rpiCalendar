# Mario Formisano. February 2020
# Scrape the RPI academic calendar and generate an ICS file
# Selenium compatibility on MacOS Catalina: Refer to https://github.com/mozilla/geckodriver/releases/tag/v0.26.0

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from ics import Calendar, Event

URL = "https://info.rpi.edu/registrar/academic-calendar/"
monthNums = { "January" : "01",
              "February" : "02",
              "March" : "03",
              "April" : "04",
              "May" : "05",
              "June" : "06",
              "July" : "07",
              "August" : "08",
              "September" : "09",
              "October" : "10",
              "November" : "11",
              "December" : "12"
            }

def dateFormat(dateStr):
    # "April 2, 2020" -> "4-2-2020"
    dateStr.strip()
    tokens = dateStr.split()
    day = tokens[1][:-1]
    if len(day) == 1:
        day = "0" + day
    return tokens[2] + "-" + monthNums[tokens[0]] + "-" + day

def main():
    print("Connecting to info.rpi.edu ...")
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(URL)
        # Make soup
        soup = bs(driver.page_source, "html.parser")

        rawEntries = soup.findAll("tr")
    except:
        print("Something went wrong.  If on MacOS, check Catalina compatibility: https://github.com/mozilla/geckodriver/releases/tag/v0.26.0")
        return -1

    print("Successfully connected, scraped: Creating calendar ...")
    entries = []

    dates = soup.findAll(class_="date")
    numEvents = len(dates)
    # Clean up
    for i in range(len(rawEntries)):
        entry = str(rawEntries[i])
        # Month Markers are shorter
        if len(entry) < 50:
            continue
        else:
            entry = entry[:-14]
            entry = entry[ (entry.rfind('>') + 1) :]
            # print(entry)
            entries.append(entry)

    cal = Calendar()

    for i in range(numEvents):
        date = str(dates[i])
        date = date[17:]
        date = date[:-5]
        # print(date, ":", entries[i])
        e = Event()
        e.name = entries[i]
        # print(e.name)
        if " - " in date:
            # Multiple days
            e.begin = dateFormat(date[:date.find(" - ")])
            # print("input", dateFormat(date[:date.find(" - ")]))
            # print("Begin", e.begin)
            e.make_all_day()
            e.end = dateFormat(date[date.find(" - ") + 3:])
            # print("End", e.end)
        else:
            e.begin = dateFormat(date)
            e.make_all_day()
            # print(e.begin)
        # print()
        cal.events.add(e)
    with open('academic_calendar.ics', 'w') as myfile:
        myfile.writelines(cal)
    print("\nDone. Check directory for 'academic_calendar.ics'.")
    return 0

if __name__ == "__main__":
    main()
