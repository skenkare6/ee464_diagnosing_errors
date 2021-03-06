test_that("check handling of datasets with leading and trailing NAs", {
  raw_data[1:10, "count"] <- NA
  raw_data[length(raw_data[[2L]]), "count"] <- NA
  results <- AnomalyDetectionVec(raw_data[[2]], max_anoms=0.02, period=1440, direction='both', plot=T)
  expect_equal(length(results$anoms), 2)
  expect_equal(length(results$anoms[[2L]]), 131)
  expect_equal(class(results$plot), c("gg", "ggplot"))
})
