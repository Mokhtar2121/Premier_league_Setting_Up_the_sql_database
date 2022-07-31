import time
import datetime

import mysql.connector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
mydb = mysql.connector.connect(  # connection to the DB
    host="localhost",
    user="root",
    password="Fireandblood",
    database="premier_league"
)
cur = mydb.cursor()
driver = webdriver.Chrome(ChromeDriverManager().install())


#  utility functions
def get_match_date_month(input):  # the fucntion takes a full date and retuns the month and day in integer values
    x = False
    day = ""
    month = ""
    input = input[3:].strip()
    for i in input:
        if i.isdigit() and x == False:
            day += i
        else:
            x = True
        if i.isalpha(): month += i
    month = time.strptime(month, '%b').tm_mon

    return (locale.atoi(day), month)


def extractDate(input):  # takes input string and returns the formatted date accpeted by sql
    day = ""
    year = ""
    month = ""
    slashCount = 0
    for i in input:
        if i == '/': slashCount += 1
        if i.isdigit():
            if slashCount == 0:
                day += i
            elif slashCount == 1:
                month += i
            else:
                year += i

    return datetime.datetime(locale.atoi(year), locale.atoi(month), locale.atoi(day))


#  utitlity functions :
def removecommas(input):
    input = input.strip()
    ans = ""
    for i in input:
        if i != ',' and i.isdigit(): ans += i

    return int(ans)


def removechars(input):  # clean a string and return a float
    input = input.strip()
    ans = ""
    for i in input:
        if i.isdigit(): ans += i

    return float(ans)


def checkattribute(att, webDriver):  # check if a web element has an attrbute named att
    try:
        tmp = webDriver.get_attribute(att)

    except:
        return False
    return True  #


def check_if_clickcable(xpth, webdrive):  # check if a web element is clicable or not yet, and waits for it 10 seconds
    try:
        WebDriverWait(webdrive, 10).until(EC.element_to_be_clickable(By.XPATH, xpth))
    except:
        print("ignored")
        return False
    return True


def FullnameDivider(input):  ## divide into first name and last name

    first = ""
    second = ""
    cur = False
    for i in input:
        if (i == ' '): cur = True
        if (cur == False):
            first += i
        else:
            second += i

    return (first, second)


def addressdivider(Faddress):
    countComa = 0
    city = ""
    street = ""
    for i in Faddress:
        if i == ',': countComa += 1
        if (countComa == 2): city += i
        if (countComa < 2): street += i
    return (city, street)


def trim_team_name(input):  # extarct team name in the player detais page

    if input == "Brighton and Hove Albion": return input
    ans = ""
    countWords = 0

    for i in input:
        if i == ' ': countWords += 1
        if i == '(' or countWords > 1: break
        if i.isalpha() or i.isspace(): ans += i
    if ans[-1] == ' ': ans = ans[:-1]
    return ans


def hasstrong(j):  # check if web elment has an elemnt with a tag = string
    try:
        WebDriverWait(j, 2).until(EC.presence_of_element_located((By.TAG_NAME, "strong")))
    except:
        return False
    return True


def pitch_divider(string):  # divide the string into pitch lenght and width
    a = ""
    b = ""
    x = False
    for i in string:
        if i == 'x': x = True
        if (not x):
            if (i.isdigit()): a += i
        else:
            if i.isdigit(): b += i
    return (a, b)


def check_exists_by_xpath(xpath, webDriver):  # chck if a web element exsits or not after 7 seconds of wait
    try:
        WebDriverWait(webDriver, 3).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        print("ignore")
        return False

    return True


