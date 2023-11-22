import requests

def run_fraud_analysis():
    url = "http://127.0.0.1:8000/predict_all"  # Replace with the API endpoint URL
    headers = {'Content-Type' : 'application/json'}  # Replace with your authentication headers


    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        # Process the response data
        # analysis_result = response.json()
        # Perform further actions based on the analysis result

        print("Fraud analysis completed successfully.")

    except requests.exceptions.RequestException as e:
        print("Error occurred during API request:", e)

if __name__ == "__main__":
    run_fraud_analysis()