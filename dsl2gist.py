"""
dsl2gist.py <input folder> <output folder> <output file extension>

For each file in the input folder:

  process the file with the DSL_engine
  send output to output folder, using the same file name with the output file extension.
"""
from os import walk
import sys

input_folder = sys.argv[1]

def get_files_in_folder(folder):
    f = []
    for (dirpath, dirnames, filenames) in walk(folder):
        f.extend(filenames)
        break
    return f

files = get_files_in_folder(input_folder)
def create_all_applier(method, doc=None):
    def on_all(seq, *args, **kwargs):
        for obj in seq:
            getattr(obj, method)(*args, **kwargs)
    on_all.__doc__ = doc
    return on_all

def pipeline(file, input_folder, output_folder):
    input_channel_parameters = "input file {}/{}".format(input_folder, file).split()
    output_channel_parameters = "output file {}/{}".format(output_folder, file).split()

list(map(lambda x:print(x),files))

z = """
    channelFactory = ChannelFactory()
    input_channel = channelFactory.createInputChannel(input_channel_parameters)
    output_channels = channelFactory.createOutputChannels(output_channel_parameters)
    processor = channelFactory.createProcessor(processor_parameters, output_channels)
    pipe = Pipe(input_channel, output_channels, processor)
    pipe.activate()
    processor.terminate()
"""
