from dataclasses import dataclass

@dataclass
class S3MAuthContext:
    api_token : str
    base_url  : str = "https://s3m.apps.olivine.ccs.ornl.gov"
