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
season_won = []
season_efg_opp = []
season_tov_opp = []
season_orb_opp = []
season_ftr_opp = []
season_scr_opp = []


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

    # Opponent team variables
    match_fgm_opp = 0
    match_fga_opp = 0
    match_ftm_opp = 0
    match_fta_opp = 0
    match_3pm_opp = 0
    match_to_opp  = 0
    match_orb_opp = 0
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


        # And the same for the opponent
        for index, player_opp in data_opp.iterrows():
            fgma  = player_opp['FGM-A'].split("-")
            ftma  = player_opp['FTM-A'].split("-")
            v3pma = player_opp['3PM-A'].split("-")
            to    = player_opp['TO']
            orb   = str(player_opp['Off'])
            drb   = player_opp['Def']
            pts   = player_opp['PTS']

            if player_opp['#'] != "&nbsp;":
                match_fgm_opp += int(fgma[0])
                match_fga_opp += int(fgma[1])
                match_3pm_opp += int(v3pma[0])
                match_ftm_opp += int(ftma[0])
                match_fta_opp += int(ftma[1])
                match_to_opp  += int(to)

            if orb != "&nbsp;":
                match_orb_opp += int(orb.split('.', 1)[0])
            if drb != "&nbsp;":
                match_drb_opp += int(drb)
            if pts != "&nbsp;":
                match_scr_opp += int(pts)

        # Calculate the four (eight in fact) factors of the match
        efg = (match_fgm+0.5*match_3pm)/match_fga
        tov = match_to/(match_fga+0.44*match_fta+match_to)
        orb = match_orb/(match_orb+match_drb_opp)
        ftr = match_ftm/match_fta
        scr = match_scr
        won = 1 if match_scr>match_scr_opp else 0
        efg_opp = (match_fgm_opp+0.5*match_3pm_opp)/match_fga_opp
        tov_opp = match_to_opp/(match_fga_opp+0.44*match_fta_opp+match_to_opp)
        orb_opp = match_orb_opp/(match_orb_opp+match_drb)
        ftr_opp = match_ftm_opp/match_fta_opp
        scr_opp = match_scr_opp

        # Send the stats to the season variables
        season_efg.append(efg)
        season_tov.append(tov)
        season_orb.append(orb)
        season_ftr.append(ftr)
        season_scr.append(scr)
        season_won.append(won)
        season_efg_opp.append(efg_opp)
        season_tov_opp.append(tov_opp)
        season_orb_opp.append(orb_opp)
        season_ftr_opp.append(ftr_opp)
        season_scr_opp.append(scr_opp)



# OUTPUT FOR DEBUG
"""
print(season_efg)
print(season_tov)
print(season_orb)
print(season_ftr)
print(season_scr)
print(season_won)
print(season_efg_opp)
print(season_tov_opp)
print(season_orb_opp)
print(season_ftr_opp)
print(season_scr_opp)
"""


### WRITE FOUR FACTORS TO CSV ###

df = pd.DataFrame(data={
    "efg":season_efg, "tov":season_tov, "orb":season_orb, "ftr":season_ftr, "scr":season_scr,
    "won":season_won,
    "efg_opp":season_efg_opp, "tov_opp":season_tov_opp, "orb_opp":season_orb_opp, "ftr_opp":season_ftr_opp, "scr_opp":season_scr_opp})
df.to_csv(os.path.dirname(__file__)+"/fourFactors.csv", sep=',',index=False)
