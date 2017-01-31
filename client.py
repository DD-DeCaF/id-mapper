import asyncio

from id_mapper.stubs import IDMappingStub, QueryRequest
from venom.rpc.comms.aiohttp import Client

client = Client(IDMappingStub, 'http://localhost')

async def find_match(met_id, db_from, db_to):
    response = await client.invoke(
        IDMappingStub,
        IDMappingStub.query,
        QueryRequest(id=met_id, db_from=db_from, db_to=db_to))
    print('response:', response.message)

loop = asyncio.get_event_loop()
loop.run_until_complete(find_match('MNXR1', 'mnx', 'bigg'))