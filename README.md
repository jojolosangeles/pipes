### pipes

Pipes takes a line of text from any input, processes it, and writes 
a line of text to any output.

The options for input:

- stdin
- file
- websocket
- rabbitmq queue

The options for output:

- stdout
- file
- websocket
- rabbitmq queue

The options for processing:

- passthrough
- dsl processor (from a different project)

## The goal

Take DSL input, and output a complete visualization by passing through
a series of independently running processes.

For example, the DSL of ddia-figure5-2, the sequence is:

```
    entities User 1234, Leader, Follower 1/2
    u1 (1)update users set picture_url='me-new.jpg' where user_id=1234 l
    (2)waiting for follower's ok l
    l (1)data change f1
    l (3)data change f2
    f1 (1)ok l
    l (1)ok u1
    f2 (1)ok l
```

To visualize this on observable.com, this JSON is produced:

```
{
  "entities": [
    "User 1234",
    "Leader",
    "Follower 1",
    "Follower 2"
  ],
  "timeline": [
    {
      "from_entity": "User 1234",
      "to_entity": "Leader",
      "start_time": "0",
      "end_time": "1",
      "message": "update users set picture_url='me-new.jpg' where user_id=1234"
    },
    {
      "from_entity": "Leader",
      "to_entity": "Leader",
      "start_time": "1",
      "end_time": "3",
      "message": "waiting for follower's ok"
    },
    {
      "from_entity": "Leader",
      "to_entity": "Follower 1",
      "start_time": "1",
      "end_time": "2",
      "message": "data change"
    },
    {
      "from_entity": "Leader",
      "to_entity": "Follower 2",
      "start_time": "1",
      "end_time": "4",
      "message": "data change"
    },
    {
      "from_entity": "Follower 1",
      "to_entity": "Leader",
      "start_time": "2",
      "end_time": "3",
      "message": "ok"
    },
    {
      "from_entity": "Leader",
      "to_entity": "User 1234",
      "start_time": "3",
      "end_time": "4",
      "message": "ok"
    },
    {
      "from_entity": "Follower 2",
      "to_entity": "Leader",
      "start_time": "4",
      "end_time": "5",
      "message": "ok"
    }
  ]
}
```


## Configuration

- input
