test_that("check handling of datasets with NAs in the middle", {
  raw_data[floor(length(raw_data[[2L]])/2), "count"] <- NA
  expect_error(AnomalyDetectionVec(raw_data[[2L]], max_anoms=0.02, period=1440, direction='both'))
})
