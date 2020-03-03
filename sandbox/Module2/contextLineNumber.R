#Prints an associated R object for a given filename and line number
#Arguments (required): filename line_number

args <- commandArgs(trailingOnly=TRUE)
filename <- args[1]
line <- args[2]

source(filename, keep.source=TRUE)
objects <- findLineNum(paste(filename, line, sep="#"))
if (length(objects) > 0) {
	#print(objects[[1]]) #Print all data for the object
	cat(objects[[1]]$name, "\n")
}
