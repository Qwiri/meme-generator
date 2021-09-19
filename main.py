from PIL import Image, ImageDraw, ImageFont
import sys
import json

config = json.load(open("config.json", 'r'))


if sys.argv[1] == "help":
    print(
    """
    [---- Fast Meme Generator v1.0 ----]
    Usage:
        python main.py MEMETEMPLATE TEXT [FontSize]

        MEMETEMPLATE:
            monke

    """)
    exit()



printingText = ' '.join([str(v) for v in sys.argv[2:len(sys.argv)]])
fontSize = sys.argv[1]

template = Image.open('res/monke.png')
font = ImageFont.truetype("arial.ttf", int(fontSize))
d1 = ImageDraw.Draw(template)

d1.text(
    (1200,70),
    printingText,
    fill = (0, 0, 0),
    font = font,
    anchor = 'mm'
)
def alNumify(input_string):
    final_string = ""
    for character in input_string:
        if(character.isalnum()):
            # if character is alphanumeric concat to final_string
            final_string = final_string + character
    return final_string

template.save(alNumify(printingText) + ".png")
