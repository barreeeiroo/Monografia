#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import csv
import pandas as pd

# Working directory
datadir = os.path.dirname(__file__) + '/../scrapper/fourFactors/csv/'

# Load all data files
files = os.listdir(datadir)
files.remove(".gitkeep")
files = sorted(files, key=lambda x:(len(x),x.lower()))


# Season variables
season_efg = []
season_tov = []
season_orb = []
season_ftr = []
season_scr = []


parsed = []
for f in files:
    # Desired team variables
    match_fgm = 0
    match_fga = 0
    match_ftm = 0
    match_fta = 0
    match_3pm = 0
    match_to  = 0
    match_orb = 0
    match_drb = 0
    match_scr = 0

    # Opponent variables
    match_drb_opp = 0
    match_scr_opp = 0

    if f not in parsed:
        # First we have to read ALL the files
        data = pd.read_csv(datadir+f)
        parsed.append(f)
        data_opp = pd.read_csv(datadir+f.replace("A.csv", "B.csv"))
        parsed.append(f.replace("A.csv", "B.csv"))

        # First we parse the data from the desired team
        process = True
        for index, player in data.iterrows():
            # These are all the neede stats from the desired team
            fgma  = player['FGM-A'].split("-")
            ftma  = player['FTM-A'].split("-")
            v3pma = player['3PM-A'].split("-")
            to    = player['TO']
            orb   = str(player['Off'])
            drb   = player['Def']
            pts   = player['PTS']

            if player['#'] != "&nbsp;":
                match_fgm += int(fgma[0])
                match_fga += int(fgma[1])
                match_3pm += int(v3pma[0])
                match_ftm += int(ftma[0])
                match_fta += int(ftma[1])
                match_to  += int(to)

            if orb != "&nbsp;":
                match_orb += int(orb.split('.', 1)[0])
            if drb != "&nbsp;":
                match_drb += int(drb)
            if pts != "&nbsp;":
                match_scr += int(pts)


        # And later on the opponent
        for index, player_opp in data_opp.iterrows():
            drb = player_opp['Def']
            pts = player_opp['PTS']

            # We only need from the opponent the DRB data and the score
            if drb != "&nbsp;":
                match_drb_opp += int(drb)
            if pts != "&nbsp;":
                match_scr_opp += int(pts)

        # Calculate the four factors of the match
        efg = (match_fgm+0.5*match_3pm)/match_fga
        tov = match_to/(match_fga+0.44*match_fta+match_to)
        orb = match_orb/(match_orb+match_drb_opp)
        ftr = match_ftm/match_fta
        won = 1 if match_scr>match_scr_opp else 0

        # Send the stats to the season variables
        season_efg.append(efg)
        season_tov.append(tov)
        season_orb.append(orb)
        season_ftr.append(ftr)
        season_scr.append(won)



# OUTPUT FOR DEBUG
"""
print(season_efg)
print(season_tov)
print(season_orb)
print(season_ftr)
print(season_scr)
"""


### WRITE FOUR FACTORS TO CSV ###

df = pd.DataFrame(data={"efg":season_efg, "tov":season_tov, "orb":season_orb, "ftr":season_ftr, "won":season_scr})
df.to_csv(os.path.dirname(__file__)+"/fourFactors.csv", sep=',',index=False)
