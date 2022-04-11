#!/usr/bin/python
# coding=utf-8

import os
import fitz
import argparse
from PIL import Image
from itertools import product

rgb_sum_standard = 600

def get_pdf(file_path):
    """
    Get the PDF files to be processed.
    :return:
    """
    global rgb_sum_standard

    pdf_folder = os.path.abspath(os.path.join(file_path, "..")) + '/' + 'folder'
    if not os.path.exists(pdf_folder):
        os.mkdir(pdf_folder)

    page_num = 0
    pdf_file = fitz.open(file_path)
    for page in pdf_file:
        pixmap = page.get_pixmap()
        for pos in product(range(pixmap.width), range(pixmap.height)):
            rgb = pixmap.pixel(pos[0], pos[1])
            if (sum(rgb) >= rgb_sum_standard):
                pixmap.set_pixel(pos[0], pos[1], (255, 255, 255))
        pixmap.pil_save(pdf_folder + '/' + str(page_num) + '.png')
        page_num = page_num + 1

    img2pdf(pdf_folder)


def get_image(file_path):
    """
    Get the image file to be processed.
    :return:
    """
    global rgb_sum_standard

    img = Image.open(file_path)
    width, height = img.size

    for pos in product(range(width), range(height)):
        rgb_real = img.getpixel(pos)[:3]
        if sum(rgb_real) > rgb_sum_standard:
            img.putpixel(pos, (255, 255, 255))

    save_path = os.path.abspath(os.path.join(file_path, "..")) + '/' + 'new.' + file_path.split('.')[-1]
    img.save(save_path)
    print('\033[1;35mSave successfully!\033[0m')


def get_logo():
    """
    Generate the logo and print it on terminal.
    :return:
    """
    logo_file = open(r'logo.txt')
    logo_file = logo_file.read()
    print('\033[1;35m\t' + logo_file + '\033[0m')


def get_command():
    """
    Use the command to obtain the image file or PDF file in the terminal.
    :return:
    """
    parser = argparse.ArgumentParser(prog='python main.py')
    parser.add_argument('file_type', help='Please enter the file type to be handle, input Image or PDF.', type=str)
    parser.add_argument('file_path', help='Please enter the Image or PDF file.', type=str)
    args = parser.parse_args()
    return args.file_type, args.file_path


def img2pdf(pdf_folder):
    """
    Remove the watermark after the conversion of the picture to PDF.
    :param pdf_folder:
    :return:
    """
    pdf = fitz.open()
    img_files = sorted(os.listdir(pdf_folder), key=lambda x: int(str(x).split('.')[0]))
    for img in img_files:
        imgdoc = fitz.open(pdf_folder + '\\' + img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open("pdf", pdfbytes)
        pdf.insertPDF(imgpdf)
    pdf.save(pdf_folder + '\\' + 'new.pdf')
    pdf.close()
    print('\033[1;35mSave successfully!\033[0m')


def main():
    """
    Logic Functions.
    :return:
    """
    get_logo()
    file_type, file_path = get_command()
    if file_type == 'Image':
        get_image(file_path)
    else:
        get_pdf(file_path)


if __name__ == '__main__':
    main()