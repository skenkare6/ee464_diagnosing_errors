test_that("checking for errors if time series has constant value for all values", {
    data <- rep(1,1000)
    expect_true({AnomalyDetectionVec(data, period=14, plot=T, direction='both'); TRUE})

})
