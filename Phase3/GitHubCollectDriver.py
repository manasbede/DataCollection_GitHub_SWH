import os,glob,subprocess

#   This is driver program for GitHub data collection
#   Part 1: Copy unavailable URL copy file from Phase2, split data in equal 2 sub samples for parallel data collection process.
#   Part 2: Create 2 copies of GitHubTravel.py for parallel data collection.
#   Part 3: Create 2 copies of GitHubDownload.py file for downloading files from GitHub
#           Rate Limits of GitHub: 60 per hour without token, 5000 per hour with token.

#   Slicing unavailabe URL file from Phase2
def create_dataset_slice():
    cur_dir=os.getcwd()
    with open(rf"{cur_dir}\Phase2\unavailable_swh.txt","r") as file:
        url_data=file.readlines()
    total_urls=len(url_data)
    slice_size=int(total_urls/2)

    for iter in range(0,2):
        with open(rf"{cur_dir}\Phase3\url{iter+1}.txt","w") as tmp:
            tmp.writelines(url_data[iter*slice_size:((iter+1)*slice_size)])


#   Creating 2 copies of GitHubTravel.py
def create_githubtravel_copy():
    #   Replace dummy tokens by original tokens
    tokens=["token1","token2"]

    cur_dir=os.getcwd()
    with open(rf"{cur_dir}\Phase3\GitHubTravel.py","r") as file:
        code_copy=file.read()

    for iter in range(0,2):
        tmp_data=code_copy
        tmp_data=tmp_data.replace('url0.txt',f'url{iter+1}.txt')
        tmp_data=tmp_data.replace('file_to_dl_url0.txt',f'file_to_dl_url{iter+1}.txt')
        tmp_data=tmp_data.replace('private_github_token',f'{tokens[iter]}')
        with open(rf"{cur_dir}\Phase3\githubtrvl{iter+1}.py","w") as tmp:
            tmp.write(tmp_data)

def create_githubdownload_copy():
    #   Replace dummy tokens by original tokens
    tokens=["token1","token2"]

    cur_dir=os.getcwd()
    with open(rf"{cur_dir}\Phase3\GitHubTravel.py","r") as file:
        code_copy=file.read()

    for iter in range(0,2):
        tmp_data=code_copy
        tmp_data=tmp_data.replace('file_to_dl_url0.txt',f'file_to_dl_url{iter+1}.txt')
        tmp_data=tmp_data.replace('private_github_token',f'{tokens[iter]}')
        with open(rf"{cur_dir}\Phase3\githubdwnld{iter+1}.py","w") as tmp:
            tmp.write(tmp_data)

def delete_slice_n_copies():
    cur_dir=os.getcwd()
    for fi in glob.glob(f"{cur_dir}\Phase3\githubtrvl*"):
        # print(fi)
        os.remove(fi)
    for fi in glob.glob(f"{cur_dir}\Phase3\githubdwnld*"):
        # print(fi)
        os.remove(fi)

def parallel_process_travel():
    cur_dir=os.getcwd()
    script_path=f"{cur_dir}\Phase3"
    log_path=f"{cur_dir}\Phase3\travellogs"
    for iter in range(1,11):
        script=f"{script_path}\githubtrvl{iter}.py"
        print(f"Starting parallel script {iter} for collecting downlaod URL")
        output_log_path = f"{log_path}\output{iter}.log"
        error_log_path = f"{log_path}\error{iter}.log"
        # Open files for writing the logs
        with open(output_log_path, 'w') as output_log, open(error_log_path, 'w') as error_log:
            # Use subprocess.Popen to start the script in the background and redirect the output streams
            process = subprocess.Popen(
                ['python', script],
                stdout=output_log,
                stderr=error_log,
                stdin=subprocess.PIPE
            )
            print("Process ID: ", process.pid)

def parallel_process_download():
    cur_dir=os.getcwd()
    script_path=f"{cur_dir}\Phase3"
    log_path=f"{cur_dir}\Phase3\downloadlogs"
    for iter in range(1,11):
        script=f"{script_path}\githubdwnld{iter}.py"
        print(f"Starting parallel script {iter} for collecting downlaod URL")
        output_log_path = f"{log_path}\output{iter}.log"
        error_log_path = f"{log_path}\error{iter}.log"
        # Open files for writing the logs
        with open(output_log_path, 'w') as output_log, open(error_log_path, 'w') as error_log:
            # Use subprocess.Popen to start the script in the background and redirect the output streams
            process = subprocess.Popen(
                ['python', script],
                stdout=output_log,
                stderr=error_log,
                stdin=subprocess.PIPE
            )
            print("Process ID: ", process.pid)

if __name__ == "__main__":
    create_dataset_slice()
    create_githubtravel_copy()
    create_githubdownload_copy()
    #parallel_process_travel()
    #parallel_process_download()