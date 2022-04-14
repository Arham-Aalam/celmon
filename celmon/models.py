import json
from typing import Any

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

{'celery@mnode': [],                   
 'celery@rnode': [{'id': 'd8c56f69-36d6-4462-bc7b-63b8ff4bf8d4',                                                                                              
   'name': 'process_report',                                                   
   'args': [{'first_name': 'name',                                            
     },                                                    
    'idi',                         
    387],                              
   'kwargs': {'host': 'https://xyz.ai'},                                                                                                             
   'type': 'process_report',                                                   
   'hostname': 'celery@rnode',                                                 
   'time_start': 1649221920.0255055,                                           
   'acknowledged': True,                                                       
   'delivery_info': {'exchange': '',                                           
    'routing_key': 'reports',                                                  
    'priority': 0,                     
    'redelivered': None},                                                      
   'worker_pid': 390949}]} 
'''
class Task(object):

    def __init__(self, data: Any) -> None:
        if isinstance(data, bytes):
            data = self._parse(data)
        self.data = data

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

Node can contain multipe queues

{"celery@9eabf02592f0": 
    [{"name": "keyword_search", 
        "exchange": 
            {"name": "keyword_search", "type": "direct", "arguments": null, "durable": true, "passive": false, "auto_delete": false, "delivery_mode": null, "no_declare": false}, "routing_key": "keyword_search", "queue_arguments": null, "binding_arguments": null, "consumer_arguments": null, "durable": true, "exclusive": false, "auto_delete": false, "no_ack": false, "alias": null, "bindings": [], "no_declare": null, "expires": null, "message_ttl": null, "max_length": null, "max_length_bytes": null, "max_priority": null}], "celery@mnode": [{"name": "monitoring", "exchange": {"name": "monitoring", "type": "direct", "arguments": null, "durable": true, "passive": false, "auto_delete": false, "delivery_mode": null, "no_declare": false}, "routing_key": "monitoring", "queue_arguments": null, "binding_arguments": null, "consumer_arguments": null, "durable": true, "exclusive": false, "auto_delete": false, "no_ack": false, "alias": null, "bindings": [], "no_declare": null, "expires": null, "message_ttl": null, "max_length": null, "max_length_bytes": null, "max_priority": null}], 
"celery@rnode": [{"name": "reports", "exchange": {"name": "reports", "type": "direct", "arguments": null, "durable": true, "passive": false, "auto_delete": false, "delivery_mode": null, "no_declare": false}, "routing_key": "reports", "queue_arguments": null, "binding_arguments": null, "consumer_arguments": null, "durable": true, "exclusive": false, "auto_delete": false, "no_ack": false, "alias": null, "bindings": [], "no_declare": null, "expires": null, "message_ttl": null, "max_length": null, "max_length_bytes": null, "max_priority": null}]}
'''
class NodeItem(object):
    
    def __init__(self, data: bytes) -> None:
        self.data = self._parse(data)

        # TODO: Need to define and set member variables.

    def __init__(self, node, data) -> None:
        self.data = data
        self.node = node
        self.queues = [d['name'] for d in self.data]

    def _parse(self, data: bytes) -> dict:
        data = data.decode('utf-8')
        return json.loads(data)

    def __str__(self) -> str:
        return self.node + '\n' + json.dumps(self.data, indent=4)

'''
"{"body": "W1sxLCAzXSwge30sIHsiY2FsbGJhY2tzIjogbnVsbCwgImVycmJhY2tzIjogbnVsbCwgImNoYWluIjogbnVsbCwgImNob3JkIjogbnVsbH1d", "content-encoding": "utf-
8", "content-type": "application/json", "headers": {"lang": "py", "task": "add", "id": "bfdebfa0-8591-44fc-aa58-0fe317e4c013", "shadow": 
null, "eta": null, "expires": null, "group": null, "group_index": null, "retries": 0, "timelimit": [null, null], "root_id": "bfdebfa0-8591-44fc
-aa58-0fe317e4c013", "parent_id": null, "argsrepr": "(1, 3)", "kwargsrepr": "{}", "origin": "gen523790@7b25640d2cdd", "ignore_result": false}
, "properties": {"correlation_id": "bfdebfa0-8591-44fc-aa58-0fe317e4c013", "reply_to": "39dd6aa1-ff80-3175-8262-c39c6eac9fa1", "delivery_mode": 2,
 "delivery_info": {"exchange": "", "routing_key": "reports"}, "priority": 0, "body_encoding": "base64", "delivery_tag": "d6b1ede2-7013-41e1
-bc4d-5b0a9cf3361d"}}"
'''
class PendingTask(Task):

    def __init__(self, data: bytes) -> None:
        super().__init__(data)