#   This program is to identify keywords from all YAML files

import pandas as pd
import time,re
import os,glob
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.reader import Reader
yaml = YAML(typ='safe')

fileLocation=rf"C:\Users\mbedek\Documents\GitHub\DataCollection_GitHub_SWH\Dataset\YAML_DATASET"
cwd=os.getcwd()

def main():
    fileData=[]
    counter=0
    for f in Path(fileLocation).glob("*"):
        f=str(f).split(f"{fileLocation}\\")[1]
        fileData.append(f)
    print(counter,len(fileData))

    for fileToCheck in fileData:
        print(fileToCheck)
        counter+=1
        print("Current File Number: ", counter)
        keywords=[]
        try:
            with open(f"{fileLocation}\\{fileToCheck}","r", encoding="utf-8") as file:
                content=file.readlines()
        except:
            try:
                with open(f"{fileLocation}\\{fileToCheck}","r", encoding="utf-16") as file:
                    content=file.readlines()
            except:
                print("Issue")
                continue
        for cnt in content:
            cnt=cnt.strip()
            tmp=cnt.split(": ")
            if (len(tmp)>1):
                try:
                    if (tmp[0][0]!="#"):
                        tmp=tmp[0].split()
                        #print(tmp)
                        if len(tmp)>1:
                            tmp=[value for value in tmp if any(char.isalnum() for char in value)]
                        tmp=" ".join(tmp)
                        #print(tmp)
                        lenght=len(tmp.split())
                        #print(tmp)
                        if(lenght==1):
                            #print(tmp)
                            tmp=tmp.replace("'","")
                            tmp=tmp.replace('"','')
                            pattern = re.compile(r'[^a-zA-Z0-9-_]|^[^a-zA-Z0-9_]|[^a-zA-Z0-9_]$')
                            if re.search(pattern,tmp):
                                #print(tmp)
                                print(tmp," Not a keyword")
                            else:
                                keywords.append(tmp)
                except:
                    print("Issue with keyword, skipping it")
        keywords=list(set(keywords))
        #print(keywords)
        #time.sleep(10)
        try:
            open(f"{cwd}\\Phase4\\SWHKeyWords.txt","a").write(f"{fileToCheck.split('.')[0]}:{keywords}\n")
        except:
            open(f"{cwd}\\Phase4\\issue.txt","a").write(f"{fileToCheck.split('.')[0]}\n")
if __name__ == "__main__":
    main()
