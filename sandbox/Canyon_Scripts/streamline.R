library(devtools)
devtools::load_all(".")

args <- commandArgs()
print(args)

source_file<-args[6]
test_file<-args[7]
naming<-args[8]


library(covr)
print("before")
cov<-file_coverage(source_file,test_file)
print("after")

yy <- file(naming,open="wt")
sink(yy,type="output")
sink(yy,type="message")
cat("*****Running COVR Function print\n\n")
print(cov,group="function")
cat("\n*****Closing sink connection")
sink()
sink()
