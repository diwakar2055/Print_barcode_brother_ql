import argparse
import time
from pdf417 import encode, render_image, render_svg
from PIL import Image, ImageDraw, ImageFont
from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends.helpers import send
from barcode import Code128
from barcode.writer import ImageWriter
import io
import time

from brother_ql.conversion import convert

import zpl
from zebra import Zebra

backend = None
model = 'QL-800'
imagex = 2268
imagey = 2930

img_x= 380
img_y = 250

# printer = 'usb://Brother/QL-800?serial=000J1Z243599'
printer = 'usb://0x04f9:0x209b'

font_bold = ImageFont.truetype("assets/arial-black.ttf", 38)
font_condensed = ImageFont.truetype("assets/arial-condensed.ttf", 30)
font_regular = ImageFont.truetype("assets/arial.ttf", 120)
font_roboto = ImageFont.truetype("assets/Roboto-Regular.ttf", 120)
font_roboto_small = ImageFont.truetype("./assets/Roboto-Regular.ttf", 20)
font_roboto_for_label = ImageFont.truetype("assets/Roboto-Regular.ttf", 23)

def print_PCBID(placeholder, model_id, current_fota_ver, current_dfota_ver, imei, mac, batch, serial, token):
    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True
    # model_id,fota_version,dfota_version,serial,token,imei,mac

    canvas = Image.new('RGB', (img_x+20, 30), color=(255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((120, 0), f'S/N : {serial}', font=font_roboto_small, fill=(0, 0, 0))

    canvas.save(f'assets/{serial}_PCBID.png')

    printable_canvas = Image.open(f'assets/{serial}_PCBID.png')
    # Create the label
    create_label(qlr, printable_canvas, '62', cut=True, dither=True, threshold=40, compress=True, red=False)

    for i in range(1):
        send(instructions=qlr.data, printer_identifier=printer, backend_identifier=backend, blocking=True)

def print_ID(placeholder, model_id, current_fota_ver, current_dfota_ver, imei, mac, batch, serial, token):

    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True
    # model_id,fota_version,dfota_version,serial,token,imei,mac
    encoded_text = f"{model_id},{current_fota_ver},{current_dfota_ver},{serial},{token},{imei},{mac}"
    print("To be encoded: ", encoded_text)

    # Convert to code words
    codes = encode(encoded_text, columns=3) # change columns to stretch the horizontal size of the code

    # Generate barcode as image
    image = render_image(codes)  # Pillow Image object
    image.save(f'assets/{serial}_ID.png')

    # canvas = Image.new('RGB', (img_x, img_y), color=(255, 255, 255))
    pdf_encoded_image = Image.open(f'assets/{serial}_ID.png')

    canvas = Image.new('RGB', (img_x+20, img_y), color=(255, 255, 255))
    canvas.paste(pdf_encoded_image, (0, 5))
    draw = ImageDraw.Draw(canvas)
    draw.text((120, 0), f'S/N : {serial}', font=font_roboto_small, fill=(0, 0, 0))

    canvas.save(f'assets/{serial}_ID.png')

    printable_canvas = Image.open(f'assets/{serial}_ID.png')
    # Create the label
    create_label(qlr, printable_canvas, '62', cut=True, dither=True, threshold=40, compress=True, red=False)

    for i in range(1):
        send(instructions=qlr.data, printer_identifier=printer, backend_identifier=backend, blocking=True)


# def print_brother_label(placeholder, model_id, current_fota_ver, current_dfota_ver, imei, mac, batch, serial, token):
#     qlr = BrotherQLRaster(model)
#     qlr.exception_on_warning = True

#     canvas = Image.new('RGB', (imagex, imagey), color=(255, 255, 255))
    
#     # Load the placeholder image
#     placeholder = Image.open(placeholder)
    
#     #resize the placeholder


#     # Paste the placeholder onto the canvas
#     canvas.paste(placeholder, (0, 0))

#     # Create the barcode
#     writer = ImageWriter()
#     writer.module_height = 12
#     barcode = Code128(f'{serial}', writer=writer)

#     # Save the barcode image into a BytesIO object
#     raw_barcode = io.BytesIO()
#     barcode.write(
#         raw_barcode,
#         options=dict(module_width=0.31, module_height=12, text_distance=2.5, font_size=6),
#     )

#     # Load the barcode image into memory
#     barcode_image = Image.open(raw_barcode)

#     # Resize the barcode image to the desired height (200 pixels)
#     aspect_ratio = barcode_image.width / barcode_image.height
#     barcode_image = barcode_image.resize((int(1100 * aspect_ratio), 1100))

#     # Paste the barcode image onto the canvas
#     canvas.paste(barcode_image, (100, 720))

#     # Create an ImageDraw object to add the IMEI and MAC address
#     draw = ImageDraw.Draw(canvas)

#     if len(imei) > 0:
#         if len(mac) == 0:
#             draw.text((475, 1700), f'IMEI: {imei}', font=font_roboto, fill=(0, 0, 0))
#         else:
#             draw.text((475, 1720), f'IMEI: {imei}', font=font_roboto, fill=(0, 0, 0))

#     if len(mac) > 0:
#         if len(imei) == 0:
#             draw.text((525, 1800), f'MAC: {mac}', font=font_roboto, fill=(0, 0, 0))
#         else:
#             draw.text((525, 1860), f'MAC: {mac}', font=font_roboto, fill=(0, 0, 0))

#     canvas.save(f'assets/{serial}_Label.png')

#     new_canvas = Image.new('RGB', (imagey, imagex), color=(255, 255, 255))
#     new_image = Image.open(f'assets/{serial}_Label.png')

#     new_canvas = new_image.rotate(90, expand=True)
#     new_canvas.save(f'assets/{serial}_Label.png')

#     printable_canvas = Image.open(f'assets/{serial}_Label.png')

#     ''' if you want to print via brother printer run this
#     # # Create the label
#     # create_label(qlr, printable_canvas, '62', cut=True, dither=True, threshold=40, compress=True, red=False)

#     # # Send the instructions to the printer and print 1 copies
#     # for i in range(1):
#     #     send(instructions=qlr.data, printer_identifier=printer, backend_identifier=backend, blocking=True)
#     '''

def print_zebra_label(placeholder, model_id, current_fota_ver, current_dfota_ver, imei, mac, batch, serial, token):
   
    canvas = Image.new('RGB', (478, 717), color=(255, 255, 255))
    
    # Load the placeholder image
    placeholder = Image.open(placeholder)
    
    #resize the placeholder


    # Paste the placeholder onto the canvas
    canvas.paste(placeholder, (0, 0))

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
    barcode_image = barcode_image.resize((int(200 * aspect_ratio), 200))

    # Paste the barcode image onto the canvas
    canvas.paste(barcode_image, (50, 230))

    # Create an ImageDraw object to add the IMEI and MAC address
    draw = ImageDraw.Draw(canvas)

    if len(imei) > 0:
        if len(mac) == 0:
            draw.text((108, 425), f'IMEI: {imei}', font=font_roboto_for_label, fill=(0, 0, 0))
        else:
            draw.text((108, 425), f'IMEI: {imei}', font=font_roboto_for_label, fill=(0, 0, 0))

    if len(mac) > 0:
        if len(imei) == 0:
            draw.text((115, 455), f'MAC: {mac}', font=font_roboto_for_label, fill=(0, 0, 0))
        else:
            draw.text((115, 455), f'MAC: {mac}', font=font_roboto_for_label, fill=(0, 0, 0))

    canvas.save(f'assets/{serial}_Label.png')

    new_canvas = Image.new('RGB', (60, 40), color=(255, 255, 255))
    new_image = Image.open(f'assets/{serial}_Label.png')

    new_canvas = new_image.rotate(90, expand=True)
    new_canvas.save(f'assets/{serial}_Label.png')

    printable_canvas = Image.open(f'assets/{serial}_Label.png')


    l = zpl.Label(40,60)
    height = 40
    image_width = 60
    l.origin(0,0)
    image_height = l.write_graphic(
        Image.open(f'assets/{serial}_Label.png'),
        image_width)
    l.endorigin()


    # The name of the printer as it appears on your system
    printer_name = "ZDesigner ZD421-300dpi ZPL"  # Replace with your actual printer name

    # Create a Zebra object with the printer name
    z = Zebra(printer_name)

    # Send the ZPL to the printer
    z.output(l.dumpZPL())

    # print(l.dumpZPL())
    # l.preview()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--placeholder', help='Path to Placeholder Image', required=False)
    parser.add_argument('--modeln', help='model_number', required=False)
    parser.add_argument('--fota', help='current_fota_version number', required=True)
    parser.add_argument('--dfota', help='current_dfota_version number', required=True)
    parser.add_argument('--imei', help='IMEI number', required=False)
    parser.add_argument('--mac', help='MAC address', required=False)
    parser.add_argument('--batch', help='Batch number', required=True)
    parser.add_argument('--serial', help='Serial number', required=True)
    parser.add_argument('--token', help='token number', required=True)

    args = parser.parse_args()

    print_ID(args.placeholder, args.modeln, args.fota, args.dfota, args.imei, args.mac, args.batch, args.serial,args.token)
    print_zebra_label(args.placeholder, args.modeln, args.fota, args.dfota, args.imei, args.mac, args.batch, args.serial,args.token)
    print_PCBID(args.placeholder, args.modeln, args.fota, args.dfota, args.imei, args.mac, args.batch, args.serial,args.token)
