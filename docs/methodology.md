# Modeling Methodology

## Business Problem

Provide a transparent initial asking-price estimate from a property's physical
characteristics and broad location. The result is a decision aid, not an
automated valuation or appraisal.

## Workflow

The `Property_ID` field is dropped before modeling. A seeded 80/20 split reserves
60 rows for final testing. Every preprocessing operation is inside a scikit-learn
pipeline, so imputers, scaling, and one-hot categories are learned within each
training fold. Five-fold shuffled cross-validation on the training partition
selects among Linear Regression, Random Forest, and Gradient Boosting by mean R².

The report includes test MAE, RMSE, R², and MAPE, plus cross-validation mean and
standard deviation. Feature impact is measured with permutation importance on
the held-out test set; larger positive R² decrease means that shuffling a
feature harms predictions more. This is a model-specific diagnostic, not causal
evidence.

An indicative range uses the 90th percentile of absolute test residuals around
the estimate. With only 60 test cases, this is a rough empirical error band and
does not guarantee coverage for future properties. Synthetic-looking patterns
and the small sample make this a learning project; stronger business use needs
more representative, current, geographically grounded data.

## Complexity and Trade-offs

Linear Regression offers a compact, interpretable baseline but can miss
nonlinear interactions. Tree ensembles can capture nonlinearities but are less
transparent and can overfit small datasets. The selected model is chosen by
cross-validation rather than complexity alone. Compare CV dispersion and held-out
error alongside R² before treating a modest score difference as meaningful.

## Business Interpretation

Importance rankings describe reliance of this fitted model on this dataset.
They do not mean that changing a feature will cause the predicted price to
change by a particular amount. Location, property type, size, and condition
effects can be confounded by unobserved neighborhood and market factors.