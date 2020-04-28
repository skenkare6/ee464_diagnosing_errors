library(AnomalyDetection)

listFunctionNames <- function(filename) {
  temp.env <- new.env()
  sys.source(filename, envir = temp.env)
  functions <- lsf.str(envir=temp.env)
  rm(temp.env)
  return(functions)
}

args = commandArgs(trailingOnly=TRUE)
setwd(args[1])
# setwd("AnomalyDetection/tests/testthat")
print(listFunctionNames(args[2]))

# listFunctions("AnomalyDetectionTs", recursive=FALSE)
