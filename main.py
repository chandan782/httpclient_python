import logging
from httpclient import HttpClient

# Usage example
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Create and configure the HTTP client with environment-based configuration
    client = HttpClient()

    # Send an HTTP GET request
    try:
        response = client.request("GET", "https://gorest.co.in/public/v2/posts")

        # Check the response status code
        if response.status_code == 200:
            print("Request was successful.")
        else:
            print(f"Request failed with status code {response.status_code}")

        # Access the response content (response.text) or JSON data (response.json())
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        