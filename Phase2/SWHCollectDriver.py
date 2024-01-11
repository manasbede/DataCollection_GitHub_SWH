import os,glob,subprocess

#   This is driver program for SWH data collection
#   Part 1: Copy final URL copy file from Phase1, split data in equal 10 sub samples for parallel data collection process.
#   Part 2: Create 10 copies of SWHTravel.py for parallel data collection and replace SWH authentication token.
#           Rate Limits of SWH: 120 per hour without token, 1200 per hour with token.

#   Slicing dataset file from Phase1
def create_dataset_slice():
    cur_dir=os.getcwd()
    with open(f"{cur_dir}\Phase1\github_urls.txt","r") as file:
        url_data=file.readlines()
    total_urls=len(url_data)
    slice_size=int(total_urls/10)

    for iter in range(0,10):
        if iter < 9:
            with open(f"{cur_dir}\Phase2\slice{iter+1}.txt","w") as tmp:
                tmp.writelines(url_data[iter*slice_size:((iter+1)*slice_size)])
        else:
            with open(f"{cur_dir}\Phase2\slice{iter+1}.txt","w") as tmp:
                tmp.writelines(url_data[iter*slice_size:total_urls])


#   Creating 10 copies of SWHTravel.py
def create_swhtravel_copy():
    #   Replace dummy tokens by original tokens
    tokens=["token1","token2","token3","token4","token5","token6","token7","token8","token9","token10"]

    cur_dir=os.getcwd()
    with open(f"{cur_dir}\Phase2\SWHStash.py","r") as file:
        code_copy=file.read()

    for iter in range(0,10):
        tmp_data=code_copy
        tmp_data=tmp_data.replace('i=0',f'i={iter+1}')
        tmp_data=tmp_data.replace('token=""',f'token="{tokens[iter]}"')
        with open(f"{cur_dir}\Phase2\swhstash{iter+1}.py","w") as tmp:
            tmp.write(tmp_data)

def delete_slice_n_copies():
    cur_dir=os.getcwd()
    for fi in glob.glob(f"{cur_dir}\Phase2\slice*"):
        # print(fi)
        os.remove(fi)
    for fi in glob.glob(f"{cur_dir}\Phase2\swhstash*"):
        # print(fi)
        os.remove(fi)

def parallel_process():
    cur_dir=os.getcwd()
    script_path=f"{cur_dir}\Phase2"
    log_path=f"{cur_dir}\Phase2\logs"
    for iter in range(1,11):
        script=f"{script_path}\swhstash{iter}.py"
        print(f"Starting parallel script {iter} for collecting data")
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
    create_swhtravel_copy()
    #parallel_process()