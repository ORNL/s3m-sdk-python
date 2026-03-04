from dataclasses import dataclass

@dataclass
class OLCFAPIClient:
    api_token : str
    base_url : str = 'https://s3m.olcf.ornl.gov'