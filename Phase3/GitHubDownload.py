import requests
import os,time, datetime, calendar

cur_dir=os.getcwd()
headers={ "Authorization": f"Bearer private_github_token",}

with open(f"{cur_dir}\Phase3\file_to_dl_url0.txt","r") as url1:
    data=url1.readlines()

data_size=len(data)
data_to_dl=data[data_size]
session_counter=0
counter=0
session=requests.Session()
for url in data_to_dl:
    print(f"Base URL: {url}")
    url=url.strip()
    if (session_counter>=10):
        print("Changing session")
        session_counter=0
        session.close()
        session=requests.Session()
    response=session.get(url,headers=headers)
    if response.status_code == 200:
        file_name=url.split("https://api.github.com/repos/")[1].replace("/","_")
        try:
            print("Download URL: ",response.json()['download_url'])
            download=session.get(response.json()['download_url'],headers=headers)
            try:
                open(f'{cur_dir}\Dataset\GitHub\{file_name}', 'wb').write(download.content)
            except:
                fname=file_name.split("_")[-1].replace(":","")
                open(f'{cur_dir}\Dataset\GitHub\{file_name.split("_contents")[0]}{fname}', 'wb').write(download.content)
        except:
            print("Unable to fetch file")
    else:
        print("Issues while getting the file")
    
    date=datetime.datetime.utcnow()
    timen=calendar.timegm(date.utctimetuple())
    print("Current Request Limit: ",response.headers['X-RateLimit-Remaining'])
    if(int(response.headers['X-RateLimit-Remaining']) < 3):
        print("Waiting due to RateLimit", int(response.headers['X-RateLimit-Reset']))
        time.sleep(int(response.headers['X-RateLimit-Reset'])-int(timen))
        time.sleep(10)
        print("Resuming")
    session_counter+=1
    #time.sleep(3)