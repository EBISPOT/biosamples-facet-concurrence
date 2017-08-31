#!/usr/bin/python

# Crawler script- get me a list of keys for every sample.

import requests
import math
import csv
from multiprocessing import Process


# BioSample API request module

def api_samples(parms):
    startpage = parms["start"]
    endpage = parms["end"]
    name = parms["name"]
    page_size = parms["size"]

    print("In api_samples", startpage, endpage)

    # counter_page = startpage

    # Open a file to write into it
    # `with` will close the file automatically
    with open(name + '.csv', 'w') as f:

        for counter_page in range(startpage, endpage + 1):

            # Initialize keys_list variable
            keys_list = []
            query_params = {
                "page": counter_page,
                "size": page_size,
            }

            # Request the API for the samples
            response = requests.get('http://www.ebi.ac.uk/biosamples/api/samples/', params=query_params)
            if response.status_code is not 200:
                # If the status code of the response is not 200 (OK), something is wrong with the API
                # Return the process
                print('Something wrong happening...')
                return

            # counter_page = counter_page + 1
            if counter_page % 100 == 0:
                print("Process " + name + " reached " + str(counter_page))

            # Looking through the JSON:
            # Get all samples on the page
            samples_in_page = response.json()['_embedded']['samples']

            # For each sample, get characteristics types and save them in the key_list variable
            for sample in samples_in_page:
                sample_characteristics = sample['characteristics']
                sample_keys = list(sample_characteristics.keys())
                keys_list.append(sample_keys)

            # Write the characteristics list into the file
            writer = csv.writer(f)
            writer.writerows(keys_list)

# Main Method
if __name__ == "__main__":

    # Splitting up the BioSamples Pages into equal chunks for multithreading
    numberOfParalelJobs = 8
    pageSize = 500
    query_params = {
        "size": pageSize,
    }
    rel = requests.get('http://www.ebi.ac.uk/biosamples/api/samples/', params=query_params)
    reply = rel.json()
    totalPageNumer = reply['page']['totalPages']

    startpoint = 0
    init = []
    for i in range(1, numberOfParalelJobs + 1):
        params = dict()
        params['run'] = i
        params['size'] = pageSize
        params['name'] = "Thread{}_results".format(str(i))
        params['start'] = startpoint

        endpoint = math.ceil(totalPageNumer / float(numberOfParalelJobs)) * i
        if endpoint < int(totalPageNumer):
            params['end'] = int(endpoint)
        else:
            params['end'] = totalPageNumer

        init.append(params)
        startpoint = int(endpoint) + 1

    processlist = []
    for entry in init:
        p = Process(target=api_samples, args=[entry])
        p.start()
        processlist.append(p)

    print("All process started")

    # Going through the process list, waiting for everything to finish
    for procs in processlist:
        procs.join()

    print("All finished")
