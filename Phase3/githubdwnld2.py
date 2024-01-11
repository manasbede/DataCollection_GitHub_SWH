import requests
import os,time, datetime, calendar

def get_repository_contents(session,owner, repo, path="", recursive=False):
    date=datetime.datetime.utcnow()
    #print(date)
    timen=calendar.timegm(date.utctimetuple())
    base_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    #print(base_url)
    params = {"recursive": 1} if recursive else {}

    headers={ "Authorization": f"Bearer token2",}
    response = session.get(base_url, params=params, headers=headers, timeout=60)

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
            response = session.get(base_url, params=params, headers=headers, timeout=60)
            print("Current Request Limit: ",response.headers['X-RateLimit-Remaining'])
            if(int(response.headers['X-RateLimit-Remaining']) < 3):
                print("Waiting due to RateLimit", int(response.headers['X-RateLimit-Reset']))
                time.sleep(int(response.headers['X-RateLimit-Reset'])-int(timen))
                time.sleep(10)
                print("Resuming")
        except:
            print("Still some issue")
    #print(response.headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve contents. Status code: {response.status_code}")
        return None

def travel_repository_contents(session, owner, repo, path="", recursive=False, indent=0):
    contents = get_repository_contents(session, owner, repo, path, recursive)

    if contents is not None:
        for item in contents:
            if item["type"] == "dir":
                travel_repository_contents(session, owner, repo, item["path"], recursive, indent + 1)
            else:
                if (".yml" in item['name'] or ".yaml" in item['name']):
                    #get_file(session, owner, repo, item['path'], item['name'])
                    #print(session)
                    print("Getting file Loop")
                    cur_dir=os.getcwd()
                    base_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{item['path']}"
                    print(base_url)
                    with open(f"{cur_dir}\Phase3\file_to_dl_url2.txt","a") as tmp:
                        tmp.write(base_url)
                        tmp.write("\n")

session_counter=0
counter=0
session=requests.Session()
cur_dir=os.getcwd()
with open(f"{cur_dir}\Phase3\url0.txt","r") as file:
    urls=file.readlines()
for base_url in urls:
    print(f"Base URL: {base_url}")
    if (session_counter>=10):
        print("Changing session")
        session_counter=0
        session.close()
        session=requests.Session()
    start = time.time()
    counter+=1
    print(counter)
    owner=base_url.split("/")[3]
    repo=base_url.split("/")[4].strip()
    path = ""
    recursive = True
    try:
        travel_repository_contents(session=session, owner=owner, repo=repo, path=path, recursive=recursive)
    except:
        with open(f"{cur_dir}\Phase3\unavailable_github.txt","a") as tmp:
            tmp.write(base_url)
    end = time.time()
    print(end - start)
    time.sleep(3)
    session_counter+=1