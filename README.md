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

For the DSL, the sequence is:

file -> json events -> timelines for each entity -> visualization data (files)

## Configuration

- input
