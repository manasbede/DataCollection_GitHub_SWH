# DataCollection_GitHub_SWH
## About this Project
Purpose of this project is to find all public repositories on GitHub and Software Heritage which contains a specific type of file.
## Software Heritage (SWH)
Software Heritage initiative is to collect all publicly available software in source code form together with its development history, replicate it massively to ensure its preservation, and share it with everyone who needs it. The Software Heritage archive is growing over time as we crawl new source code from software projects and development forges. Software Heritage contains source codes from different platforms like GitHub, GitLab, GNU, Maven, Bitbucket etc.

Structured collection of data is a key benifit of refering software heritage. Software Heritage facilitates a systematic traversal of any repository. Starting from the Origin (Repository URL), navigating to the actual content of the repository is straightforward. The Software Heritage system holds a significant advantage, as it incorporates the feature of assigning a unique object ID to each Origin, Snapshot, Release, Revision, and Directory.

### Limitations of Different SWH Platforms :
1.  Software Fuse:
	It is  Debian based filesystem structure to browse the software heritage archive. To browse the file system locally first step is to get origin of repository. To get list of all repositories, swh.fuse has "web search" feature. 

	Limitations: 
	1.  Only 10000 repository response in a query.
	2.  Feature not available to store the query checkpoint, hence getting same results.
    3.  Web Search does not have feature to search for repositories which contains specific filetype, hence search is limited to "Repository Name" search. 
2.  Web search: 
	Software Heritage has web search interface, which has option to search for the pattern in metadata instead of just URL. Also, it has filter for visit type.
	
    Limitation:
    1.  Very time consuming to collect all possible repositories
			
3.  Software Graph:
	SH has different API for dataset travel, one of the option is software graph. It is graph representation of the Software Heritage Archive. 

    Limitation:
    1.  Endpoints problem, For graph traversal compressed huge size graph is required, Space requirements are in TiB.

## Project Approach :
1.  Phase 0 : Collecting GitHub repository count trends for the repositories containing specific type of files and deciding scraping date slots
2.  Phase 1 : Capturing repostiry URLs from GitHub using Python and request package. Limitation: maximum 1000 URLs per query.
3.  Phase 2 : Checking URLs on SWH and collecting required files. Also, keeping track of unavailable repositories on SWH. | Limitation: Rate Limit, Slow Server Response
4.  Phase 3 : Scraping repositories from GitHub which are unavailable on SWH. | Limitation: Rate Limit, Session Management issue.

##  Project Stats for YAML and YML File Collection :
Platform|Rate Limit|Number of Repositories to Check|Average Requests Per Repository|Average Repositories Checked per hr|Total Estimated Time in Hrs|Number of Parallel Process|Expected Time in Hrs|Actual Time Taken
--- | --- | --- | --- |--- |--- |--- |--- |---
SWH|1200|37996|20|60|633.27|10|63.3|75.2
GitHub|5000|14877|20|250|59.508|2|29.754|31

## Project Execution
`python3 main.py`

## Current Development Phase :
Phase4: 
1. Extracting KeyWords from the YAML files
2. Overlapping KeyWords with most common keywords of different devops development platforms
3. Finding potential pipelines according to category