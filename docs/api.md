# API Reference

Start the API from the project root after training:

```powershell
python -m uvicorn app.api:app --reload
```

`GET /health` returns status and active model version, or HTTP 503 if no model is
available. `POST /predict` accepts JSON and responds with an estimate, empirical
range, algorithm, and model version. Invalid or missing inputs return HTTP 422.

```json
{
  "Area": 1500,
  "Bedrooms": 3,
  "Bathrooms": 2,
  "Age": 5,
  "Location": "City Center",
  "Property_Type": "Apartment"
}
```

The response fields are `estimated_price`, `estimated_range_low`,
`estimated_range_high`, `range_method`, `model_version`, and `algorithm`.
Interactive OpenAPI docs are available at `/docs` while the API is running.