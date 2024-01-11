import requests
import os
import time
from pysondb import db
import datetime
import calendar,re

i=8
token="token8"
header={"Authorization": f"Bearer {token}"}
#   For basic example taking one experiment : https://github.com/endrebak/yaml-config-updater/
curr_path=os.getcwd()
dataset_dir=f"{curr_path}\Dataset\SWH"
db_url=db.getDb(f"{dataset_dir}\split{i}.json")

def get_response(url,session):
    date=datetime.datetime.utcnow()
    #print(date)
    timen=calendar.timegm(date.utctimetuple())
    #print(time)

    response=session.get(url, headers=header)
    #print(response.headers)
    try:
        print("Current Request Limit: ",response.headers['X-RateLimit-Remaining'])
        if(int(response.headers['X-RateLimit-Remaining']) < 3):
            print("Waiting due to RateLimit", int(response.headers['X-RateLimit-Reset']))
            time.sleep(int(response.headers['X-RateLimit-Reset'])-int(timen))
            time.sleep(10)
            print("Resuming")
    except:
        print("Exception in getting data, trying again")
        time.sleep(5)
        try:
            response=session.get(url, headers=header)
            print("Current Request Limit: ",response.headers['X-RateLimit-Remaining'])
            if(int(response.headers['X-RateLimit-Remaining']) < 3):
                print("Waiting due to RateLimit", int(response.headers['X-RateLimit-Reset']))
                time.sleep(int(response.headers['X-RateLimit-Reset'])-int(timen))
                time.sleep(10)
                print("Resuming")
        except:
            print("Still some issue")

    try:
        if(response.content.decode('ascii')=="Not Found"):
            return "error"
    except:
        print("Exception in decoding, skipping check")
        # return "error"
    response=response.json()
    return response

def get_file(url,session):
    response=session.get(url)
    return response

def directory_travel(data,session):
    yaml_file={}
    for content in data:
        #print(content)
        if content['type'] == 'file':
            if '.yml' in content['name'] or '.yaml' in content['name']:
                #print(content['name'])
                unique_file_name=content['target']+content['name']
                yaml_file[unique_file_name]=content['target_url']
        elif content['type'] == "dir":
            sub_directory=get_response(content['target_url'],session)
            yaml_file={**yaml_file,**directory_travel(sub_directory,session)}
        else:
            print("Unknown dir or file type")
    return yaml_file





with open(f"{curr_path}\Phase2\slice{i}.txt",'r') as file:
    urls=file.readlines()

session_counter=0
possible_files=[]
counter=0
session=requests.Session()
for base_url in urls:
    if (session_counter>=10):
        print("Changing session")
        session_counter=0
        session.close()
        session=requests.Session()
    start = time.time()
    counter+=1
    print(counter)
    #   Base URL
    base_url=base_url.strip()
    base_url=f"https://archive.softwareheritage.org/api/1/origin/{base_url}/visits/"
    print("Base URL:",base_url)
    response=get_response(base_url,session)

    if "error" not in response:
        # for data in response:
        try:
            data=response[0]
        except:
            print("Found Issue, waiting for 10 secods buffer")
            time.sleep(10)
            try:
                response=get_response(base_url,session)
                data=response[0]
            except:
                print("Still facing same issue, ignoring this url trying next data")
                with open(f"{curr_path}\Phase2\unavailable_swh.txt","a") as tmp:
                    tmp.write(base_url)
                    tmp.write("\n")
                continue
        
        try:
            print("Snapshot URL:",data['snapshot_url'])
            snapshot=get_response(data['snapshot_url'],session)
        except:
            print("Found Issue, waiting for 10 secods buffer")
            time.sleep(10)
            try:
                response=get_response(base_url,session)
                data=response[0]
                snapshot=get_response(data['snapshot_url'],session)
            except:
                print("Still facing same issue, ignoring this url trying next data")
                with open(f"{curr_path}\Phase2\unavailable_swh.txt","a") as tmp:
                    tmp.write(base_url)
                    tmp.write("\n")
                continue
        #   Looking only for HEAD branch
        
        try:
            #snapshot=get_response(data['snapshot_url'])
            print("Revision URL:",snapshot['branches']['HEAD']['target_url'])
            revision=get_response(snapshot['branches']['HEAD']['target_url'],session)
        except:
            print("Found Issue, waiting for 10 secods buffer")
            time.sleep(10)
            try:
                snapshot=get_response(data['snapshot_url'],session)
                print("Revision URL:",snapshot['branches']['HEAD']['target_url'])
                revision=get_response(snapshot['branches']['HEAD']['target_url'],session)
            except:
                print("Still facing same issue, ignoring this url trying next data")
                with open(f"{curr_path}\Phase2\unavailable_swh.txt","a") as tmp:
                    tmp.write(base_url)
                    tmp.write("\n")
                continue
        
        #   Looking for directory
        
        try:
            print("Directory URL:",revision['directory_url'])
            directory=get_response(revision['directory_url'],session)
        except:
            print("Found Issue, waiting for 10 secods buffer")
            time.sleep(10)
            try:
                revision=get_response(snapshot['branches']['HEAD']['target_url'],session)
                print("Directory URL:",revision['directory_url'])
                directory=get_response(revision['directory_url'],session)
            except:
                print("Still facing same issue, ignoring this url trying next data")
                with open(f"{curr_path}\Phase2\unavailable_swh.txt","a") as tmp:
                    tmp.write(base_url)
                    tmp.write("\n")
                continue
        try:
            yaml_dir=directory_travel(directory,session=session)
            #print(yaml_dir)
            for key,value in yaml_dir.items():
                #print(key,value)
                content_url=f"{value}raw/"
                filecontent=get_file(content_url,session)
                try:
                    open(f'{dataset_dir}\{key}', 'wb').write(filecontent.content)
                except:
                    key=re.sub('[^A-Za-z0-9]+', '', key)
                    open(f'{dataset_dir}\{key}', 'wb').write(filecontent.content)
                db_url.add({'Base':base_url,'Snapshot':data['snapshot_url'],'Revision':snapshot['branches']['HEAD']['target_url'],'Directory':revision['directory_url'],'File_Key':key})
        except:
            print("Issue with the directory or repository, skipping it and adding to unavailable list")
            with open(f"{curr_path}\Phase2\unavailable_swh.txt","a") as tmp:
                tmp.write(base_url)
                tmp.write("\n")


    else:
        print("URL not present on SWH")
        with open(f"{curr_path}\Phase2\unavailable_swh.txt","a") as tmp:
            tmp.write(base_url)
            tmp.write("\n")

    end = time.time()
    print(end - start)
    time.sleep(8)
    session_counter+=1