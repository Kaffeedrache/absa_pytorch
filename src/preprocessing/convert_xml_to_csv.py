#!/usr/bin/env python3

# Convert the data from the SemEval xml format to csv
# output file 1: one line per category annotation
# output file 2: one line per term annotation

# You can get the data from the SemEval 2014 web page:
# http://alt.qcri.org/semeval2014/task4/index.php?id=data-and-tools

# @author Wiltrud Kessler, 2019-11-06

from xml.dom import minidom
import xml.etree.cElementTree as ET
from pandas import DataFrame



def writeOut(sentences, filename):
	i = 0
	for s in sentences:
		print(s)
		i+= 1
		if i>10:
			break

	df = DataFrame.from_dict(sentences)
	df.polarity.replace(['negative', 'positive', 'neutral'], ['-1', '1', '0'], inplace=True)
	df.to_csv(filename, index=False)

def convert(in_filename, out_filename1, out_filename2):
	sentences_aspects = []
	sentences_categories = []

	tree = ET.ElementTree(file=in_filename)
	sentnum = 0
	for index, sentence in enumerate(tree.iter(tag='sentence')):
		sentnum+=1
		s = {}
		s['sid'] = sentence.attrib['id']
		for elem in sentence.iter():
			if(elem.tag=='text'):
				s['text'] = elem.text
			elif(elem.tag=='aspectTerms'):
				#s['aspectTerms'] = []  # aggregate on sentece level
				i = 0
				for at in elem.iter():
					attr = at.attrib
					if('term' not in attr):
						continue
					i+=1
					s2 = {}
					s2['aid'] = s['sid'] + '-' + str(i)
					#s['aspectTerms'].append(at.attrib) # aggregate on sentece level
					sentences_aspects.append({**s, **s2, **at.attrib})
			elif(elem.tag=='aspectCategories'):
				#s['aspectCats'] = [] # aggregate on sentece level
				for ac in elem.iter():
					attr = ac.attrib
					if('category' not in attr):
						continue
					#s['aspectCats'].append(attr) # aggregate on sentece level
					s2 = {}
					s2['aid'] = s['sid'] + '-' + str(i)
					sentences_categories.append({**s, **s2, **ac.attrib})
		#train_sentences.append(s) # aggregate on sentece level

	writeOut(sentences_aspects, out_filename1)
	writeOut(sentences_categories, out_filename2)


convert('./data/restaurants-trial.xml','./data2/semeval2014_restaurants_test_term.csv','./data2/semeval2014_restaurants_test_category.csv')

convert('./data/Restaurants_Train_v2.xml', './data2/semeval2014_restaurants_train_term.csv', './data2/semeval2014_restaurants_train_category.csv')
