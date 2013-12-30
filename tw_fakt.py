#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import argparse
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

def convert_pdf_to_string(path):

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    fp = file(path, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()

    str = retstr.getvalue()
    retstr.close()
    return str


#def read_pdf(pdf):
#    return os.popen("pdf2txt " + pdf).read()

def get_kons_number(pdfcontent):
    match = re.search("(?<=KONSULENTNR)\\s*([0-9]{4})", pdfcontent)
    if match:
        return match.group(1)
    return None

def get_total_sum(pdfcontent):
    match = re.search("(BETALE SENEST DEN)\\s*([0-9]{4}\\.[0-9]{2}\\.[0-9]{2})\\s*([0-9]{1,6},[0-9]{2}|-[0-9]{1,6},[0-9]{2})", pdfcontent)
    if match:
        return match.group(3)
    return None

def get_path(pdf):
    return os.path.abspath(pdf)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--descriptive", help="Makes output more descriptive", action="store_true")
    parser.add_argument("-k", "--konsulentnr", help="Outputs the consultant numbers", action="store_true")
    parser.add_argument("-s", "--totalsum", help="Outputs the total sum of the invoice", action="store_true")
    parser.add_argument("pdf", help="The pdf", type=str)
    args = parser.parse_args()

    if args.konsulentnr:
        if args.descriptive:
            print("Konsulentnummer: " + get_kons_number(convert_pdf_to_string(get_path(args.pdf))))
        else:
            print(get_kons_number(convert_pdf_to_string(get_path(args.pdf))))
    
    if args.totalsum:
        if args.descriptive:
            print("Total sum: " + get_total_sum(convert_pdf_to_string(get_path(args.pdf))))
        else:
            print(get_total_sum(convert_pdf_to_string(get_path(args.pdf))))

main()
