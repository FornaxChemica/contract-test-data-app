# Rental Contract Test Data Generator (Containerized)
A small Python web app that generates sample rental-contract records for testing the capstone rental-contract portal.
It uses only the Python standard library, so the image stays small.

Build:  docker build -t contract-test-data .
Run:    docker run -d -p 8080:8080 --name contract-app contract-test-data
Open:   http://localhost:8080  or  http://localhost:8080/api/contracts?count=5
Stop:   docker stop contract-app && docker rm contract-app
