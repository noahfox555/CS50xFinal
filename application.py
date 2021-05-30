from flask import Flask, render_template, request
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///baseball.db")

@app.route("/")
def index():
    return render_template("newsearch.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        first_name = request.form.get("firstname").strip().lower()
        # get the first part typed in
        last_name = request.form.get("lastname").strip().lower()
        # get the second part typed in

        playerid = db.execute("Select playerID From people where nameFirst=:first_name and nameLast=:last_name", first_name=first_name, last_name=last_name)
        first_name=first_name.capitalize()
        last_name=last_name.capitalize()

        if playerid == []:
            return render_template("failure.html", first_name=first_name, last_name=last_name)
        playerid = playerid[0]
        playerid = playerid['playerID']
# get position of player
        position = db.execute("Select POS, people.playerID From people, fielding where people.playerID=:playerid and people.playerID=fielding.playerID", playerid=playerid)
        length = len(position)
        i = 0
        while i < length:
            position[i]['positions'] = set([position[i]['POS']])
            i += 1
        i = 0
        while i < length - 1:
            if position[i]['playerID'] == position[i+1]['playerID']:
                position[i]['positions'] = position[i]['positions'] | position[i+1]['positions']
                position.remove(position[i+1])
                length -= 1
                i -= 1
            i += 1

        i = 0
        while i < length:
            s = ', '
            position[i]['positions'] = s.join(position[i]['positions'])
            position = position[i]['positions']
            i += 1
# query for hitter which is used in both cases
# determine batting average
        hitter = db.execute("Select birthYear, nameFirst, nameLast, batting.yearID, weight, height, bats, throws, batting.G, batting.AB, batting.R, batting.H, batting.'2B', batting.'3B', batting.HR, batting.RBI, batting.SB, batting.BB, batting.SO, batting.teamID, teams.name From people, batting, teams where people.playerID=:playerid and batting.playerID=:playerid and people.playerID = batting.playerID and teams.teamID=batting.teamID and batting.yearID=teams.yearID", playerid=playerid)
        length = len(hitter)
        i = 0
        while i < length:
            hitter[i]['average'] = "n/a"
            if hitter[i]['AB'] == 0:
                hitter[i]['average'] == "n/a"
            else:
                hitter[i]['average'] = str(format(hitter[i]['H']/hitter[i]['AB'], '.3f')).lstrip('0')
                if hitter[i]['average'] == '.0':
                    hitter[i]['average'] == '.000'
            i += 1
# calculate total columns
        i = 0
        years = length
        gamesplayed = 0
        totalab = 0
        totalruns = 0
        totalhits = 0
        totalhr = 0
        totalrbi = 0
        totalsb = 0
        totalbb = 0
        totalso = 0
        totalaverage = 0
        totalavg = 0
        while i < length:
            gamesplayed += hitter[i]['G']
            totalab += hitter[i]['AB']
            totalruns += hitter[i]['R']
            totalhits += hitter[i]['H']
            totalhr += hitter[i]['HR']
            totalrbi += hitter[i]['RBI']
            if hitter[i]['SB'] == None:
                pass
            else:
                totalsb += hitter[i]['SB']
            totalbb += hitter[i]['BB']
            if hitter[i]['SO'] == None:
                pass
            else:
                totalso += hitter[i]['SO']
            i+=1
        totalavg = str(format(totalhits/totalab, '.3f')).lstrip('0')
#determine which route player should go to based on position
        if 'P' in position:
            pitcher = db.execute("Select birthYear, WP, nameFirst, nameLast, pitching.IPouts, pitching.yearID, weight, height, bats, throws, pitching.W, pitching.L, pitching.G, pitching.GS, pitching.SHO, pitching.SV, pitching.H, pitching.ER, pitching.HR, pitching.BB, pitching.SO, pitching.BAOpp, pitching.ERA, teams.name From people, pitching, teams where people.playerID=:playerid and pitching.playerID=:playerid and people.playerID = pitching.playerID and teams.teamID=pitching.teamID and pitching.yearID=teams.yearID", playerid=playerid)
            length = len(pitcher)
            i = 0
            while i < length:
                pitcher[i]['IP'] = format(pitcher[i]['IPouts']/3, '.2f')
                i += 1
            i = 0
            pyears = length
            pwins = 0
            plosses = 0
            pgames = 0
            pstarts = 0
            IP = 0
            pshutouts = 0
            psaves = 0
            phits = 0
            per = 0
            phr = 0
            pbb = 0
            pso = 0
            wp = 0
            while i < length:
                if pitcher[i]['W'] == 'n/a':
                    pass
                else:
                    pwins += pitcher[i]['W']

                IP += round(pitcher[i]['IPouts']/3, 1)
                plosses += pitcher[i]['L']
                pgames += pitcher[i]['G']
                pstarts += pitcher[i]['GS']
                pshutouts += pitcher[i]['SHO']
                psaves += pitcher[i]['SV']
                phits += pitcher[i]['H']
                per += pitcher[i]['ER']
                phr += pitcher[i]['HR']
                pbb += pitcher[i]['BB']
                pso += pitcher[i]['SO']
                wp += pitcher[i]['WP']
                i+=1
            ERA = format(per/(IP/9), '.3')
            for info in pitcher:
                first = info['nameFirst']
                last = info['nameLast']
                if info['weight'] == None:
                    weight = 'n/a'
                else:
                    weight = info['weight']
                if info['bats'] == None:
                    bats = 'n/a'
                else:
                    bats = info['bats']
                if info['height'] == None:
                    height = 'n/a'
                else:
                    height = round(info['height']/12, 2)
                if info['throws'] == None:
                    throws = 'n/a'
                else:
                    throws = info['throws']
                if info['birthYear'] == None:
                    birthyear = 'n/a'
                else:
                    birthyear = info['birthYear']
            return render_template("pitchers.html", wp=wp, ERA=ERA, IP=IP, pyears=pyears, pwins=pwins, plosses=plosses, pgames=pgames, pstarts=pstarts, pshutouts=pshutouts, psaves=psaves, phits=phits, per=per, phr=phr, pbb=pbb, pso=pso, totalavg=totalavg, totalab=totalab, totalruns=totalruns, totalhits=totalhits, totalhr=totalhr, totalrbi=totalrbi, totalsb=totalsb, totalbb=totalbb, totalso=totalso, years=years, gamesplayed=gamesplayed, birthyear=birthyear, first_name=first_name, last_name=last_name, hitter=hitter, pitcher=pitcher, position=position, first=first, last=last, weight=weight, height=height, bats=bats, throws=throws)
        else:
            for info in hitter:
                first = info['nameFirst']
                last = info['nameLast']
                if info['weight'] == None:
                    weight = 'n/a'
                else:
                    weight = info['weight']
                if info['bats'] == None:
                    bats = 'n/a'
                else:
                    bats = info['bats']
                if info['height'] == None:
                    height = 'n/a'
                else:
                    height = round(info['height']/12, 2)
                if info['throws'] == None:
                    throws = 'n/a'
                else:
                    throws = info['throws']
                if info['birthYear'] == None:
                    birthyear = 'n/a'
                else:
                    birthyear = info['birthYear']
            return render_template("positionplayers.html", totalavg=totalavg, totalab=totalab, totalruns=totalruns, totalhits=totalhits, totalhr=totalhr, totalrbi=totalrbi, totalsb=totalsb, totalbb=totalbb, totalso=totalso, years=years, gamesplayed=gamesplayed, birthyear=birthyear, first_name=first_name, last_name=last_name, hitter=hitter, position=position, first=first, last=last, weight=weight, height=height, bats=bats, throws=throws)
    else:
        return render_template("newsearch.html")

# select player id (which they would be searching up)
# use that player id to query batting or pitchihng and people and spit out that information

@app.route("/failure", methods=["GET", "POST"])
def failure():
    if request.method == "POST":
        databasehitters = db.execute("Select nameFirst, nameLast, birthYear From people ORDER BY birthYear ASC")
        return ("/search")

@app.route("/database", methods=["GET", "POST"])
def database():
    if request.method == "GET":
        database = db.execute("Select nameFirst, nameLast, birthYear From people ORDER BY birthYear ASC")
        populate = len(database)
        return render_template("/database.html", database=database, populate=populate)
    else:
        dropdown1 = request.form.get('dropdown')
        dropdown2 = request.form.get('dropdown2')
        dropdown3 = request.form.get('dropdown3')
        if dropdown1 == 'select' and dropdown2 == 'select' and dropdown3 == 'select':
            database = db.execute("Select nameFirst, nameLast, birthYear From people ORDER BY birthYear ASC")
            populate = len(database)
            return render_template("/database.html", database=database, populate=populate)
# just dropdown 1
        elif dropdown1 != 'select' and dropdown2 == 'select' and dropdown3 == 'select':
            print(dropdown1)
            if dropdown1 == 'nameFirst' or dropdown1 == 'nameLast':
                search = request.form.get('search').strip().lower()
            elif dropdown1 == 'POS':
                search = request.form.get('search').strip().upper()
            else:
                search = request.form.get('search').strip().upper()

            player = db.execute("Select DISTINCT nameFirst, nameLast, birthYear, throws, bats, POS, name, people.playerID From people, fielding, teams Where " + dropdown1 + "='" + search + "' and people.playerID=fielding.playerID and fielding.teamID=teams.teamID and fielding.yearID=teams.yearID order by nameLast ASC Limit 5000")
            if not search or player == []:
                database = db.execute("Select nameFirst, nameLast, birthYear From people ORDER BY birthYear ASC")
                populate = len(database)
                return render_template("/databasefailure.html", database=database, populate=populate)
            else:
                length = len(player)
                i = 0
                while i < length:
                    player[i]['teams'] = set([player[i]['name']])
                    player[i]['positions'] = set([player[i]['POS']])
                    i += 1
                i = 0
                while i < length - 1:
                    if player[i]['playerID'] == player[i+1]['playerID']:
                        player[i]['positions'] = player[i]['positions'] | player[i+1]['positions']
                        player[i]['teams'] = player[i]['teams'] | player[i+1]['teams']
                        player.remove(player[i+1])
                        length -= 1
                        i -= 1
                    i += 1

                i = 0
                while i < length:
                    s = ', '
                    player[i]['teams'] =s.join(player[i]['teams'])
                    player[i]['positions'] = s.join(player[i]['positions'])
                    print(player[i]['teams'])
                    i += 1
                populate = len(player)
                return render_template('/databaseplayer.html', player=player, populate=populate)

# dropdown 1 and 2
        elif dropdown1 != 'select' and dropdown2 != 'select' and dropdown3 == 'select':
            if dropdown1 == 'nameFirst' or dropdown1 == 'nameLast':
                search = request.form.get('search').strip().lower()
            elif dropdown1 == 'POS':
                search = request.form.get('search').strip().upper()
            else:
                search = request.form.get('search').strip().capitalize()

            if dropdown2 == 'nameFirst' or dropdown2 == 'nameLast':
                search2 = request.form.get('search2').strip().lower()
            elif dropdown2 == 'POS':
                search2 = request.form.get('search2').strip().upper()
            else:
                search2 = request.form.get('search2').strip().capitalize()
            player = db.execute("Select DISTINCT nameFirst, nameLast, birthYear, throws, bats, POS, name, people.playerID From people, fielding, teams Where " + dropdown1 + "='" + search + "' and " + dropdown2 + "='" + search2 +"' and people.playerID=fielding.playerID and fielding.teamID=teams.teamID and fielding.yearID=teams.yearID order by nameLast ASC Limit 5000")
            if not search or not search2 or player == []:
                database = db.execute("Select nameFirst, nameLast, birthYear From people ORDER BY birthYear ASC")
                return render_template("/databasefailure.html", database=database)
            else:
                length = len(player)
                i = 0
                while i < length:
                    player[i]['teams'] = set([player[i]['name']])
                    player[i]['positions'] = set([player[i]['POS']])
                    i += 1
                i = 0
                while i < length - 1:
                    if player[i]['playerID'] == player[i+1]['playerID']:
                        player[i]['positions'] = player[i]['positions'] | player[i+1]['positions']
                        player[i]['teams'] = player[i]['teams'] | player[i+1]['teams']
                        player.remove(player[i+1])
                        length -= 1
                        i -= 1
                    i += 1

                i = 0
                while i < length:
                    s = ', '
                    player[i]['teams'] =s.join(player[i]['teams'])
                    player[i]['positions'] = s.join(player[i]['positions'])
                    print(player[i]['teams'])
                    i += 1
                populate = len(player)
                return render_template('/databaseplayer.html', player=player, populate=populate)
# drop down 1 2 and 3
        elif dropdown1 != 'select' and dropdown2 != 'select' and dropdown3 != 'select':
            if dropdown1 == 'nameFirst' or dropdown1 == 'nameLast':
                search = request.form.get('search').strip().lower()
            elif dropdown1 == 'POS':
                search = request.form.get('search').strip().upper()
            else:
                search = request.form.get('search').strip().capitalize()

            if dropdown2 == 'nameFirst' or dropdown2 == 'nameLast':
                search2 = request.form.get('search2').strip().lower()
            elif dropdown2 == 'POS':
                search = request.form.get('search2').strip().upper()
            else:
                search2 = request.form.get('search2').strip().capitalize()

            if dropdown3 == 'nameFirst' or dropdown3 == 'nameLast':
                search3 = request.form.get('search3').strip().lower()
            elif dropdown3 == 'POS':
                search3 = request.form.get('search3').strip().upper()
            else:
                search3 = request.form.get('search3').strip().capitalize()
            player = db.execute("Select DISTINCT nameFirst, nameLast, birthYear, throws, bats, POS, name, people.playerID From people, fielding, teams Where " + dropdown1 + "='" + search + "' and " + dropdown2 + "='" + search2 + "' and " + dropdown3 + "='" + search3 + "' and people.playerID=fielding.playerID and fielding.teamID=teams.teamID and fielding.yearID=teams.yearID order by nameLast ASC  Limit 5000")
            if not search or not search2 or not search3 or player == []:
                database = db.execute("Select nameFirst, nameLast, birthYear From people ORDER BY birthYear ASC")
                return render_template("/databasefailure.html", database=database)
            else:
                length = len(player)
                i = 0
                while i < length:
                    player[i]['teams'] = set([player[i]['name']])
                    player[i]['positions'] = set([player[i]['POS']])
                    i += 1
                i = 0
                while i < length - 1:
                    if player[i]['playerID'] == player[i+1]['playerID']:
                        player[i]['positions'] = player[i]['positions'] | player[i+1]['positions']
                        player[i]['teams'] = player[i]['teams'] | player[i+1]['teams']
                        player.remove(player[i+1])
                        length -= 1
                        i -= 1
                    i += 1

                i = 0
                while i < length:
                    s = ', '
                    player[i]['teams'] =s.join(player[i]['teams'])
                    player[i]['positions'] = s.join(player[i]['positions'])
                    print(player[i]['teams'])
                    i += 1
                return render_template('/databaseplayer.html', player=player)
# just dropdown 2
        elif dropdown1 == 'select' and dropdown2 != 'select' and dropdown3 == 'select':
            if dropdown2 == 'nameFirst' or dropdown2 == 'nameLast':
                search2 = request.form.get('search2').strip().lower()
            elif dropdown2 == 'POS':
                search2 = request.form.get('search2').strip().upper()
            else:
                search2 = request.form.get('search2').strip().capitalize()
            player = db.execute("Select DISTINCT nameFirst, nameLast, birthYear, throws, bats, POS, name, people.playerID From people, fielding, teams Where " + dropdown2 + "='" + search2 + "' and people.playerID=fielding.playerID and fielding.teamID=teams.teamID and fielding.yearID=teams.yearID order by nameLast ASC Limit 5000")
            if not search2 or player == []:
                database = db.execute("Select nameFirst, nameLast, birthYear From people ORDER BY birthYear ASC")
                return render_template("/databasefailure.html", database=database)
            else:
                length = len(player)
                i = 0
                while i < length:
                    player[i]['teams'] = set([player[i]['name']])
                    player[i]['positions'] = set([player[i]['POS']])
                    i += 1
                i = 0
                while i < length - 1:
                    if player[i]['playerID'] == player[i+1]['playerID']:
                        player[i]['positions'] = player[i]['positions'] | player[i+1]['positions']
                        player[i]['teams'] = player[i]['teams'] | player[i+1]['teams']
                        player.remove(player[i+1])
                        length -= 1
                        i -= 1
                    i += 1

                i = 0
                while i < length:
                    s = ', '
                    player[i]['teams'] =s.join(player[i]['teams'])
                    player[i]['positions'] = s.join(player[i]['positions'])
                    print(player[i]['teams'])
                    i += 1
                populate = len(player)
                return render_template('/databaseplayer.html', player=player, populate=populate)
# just drop down 3
        elif dropdown1 == 'select' and dropdown2 == 'select' and dropdown3 != 'select':
            if dropdown3 == 'nameFirst' or dropdown3 == 'nameLast':
                search3 = request.form.get('search3').strip().lower()
            elif dropdown3 == 'POS':
                search3 = request.form.get('search3').strip().upper()
            else:
                search3 = request.form.get('search3').strip().capitalize()
            player = db.execute("Select DISTINCT nameFirst, nameLast, birthYear, throws, bats, POS, name, people.playerID From people, fielding, teams Where " + dropdown3 + "='" + search3 + "' and people.playerID=fielding.playerID and fielding.teamID=teams.teamID and fielding.yearID=teams.yearID order by nameLast ASC Limit 5000")
            if not search3 or player == []:
                database = db.execute("Select nameFirst, nameLast, birthYear From people ORDER BY birthYear ASC")
                return render_template("/databasefailure.html", database=database)
            else:
                length = len(player)
                i = 0
                while i < length:
                    player[i]['teams'] = set([player[i]['name']])
                    player[i]['positions'] = set([player[i]['POS']])
                    i += 1
                i = 0
                while i < length - 1:
                    if player[i]['playerID'] == player[i+1]['playerID']:
                        player[i]['positions'] = player[i]['positions'] | player[i+1]['positions']
                        player[i]['teams'] = player[i]['teams'] | player[i+1]['teams']
                        player.remove(player[i+1])
                        length -= 1
                        i -= 1
                    i += 1

                i = 0
                while i < length:
                    s = ', '
                    player[i]['teams'] =s.join(player[i]['teams'])
                    player[i]['positions'] = s.join(player[i]['positions'])
                    print(player[i]['teams'])
                    i += 1
                populate = len(player)
                return render_template('/databaseplayer.html', player=player, populate=populate)
# dropdown 1 and 3
        elif dropdown1 != 'select' and dropdown2 == 'select' and dropdown3 != 'select':
            if dropdown1 == 'nameFirst' or dropdown1 == 'nameLast':
                search = request.form.get('search').strip().lower()
            elif dropdown1 == 'POS':
                search = request.form.get('search').strip().upper()
            else:
                search = request.form.get('search').strip().capitalize()

            if dropdown3 == 'nameFirst' or dropdown3 == 'nameLast':
                search3 = request.form.get('search3').strip().lower()
            elif dropdown3 == 'POS':
                search3 = request.form.get('search3').strip().upper()
            else:
                search3 = request.form.get('search3').strip().capitalize()
            player = db.execute("Select DISTINCT nameFirst, nameLast, birthYear, throws, bats, POS, name, people.playerID From people, fielding, teams Where " + dropdown1 + "='" + search + "' and " + dropdown3 + "='" + search3 +"' and people.playerID=fielding.playerID and fielding.teamID=teams.teamID and fielding.yearID=teams.yearID order by nameLast ASC Limit 5000")
            if not search or not search3 or player == []:
                database = db.execute("Select nameFirst, nameLast, birthYear From people ORDER BY birthYear ASC")
                return render_template("/databasefailure.html", database=database)
            else:
                length = len(player)
                i = 0
                while i < length:
                    player[i]['teams'] = set([player[i]['name']])
                    player[i]['positions'] = set([player[i]['POS']])
                    i += 1
                i = 0
                while i < length - 1:
                    if player[i]['playerID'] == player[i+1]['playerID']:
                        player[i]['positions'] = player[i]['positions'] | player[i+1]['positions']
                        player[i]['teams'] = player[i]['teams'] | player[i+1]['teams']
                        player.remove(player[i+1])
                        length -= 1
                        i -= 1
                    i += 1

                i = 0
                while i < length:
                    s = ', '
                    player[i]['teams'] =s.join(player[i]['teams'])
                    player[i]['positions'] = s.join(player[i]['positions'])
                    print(player[i]['teams'])
                    i += 1
                populate = len(player)
                return render_template('/databaseplayer.html', player=player, populate=populate)
# dropdown 2 and 3
        elif dropdown1 == 'select' and dropdown2 != 'select' and dropdown3 != 'select':
            if dropdown2 == 'nameFirst' or dropdown2 == 'nameLast':
                search2 = request.form.get('search2').strip().lower()
            elif dropdown2 == 'POS':
                search2 = request.form.get('search2').strip().upper()
            else:
                search2 = request.form.get('search2').strip().capitalize()

            if dropdown3 == 'nameFirst' or dropdown3 == 'nameLast':
                search3 = request.form.get('search3').strip().lower()
            elif dropdown3 == 'POS':
                search3 = request.form.get('search3').strip().upper()
            else:
                search3 = request.form.get('search3').strip().capitalize()
            player = db.execute("Select DISTINCT nameFirst, nameLast, birthYear, throws, bats, POS, name, people.playerID From people, fielding, teams Where " + dropdown2 + "='" + search2 + "' and " + dropdown3 + "='" + search3 + "' and people.playerID=fielding.playerID and fielding.teamID=teams.teamID and fielding.yearID=teams.yearID order by nameLast ASC Limit 5000")
            if not search2 or not search3 or player == []:
                database = db.execute("Select nameFirst, nameLast, birthYear From people ORDER BY birthYear ASC")
                return render_template("/databasefailure.html", database=database)
            else:
                length = len(player)
                i = 0
                while i < length:
                    player[i]['teams'] = set([player[i]['name']])
                    player[i]['positions'] = set([player[i]['POS']])
                    i += 1
                i = 0
                while i < length - 1:
                    if player[i]['playerID'] == player[i+1]['playerID']:
                        player[i]['positions'] = player[i]['positions'] | player[i+1]['positions']
                        player[i]['teams'] = player[i]['teams'] | player[i+1]['teams']
                        player.remove(player[i+1])
                        length -= 1
                        i -= 1
                    i += 1

                i = 0
                while i < length:
                    s = ', '
                    player[i]['teams'] =s.join(player[i]['teams'])
                    player[i]['positions'] = s.join(player[i]['positions'])
                    print(player[i]['teams'])
                    i += 1

                populate = len(player)
                return render_template('/databaseplayer.html', player=player, populate=populate)