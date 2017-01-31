from venom.fields import String, Repeat
from venom.message import Message
from venom.rpc import Stub
from venom.rpc.stub import RPC


class QueryRequest(Message):
    id = String()
    db_from = String()
    db_to = String()


class QueryResponse(Message):
    ids = Repeat(String())


class IDMappingStub(Stub):
    query = RPC.http.GET('./query', QueryRequest, QueryResponse)