def results():  # crawling over the results of the amtches

    url = 'https://www.premierleague.com/results?co=1&se=418&cl=-1'
    driver.get(url)
    time.sleep(15)  # sleep until cookie notifcaiton is cancelled
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scrll unitl end of page
    time.sleep(20)
    # if the div targed nor found ignreo
    if (check_exists_by_xpath("/html/body/main/div[3]/div[1]/div[2]/section", driver)):
        main = driver.find_element(by=By.XPATH, value="/html/body/main/div[3]/div[1]/div[2]/section")
    else:
        return 0

    rows = main.find_elements(by=By.CLASS_NAME, value="matchFixtureContainer")
    links = []
    for i in rows:
        link = i.find_element(by=By.TAG_NAME, value="div").get_attribute("data-href")
        link = 'https://' + link[2:]

        links.append(link)
    for i in links:  # navigating to the deeatls of each match
        driver.get(i)
        time.sleep(4)

        if check_exists_by_xpath("/html/body/main/div/section[2]/div[2]/div[2]/div[1]/div/div/ul",
                                 driver) == False: continue
        # clicking the stats tab
        driver.find_element(by=By.XPATH,
                            value="/html/body/main/div/section[2]/div[2]/div[2]/div[1]/div/div/ul/li[3]").click()
        time.sleep(4)
        # fetching all the needed attribte
        totalGoals = driver.find_element(by=By.XPATH,
                                         value="/html/body/main/div/section[2]/div[2]/section/div[3]/div/div/div[1]/div[2]/div/div").text
        homeTeam_goals = totalGoals[0]
        awayTeam_goals = totalGoals[-1]
        homeTeam = driver.find_element(by=By.XPATH,
                                       value="/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/thead/tr/th[1]").text
        awayTeam = driver.find_element(by=By.XPATH,
                                       value="/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/thead/tr/th[3]").text
        fulldate = driver.find_element(by=By.XPATH,
                                       value="/html/body/main/div/section[2]/div[2]/section/div[1]/div/div[1]/div[1]").text
        season = locale.atoi(fulldate[-4:])
        month = get_match_date_month(fulldate)[1]
        day = get_match_date_month(fulldate)[0]
        formattedDate = datetime.datetime(season, month, day)
        table = driver.find_element(by=By.XPATH,
                                    value="/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody")
        divs = table.find_elements(by=By.TAG_NAME, value="tr")

        homeTeam_possesion = '0'
        homeTeam_yellowcards = '0'
        awayTeam_yellowcards = '0'
        numOfShotsHomeTeam = '0'
        numOfShotsAwayTeam = '0'
        numOfRedCardsHomeTeam = '0'
        numOfRedCardsAwayTeam = '0'

        numOfFoulsHomeTeam = '0'
        numOfFoulsAwayTeam = '0'

        for j in divs:  # navigagin to the rows of ths status paper // each row has three attribues , and the middle is a stirng that idneifty the type of the statsi
            attributes = j.find_elements(by=By.TAG_NAME, value="p")
            if attributes[1].text.strip() == "Possession %":
                homeTeam_possesion = attributes[0].text

            if attributes[1].text.strip() == "Shots":
                numOfShotsHomeTeam = attributes[0].text
                numOfShotsAwayTeam = attributes[2].text

            if attributes[1].text.strip() == "Yellow cards":
                awayTeam_yellowcards = attributes[2].text
                homeTeam_yellowcards = attributes[0].text

            if attributes[1].text.strip() == "Red cards ":
                numOfRedCardsAwayTeam = attributes[2].text
                numOfRedCardsHomeTeam = attributes[0].text

            if attributes[1].text.strip() == "Fouls conceded":
                numOfFoulsAwayTeam = attributes[2].text
                numOfFoulsHomeTeam = attributes[0].text

        try:
            cur.execute(
                'insert into `match` (home_club,away_club,date_of_match,match_season,number_of_goals_home_team,number_of_goals_away_team,number_of_shots_home_team, number_of_shots_away_team,number_of_fouls_home_team,number_of_fouls_away_team,number_of_redcards_away_team,number_of_yellow_away_team,number_of_redcards_home_team,number_of_yellow_home_team,possesion_of_home_team)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (homeTeam, awayTeam, formattedDate, season, homeTeam_goals, awayTeam_goals, numOfShotsHomeTeam,
                 numOfShotsAwayTeam, numOfFoulsHomeTeam, numOfFoulsAwayTeam, numOfRedCardsAwayTeam,
                 awayTeam_yellowcards, numOfRedCardsHomeTeam, homeTeam_yellowcards, homeTeam_possesion))
            mydb.commit()
        except:
            print("ignore query, dublicate")


