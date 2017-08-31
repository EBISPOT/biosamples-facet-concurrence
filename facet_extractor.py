#!/usr/bin/python
#Script to call Solr facets for a given search and return no. of values.
#Then for each facet return all those values for each facet
#Eventually putting them in a format for reading by R


import requests
import json
import re
print("facets_name,facets_count")
results = []
#the inital search for facets
q = "*:*"
facet = "crt_type_ft"
query_params = {
    "q" : q,
    "wt" : "json",
    "rows": 0,
    "facet": "true",
    "facet.field": facet,
    "facet.limit": -1,
    "facet.sort": "count",
    "facet.mincount": "1"
}
response = requests.get('http://cocoa.ebi.ac.uk:8989/solr/merged/select', params=query_params)
# facets = response.json()['facet_counts']

facets = response.json()['facet_counts']['facet_fields'][facet]

# if facets not in results:
# 	results.append(facets)
# print(results, len(results))


facets_name = facets[::2]
facets_count = facets[1::2]


for i in range(len(facets_name)):
    print('{},{}'.format(facets_name[i], facets_count[i]))



