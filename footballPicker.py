from lxml import html
import requests
import footballFuncs as ff
from bs4 import BeautifulSoup
import os, json
import db

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

###################
# CBS Predictions #
###################
def getCBS(teamDict, week):
    page = requests.get(f'https://www.cbssports.com/nfl/picks/experts/straight-up/{week}/')

    tree = html.fromstring(page.content)
    soup = BeautifulSoup(page.content, 'lxml')

    teamsPre = tree.xpath('//p[@class="TableExpertPicks-pick "]/text()')
    teamsPost = tree.xpath('//p[@class="TableExpertPicks-pick TableExpertPicks-pick--checked"]/text()')

    tm = soup.find_all("span", class_="GameMatchup-teamAbbr")
    records = soup.find_all("span", class_="GameMatchup-teamRecord")

    teams = teamsPre + teamsPost

    for i in range(len(teams)):
        teams[i] = teams[i].strip()
        
        ff.addDict(teams[i], teamDict)
    
    for i in range(len(tm)):
        txt = ff.lengthenName(tm[i].text)
        teamDict[txt][4] = records[i].text

    return teamDict

# --------------------------------------------------

###############
# Sportsbooks #
###############

# Bet US Sportsbook
def getBetUS(teamDict):
    page0 = requests.get("https://www.betus.com.pa/sportsbook/nfl/")
    tree0 = html.fromstring(page0.content)

    teams0 = []

    for d in range(3):
        for g in range(15):
            d = str(d).zfill(2)
            g = str(g).zfill(2)
            
            Vteam = tree0.xpath(f'//a[@id="ctl00_ctl00_M_middle_ConstructorLines1_GameLines1_repHeaders_ctl{d}_repLines_ctl{g}_lnkTeamNameVisitorDesktop"]/text()')
            VteamML = tree0.xpath(f'//span[@id="ctl00_ctl00_M_middle_ConstructorLines1_GameLines1_repHeaders_ctl{d}_repLines_ctl{g}_lblBetVisitorMoneyLine"]/text()')
            
            Hteam = tree0.xpath(f'//a[@id="ctl00_ctl00_M_middle_ConstructorLines1_GameLines1_repHeaders_ctl{d}_repLines_ctl{g}_lnkTeamNameHomeDesktop"]/text()')
            HteamML = tree0.xpath(f'//span[@id="ctl00_ctl00_M_middle_ConstructorLines1_GameLines1_repHeaders_ctl{d}_repLines_ctl{g}_lblBetHomeMoneyLine"]/text()')
            

            if VteamML != []:
                teams0.append([Vteam[0], VteamML[0]])
            if HteamML != []:
                teams0.append([Hteam[0], HteamML[0]])

    if teams0 == []:
                print("\n\nBet US has broken links\n\n")

    for i in range(len(teams0)):
        teamDict[teams0[i][0]][2].append(teams0[i][1])

    ff.getOdds(teams0)

    for i in range(len(teams0)):
        teamDict[teams0[i][0]][1].append(teams0[i][1])
    return teamDict


#Bet Online Sportsbook
def getBetOnline(teamDict):
    page0 = requests.get("https://classic.betonline.ag/sportsbook/football/nfl", headers=headers)

    teams0 = []
    soup = BeautifulSoup(page0.content, 'lxml')
    names0 = soup.find_all("td", class_="col_teamname bdevtt")

    mls = soup.find_all("td", class_ = "odds bdevtt moneylineodds displayOdds")
    for i in range(len(mls)):
        teams0.append([names0[i].text.strip(), mls[i].text])
    
    if teams0 == []:
                print("\n\nBet US has broken links\n\n")
    
    for i in range(len(teams0)):
        teamDict[teams0[i][0]][2].append(teams0[i][1])

    ff.getOdds(teams0)

    for i in range(len(teams0)):
        teamDict[teams0[i][0]][1].append(teams0[i][1])
    return teamDict


# MyBookie
def getMyBookie(teamDict):
    page0 = requests.get("https://mybookie.ag/sportsbook/nfl/", headers=headers)

    teams0 = []
    soup = BeautifulSoup(page0.content, 'lxml')
    divs = soup.find_all("button", class_ = "lines-odds")

    for i in range(len(divs)):
        # print(divs)
        # print(teams0[i].text, divs[i].text)
        if divs[i]["data-wager-type"] == "ml" and divs[i]["data-sportid"] == "4":
            teams0.append([divs[i]["data-team"], divs[i]["data-odd"]])

    if teams0 == []:
                print("\n\nMy Bookie has broken links\n\n")
    
    for i in range(len(teams0)):
        teamDict[teams0[i][0]][2].append(teams0[i][1])

    ff.getOdds(teams0)

    for i in range(len(teams0)):
        
        teamDict[teams0[i][0]][1].append(teams0[i][1])
    return teamDict


