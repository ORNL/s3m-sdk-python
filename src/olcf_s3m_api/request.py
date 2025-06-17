import requests

from requests.exceptions import RequestException, Timeout, ConnectionError as ReqConnectionError
from .error import S3MError, AuthenticationError

class S3MRequest:
	def __init__(self, default_headers=None, timeout=10):
		self.default_headers = default_headers or {}
		self.timeout = timeout
	
	def _request(self, method, url, headers=None, **kwargs):
		merged_headers = {**self.default_headers, **(headers or {})}

		try:
			response = requests.request(
				method=method.upper(),
				url=url,
				headers=merged_headers,
				timeout=self.timeout,
				**kwargs
			)

			if response.status_code == 401:
				raise AuthenticationError("Unauthorized request to URL: {}".format(url))
			elif response.status_code >= 400:
				raise S3MError("HTTP {} Error for URL {}: {}".format(response.status_code, url, response.text))

			return response

		except Timeout:
			raise S3MError("Timeout occurred when accessing URL: {}".format(url))
		except ReqConnectionError:
			raise S3MError("Connection error occurred for URL: {}".format(url))
		except RequestException as e:
			raise S3MError("RequestException: {} for URL: {}".format(str(e), url))
		except S3MError:
			raise
		except Exception as e:
			raise S3MError("Unexpected error: {} for URL: {}".format(str(e), url))

	def get(self, url, headers=None, **kwargs):
		return self._request("GET", url, headers=headers, **kwargs)

	def post(self, url, headers=None, data=None, json=None, **kwargs):
		return self._request("POST", url, headers=headers, data=data, json=json, **kwargs)

	def put(self, url, headers=None, data=None, json=None, **kwargs):
		return self._request("PUT", url, headers=headers, data=data, json=json, **kwargs)

	def delete(self, url, headers=None, **kwargs):
		return self._request("DELETE", url, headers=headers, **kwargs)
