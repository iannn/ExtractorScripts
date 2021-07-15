#Starter for initializing databases of items from the GW2 api
"""Organizing the GW2 Items db

Before the upgrade salvage profit can be computed, the following needs to be sorted out:
    Runes
    Sigils
    Armour
    Weapons
    Trinkets (Rings, Earings, Amulets all good with upgrades being sold)

The purpose of this script is to create the organized database, or "database"
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
Select 200 ids or less to request from api
Iterate over block of ids:
    Check type for item with appropriate 'type' that has 'suffix_item_id'
        if true
            construct database dictionary
            add dictionary to database
            append dictionaries with info of what values are being stored
        if false,
            continue to next entry
Close anything that needs to be closed
Fin. Databases should be ready to use by other scripts now

"""

"""API limitations

After some tests and looking on the forums, you can request 200 items at once
I am concerned about api timeout because of spamming
Processing 200 entries, a counter trigger I thought worked well not realizing it was the api limit is the way to go
"""
##Begin Imports

#Import GW2 API
from gw2api import GuildWars2Client
gw2_client = GuildWars2Client()

#Import "database" driver
import csv

##End Imports

#Get the big list of item ids from gw2api - NOT A GIANT LIST OF DICTIONARIES
print("Getting all gw2 item ids")
gw2_allitems = gw2_client.items.get()
print("Received all gw2 item ids")

#because of the 200 id limit/api cabaility, this big list needs to be split into lists of 200 or less
#I had to look up and test list comprehension and generators for this
block_size = 200 #don't hard code the api block size
gw2_allitems_blocks = [gw2_allitems[i:i+block_size] for i in range(0, len(gw2_allitems), block_size)]

#purposefully sabotaging for testing
gw2_allitems_blocks = [gw2_allitems_blocks[0], gw2_allitems_blocks[1]]

#Keys to write
#commit to full csv for now. ids only. Let the spreadsheet pull name
#keynames = ['id', 'name','type','suffix_item_id' ]
keynames = ['id', 'suffix_item_id']#I only really need these 2 id's for the csv

##Big CSV writing loop

"""open csv with paramaters
open as write - 'w'
set newline to avoid errors as per docs-  newline=''

"""
with open('UpgradeSalvageCandidates.csv', 'w', newline='') as csvfile:
    print("CSV opened")

#write header
    keynames
    writer = csv.DictWriter(csvfile,fieldnames=keynames,extrasaction='ignore')
    writer.writeheader()

#I want counters to help debug/check
    loop_counter=0
    write_counter=0
#main writing loop
    ids_write = {'id':0, 'suffix_item_id':0}#temporary dict for writing to csv
    print("starting big loop")

    for item_i in gw2_allitems_blocks:
        API_tmp = gw2_client.items.get(ids=item_i)
        #API_tmp is now a list of dictionaries
        #item_i is a list so using ids WILL NOT FAIL because of library behaviour

        #Iterate over block of dictionaries
        for dict_tmp in API_tmp:
            #check for desired type, then for upgrade
            #no rune/sigil in gear should result in key 'suffix_item_id' not being present
            if dict_tmp['type'] in ['Weapon' or 'Armor' or 'Back' or 'Trinket']:
                if 'suffix_item_id' in dict_tmp['details']:
                    #is of both correct type AND has suffix_item_id
                    ids_write['id'] = dict_tmp['id']
                    ids_write['suffix_item_id']=dict_tmp['details']['suffix_item_id']
                    #write each passing item call to csv
                    writer.writerow(ids_write)
                    #update the counter and rewrite the ids_write
                    write_counter+=1
                    if write_counter % 100 == 0: print("Write counter at ", write_counter)
                    ids_write['id'] = write_counter
                    ids_write['suffix_item_id']= write_counter

            loop_counter +=1
            if loop_counter % 200 == 0: print("Loop counter at ", loop_counter)

"""
close csv
"""
print("The total number of gear pairs found was ", write_counter)
print("Processed ", loop_counter, " entries")
