test_that("both directions, e_value, threshold set to med_max", {
  results <- AnomalyDetectionVec(raw_data[[2L]], max_anoms=0.02, direction='both', period=1440, threshold="med_max", e_value=TRUE)
  expect_equal(length(results$anoms), 3)
  expect_equal(length(results$anoms[[2L]]), 6)
  expect_equal(results$plot, NULL)
})
