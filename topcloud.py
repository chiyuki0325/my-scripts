#!/usr/bin/python3
from re import sub
from os import popen
from subprocess import Popen,PIPE
from pathlib import Path
from wordcloud import WordCloud


def topcloud():
    command_list = []
    if not Path('/usr/bin/top').is_symlink():
        output = str(execute("top -b -n 1")).split("\\n")[7:]
    else:
        output = str(execute("top -b -n 1")).split("\\n")[4:]
    for line in output[:-1]:
        line = sub(r'\s+', ' ', line).strip()
        fields = line.split(" ")
        try:
            if fields[11].count("/") > 0:
                command = fields[11].split("/")[0]
            else:
                command = fields[11]

            cpu = float(fields[8].replace(",", "."))
            mem = float(fields[9].replace(",", "."))

            if command != "top":
                command_list.append((command, cpu, mem))
        except BaseException:
            pass
    command_dict = {}
    for command, cpu, mem in command_list:
        if command in command_dict:
            command_dict[command][0] += cpu
            command_dict[command][1] += mem
        else:
            command_dict[command] = [cpu + 1, mem + 1]

    resource_dict = {}

    for command, [cpu, mem] in command_dict.items():
        resource_dict[command] = (cpu ** 2 + mem ** 2) ** 0.5

    width, height = None, None
    try:
        width, height = ((popen("xrandr | grep '*'").read()).split()[0]).split("x")
        width = int(width)
        height = int(height)
    except BaseException:
        pass
    if not width or not height:
        width = 1920
        height = 1080
    background = "#101010"
    margin = 20

    try:
        print(resource_dict)
        cloud = WordCloud(
            background_color=background,
            width=width - 2 * int(margin),
            height=height - 2 * int(margin)
        ).generate_from_frequencies(resource_dict)
    except ValueError:
        return "error"
    cloud.to_file("/tmp/cloud.png")
    return "success"

def execute(command):
    result=Popen(command,shell=True, stdout=PIPE).stdout.read()
    return result

print(topcloud())