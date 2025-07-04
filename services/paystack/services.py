from .base import PaystackBase
import requests
from logger import logger


class PaystackEndpoints(PaystackBase):
    def list_banks(self):
        try:
            url = f"{self.url}/bank?country={self.country}"
            response = requests.get(url, headers=self.header)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"{e}: error from list_banks")
            return {}

    def resolve_account(self, account_number, bank_code):
        try:
            logger.info(f"{self.header}: header from resolve_account")
            url = f"{self.url}/bank/resolve?account_number={account_number}&bank_code={bank_code}"
            response = requests.get(url, headers=self.header)
            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx and 5xx)

            return response.json(), response.status_code

        except requests.exceptions.HTTPError as http_err:
            # Handles HTTP errors (4xx, 5xx)
            logger.info(f"HTTP error occurred: {http_err}")
            return {}, 500

        except requests.exceptions.RequestException as req_err:
            # Handles other requests exceptions (e.g., connection errors)
            logger.info(f"Request exception occurred: {req_err}")
            return {}, 500

        except Exception as e:
            # Handles all other exceptions
            logger.info(f"An error occurred: {e}")
            return {}, 500

    def verify_transaction(self, reference):
        """
        Verifies a Paystack transaction by reference.
        Returns (response_json, status_code)
        """
        try:
            url = f"{self.url}/transaction/verify/{reference}"
            logger.info(f"url: {url}")
            response = requests.get(url, headers=self.header)
            logger.info(f"g=header: {self.header}")
            response.raise_for_status()
            logger.info(f"response: {response.json()}")
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            logger.info(f"HTTP error occurred: {http_err}")
            return {}, 500
        except requests.exceptions.RequestException as req_err:
            logger.info(f"Request exception occurred: {req_err}")
            return {}, 500
        except Exception as e:
            logger.info(f"An error occurred: {e}")
            return {}, 500
