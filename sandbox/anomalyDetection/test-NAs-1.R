test_that("check handling of datasets with NAs in the middle", {
  raw_data[floor(length(raw_data[[2L]])/2), "count"] <- NA
  expect_error(AnomalyDetectionTs(raw_data, max_anoms=0.02, direction='both'))
})
