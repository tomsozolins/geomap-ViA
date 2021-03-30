import inspect
import httpx
from loguru import logger

class Oracle():
  
    def __init__(self):
        try:
            with open('/var/run/secrets/ORACLE_ENDPOINT') as f: self.oracle_endpoint = f.read()
            with open('/var/run/secrets/ORACLE_USER') as f: self.oracle_user = f.read()
            with open('/var/run/secrets/ORACLE_PASS') as f: self.oracle_pass = f.read()
        except:
            # For development environment
            with open('secrets/.ORACLE_ENDPOINT') as f: self.oracle_endpoint = f.read()
            with open('secrets/.ORACLE_USER') as f: self.oracle_user = f.read()
            with open('secrets/.ORACLE_PASS') as f: self.oracle_pass = f.read()
        
        self.timeout = 30

        self.headers = None
        self.data = None
        self.params = None

        self.host_type = None
        self.model = None
        self.hostid = None
        self.vendor = None
        self.location_lat = None
        self.location_lon = None
        self.host_name = None
    
    async def request(self, method, url):
        self.method = method
        self.rest_url = url
        async with httpx.AsyncClient(
                verify=False,
                auth=httpx.BasicAuth(self.oracle_user, self.oracle_pass),
                params=self.params,
                headers=self.headers,
                timeout=self.timeout) as client:
            try:
                r = await client.request(self.method, f'{self.oracle_endpoint}{self.rest_url}', data=self.data, params=self.params)
                logger.info(f"""{self.__class__.__name__} - {inspect.stack()[1].function} - {r.status_code}""")
                return r
            except httpx.HTTPError as e:
                logger.exception(f"""{self.__class__.__name__} - {inspect.stack()[1].function} - {e}""")

    async def delete_geo_points(self):
        await self.request('DELETE', '/geoapi/delete')

    async def create_geo_point(self):
        self.params = {
            'host_type': self.host_type,
            'host_model': self.model,
            'hostid': self.hostid,
            'vendor': self.vendor,
            'location_lat': self.location_lat,
            'location_lon': self.location_lon,
            'host_name': self.host_name
        }
        await self.request('POST', '/geoapi/insert')
    
        