def plays_for():
    url = 'https://www.premierleague.com/players?se=274&cl=-1'
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(14)

    main2 = driver.find_element(by=By.XPATH, value="/html/body/main/div[2]/div[1]/div/div/table/tbody")

    rows = main2.find_elements(by=By.TAG_NAME, value="tr")
    players = []
    for i in rows:
        # getting then ame and nationality and postiion from the main page
        link = i.find_element(by=By.CLASS_NAME, value="playerName").get_attribute("href")
        Fname = i.find_element(by=By.CLASS_NAME, value="playerName").text
        position = i.find_element(by=By.CLASS_NAME, value='hide-s').text

        nationality = i.find_element(by=By.CLASS_NAME, value='playerCountry').text
        firstName = FullnameDivider(Fname)[0]
        players.append((link, firstName, nationality, position))

    for i in players:  # navigating throught the detaied pages on players
        driver.get(i[0])
        if (check_exists_by_xpath("/html/body/main/div[3]/div/div/div[3]/table/tbody", driver)):
            table = driver.find_element(by=By.XPATH, value="/html/body/main/div[3]/div/div/div[3]/table/tbody")
        else:
            continue
        rows = table.find_elements(by=By.CLASS_NAME, value="table")
        # add an exception here

        counter = 4
        for j in rows:
            if (counter == 0): break
            team = j.find_element(by=By.CLASS_NAME, value="team").text
            team = trim_team_name(team)
            season = j.find_element(by=By.CLASS_NAME, value="season").text[5:]
            try:
                cur.execute('insert into plays_for values (%s, %s,%s,%s,%s)', (i[1], i[3], i[2], team, season))
                mydb.commit()

            except:
                print("ignore dubilcate")
            counter -= 1


