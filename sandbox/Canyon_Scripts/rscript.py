import subprocess
import os
import time
from datetime import date

#Switch directory to root of code repo
canyon_dir=os.getcwd()
os.chdir("../anomalyDetection/AnomalyDetection/")
cwd=os.getcwd()

#Get time information for post script of match
t=time.localtime()
current_time = time.strftime("%H:%M", t)
today=date.today()
month=str(today.month)
day=str(today.day)
post=month+"_"+day+"_"+current_time

#Get files in source and test directories
r_source_dir=cwd+"/R/"
r_test_dir=cwd+"/tests/testthat/"
source_arr=os.listdir(r_source_dir)
test_arr=os.listdir(r_test_dir)

test_len = str(len(test_arr))
source_len = str(len(source_arr))


#rqqq=cwd+"/R/date_utils.R"
#rddd=cwd+"/tests/testthat/test-ts.R"

for test in test_arr:
	#for source in source_arr:
		#name=test+"<=====>"+source+"______"+post
		subprocess.call(['Rscript',canyon_dir+"/args.R",test,canyon_dir,test_len,source_len])
# for entry in source_arr:
#     for entry1 in test_arr:
#         name=entry+"<=====>"+entry1+"______"+post
#         subprocess.call(['Rscript',canyon_dir+"/args.R",entry,entry1,name,canyon_dir])
#         #print(entry+"<=====>"+entry1+"______"+post)
        


        #filename=os.fsdecode(file)
        #print(filename)
    #filename1=os.fsdecode(file)
    #print(filename1+filename)

#subprocess.call(['Rscript','./Canyon_Scripts/args.R',rqqq,rddd])
#
