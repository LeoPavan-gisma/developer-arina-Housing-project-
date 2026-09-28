# Data Dictionary

The project uses the supplied 300-row `house_prices.csv` file. The same file is
also preserved at `data/house_prices.csv`; training reads the root copy.

| Column | Type | Meaning | Model use |
|---|---|---|---|
| `Property_ID` | string | Listing identifier | Excluded |
| `Area` | integer | Interior area in square feet | Numeric predictor |
| `Bedrooms` | integer | Number of bedrooms | Numeric predictor |
| `Bathrooms` | integer | Number of bathrooms | Numeric predictor |
| `Age` | integer | Property age in years | Numeric predictor |
| `Location` | category | City Center, Suburb, or Rural | One-hot predictor |
| `Property_Type` | category | Apartment, House, or Villa | One-hot predictor |
| `Price` | integer | Asking price in INR | Prediction target |

The source contains 300 complete rows. Feature values in prediction requests are
validated to sensible operational ranges; unknown non-empty categories are
accepted and safely ignored by the fitted one-hot encoder.