library(devtools)
library(methods)
library(testthat)
#devtools::load_all(".")


args <- commandArgs()

source_file<-args[6]
test_file<-args[7]
naming<-args[8]
canyon_dir<-args[9]

source_path<-paste("./R/",source_file,sep="")
test_path<-paste("./tests/testthat/",test_file,sep="")

#test percent with listing of source files
#test1
#func1 - 30%

#print(source_path)
#print(test_path)

#print(args)

library(covr)
#print("idk")
#print("before")
#print(source_file)
#print(test_file)
#print(getwd())

cov<-file_coverage(source_path,test_path)
#print("after")

#print("******************")
#print(paste(canyon_dir,"/output/",sep=""))

setwd(paste(canyon_dir,"/output/",sep=""))

yy <- file(print(paste(naming,".txt",sep="")),open="wt")
sink(yy,type="output")
sink(yy,type="message")
cat(source_file)
cat(" ")
cat(test_file)
cat("\n\n")
cat("*****Running COVR Function print\n\n")
print(cov,group="function")
cat("\n*****Closing sink connection")
sink()
sink()


