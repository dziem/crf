#edit distance with normalized cost & window 2
import numpy as np
from weighted_levenshtein import lev, osa, dam_lev
from string import ascii_lowercase
import csv
from itertools import combinations
import unicodedata

brand = []
with open('brand.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        brand.append(unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore'))

alfha = 0.4
threshold = 30

insert_costs = np.full(128, 100, dtype=np.float64)
insert_costs[ord('-')] = 10
insert_costs[ord(' ')] = 10

delete_costs = np.full(128, 100, dtype=np.float64)
delete_costs[ord('-')] = 10
delete_costs[ord(' ')] = 10

substitute_costs = np.full((128,128), 50, dtype=np.float64)
for c in ascii_lowercase:
	substitute_costs[ord(c), ord(c.capitalize())] = 10
	substitute_costs[ord(c), ord(c)] = 0
	substitute_costs[ord(c.capitalize()), ord(c)] = 10
	substitute_costs[ord(c.capitalize()), ord(c.capitalize())] = 0
substitute_costs[ord('-'), ord(' ')] = 10
substitute_costs[ord(' '), ord('-')] = 10
for i in range(10):
	for j in range(10):
		if i == j:
			substitute_costs[ord(str(i)), ord(str(j))] = 0
			substitute_costs[ord(str(j)), ord(str(i))] = 0
		else:
			substitute_costs[ord(str(i)), ord(str(j))] = 10
			substitute_costs[ord(str(j)), ord(str(i))] = 10

def edit_distance_normalized_cost(word, target):
	cost = lev(word, target, insert_costs=insert_costs, delete_costs=delete_costs, substitute_costs=substitute_costs)
	return (cost + alfha) / len(target)

def check_under_threshold(cost):
	if cost <= threshold:
		return True
	else:
		return False

def check_edit_distance(sentence, pos):
	words = sentence.split()
	if pos == 0: #start
		candidate = [" ".join(a) for a in combinations([words[pos], words[pos + 1], words[pos + 2]], 2)]
	elif pos == 1: #1 after start
		candidate = [" ".join(a) for a in combinations([words[pos - 1], words[pos], words[pos + 1], words[pos + 2]], 2)]
	elif pos == len(words) - 2: #1 before last
		candidate = [" ".join(a) for a in combinations([words[pos - 2], words[pos - 1], words[pos], words[pos + 1]], 2)]
	elif pos == len(words) - 1: #last
		candidate = [" ".join(a) for a in combinations([words[pos - 2], words[pos - 1], words[pos]], 2)]
	else: #anywhere else
		candidate = [" ".join(a) for a in combinations([words[pos - 2], words[pos - 1], words[pos], words[pos + 1], words[pos + 2]], 2)]
	exist = False
	for b in brand:
		for c in candidate:
			if check_under_threshold(edit_distance_normalized_cost(c,b)) :
				exist = True
				break
	return exist

print(check_edit_distance('lorem ipsum dolor amet',0))