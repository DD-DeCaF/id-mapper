from venom.fields import String, Repeat
from venom.message import Message
from venom.rpc import Stub, http


class QueryRequest(Message):
    id = String()
    db_from = String()
    db_to = String()


class QueryResponse(Message):
    ids = Repeat(String())


class IDMappingStub(Stub):
    @http.GET('./query')
    def query(self, request: QueryRequest) -> QueryResponse:
        raise NotImplementedError
