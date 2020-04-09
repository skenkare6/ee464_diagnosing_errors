library(AnomalyDetection)

listFunctionNames <- function(filename) {
  temp.env <- new.env()
  sys.source(filename, envir = temp.env)
  functions <- lsf.str(envir=temp.env)
  rm(temp.env)
  return(functions)
}

setwd("AnomalyDetection/R")
# setwd("AnomalyDetection/tests/testthat")
files <- list.files()
for (i in seq_along(files)) {
    cat("FILE: ", files[i], "\n")
    if (!startsWith(files[i], "devscript") && endsWith(files[i], ".R")) {
    	# print(files[i])
        print(listFunctionNames(files[i]))
    }
}

# listFunctions("AnomalyDetectionTs", recursive=FALSE)
