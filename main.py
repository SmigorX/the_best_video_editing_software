import os
os.environ["IMAGEIO_USE_GPU"] = "true"

from moviepy.editor import VideoFileClip
import argparse


class ArgParser:
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(description='Do some video stuff')
        self.arg_parser.add_argument('-S', '--start', type=int, help='Start of cut')
        self.arg_parser.add_argument('-E', '--end', type=int, help='End of cut')
        self.arg_parser.add_argument('-I', '--input', type=str, help='Input file', required=True)
        self.arg_parser.add_argument('-O', '--output', type=str, help='Output file', required=True)
        self.arg_parser.add_argument('-W', '--width', type=int, help='Output width')
        self.arg_parser.add_argument('-H', '--height', type=int, help='Output height')
        self.arg_parser.add_argument('-T', '--type', type=str, help='Output type', choices=['mp4', 'gif'], required=True)

        self.arg_parser.usage = "main.py [-h for help]"
        self.parameters = self.arg_parser.parse_args()
        self.ValidateArguments()

    def ValidateArguments(self):
        self.CheckFileExists()
        self.CheckHelp()
        self.Checkresolution()
        self.CheckCut()

    def CheckFileExists(self):
        if not os.path.isfile(self.arg_parser.parse_args().input):
            raise argparse.ArgumentTypeError("File not found")

    def CheckHelp(self):
        if 'help' in self.parameters:
            self.arg_parser.print_help()
            exit()

    def Checkresolution(self):
        if self.arg_parser.parse_args().width and self.arg_parser.parse_args().height is None:
            raise argparse.ArgumentTypeError("You must specify both width and height")
        elif self.arg_parser.parse_args().height and self.arg_parser.parse_args().width is None:
            raise argparse.ArgumentTypeError("You must specify both width and height")

    def CheckCut(self):
        if self.arg_parser.parse_args().start and self.arg_parser.parse_args().end is None:
            raise argparse.ArgumentTypeError("You must specify both start and end")
        elif self.arg_parser.parse_args().end and self.arg_parser.parse_args().start is None:
            raise argparse.ArgumentTypeError("You must specify both start and end")


def VideoOperations():
    parameters = ArgParser().parameters

    #loading
    file = VideoFileClip(parameters.input)

    #cutting
    if parameters.start and parameters.end is not None:
        file = file.subclip(parameters.start, parameters.end - file.duration)

    #resizing
    if parameters.width and parameters.height is not None:
        file = file.resize(width=parameters.width, height=parameters.height)

    #saving
    if parameters.type == 'mp4':
        file.write_videofile(f"{parameters.output}.mp4", codec='libx264', fps=file.fps)
        print("worked")
    if parameters.type == 'gif':
        file.write_videofile(f"{parameters.output}.gif", codec='gif', fps=file.fps)

    file.close()


VideoOperations()
