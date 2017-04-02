#!/usr/bin/env python
import os
import pymongo
import csv

'''
First, download your csv file, e.g. from the command line, issue:
wget https://files.datapress.com/london/dataset/number-international-visitors-london/2017-01-26T18:50:00/international-visitors-london-raw.csv
'''

if 'OPENSHIFT_MONGODB_DB_URL' not in os.environ:
    print('"OPENSHIFT_MONGODB_DB_URL" is not set in the environment variables.')
    print('Connecting to openshift to obtain its value ...')
    import subprocess
    # Note: change the name of your app here  -- mine is called apitest1 for some reason ;P 
    MY_APP_NAME = 'stv30apitest1'
    my_shell_command = "rhc ssh -a {} env | grep OPENSHIFT_MONGODB_DB_URL".format(MY_APP_NAME)
    proc = subprocess.Popen([my_shell_command], stdout=subprocess.PIPE, shell=True)
    (imported_mongodb_url, error_in_importing_mongodb_url) = proc.communicate()
    imported_mongodb_url = imported_mongodb_url.strip().split('=')[-1]
    print('"OPENSHIFT_MONGODB_DB_URL" value imported!')
    imported_mongodb_url = imported_mongodb_url.split('@')
    local_mongo_url = imported_mongodb_url[0]+'@127.0.0.1:27017'
    print('''"OPENSHIFT_MONGODB_DB_URL" value modified to connect 
        to the localhost\n (assuming portforwarding is established)''')
    os.environ['OPENSHIFT_MONGODB_DB_URL'] = local_mongo_url
  
print('Connecting to the mongodb on openshift ...')
connection_string = os.environ['OPENSHIFT_MONGODB_DB_URL']
myMongo_client = pymongo.MongoClient(connection_string)
print('Connection Established!\n\n')
MY_APP_NAME = 'stv30apitest1'
print('Now creating a collection named "London_Visitors" and populating it with documents...')
# Note: make sure you have set your app name correctly, otherwise it creates a whole new 
# database called apitest1!
if MY_APP_NAME in myMongo_client.database_names():
    myMongo_London_DB_client = myMongo_client.MY_APP_NAME.London
else:
    raise ValueError('The database named {} does not exist!'.format(MY_APP_NAME))

filepath = 'international-visitors-london-raw.csv' 
# the next two lines are just for the progress bar :p
with open(filepath, "rb") as f:
    my_total_number_of_documents = len(f.readlines())
    my_progress_bar_steps = my_total_number_of_documents/20

    
with open(filepath, "rb") as f:
    reader = csv.reader(f, delimiter=",", skipinitialspace=True)
    field_names = reader.next()
    print(field_names)
    reader = csv.DictReader(f, field_names, skipinitialspace=True)
    
    if myMongo_London_DB_client.count() > 0: 
        print('The collection is already non-empty and has {} many documents!'.format(myMongo_London_DB_client.count()))
        user_conform = raw_input('Do you really want to overwrite the data [y/n]?')
        if user_conform == 'y':
            myMongo_London_DB_client.drop()
            print(myMongo_London_DB_client.count())
        
    if myMongo_London_DB_client.count() == 0 or user_conform == 'y':
        for (i, doc) in enumerate(reader):
            myMongo_London_DB_client.insert_one(doc)
            if i%my_progress_bar_steps == 0:
                print('{}%..'.format(100*i/my_total_number_of_documents)),

        print('100% finished Imporing the entire csv to mongodb!')
        
 
print('Performing an example (simple) query to see if the collection is created properly:')
test_query_response = myMongo_London_DB_client.find({'year':'2015','purpose':'Business'})
for (attr, val) in test_query_response.iter_items():
    print('{}:{}'.format(attr,value))


print('Now closing the mongodb connections...')
myMongo_client.close()
