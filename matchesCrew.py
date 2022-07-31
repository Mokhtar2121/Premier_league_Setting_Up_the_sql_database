import mysql
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import mysql.connector

PATH = Service("C:\Program Files\chromedriver.exe")
driver = webdriver.Chrome(service=PATH)
driver.get("https://www.premierleague.com/results")

mydp = mysql.connector.connect(host="localhost", user="root", password="Qaisaleh12010@auc", database="premier_league",
                               auth_plugin='mysql_native_password')

if (mydp):
    print("connected")
    mycursor = mydp.cursor()
else:
    print("Notconnected")


def matchDate(date):
    d = date[4:]
    dateEdited = datetime.strptime(d, "%d %b %Y")

    return dateEdited.strftime('%d %m %Y')


def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


time.sleep(5)
try:
    element = WebDriverWait(driver, 1).until(
        Ec.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[1]/div[5]/button[1]"))
    )

    element.click()
finally:
    print("Done alcookies")
time.sleep(2)
buttomChoices = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[1]/section/div[3]/div[2]")
buttomChoices.click()
listOptions = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[1]/section/div[3]/ul")
Options = listOptions.find_elements(By.TAG_NAME, "li")
matchesLinks = []

for i in range(4):

    print(Options[i].text)
    Options[i].click()

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(50)
    driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")

    bigTable = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[1]/div[2]/section")
    smallList = bigTable.find_elements(By.CLASS_NAME, "fixtures__matches-list")
    print(len(smallList))
    for y in smallList:
        matches = y.find_elements(By.CLASS_NAME, "matchFixtureContainer")
        for m in matches:
            href = m.find_element(By.TAG_NAME, "div")
            matchesLinks.append(href.get_attribute("data-href"))
    buttomChoices.click()
    time.sleep(1)

for i in range(len(matchesLinks)):

    print(i)
    link = "https://" + matchesLinks[i][2:]

    print(link)
    driver.get(link)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(10)
    buttonStatus = driver.find_element(By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[1]/div/div/ul/li[3]")
    buttonStatus.click()
    matchBiografics = driver.find_element(By.XPATH, "/html/body/main/div/section[2]/div[2]/section/div[1]/div/div[1]")
    bios = matchBiografics.text.split("\n")
    # dateMatch = matchBiografics.find_element(By.CLASS_NAME, "matchDate renderMatchDateContainer")
    matchStad = matchBiografics.find_element(By.CLASS_NAME, "stadium").text
    Attendance = bios[len(bios) - 1][4:].replace(",", "")
    if Attendance[0].isalpha() or (Attendance[0] == " " and Attendance[1].isalpha()):
        Attendance = None
    ModDate = matchDate(bios[0])
    if matchStad.find(","):
        matchStad = matchStad.split(",")[0]

    time.sleep(1)
    table = driver.find_element(By.XPATH,
                                "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table")
    tbl = (table.text).split("\n")
    ddate = ModDate.split(" ")
    MMdate = ddate[2] + "-" + ddate[1] + "-" + ddate[0]
    season = ""
    if int(ddate[1]) >= 8 :
        season = ddate[2]  + "/" + str(int(ddate[2]) + 1)[2:]
    else:
        season = str(int(ddate[2]) - 1) + "/" + str(ddate[2])[2:]

    home = tbl[0]
    away = tbl[1]
    PossessionH = 0.0
    PossessionA = 0.0
    ShotsH = 0
    ShotsA = 0
    result = driver.find_element(By.XPATH, "/html/body/main/div/section[2]/div[2]/section/div[3]/div/div/div[1]/div["
                                           "2]/div/div").text
    Red_cardsH = 0
    Red_cardsA = 0
    Yellow_cardsH = 0
    Yellow_cardsA = 0
    Fouls_concededH = 0
    Fouls_concededA = 0
    for y in range(2, len(tbl)):
        x = tbl[y].split(" ")
        if "Possession" in x:
            index = x.index("Possession")
            PossessionH = float(x[index - 1])
            PossessionA = float(x[index + 2])
        if "target" in x:
            continue
        if "Shots" in x:
            index = x.index("Shots")
            ShotsH = int(x[index - 1])
            ShotsA = int(x[index + 1])
        if "Yellow" in x:
            index = x.index("Yellow")
            Yellow_cardsH = int(x[index - 1])
            Yellow_cardsA = int(x[index + 2])
        if "Red" in x:
            index = x.index("Red")
            Red_cardsH = int(x[index - 1])
            Red_cardA = int(x[index + 2])
        if "Fouls" in x:
            index = x.index("Fouls")
            Fouls_concededH = int(x[index - 1])
            Fouls_concededA = int(x[index + 2])

    goals = result.split("-")
    print("date: " + ModDate)
    print("Season: " + season)
    print("Stad: " + matchStad)
    print("Att: " + str(Attendance))
    print("Home: " + home)
    print("Away: " + away)
    print("Result: " + result)
    print("GoalsH: " + goals[0])
    print("GoalsA: " + goals[1])
    print("PossessionH: " + str(PossessionH))
    print("PossessionA: " + str(PossessionA))
    print("ShotsH: " + str(ShotsH))
    print("ShotsA: " + str(ShotsA))
    print("Red_cardsH: " + str(Red_cardsH))
    print("Red_cardsA: " + str(Red_cardsA))
    print("Yellow_cardsH: " + str(Yellow_cardsH))
    print("Yellow_cardsA: " + str(Yellow_cardsA))
    print("Fouls_concededH: " + str(Fouls_concededH))
    print("Fouls_concededA: " + str(Fouls_concededA))

    sql1 = "insert into `match_game` values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    val = (
    season, MMdate, result, home, away, matchStad, Attendance, goals[0], goals[1], PossessionH, PossessionA, ShotsH,
    ShotsA, Yellow_cardsH, Yellow_cardsA, Red_cardsH, Red_cardsA, Fouls_concededH, Fouls_concededA)
    try:
        mycursor.execute(sql1, val)
    except:
        print ("Double Row")


    mydp.commit()
