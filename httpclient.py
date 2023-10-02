from config import Config
import logging
import requests
import json

class HttpClient:
    def __init__(self, config=None):
        self.config = config or Config()
        self.session = self.config.transport
        
    def request(self, method, url, headers=None, data=None):
        req_kwargs = {
            "method": method,
            "url" : url,
            "headers": headers,
            "data": data,
            "timeout": self.config.timeout
        }
        
        if self.config.use_proxy:
            req_kwargs["proxies"] = self.config.proxy_url
            
        try:
            response = self.session.request(**req_kwargs)
            response.raise_for_status()
            
            if self.config.log_req_res_enable:
                logging.info(f"Request: {method} {url}")
                if headers:
                    logging.info(f"Request Headers: {headers}")
                if data:
                    logging.info(f"Request Body: {data}")
                
                logging.info(f"Response: {response.status_code} {response.reason}")
                if response.headers:
                    logging.info(f"Response Headers: {response.headers}")
                if self.config.log_req_res_body_enable:
                    try:
                        response_data = response.json()
                        logging.info(f"Response Body: {json.dumps(response_data, indent=2)}")
                        
                    except ValueError:
                        logging.info(f"Respnse Body: {response.text}")
            
            return response

        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            logging.error(f"RequestException: {str(e)}")
            raise

        except requests.exceptions.HTTPError as e:
            # Handle HTTP error responses (4xx and 5xx status codes)
            logging.error(f"HTTPError: {str(e)}")
            raise

        except Exception as e:
            # Handle other unexpected errors
            logging.error(f"Unexpected Error: {str(e)}")
            raise