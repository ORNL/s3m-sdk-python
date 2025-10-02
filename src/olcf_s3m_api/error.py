import logging
import sys

# Configure basic logging to stdout
logging.basicConfig(
	level = logging.ERROR,
	format = "%(asctime)s - %(levelname)s - %(message)s",
	handlers = [logging.StreamHandler(sys.stdout)]
)

# Generic error case
class S3MError(Exception):
	def __init__(self, message = "S3M Error"):
		self.message = message
		super().__init__(self.message)
		logging.error(self.message)

# Authentication
class AuthenticationError(S3MError):
	def __init__(self, message = ""):
		super().__init__(message)

# Job Errors
class S3MJobIDError(S3MError):
	def __init__(self, message = "", jobid = "-1"):
		super().__init__(f"Job ID: {jobid}. {message}")
