import argparse
import time
from PIL import Image, ImageDraw, ImageFont
from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends.helpers import send
from barcode import Code128
from barcode.writer import ImageWriter
import io
import time

from brother_ql.conversion import convert

backend = None
model = 'QL-800'
imagex = 390
imagey = 130



# printer = 'usb://Brother/QL-800?serial=000J1Z243599'
printer = 'usb://0x04f9:0x209b'

font_bold = ImageFont.truetype("assets/arial-black.ttf", 38)
font_condensed = ImageFont.truetype("assets/arial-condensed.ttf", 30)
font_regular = ImageFont.truetype("assets/arial.ttf", 120)
font_roboto = ImageFont.truetype("assets/Roboto-Regular.ttf", 120)
font_roboto_small = ImageFont.truetype("./assets/Roboto-Regular.ttf", 20)
font_roboto_for_label = ImageFont.truetype("assets/Roboto-Regular.ttf", 23)


def print_brother_label(serial):
    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    canvas = Image.new('RGB', (imagex, imagey), color=(255, 255, 255))
    
    


    
    # Create the barcode
    writer = ImageWriter()
    writer.module_height = 12
    barcode = Code128(f'{serial}', writer=writer)

    # Save the barcode image into a BytesIO object
    raw_barcode = io.BytesIO()
    barcode.write(
        raw_barcode,
        options=dict(module_width=0.31, module_height=12, text_distance=2.5, font_size=6),
    )

    # Load the barcode image into memory
    barcode_image = Image.open(raw_barcode)

    # Resize the barcode image to the desired height (200 pixels)
    aspect_ratio = barcode_image.width / barcode_image.height
    
    print(barcode_image.width)
    print(barcode_image.height)

    barcode_image = barcode_image.resize((int(120 * aspect_ratio), 150))

    # Paste the barcode image onto the canvas
    canvas.paste(barcode_image, (60,0))

    canvas.save(f'assets/{serial}_Label.png')

    # new_canvas = Image.new('RGB', (430, 215), color=(255, 255, 255))
    # new_image = Image.open(f'assets/{serial}_Label.png')

    # new_canvas = new_image.rotate(90, expand=True)
    # new_canvas.save(f'assets/{serial}_Label.png')


    printable_canvas = Image.open(f'assets/{serial}_Label.png')


    ''' if you want to print via brother printer run this'''
    # Create the label
    create_label(qlr, printable_canvas, '29', cut=True, dither=True, threshold=40, compress=True, red=False)

    # Send the instructions to the printer and print 1 copies
    for i in range(1):
        send(instructions=qlr.data, printer_identifier=printer, backend_identifier=backend, blocking=True)
    #     print("hello")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--serial', help='Enter serial number', required=True)
    # args = parser.parse_args()
    # print_brother_label(args.serial)

    while True:
        # Getting input from the user
        user_input = input("Enter serial no to print ")

        # Check if the input is 'exit' to break the loop
        if user_input.lower() == 'exit':
            print("Exiting the loop...")
            break

        # Passing the input value to the function
        print_brother_label(user_input)