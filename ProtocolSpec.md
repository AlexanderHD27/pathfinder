
## Connection Details
TCP Port: 1337

Message format:
```
{
    "op": "<command>",
    "<parameter0>": "<value0>",
    "<parameter1>": "<value1>",
    ...
}
```

## Commands
### `echo`
Just replies with the same package, that was sent

### `move`
Moves the robot by `n` squares into the current facing direction <br>
`n`: int

### `turn`
Turns the robot to `n` degree relative to starting position <br>
`n`: int

### `color`
Returns current value of the color sensor as rgb value <br>
Response: `{"color": [int, int, int]}`

### `scan`
Scans the surrounding for walls relative to current orientation. The results are returned in the order left, front, right <br>
Response: `{"color": [int, int, int]}`

### `con`
Prints `msg` to the robots stdout
`msg`: str

### `conIn`
Reads from robots stdin. First prints `msg` if present
`msg`: str
Response: `{"input": str}`

### `led`
Set the led group `group` to the color `color`. If `color` is not a valid color the leds shut off
`group`: `"LEFT"` or `"RIGHT"`
`color`: `"BLACK"`, `"RED"`, `"GREEN"`, `"AMBER"`, `"ORANGE"` or `"YELLOW"`

### `reset`
Resets everything
(Not implemented)

### `status`
Returns the robot status
(Not implemented)

