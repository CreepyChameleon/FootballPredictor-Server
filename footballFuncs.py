def addDict(team, dict):
    if team == "ARI":
        dict["Arizona Cardinals"][0] += 1
    elif team == "ATL":
        dict["Atlanta Falcons"][0] += 1
    elif team == "BAL":
        dict["Baltimore Ravens"][0] += 1
    elif team == "BUF":
        dict["Buffalo Bills"][0] += 1
    elif team == "CAR":
        dict["Carolina Panthers"][0] += 1
    elif team == "CHI":
        dict["Chicago Bears"][0] += 1
    elif team == "CIN":
        dict["Cincinnati Bengals"][0] += 1
    elif team == "CLE":
        dict["Cleveland Browns"][0] += 1
    elif team == "DAL":
        dict["Dallas Cowboys"][0] += 1
    elif team == "DEN":
        dict["Denver Broncos"][0] += 1
    elif team == "DET":
        dict["Detroit Lions"][0] += 1
    elif team == "GB":
        dict["Green Bay Packers"][0] += 1
    elif team == "HOU":
        dict["Houston Texans"][0] += 1
    elif team == "IND":
        dict["Indianapolis Colts"][0] += 1
    elif team == "JAC":
        dict["Jacksonville Jaguars"][0] += 1
    elif team == "KC":
        dict["Kansas City Chiefs"][0] += 1
    elif team == "LV":
        dict["Las Vegas Raiders"][0] += 1
    elif team == "LAC":
        dict["Los Angeles Chargers"][0] += 1
    elif team == "LAR":
        dict["Los Angeles Rams"][0] += 1
    elif team == "MIA":
        dict["Miami Dolphins"][0] += 1
    elif team == "MIN":
        dict["Minnesota Vikings"][0] += 1
    elif team == "NE":
        dict["New England Patriots"][0] += 1
    elif team == "NO":
        dict["New Orleans Saints"][0] += 1
    elif team == "NYG":
        dict["New York Giants"][0] += 1
    elif team == "NYJ":
        dict["New York Jets"][0] += 1
    elif team == "PHI":
        dict["Philadelphia Eagles"][0] += 1
    elif team == "PIT":
        dict["Pittsburgh Steelers"][0] += 1
    elif team == "SF":
        dict["San Francisco 49ers"][0] += 1
    elif team == "SEA":
        dict["Seattle Seahawks"][0] += 1
    elif team == "TB":
        dict["Tampa Bay Buccaneers"][0] += 1
    elif team == "TEN":
        dict["Tennessee Titans"][0] += 1
    elif team == "WAS":
        dict["Washington Football Team"][0] += 1

def getOdds(teams):
    for i, t in enumerate(teams):
        ml = t[1]
        odds = 0
        if ml[0] == "-":
            ml = int(ml[1:])
            odds = ml / (ml + 100)*100
        elif ml[0] == "+":
            ml = int(ml[1:])
            odds = 100 / (ml + 100)*100
        else:
            ml = int(ml)
            odds = 100 / (ml + 100)*100
        teams[i][1] = round(odds, 2)

def lengthenName(team):
    name = ""
    if team == "ARI":
        name = "Arizona Cardinals"
    elif team == "ATL":
        name = "Atlanta Falcons"
    elif team == "BAL":
        name = "Baltimore Ravens"
    elif team == "BUF":
        name = "Buffalo Bills"
    elif team == "CAR":
        name = "Carolina Panthers"
    elif team == "CHI":
        name = "Chicago Bears"
    elif team == "CIN":
        name = "Cincinnati Bengals"
    elif team == "CLE":
        name = "Cleveland Browns"
    elif team == "DAL":
        name = "Dallas Cowboys"
    elif team == "DEN":
        name = "Denver Broncos"
    elif team == "DET":
        name = "Detroit Lions"
    elif team == "GB":
        name = "Green Bay Packers"
    elif team == "HOU":
        name = "Houston Texans"
    elif team == "IND":
        name = "Indianapolis Colts"
    elif team == "JAC" or team == "JAX":
        name = "Jacksonville Jaguars"
    elif team == "KC":
        name = "Kansas City Chiefs"
    elif team == "LV":
        name = "Las Vegas Raiders"
    elif team == "LAC":
        name = "Los Angeles Chargers"
    elif team == "LAR":
        name = "Los Angeles Rams"
    elif team == "MIA":
        name = "Miami Dolphins"
    elif team == "MIN":
        name = "Minnesota Vikings"
    elif team == "NE":
        name = "New England Patriots"
    elif team == "NO":
        name = "New Orleans Saints"
    elif team == "NYG":
        name = "New York Giants"
    elif team == "NYJ":
        name = "New York Jets"
    elif team == "PHI":
        name = "Philadelphia Eagles"
    elif team == "PIT":
        name = "Pittsburgh Steelers"
    elif team == "SF":
        name = "San Francisco 49ers"
    elif team == "SEA":
        name = "Seattle Seahawks"
    elif team == "TB":
        name = "Tampa Bay Buccaneers"
    elif team == "TEN":
        name = "Tennessee Titans"
    elif team == "WAS":
        name = "Washington Football Team"
    else:
        print("ERROR", team)
    return name