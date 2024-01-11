import requests
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np
import time,os

#   For this experiment, considering year range from 2008 to 2023 (01-01-2008 to 01-11-2023)

def main():
    repository_count_yaml=[]
    repository_count_yml=[]
    session=requests.Session()
    cur_dir=os.getcwd()


    for year in range(2008, 2024):
        url=f""
        url_yml=f""
        if year == 2023:
            url=f"https://github.com/search?q=yaml+in:filename+created:{year}-01-01..{year}-11-01&type=Repositories"
            url_yml=f"https://github.com/search?q=yml+in:filename+created:{year}-01-01..{year}-11-01&type=Repositories"
        else:
            url=f"https://github.com/search?q=yaml+in:filename+created:{year}-01-01..{year}-12-31&type=Repositories"
            url_yml=f"https://github.com/search?q=yml+in:filename+created:{year}-01-01..{year}-12-31&type=Repositories"

        print(year)
        r= session.get(url)
        print(r.json()['payload']['result_count'])
        repository_count_yaml.append(int(r.json()['payload']['result_count']))
        time.sleep(10)


        r= session.get(url_yml)
        print(r.json()['payload']['result_count'])
        repository_count_yml.append(int(r.json()['payload']['result_count']))
        del url
        del url_yml
        time.sleep(10)

    years=[data for data in range(2008, 2024)]
    # repository_count_yaml=[58, 151, 145, 242, 375, 530, 859, 1229, 1431, 2149, 2642, 3303, 4211, 4236, 5119, 4836]
    # repository_count_yml=[9, 21, 30, 34, 86, 92, 186, 292, 450, 719, 867, 1121, 1301, 1342, 1641, 1627]

    print("YAML repository count: ", repository_count_yaml)
    print("YML repository count: ", repository_count_yml)

    X_Y_Spline = make_interp_spline(years, repository_count_yaml)
    X_ = np.linspace(2008,2023, 500)
    Y_ = X_Y_Spline(X_)

    fig = plt.figure(figsize = (10, 5))
    # creating the bar plot
    plt.bar(years, repository_count_yaml, color ='orange', 
            width = 0.4)
    plt.plot(X_, Y_)
    plt.fill_between(X_, Y_, color='blue', alpha=.1)
    plt.xlabel("Years")
    plt.ylabel("No. of repositories containing YAML created on GitHub")
    plt.title("Repositories containing YAML files on GitHub")
    plt.savefig(f"{cur_dir}\Phase0\YAML_Count.jpg")
    plt.show()


    X_Y_Spline = make_interp_spline(years, repository_count_yml)
    X_ = np.linspace(2008,2023, 500)
    Y_ = X_Y_Spline(X_)
    fig = plt.figure(figsize = (10, 5))
    # creating the bar plot
    plt.bar(years, repository_count_yml, color ='blue', 
            width = 0.4)
    plt.plot(X_, Y_)
    plt.fill_between(X_, Y_, color='orange', alpha=.2)
    plt.xlabel("Years")
    plt.ylabel("No. of repositories containing YML created on GitHub")
    plt.title("Repositories containing YML files on GitHub")
    plt.savefig(f"{cur_dir}\Phase0\YML_Count.jpg")
    plt.show()


    total_yaml=0
    for i in repository_count_yaml:
        total_yaml+=i


    total_yml=0
    for i in repository_count_yml:
        total_yml+=i

    files=["YAML","YML"]
    total=[total_yaml,total_yml]
    fig = plt.figure(figsize = (10, 5))
    # creating the bar plot
    plt.bar(files, total, color ='orange', 
            width = 0.4)
    plt.xlabel("File Types")
    plt.ylabel("No. of repositories containing files and created on GitHub")
    plt.title("Repositories containing specific files on GitHub")
    plt.show()

if __name__ == "__main__":
    main()