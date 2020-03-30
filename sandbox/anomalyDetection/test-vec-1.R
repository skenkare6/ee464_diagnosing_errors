test_that("both directions, e_value, with longterm", {
  results <- AnomalyDetectionVec(raw_data[[2L]], max_anoms=0.02, direction='both', period=1440, longterm_period=1440*14, e_value=TRUE)
  expect_equal(length(results$anoms), 3)
  expect_equal(length(results$anoms[[2L]]), 131)
  expect_equal(results$plot, NULL)
})
