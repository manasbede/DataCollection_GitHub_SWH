import requests
import time,os
from datetime import datetime, timedelta

def scraping_slot(slot_list,file_type):
    cur_dir=os.getcwd()
    scraping_output=[]
    #   Max Response per page 100, Checking for maximum pages 10, as maximum 1000 response for the single query
    max_pages=10
    for slot in slot_list:
        for p in range(max_pages):
            #   Configuring Url
            page=p+1
            base_url=f"https://api.github.com/search/repositories?q={file_type}+in:filename+created:{slot}&per_page=100&page={page}"
            data=requests.get(base_url).json()
            if 'message' in data:
                print(f"Search completed for {base_url}")
            else:
                for i in data['items']:
                    print(i['html_url'])
                    scraping_output.append(i['html_url'])
            time.sleep (5)
            del base_url
            del data
            del page

    with open(f"{cur_dir}\Phase1\github_output_{file_type}.txt", "a") as file:
        # Iterate through the list and append each element to a new line in the file
        for item in scraping_output:
            file.write("%s\n" % item)


def scraping_biweekly(date_list,file_type):
    cur_dir=os.getcwd()
    #   Max Response per page 100, Checking for maximum pages 10, as maximum 1000 response for the single query
    max_pages=10
    for index, date in enumerate(date_list):
        if index < len(date_list) - 1:
            next_date = date_list[index + 1]
            for p in range(max_pages):
                scraping_output=[]
                #   Configuring Url
                print(f"For reference : Date : {date}, Next Date : {next_date}, Page : {p}")
                page=p+1
                base_url=f"https://api.github.com/search/repositories?q={file_type}+in:filename+created:{date}..{next_date}&per_page=100&page={page}"
                data=requests.get(base_url).json()
                if 'message' in data:
                    print(f"Search completed for {base_url}")
                else:
                    for i in data['items']:
                        print(i['html_url'])
                        scraping_output.append(i['html_url'])
                time.sleep (5)
                del base_url
                del data
                del page
                with open(f"{cur_dir}\Phase1\github_output_{file_type}.txt", "a") as file:
                    # Iterate through the list and append each element to a new line in the file
                    for item in scraping_output:
                        file.write("%s\n" % item)


def generate_biweekly_dates(start_date, end_date):
    # Convert the input strings to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Initialize an empty list to store bi-weekly dates
    biweekly_dates = []

    # Iterate through the date range in bi-weekly intervals
    current_date = start_date
    while current_date <= end_date:
        biweekly_dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=14)

    return biweekly_dates

def main(file_name=""):
    # 2008 to 2013 : 1, 2013 to 2015 : 1, 2015 to 2016 : 1, 2016 to 2017 : 1, 2017 to 2018 : 2, 2018 to 2019 : 2, 2019 to 2020 : 3, 2020 to 2021: 4, 2021 to 2022 : 4, 2022 to today : 9
    #   Configurations

    if(file_name == ""):
        print("File name is missing")
    else:
        file_type=file_name
        first_slot="2008-01-01..2013-01-01" #   1k results
        second_slot="2013-01-01..2015-01-01" #  1k results
        third_slot="2015-01-01..2016-01-01" #  1k results
        fourth_slot="2016-01-01..2017-01-01" #  1k results
        fifth_slot="2017-01-01..2017-07-01" #  1k results
        sixth_slot="2017-07-01..2018-01-01" #  1k results
        one_k_slots=[first_slot,second_slot,third_slot,fourth_slot,fifth_slot,sixth_slot]

        scraping_slot(one_k_slots,file_type)

        #   From 2018 we can see that the data is expanding  exponentially
        #   Using bi-weekly logic to get the data
        custom_start_date = '2019-01-01'
        custom_end_date = '2023-11-01'

        biweekly_dates_list = generate_biweekly_dates(custom_start_date, custom_end_date)
        scraping_biweekly(biweekly_dates_list,file_type)



if __name__ == "__main__":
    print("Github URL Scraping")
    main("YAML")