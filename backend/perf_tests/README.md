# 🏃‍♂️ Running Performance Tests

 Prerequisits: 

 1. Start the backend app 

Follow the steps below to run performance tests:

1. Navigate to the project's root directory.
2. Run the command `make perf-tests` in the console.
3. Than launch the Locust GUI at  🚀[http://localhost:8089](http://localhost:8089).
4. Fill in the data fields on the Locust welcome page. The default inputs are provided in the `locust.conf` configuration file, but you can modify these as needed. Confirm by clicking the 'START' button.

# Generating Mock Data

You can generate fake transaction data using a dedicated endpoint. This allows you to add a specified number of transactions to the database (a test database is recommended).

Use the following link to generate mock transactions: 
`http://localhost:8000/api/only_for_purpose/mock_transactions?count=100000&days_back=30`

- **count**: The number of transactions you want to add.
- **days_back**: The number of days in the past to start generating transaction dates from.

You can call this endpoint using Postman, Swagger docs at 
`http://localhost:8000/docs#/default/mock_transactions_api_only_for_purpose_mock_transactions_post`



Macos or Linux use curl: 

```bash
curl -X POST 'http://localhost:8000/api/only_for_purpose/mock_transactions?count=10&days_back=30'
```

Windows powershell terminal
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/only_for_purpose/mock_transactions?count=10&days_back=30" -Method POST -Body @{}
```