# Celmon

A command-line monitoring tool for celery.

## Currently supports

- Django

## Supported brokers

- Redis

## Installation

```
pip install git+https://github.com/Arham-Aalam/celmon.git@master#egg=celmon
```

Development Installation
```
pip install -e git+https://github.com/Arham-Aalam/celmon.git@dev#egg=celmon
```

## Command-line usage

Get queues list
```
celmon -A project_name -qs
```

```
                       Celery queues
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ queue           ┃ node                ┃ number of tasks ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ super_important │ celery@4d2c1fd085c9 │ 0               │
└─────────────────┴─────────────────────┴─────────────────┘
```

Get all active tasks
```
celmon -A project_name -at
```

```
                                      Celery active tasks
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ task_id                              ┃ name ┃ status ┃ time_start         ┃ queue           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ c4e4d302-2a29-4a04-b808-0a81497ddaea │ test │ Active │ 1649921895.3594754 │ super_important │
└──────────────────────────────────────┴──────┴────────┴────────────────────┴─────────────────┘
```

Get all pending tasks

```
celmon -A project_name -pt
```

```
                                    All pending celery tasks
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ task_id                              ┃ name ┃ arguments ┃ keyword arguments ┃ queue           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 74eb7ed7-19be-4f86-a0ba-6c3886df3691 │ test │ ()        │ {}                │ super_important │
│ 59fcb0ad-fc7f-46d4-83fa-71b2613fb9ba │ test │ ()        │ {}                │ super_important │
│ 63a9de93-69aa-49b4-9f4f-14866923391b │ test │ ()        │ {}                │ important       │
│ 6fc66851-c4a7-4aee-a81e-396b38dd3331 │ test │ ()        │ {}                │ super_important │
│ 6c68a479-8419-4442-a10d-75d76367ed7b │ test │ ()        │ {}                │ super_important │
│ dddb2564-d4e9-4fbf-8d4e-968de105b0d5 │ test │ ()        │ {}                │ super_important │
│ 1621b4f9-3254-4e90-bb18-273fa77bc32a │ test │ ()        │ {}                │ super_important │
│ fc9ae3cb-d8a5-4217-aace-c71d757e95f0 │ test │ ()        │ {}                │ super_important │
│ 2dfdd9f9-bad8-42a5-95b1-9806cbfc7c53 │ test │ ()        │ {}                │ important       │
│ aceb1459-f5be-4b62-982f-6282e1d25a43 │ test │ ()        │ {}                │ super_important │
│ cf763df8-a6df-4286-bc78-c967523f25fa │ test │ ()        │ {}                │ super_important │
└──────────────────────────────────────┴──────┴───────────┴───────────────────┴─────────────────┘
```

Get all pending tasks by queue

```
celmon -A accepted_risk -pt -q super_important
```

```
                            Pending celery tasks for super_important
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ task_id                              ┃ name ┃ arguments ┃ keyword arguments ┃ queue           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 7f7269db-2ad3-4562-93a8-1165faa25d6b │ test │ ()        │ {}                │ super_important │
│ 0246cc21-da9a-4dac-a97e-9d69d62d997a │ test │ ()        │ {}                │ super_important │
│ 32ea5ea3-7fa6-4789-98df-a01d7f7ebd61 │ test │ ()        │ {}                │ super_important │
│ ca2b46a7-b45f-46ec-977f-52e44a500796 │ test │ ()        │ {}                │ super_important │
│ 76cdbaa1-014e-4b10-9e64-a068e38e7eb9 │ test │ ()        │ {}                │ super_important │
│ 77ca6b16-29e7-4d94-8edf-b55ce82b9511 │ test │ ()        │ {}                │ super_important │
│ 6256b5d7-ce4b-4bcb-8acb-6875b6d4c5b3 │ test │ ()        │ {}                │ super_important │
│ ddcbe336-69c6-4ea5-8e15-22ed23c043d7 │ test │ ()        │ {}                │ super_important │
│ 5dc8a47f-d380-4a95-a714-fed1450cbc39 │ test │ ()        │ {}                │ super_important │
│ 396e1a81-c957-43c0-92e5-57c99e552b28 │ test │ ()        │ {}                │ super_important │
└──────────────────────────────────────┴──────┴───────────┴───────────────────┴─────────────────┘
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Arham-Aalam/celmon/blob/master/LICENSE)
