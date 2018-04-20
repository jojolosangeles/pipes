from dsl2object.dsl_engine import DSL_Engine

dslEngine = DSL_Engine()
dslEngine.set_output_queue("jsonq")

INPUT_FILE_NAME = "data/ddia.figure5-5"

with open(INPUT_FILE_NAME) as input_stream:
    for line in input_stream.readlines():
        dslEngine.process_line(line)
        print("")