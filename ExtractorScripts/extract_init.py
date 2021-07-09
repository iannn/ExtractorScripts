#Starter for initializing databases of items from the GW2 api
"""Organizing the GW2 Items db

Before the upgrade salvage profit can be computer, the following needs to be sorted out:
    Runes
    Sigils
    Armour
    Weapons
    Trinkets (Rings, Earings, Amulets all good with upgrades being sold)

The purpose of this script is to create the organized database
Some items have salvaging restrictions so the infinite extractor is needed for some
This initial pass will not have infinite upgrade extractor items included

Cassandra require Java - ew
Mongo requires running a db service or shell instance and defaults clout stuff - no
sqlite - most basic, built-in db option
write to csv???? weapon/armour/trinket (/rune/sigil) are different csv files???
"""

"""
GW2's api returns a JSON object that the GW2 python wrapper turns into a dictionary
The entire contents of the JSON are NOT needed

This script should also pull, and probably store, all possible options for each of the fields in a table
Parsing all the flags options will be required to check for warnings/other considerations at some point
All the keys/options are on the API wiki but generating them here is easier for inputs

The following HIGH LEVEL keys appear to be needed
    name = the name of the item
    ***type = Armor, Back, Trinket, UpgradeComponent, Weapon
    level = number up to 80
    rarity = Junk, Basic, Fine, Masterwork, Rare, Exotic, Ascended, Legendary
    flags = limitations, permissions, additional modifiers for the name/gear (informational)
    id = the it number used in the API to fetch this information
    details = another dictionary full of information that changes based on type

There is another dictionary within "details" that has the important upgrade check info
This dictionary has different values based on the different values of "type" but the main keys are the same
    details - type = the subtype of the main type ie Axe, Gloves, Amulet
    ***details - suffix_item_id = where the rune or sigil id will go. Wiki says "usually" which is ????

*** type and details-suffix_item_id are the most important for filtering
DO NOT get confused with the infix_upgrade as this is a stat modifier for /v2/itemstats
"""

"""Program flow plan

Call items to get list of all items numbers
Iterate over list of ids doing the following:
    Check type for UpgradeComponent or other type with suffix_item_id
        if true
            construct database dictionary
            add dictionary to database
            append dictionaries with info of what values are being stored
        if false,
            continue to next entry
Close anything that needs to be closed
Fin. Databases should be ready to use by other scripts now

"""
##Begin Imports

#Import GW2 API
from gw2api import GuildWars2Client
gw2_client = GuildWars2Client()

#Import "database" driver
import csv

##End Imports

#Get the big list of items from gw2api
gw2_allitems = gw2_client.items.get()

#Keys to write
#commit to full csv for now. ids only. Let the spreadsheet pull name
keynames = ['id', 'name','type','suffix_item_id' ]

##Big CSV writing loop

"""open csv with paramaters
open as write - 'w'
set newline to avoid errors as per docs-  newline=''

"""
with open('UpgradeSalvageCandidates.csv', 'w', newline='') as csvfile:

#write header
#main writing loop
#call next item from gw2_allitems from gw2_client
#check for type and upgrade
#write each passing item call to csv
#details being a dictionary within a dictionary is a problem

"""
close csv
"""