def crawl_player_table():
    # run the funciton for the URIs of the last four seasons
    url = 'https://www.premierleague.com/players?se=210&cl=-1'
    driver.get(url)
    time.sleep(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(40)

    main2 = driver.find_element(by=By.XPATH, value="/html/body/main/div[2]/div[1]/div/div/table/tbody")

    rows = main2.find_elements(by=By.TAG_NAME, value="tr")
    players = []
    for i in rows:
        link = i.find_element(by=By.CLASS_NAME, value="playerName").get_attribute("href")
        Fname = i.find_element(by=By.CLASS_NAME, value="playerName").text
        position = i.find_element(by=By.CLASS_NAME, value='hide-s').text

        nationality = i.find_element(by=By.CLASS_NAME, value='playerCountry').text
        firstName = FullnameDivider(Fname)[0]
        lastName = FullnameDivider(Fname)[1]
        players.append((link, position, nationality, firstName, lastName))

    for i in players:
        driver.get(i[0])

        height = None
        DOB = None

        if (check_exists_by_xpath("/html/body/main/div[3]/div/div/div[1]/section/div/ul[3]/li[1]/div[2]", driver)):
            height = driver.find_element(by=By.XPATH,
                                         value="/html/body/main/div[3]/div/div/div[1]/section/div/ul[3]/li[1]/div[2]").text
            height = (removechars(height))
        if (check_exists_by_xpath("/html/body/main/div[3]/div/div/div[1]/section/div/ul[2]/li/div[2]", driver)):
            DOB = driver.find_element(by=By.XPATH,
                                      value="/html/body/main/div[3]/div/div/div[1]/section/div/ul[2]/li/div[2]").text
            DOB = DOB[:10]
            DOB = extractDate(DOB)

        try:
            cur.execute(
                'insert into player(f_name,l_name,date_of_birth,position,nationality,height) values (%s,%s,%s,%s,%s,%s)  ',
                (i[3], i[4], DOB, i[1], i[2], height))
            mydb.commit()
        except:
            print("ignore dubilcate insert")


def stadiums():  # the funciton crawl over all the staduims throught the links to each stadium
    driver.get("https://www.premierleague.com/clubs")
    time.sleep(5)
    table = driver.find_element(by=By.XPATH, value="/html/body/main/div[2]/div/div/div[3]/div/table/tbody")
    rows = table.find_elements(by=By.TAG_NAME, value="tr")
    links = []
    for i in rows:  # getting the names to the staduim and links to the details page
        links.append((i.find_element(by=By.CLASS_NAME, value="venue").find_element(by=By.TAG_NAME,
                                                                                   value="a").get_attribute("href"),
                      i.find_element(by=By.CLASS_NAME, value="venue").find_element(by=By.TAG_NAME, value="a").text))

    for i in links:
        driver.get(i[0])
        if (check_exists_by_xpath("/html/body/main/div[3]/div[2]/div/ul", driver) == False): continue

        driver.find_element(by=By.XPATH, value="/html/body/main/div[3]/div[2]/div/ul/li[2]").click()
        # click the stasium button

        page = driver.find_element(by=By.XPATH, value="/html/body/main/div[3]/div[3]/div[2]")
        rows = page.find_elements(by=By.TAG_NAME, value="p")
        capacity = None
        pitch = None
        fulladdress = None
        name = i[1]
        for j in rows:
            if hasstrong(j):
                if (j.find_element(by=By.TAG_NAME, value="strong").text == "Capacity:"): capacity = j.text
                if (j.find_element(by=By.TAG_NAME, value="strong").text == "Stadium address:"): fulladdress = j.text
                if (j.find_element(by=By.TAG_NAME, value="strong").text == "Pitch size:"): pitch = j.text

        cityAddress = None
        streetAdress = None
        lenght = None
        width = None
        if (pitch != None):
            lenght = pitch_divider(pitch)[0]
            width = pitch_divider(pitch)[1]
        if (fulladdress != None):
            cityAddress = addressdivider(fulladdress[17:])[0][2:]
            streetAdress = addressdivider(fulladdress[17:])[1]

        if (capacity != None):
            capacity = removecommas(str(capacity[10:]))

        cur.execute(
            "insert into stadium (name,capacity,pitch_width, pitch_height,address_city,address_street) values (%s,%s,%s,%s,%s,%s)",
            (name, capacity, width, lenght, cityAddress, streetAdress))
        mydb.commit()


def clubs():
    driver.get("https://www.premierleague.com/clubs")
    time.sleep(6)
    table = driver.find_element_by_xpath("/html/body/main/div[2]/div/div/div[3]/div/table/tbody")
    rows = table.find_elements(by=By.TAG_NAME, value="tr")
    allclubs = []
    for i in rows:
        name = i.find_element(by=By.CLASS_NAME, value="team").text
        staduim = i.find_element(by=By.CLASS_NAME, value="venue").text
        link = i.find_element(by=By.CLASS_NAME, value="venue").find_element(by=By.TAG_NAME, value="a").get_attribute(
            "href")
        allclubs.append((name, staduim, link))

    for i in allclubs:
        name = i[0]
        stadium = i[1]
        driver.get(i[2])
        website = ""
        if check_exists_by_xpath("/html/body/main/header/div[2]/div/div/div[2]/div[2]/a",
                                 driver):   website = driver.find_element(by=By.XPATH,
                                                                          value="/html/body/main/header/div[2]/div/div/div[2]/div[2]/a").get_attribute(
            "href")
        cur.execute("insert into club values (%s,%s,%s)", (name, website, stadium))
        mydb.commit()


plays_for()
time.sleep(20)
driver.quit()


