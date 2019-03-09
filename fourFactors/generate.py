#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

# Working directory
wdir = os.path.dirname(__file__) + '/../scrapper/fourFactors/csv/'

# Load all data files
files = os.listdir(wdir)
files.remove(".gitkeep")
files = sorted(files, key=lambda x:(len(x),x.lower()))


# Season variables
season_efg = []
season_tov = []
season_orb = []
season_ftr = []


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

    # Opponent variables
    match_drb_opp = 0

    if f not in parsed:
        # First we have to read ALL the files
        if f.endswith("B.csv"):
            data_opp = pd.read_csv(wdir+f)
            parsed.append(wdir+f)
            data = pd.read_csv(wdir+f.replace("B.csv", "A.csv"))
            parsed.append(f.replace("B.csv", "A.csv"))
        else:
            data = pd.read_csv(wdir+f)
            parsed.append(wdir+f)
            data_opp = pd.read_csv(wdir+f.replace("A.csv", "B.csv"))
            parsed.append(f.replace("B.csv", "A.csv"))

        # First we parse the data from the desired team
        for index, player in data.iterrows():
            # These are all the neede stats from the desired team
            fgma  = player['FGM-A'].split("-")
            ftma  = player['FTM-A'].split("-")
            v3pma = player['3PM-A'].split("-")
            to    = player['TO']
            orb   = str(player['Off'])
            drb   = player['Def']

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
        
        # And later on the opponent
        for index, player_opp in data_opp.iterrows():
            drb = player_opp['Def']
            # We only need from the opponent the DRB data
            if drb != "&nbsp;":
                match_drb_opp += int(drb)


        # Calculate the four factors of the match
        efg = (match_fgm+0.5*match_3pm)/match_fga
        tov = match_to/(match_fga+0.44*match_fta+match_to)
        orb = match_orb/(match_orb+match_drb_opp)
        ftr = match_ftm/match_fta

        # Send the stats to the season variables
        season_efg.append(efg)
        season_tov.append(tov)
        season_orb.append(orb)
        season_ftr.append(ftr)



# OUTPUT
print(season_efg)
print(season_tov)
print(season_orb)
print(season_ftr)
