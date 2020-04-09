test_that("both directions, e_value, threshold set to med_max", {
  results <- AnomalyDetectionTs(raw_data, max_anoms=0.02, direction='both', threshold="med_max", e_value=TRUE)
  expect_equal(length(results$anoms), 3)
  expect_equal(length(results$anoms[[2L]]), 4)
  expect_equal(results$plot, NULL)
})
