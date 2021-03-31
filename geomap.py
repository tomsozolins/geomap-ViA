import asyncio
import sys
import time
from contextlib import suppress

from loguru import logger
from oracle import Oracle
from pyzabbix import ZabbixAPI

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO", enqueue=True)

try:
    with open('/var/run/secrets/ZABBIX_ENDPOINT') as f: zabbix_endpoint = f.read()
    with open('/var/run/secrets/ZABBIX_USER') as f: zabbix_user = f.read()
    with open('/var/run/secrets/ZABBIX_PASS') as f: zabbix_pass = f.read()
except:
    # For development environment
    with open('secrets/.ZABBIX_ENDPOINT') as f: zabbix_endpoint = f.read()
    with open('secrets/.ZABBIX_USER') as f: zabbix_user = f.read()
    with open('secrets/.ZABBIX_PASS') as f: zabbix_pass = f.read()

async def main():

    # Zabbix API
    zapi = ZabbixAPI(zabbix_endpoint)
    zapi.session.verify = False
    zapi.login(zabbix_user, zabbix_pass)

    logger.info(f'{zapi.__class__.__name__} - getting host data')
    zabbix_data = zapi.host.get(output="extend", selectInventory=True)

    o = Oracle()

    await o.delete_geo_points()

    # initialize async task list
    async_tasks = []

    # iterate all hosts and create geo points
    for host in zabbix_data:
        o = Oracle()

        # Create geo point if latitude and logitude data exists.
        if 'location_lat' and 'location_lon' in host['inventory']:
            with suppress(Exception):
                o.location_lat = host['inventory']['location_lat']
            
            with suppress(Exception):
                o.location_lon = host['inventory']['location_lon']

            with suppress(Exception):
                o.host_name =  host['host']

            with suppress(Exception):
                o.hostid = host['hostid']

            with suppress(Exception):
                o.model = host['inventory']['model']

            with suppress(Exception):
                o.vendor = host['inventory']['vendor']

            with suppress(Exception):
                o.host_type = host['inventory']['type']

            # append task to task list
            async_tasks.append(asyncio.create_task(o.create_geo_point()))
            # return control to asyncio event loop
            await asyncio.sleep(0)

    # create geo points from async_tasks list
    await asyncio.gather(*async_tasks)
            

# Service loop
while True:
    try:
        time.sleep(3)
        logger.info('Starting loop cycle')
        start = time.time()

        asyncio.run(main())

        end = time.time()
        logger.info(f"Loop cycle finished in {round(end - start, 2)} seconds")

        logger.info(f'Next loop cycle in 20 seconds...')
        time.sleep(20)
    except Exception as e:
        logger.exception(f'{e}')
        continue

