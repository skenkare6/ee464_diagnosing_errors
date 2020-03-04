test_that("last day, both directions, with plot", {
  results <- AnomalyDetectionTs(raw_data, max_anoms=0.02, direction='both', only_last='day', plot=T)
  expect_equal(length(results$anoms), 2)
  expect_equal(length(results$anoms[[2L]]), 25)
  expect_equal(class(results$plot), c("gg", "ggplot"))
})
