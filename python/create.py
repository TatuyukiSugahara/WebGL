# -*- coding: utf8 -*-
import sys
import json

dict = []

test = {
    'book1':{
	'title':'Python Beginners',
 	'year': 2005 ,
	'page': 399 
    }
}

for i in range(0, 100000):
    dict.append(test)


f = open('out'+sys.argv[1]+'.json', 'w')
json.dump(dict, f, indent=4, sort_keys=True)

print u"成功"