import rpy2.robjects as robjects
#
r_source = robjects.r['source']
r_source('streamline.R')
#
#print('r script finished running’)