# Draftkings
def getDraftkings(teamDict):
    page0 = requests.get("https://sportsbook.draftkings.com/leagues/football/nfl", headers=headers)

    teams0 = []
    soup = BeautifulSoup(page0.content, 'lxml')

    # print(soup.prettify())

    teams = soup.find_all("div", class_="event-cell__name-text")
    divs = soup.find_all("span", class_="sportsbook-odds american no-margin default-color")

    for i in range(min(26, len(divs))):
        t = teams[i].text
        if "Giants" in t:
            t = "NYG"
        elif "Jets" in t:
            t = "NYJ"
        elif "Rams" in t:
            t = "LAR"
        elif "Chargers" in t:
            t = "LAC"
        else:
            t = t[0:3].strip()
        t = ff.lengthenName(t)

        opp = ""
        if i % 2 == 1 and i > 0: # odd number thats not zero
            opp = teams[i-1].text
            if "Giants" in opp:
                opp = "NYG"
            elif "Jets" in opp:
                opp = "NYJ"
            elif "Rams" in opp:
                opp = "LAR"
            elif "Chargers" in opp:
                opp = "LAC"
            else:
                opp = opp[0:3].strip()
            opp = ff.lengthenName(opp.upper())
        else:
            opp = teams[i+1].text
            if "Giants" in opp:
                opp = "NYG"
            elif "Jets" in opp:
                opp = "NYJ"
            elif "Rams" in opp:
                opp = "LAR"
            elif "Chargers" in opp:
                opp = "LAC"
            else:
                opp = opp[0:3].strip()
            opp = ff.lengthenName(opp.upper())
        
        teams0.append([t, divs[i].text, opp])
    if teams0 == []:
                print("\n\nDraftkings has broken links\n\n")
    
    for i in range(len(teams0)):
        d = teams0[i][2]
        n = teams0[i][0]

        teamDict[n][3] = d

    for i in range(len(teams0)):
        teamDict[teams0[i][0]][2].append(teams0[i][1])
    
    ff.getOdds(teams0)

    for i in range(len(teams0)):
        
        teamDict[teams0[i][0]][1].append(teams0[i][1])
    return teamDict


# --------------------------------------------------

def fillDict(week=5):
    tDict = {
        # "Name": [CBS_PREDICTION, [Odds], [Moneylines], "opponent", "record"], 
        "Arizona Cardinals": [0, [], [], "", ""],
        "Atlanta Falcons": [0, [], [], "", ""],
        "Carolina Panthers": [0, [], [], "", ""],
        "Chicago Bears": [0, [], [], "", ""],
        "Dallas Cowboys": [0, [], [], "", ""],
        "Detroit Lions": [0, [], [], "", ""],
        "Green Bay Packers": [0, [], [], "", ""],
        "Los Angeles Rams": [0, [], [], "", ""],
        "Minnesota Vikings": [0, [], [], "", ""],
        "New Orleans Saints": [0, [], [], "", ""],
        "New York Giants": [0, [], [], "", ""],
        "Philadelphia Eagles": [0, [], [], "", ""],
        "San Francisco 49ers": [0, [], [], "", ""],
        "Seattle Seahawks": [0, [], [], "", ""],
        "Tampa Bay Buccaneers": [0, [], [], "", ""],
        "Washington Commanders": [0, [], [], "", ""],

        "Baltimore Ravens": [0, [], [], "", ""],
        "Buffalo Bills": [0, [], [], "", ""],
        "Cincinnati Bengals": [0, [], [], "", ""],
        "Cleveland Browns": [0, [], [], "", ""] ,
        "Denver Broncos": [0, [], [], "", ""],
        "Houston Texans": [0, [], [], "", ""],
        "Indianapolis Colts": [0, [], [], "", ""],
        "Jacksonville Jaguars": [0, [], [], "", ""],
        "Kansas City Chiefs": [0, [], [], "", ""],
        "Las Vegas Raiders": [0, [], [], "", ""],
        "Los Angeles Chargers": [0, [], [], "", ""],
        "Miami Dolphins": [0, [], [], "", ""],
        "New England Patriots": [0, [], [], "", ""],
        "New York Jets": [0, [], [], "", ""],
        "Pittsburgh Steelers": [0, [], [], "", ""],
        "Tennessee Titans": [0, [], [], "", ""]
    }

    
    tDict = getCBS(tDict, week)

    tDict = getBetUS(tDict)
    tDict = getBetOnline(tDict)
    tDict = getMyBookie(tDict)
    tDict = getDraftkings(tDict)
    return tDict

### DEBUG ###
tDict = fillDict()

# print dictionary of teams and their predictions/odds
def printDict(teamDict):
    for w in sorted(teamDict, key=teamDict.get, reverse=True):
        # break
        # print(w, teamDict[w][1], teamDict[w][2])
        # break
        if len(teamDict[w][1]) > 0:
            avg = round(sum(teamDict[w][1]) / len(teamDict[w][1]), 2)
            print(w, teamDict[w][0], avg)
        else:
            print(w, teamDict[w][0], teamDict[w][1])
        pass
# printDict(tDict)

def dumpToFile(week, teamDict):
    with open(f'{os.getcwd()}/Football Picker/week{week}-odds.txt', 'w') as f:
        json.dump(teamDict, f, indent=4)
# dumpToFile(week, tDict)

# printDict(tDict)
def footballPicker(week=1):
    """
    Scrapes individual team betting data from several
    sources and compiles it, where it is then sent to
    the database
    """
    
    # fill dictionary with calls to other functions
    tDict = fillDict(week)
    for i in tDict:
        """
        week: 0,
        name: NAME,
        cbs: CBSPRED,
        odds: ODDS,
        mline: MLINE,
        opponent: OPPONENT, 
        record RECORD
        """
        if len(tDict[i][1]) > 0:
            teamD = {
                "week": week,
                "name": i,
                "cbs_pred": tDict[i][0],
                "odds": tDict[i][1],
                "oddsAvg": round(sum(tDict[i][1]) / len(tDict[i][1]), 2),
                "mline": tDict[i][2],
                "opponent": tDict[i][3],
                "record": tDict[i][4]
            }
        else:
            teamD = {
                "week": week,
                "name": i,
                "cbs_pred": tDict[i][0],
                "odds": tDict[i][1],
                "oddsAvg": 0,
                "mline": tDict[i][2],
                "opponent": tDict[i][3],
                "record": tDict[i][4]
            }
        db.ins(teamD)