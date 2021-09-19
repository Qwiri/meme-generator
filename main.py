from PIL import Image, ImageDraw, ImageFont
import json
import argparse
from io import BytesIO
import win32clipboard

def send_to_clipboard(image):
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

_types = {
    'str': str,
    'int': int,
    'float': float,
    'complex': complex,
    'bool': bool,
}

with open('templates.json', 'r') as f:
    templates = json.load(f)

with open('schema.json', 'r') as f:
    arguments = json.load(f)


parser = argparse.ArgumentParser(description=arguments["description"])

for argument in arguments["arguments"]:
    #optional Argument properties
    if 'default' in argument:
        parser.add_argument(
            '--' + argument['long'],
            help = argument['help'],
            default = argument['default'],
            type = _types[argument['type']],
            metavar = argument['var'],
            required = False
        )
    
    else:
        # required Argument properties
        parser.add_argument(
            '--' + argument['long'],
            help = argument['help'],
            type = _types[argument['type']],
            metavar = argument['var'],
            required = True
        )

args = parser.parse_args()

# Command line argument assertion

template = args.template
fontSize = args.font_size
printingText = args.text
fontPath = args.font

font = ImageFont.truetype(fontPath, int(fontSize))
image = Image.open(templates[template]['path'])
imageDraw = ImageDraw.Draw(image)

imageDraw.text(
    (templates[template]['pos'][0],templates[template]['pos'][1]),
    printingText,
    fill = (0, 0, 0),
    font = font,
    anchor = 'mm'
)

# TODO: Refactor
def alNumify(input_string):
    final_string = ""
    for character in input_string:
        if(character.isalnum()):
            # if character is alphanumeric concat to final_string
            final_string = final_string + character
    return final_string

image.save(alNumify(printingText) + ".png")

send_to_clipboard(image)

