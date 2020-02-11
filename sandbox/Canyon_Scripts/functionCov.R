
yy <- file("covFunction.txt",open="wt")
sink(yy,type="output")
sink(yy,type="message")
cat("*****Running COVR Function print\n\n")
print(cov,group="function")
cat("\n*****Closing sink connection")
sink()
sink()

