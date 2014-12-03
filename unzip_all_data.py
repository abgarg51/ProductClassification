## CHANGE ME
project_dir = '/Users/normanyu/cs229/ProductClassification/'


info = """
Index:  0 	Appliances
Index:  1 	ArtsAndCrafts
Index:  2 	Automotive
Index:  3 	Baby
Index:  4 	Beauty
Index:  5 	Books
Index:  6 	Music
Index:  7 	Collectibles
Index:  8 	Movies & TV
Index:  9 	Electronics
Index:  10 	Grocery
Index:  11 	HealthPersonalCare
Index:  12 	Tools
Index:  13 	KindleStore
Index:  14 	Kitchen
Index:  15 	LawnAndGarden
Index:  16 	Magazines
Index:  17 	Everything Else
Index:  18 	MobileApps
Index:  19 	MusicalInstruments
Index:  20 	OfficeProducts
Index:  21 	Software
Index:  22 	SportingGoods
Index:  23 	Toys
Index:  24 	VideoGames
"""

temp = [x.split() for x in info.split('\n')]
d = {row[1]: ''.join(row[2:]).lower() for row in temp if len(row) > 2}
data_sources = ['amazon',]# 'ebay', 'twitter']

from multiprocessing import Pool
from subprocess import call
import os

p = Pool(8) # use 8 cores


def shell_wrapper(l):
	# run shell command to extract data
	print "Working on: ", ' '.join(l)
	call(l)

command_list = []
for source in data_sources:
    for index, name in d.items():
        command_list.append(['python', os.path.join(project_dir, 'data_reader.py'), source, index, os.path.join(project_dir, 'data', '%s_%s.dat'%(source, name))])

# run shell_wrapper on command_list items in parallel
p.map(shell_wrapper, command_list)