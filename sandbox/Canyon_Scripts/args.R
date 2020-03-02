library(devtools)
library(methods)
#library(testthat)

devtools::load_all(".")

args <- commandArgs()


test_file<-args[6]
#source_file<-args[7]

#naming<-args[8]
canyon_dir<-args[7]
test_len<-args[8]
source_len<-args[9]

test_path<-paste("../../anomalyDetection/AnomalyDetection/tests/testthat/",test_file,sep="")
#source_path<-paste("./R/",source_file,sep="")
source_path_dir<-("./R/")

#test percent with listing of source files
#test1
#func1 - 30%
#deliniate test files with testname-# etc...

#print(source_path)
#print(test_path)

#print(args)

library(covr)

#print("idk")
#print("before")
#print(source_file)
#print(test_file)
#print(getwd())

file.names<-dir(source_path_dir,pattern ="*.R")
print(file.names)

setwd(paste(canyon_dir,"/output/",sep=""))

yy <- file(print(paste(test_file,".txt",sep="")),open="wt")
sink(yy,type="output")
sink(yy,type="message")
cat(paste("*********Coverage List for",test_file,sep=""))
cat("\n")

#return_dir<-getwd()
#print(getwd())

for(fileNumber in file.names){
	cat("\n")
	print(toupper(fileNumber))
	cov<-file_coverage(paste("../../anomalyDetection/AnomalyDetection/R/",fileNumber,sep=""),test_path)
	print(cov,group="function")

}

#cov<-file_coverage(source_path,test_path)

#print("after")

#print("******************")
#print(paste(canyon_dir,"/output/",sep=""))



# yy <- file(print(paste(test_file,".txt",sep="")),open="wt")
# sink(yy,type="output")
# sink(yy,type="message")
# cat(source_file)
# cat(" ")
# cat(test_file)
# cat("\n\n")
# cat("*****Running COVR Function print\n\n")
# print(cov,group="function")
# cat("\n*****Closing sink connection")
sink()


