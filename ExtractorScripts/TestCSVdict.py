"""
Test writing python dictionaries to csv files
"""

import csv
import itertools

#test dictionary
testD1 = {'d1key1':1111, 'd1key2':2222, 'd1key3':3333}

#test dictionary with dictionary
testD2 = {'d2key1':1111, 'd2key2':2222, 'd2dict2':{'d2key3':3333, 'd2key4':4444}}

#test dictionary lists
testD3 = [  {'d3key1':1111, 'd3key2':1222, 'd3key3':1333},
            {'d3key1':2111, 'd3key2':2222, 'd3key3':2333},
            {'d3key1':3111, 'd3key2':3222, 'd3key3':3333}
]

testD4 = [  {'d4key1':1111, 'd4key2':1222, 'd4dict2':{'d4key3':1333, 'd4key4':1444}},
            {'d4key1':1111, 'd4key2':1222, 'd4dict2':{'d4key3':1333, 'd4key4':1444}},
            {'d4key1':1111, 'd4key2':1222, 'd4dict2':{'d4key3':1333, 'd4key4':1444}}
]

print(testD1)
print(testD2)
print(testD3)
print(testD4)

#Tests work at this point

#myKeys = list(testD1)#works for the single examples
myKeys = ['d3key1','d3key2', 'd3key3', 'd3key4']

with open('dict-To-CSVtest.csv', 'w', newline='') as csvfile:
    #fieldnames = myKeys
    writer = csv.DictWriter(csvfile,fieldnames=myKeys,extrasaction='ignore')
    writer.writeheader()
    #writer.writerows(testD3)

print("finished")
