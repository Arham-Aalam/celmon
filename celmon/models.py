import json

'''
{
    "status":"SUCCESS",
    "result":null,
    "traceback":null,
    "children":[
        
    ],
    "date_done":"2022-04-01T08:00:08.460734",
    "task_id":"32e3d769-6401-45b2-bd30-f39f06e6976b"
}
'''
class Task(object):

    def __init__(self, data: bytes) -> None:
        self.data = self._parse(data)

        # TODO: Need to define and set member variables.

    def _parse(self, data: bytes) -> dict:
        data = data.decode('utf-8')
        return json.loads(data)

    def __str__(self) -> str:
        return json.dumps(self.data, indent=4)


'''
{
    "body":"W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=",
    "content-encoding":"utf-8",
    "content-type":"application/json",
    "headers":{
        "lang":"py",
        "task":"profile_monitor",
        "id":"cc4291e0-3233-4bc0-b268-05e8db50d9d4",
        "shadow":null,
        "eta":null,
        "expires":null,
        "group":null,
        "group_index":null,
        "retries":0,
        "timelimit":[
            null,
            null
        ],
        "root_id":"cc4291e0-3233-4bc0-b268-05e8db50d9d4",
        "parent_id":null,
        "argsrepr":"()",
        "kwargsrepr":"{}",
        "origin":"gen4028337@7b25640d2cdd",
        "ignore_result":false
    },
    "properties":{
        "correlation_id":"cc4291e0-3233-4bc0-b268-05e8db50d9d4",
        "reply_to":"9aa86fa2-33b4-3c7a-ac4c-b158156b40f8",
        "delivery_mode":2,
        "delivery_info":{
            "exchange":"",
            "routing_key":"monitoring"
        },
        "priority":0,
        "body_encoding":"base64",
        "delivery_tag":"afb01350-30bc-423c-b93f-f20047355b47"
    }
}
'''
class QueueItem(object):
    
    def __init__(self, data: bytes) -> None:
        self.data = self._parse(data)

        # TODO: Need to define and set member variables.

    def _parse(self, data: bytes) -> dict:
        data = data.decode('utf-8')
        return json.loads(data)

    def __str__(self) -> str:
        return json.dumps(self.data, indent=4)