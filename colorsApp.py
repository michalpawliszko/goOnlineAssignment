#!/usr/bin/env python

import argparse
import re
import sys
from colorClass import Color

#parser
parser = argparse.ArgumentParser()
parser.add_argument("--mode", "-m", required=False, default="mix",
            help="Provide one mode from: mix, lowest, highest, mix-saturate. Deafault mode:'mix' .")
parser.add_argument("--file", "-f", required=False, default="colors.txt",
            help="Provide file with colors in valid format. Deafault file: 'colors.txt' " )
parser.add_argument("--colors", "-c", required=False, nargs='+',
            help="Provide two or more colors in valid format. Valid formats: -hex e.g ff0000ff, -rgba e.g 255,0,0,255")
args = parser.parse_args()

#regex
hex_regex = "^([0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})$"
rgba_regex = "^([0-9]{1,3},){3}[0-9]{1,3}$"

#functions
def get_mix(colors):

    n = len(colors)

    average_r= round(sum(map(lambda col: col.rgba[0], colors))/n)
    average_g= round(sum(map(lambda col: col.rgba[1], colors))/n)
    average_b= round(sum(map(lambda col: col.rgba[2], colors))/n)
    average_a= round(sum(map(lambda col: col.rgba[3], colors))/n)

    return average_r,average_g,average_b,average_a

def get_lowest(colors):

    min_r = min(map(lambda col: col.rgba[0], colors))
    min_g = min(map(lambda col: col.rgba[1], colors))
    min_b = min(map(lambda col: col.rgba[2], colors))
    min_a = min(map(lambda col: col.rgba[3], colors))

    return min_r, min_g, min_b, min_a

def get_highest(colors):

    max_r = max(map(lambda col: col.rgba[0], colors))
    max_g = max(map(lambda col: col.rgba[1], colors))
    max_b = max(map(lambda col: col.rgba[2], colors))
    max_a = max(map(lambda col: col.rgba[3], colors))

    return max_r, max_g, max_b, max_a


def get_mix_saturation(colors):

    n = len(colors)
    average_saturation= sum(map(lambda col: col.hsl[1], colors))/n

    return average_saturation

#check input for colors (file or CLI)
if args.colors != None:

    if len(args.colors)<=1:
        print("At least two colors required")
        sys.exit(1)
    
    colors = []
    for color in args.colors:
        hex_search = re.search(hex_regex, color.rstrip("\n"))
        rgba_search = re.search(rgba_regex, color.rstrip("\n"))

        if hex_search:
            hex = color.rstrip("\n")
            colors.append(Color(hex=hex))


        elif rgba_search:

            rgba = tuple(map(lambda x: int(x) ,color.rstrip("\n").split(",")))
            colors.append(Color(rgba=rgba))

        else:
            print("Invalid color format provided.")
            sys.exit(1)

else:

    colors = []
    with open(args.file) as f:

        for color in f.readlines():
            hex_search = re.search(hex_regex, color.rstrip("\n"))
            rgba_search = re.search(rgba_regex, color.rstrip("\n"))

            if hex_search:
                hex = color.rstrip("\n")
                colors.append(Color(hex=hex))

            elif rgba_search:

                rgba = tuple(map(lambda x: int(x) ,color.rstrip("\n").split(",")))
                colors.append(Color(rgba=rgba))


# check mode
if args.mode == "mix":
    
    new_rgba = get_mix(colors)

    Color(rgba=new_rgba).show_details()
    sys.exit(0)


elif args.mode == "lowest":
    new_rgba = get_lowest(colors)

    Color(rgba=new_rgba).show_details()
    sys.exit(0)

elif args.mode == "highest":
    new_rgba = get_highest(colors)

    Color(rgba=new_rgba).show_details()
    sys.exit(0)

elif args.mode == "mix-saturate":

    new_saturation = get_mix_saturation(colors)
    last_color = colors[-1]

    last_color.change_saturation(new_saturation)

    last_color.show_details()
    sys.exit(0)

else:
    print("Invalid mode provided")
    sys.exit(1)

