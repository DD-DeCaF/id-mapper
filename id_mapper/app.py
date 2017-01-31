from aiohttp import web

from venom.rpc import Service, Venom
from venom.rpc.comms.aiohttp import create_app
from venom.rpc.method import http

from id_mapper.stubs import QueryRequest, QueryResponse
from id_mapper.graph import find_match


class IDMapping(Service):
    @http.GET('./query')
    def query(self, request: QueryRequest) -> QueryResponse:
        return QueryResponse(ids=find_match(
            request.id, request.db_from, request.db_to
        ))

venom = Venom()
venom.add(IDMapping)

app = create_app(venom)

if __name__ == '__main__':
    web.run_app(app)
