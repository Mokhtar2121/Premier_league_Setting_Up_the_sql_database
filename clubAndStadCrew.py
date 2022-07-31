from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pymysql
import mysql.connector

mydp = mysql.connector.connect(host="localhost", user="root", password="Qaisaleh12010@auc", database="premier_league",
                               auth_plugin='mysql_native_password')

if (mydp):
    print("connected")
    mycursor = mydp.cursor()
else:
    print("Notconnected")

PATH = Service("C:\Program Files\chromedriver.exe")
driver = webdriver.Chrome(service=PATH)
driver.get("https://www.premierleague.com/clubs")
driver.implicitly_wait(100)
driver.set_page_load_timeout(100)
time.sleep(5)
cookies = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[5]/button[1]")
cookies.click()
main = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div/div[3]/div/table")
clubs = main.find_element(By.TAG_NAME, "tbody")
table = clubs.find_elements(By.TAG_NAME, "tr")

Stadsites = []
ClubsNames = []
ClubsStadName = []

for t in table:
    site = t.find_element(By.CLASS_NAME, "team").find_element(By.TAG_NAME, "a")
    site1 = site.get_attribute("href")
    ClubsNames.append(site.text)

    sql = ("insert into club values (%s,%s)")
    clubdata = (site.text, site1)
    mycursor.execute(sql, clubdata)
    mydp.commit()

    ClubName = t.find_element(By.CLASS_NAME, "clubName")
    ClubStad = t.find_element(By.CLASS_NAME, "venue").find_element(By.TAG_NAME, "a")
    ClubsStadName.append(ClubStad.text)
    Stadsites.append(ClubStad.get_attribute("href"))
    spechialCases={"https://www.premierleague.com/clubs/24/Swindon-Town/stadium",
                         "https://www.premierleague.com/clubs/22/Wimbledon/stadium",
                         "https://www.premierleague.com/clubs/34/Fulham/stadium"}

for i in range(len(Stadsites)):
    if Stadsites[i] in spechialCases:
        continue
    driver.get(Stadsites[i])
    driver.implicitly_wait(50)
    driver.set_page_load_timeout(50)
    infoButton = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[2]/div/ul/li[2]")
    infoButton.click()

    bigText = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[3]/div[2]")

    data = bigText.text.split("\n")
    modifiedData = []
    for i2 in data:
        row = i2.split(": ")
        for j in row:
            modifiedData.append(j)

    address = ""
    cap = 0
    BuiltDate = 0
    leng = 0
    width = 0

    if "Capacity" in modifiedData:
        cap = int(modifiedData[modifiedData.index("Capacity") + 1].replace(",", ""))
    else:
        if modifiedData[0].find("capacity"):
            cap = int(modifiedData[1].replace(",", ""))
    if "Built" in modifiedData:
        BuiltDate = int(modifiedData[modifiedData.index("Built") + 1])
    else:
        if ("Opened" in modifiedData) or ("Opened" in modifiedData):
            BuiltDate = int(modifiedData[modifiedData.index("Opened") + 1])
        else:
            print("No date for " + ClubsStadName[i])

    if "Pitch size" in modifiedData:
        dimensions = modifiedData[modifiedData.index("Pitch size") + 1].split(" x ")
        strLeng = dimensions[0][:-1]
        if (strLeng.find(".")):
            len = strLeng.split(".")
            leng = int(len[0])
        else:
            leng = int(strLeng)

        strWid = dimensions[1][:-1]
        if (strWid.find(".")):
            wid = strWid.split(".")
            width = int(wid[0].replace("m", ""))
        else:
            width = int(strWid)

    if "Stadium address" in modifiedData:
        address = modifiedData[modifiedData.index("Stadium address") + 1]
    print("Name: " + ClubsStadName[i])
    print("Club: " + ClubsNames[i])
    print("address: " + address)
    print("cap: " + str(cap))
    print("width: " + str(width))
    print("leng: " + str(leng))
    print("Date: " + str(BuiltDate))

    sql = ("insert into stadium values (%s,%s,%s,%s,%s,%s,%s)")
    StaddData = (ClubsStadName[i], ClubsNames[i], address, cap, width
                 , leng, BuiltDate)
    mycursor.execute(sql, StaddData)
    mydp.commit()

    # # if (("Built:" in data) ||):
    #     print("c: "+data[data.index("Capacity:") + 1])
    # data = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[3]/div[2]")
    # info = data.find_elements(By.TAG_NAME, "p")
    # Capacity = (info[0].text).split(":")
    # if (i==0):
    #     builtDate = info[2].text.split(": ")
    #     Pitch_size = info[3].text.split(": ")
    #     address = info[4].text.split(":")
    # else:
    #     builtDate = info[1].text.split(": ")
    #     Pitch_size = info[2].text.split(": ")
    #     address = info[3].text.split(":")
    #
    #
    # cap= Capacity[1].replace(",", "")
    #
    # print(cap)
    # bultdatared=builtDate[1]
    # print(bultdatared)
    # dimensions = Pitch_size[1].split(" x " )
    # leng = dimensions[0][:-1]
    # width = dimensions[0][:-1]
    # print(leng)
    # print (width)
    # new_address = address[1][1:]
    # # print(new_address)
    # sql = ("insert into stadium values (%s,%s,%s,%s,%s,%s,%s)")
    # StaddData = (ClubsStadName[i], ClubsNames[i],new_address,int(cap), int(width)
    #              , int(leng), int(bultdatared))
    # mycursor.execute(sql,StaddData)
    # mydp.commit()
