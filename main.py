'''
@author: manasbedekar002

This project is for data scraping from Software Heritage and GitHub.
Phase0 :    This phase analyzes number of repositories available on GitHub from 2008 till date (2023 december)
Phase1 :    This phase fetches repository URLs from GitHub | Limitation: One query can give 10 pages and a page contains at max 100 URLs
Phase2 :    This phase finds fetched URLs from previous phase on Software Heritage; Looks for snapshot, revision, directory and ultimately content. Keeps track of unavailable repositories on Software Heritage
            Limitation: Recent repositories are not available on Software Heritage; Very small rate limit: 120 without token and 1200 with token, Slow server response
Phase3 :    This phase looks for repositories unavailable on Software Heritage and download content directly from GitHub | Limitation: Rate Limit 5000 and session management issue
'''

import os,time
import Phase0.GitHubTrend as GitHubTrend
import Phase1.GitHubURLScraping as GitHubURLScraping
import Phase2.SWHCollectDriver as SWHCollectDriver
import Phase3.GitHubCollectDriver as GitHubCollectDriver

def main():
    cur_dir=os.getcwd()
    #   Collecting github facts about number of repositories
    GitHubTrend.main()

    #   Collecting repositories containing YAML files from GitHub
    GitHubURLScraping.main("YAML")

    #   Collecting repositories containing YML files from GitHub
    GitHubURLScraping.main("YML")

    #   Combining both files into a single file
    with open(rf"{cur_dir}\Phase1\github_output_YAML.txt","r") as file:
        YAML=file.read()
    with open(rf"{cur_dir}\Phase1\github_output_YML.txt","r") as file:
        YML=file.read()
    with open(rf"{cur_dir}\Phase1\github_urls.txt","a") as file:
        file.write(YAML)
        file.write(YML)
    with open(rf"{cur_dir}\Phase1\github_urls.txt","r") as file:
        data=set(file.readlines)
    with open(rf"{cur_dir}\Phase1\github_urls.txt","w") as file:
        file.writelines(list(data))

    #   Collecting files from Software Heritage
    SWHCollectDriver.create_dataset_slice()
    SWHCollectDriver.create_swhtravel_copy()
    SWHCollectDriver.parallel_process()

    #   Checking for repositories unavailable on Software Heritage
    GitHubCollectDriver.create_dataset_slice()
    GitHubCollectDriver.create_githubtravel_copy()
    GitHubCollectDriver.create_githubdownload_copy()
    GitHubCollectDriver.parallel_process_travel()
    GitHubCollectDriver.parallel_process_download()

def cleanBuild():
    GitHubCollectDriver.delete_slice_n_copies()
    SWHCollectDriver.delete_slice_n_copies()

if __name__=="__main__":
    cleanBuild()
    main()