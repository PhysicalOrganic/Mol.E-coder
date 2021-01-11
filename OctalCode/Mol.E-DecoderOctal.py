#!/usr/bin/env python3

import collections
from sys import argv
from heapq import heappush, heappop, heapify
from collections import defaultdict
import xlrd
import csv

def OctalToDecimal(n):
    num = n
    dec_value = 0

    # Initializing base value
    # to 1, i.e 8^0
    base = 1

    temp = num
    while (temp):
        # Extracting last digit
        last_digit = temp % 10
        temp = int(temp / 10)

        # Multiplying last digit
        # with appropriate base
        # value and adding it
        # to dec_value
        dec_value += last_digit * base
        base = base * 8

    return dec_value


def main():

    print ()

    # get name of csv to read in and write out
    script, xlsx_file_name, octal_code = argv
    huff_codes = xlrd.open_workbook(xlsx_file_name)
    sheet = huff_codes.sheet_by_index(0)

    encoded_bitstring = ""
    oct_padding = "00000"

    with open(octal_code, 'rt') as csvfile:
        monomers = csv.reader(csvfile)
        for x in monomers:
            num = OctalToDecimal(int(x[0]))
            encoded_bitstring += oct_padding[len(str(bin(num))[2:]) - 1:] + str(bin(num))[2:]

    print (encoded_bitstring)

    wb = xlrd.open_workbook(xlsx_file_name)
    sheet = wb.sheet_by_index(0)

    sheet.cell_value(0,0)

    padding = int(sheet.cell_value(0,1))
    print ("padding: ", padding)

    for x in range(padding):
        encoded_bitstring += "0"

    print (encoded_bitstring)
    print ()
    print ()

    huff_dict = {}

    for i in range(1, sheet.nrows):
        huff_dict[str(sheet.cell_value(i, 1))] = sheet.cell_value(i, 0)

    print (huff_dict)

    decoded_string = ""
    bit_breakup = encoded_bitstring[:len(encoded_bitstring)-padding]
    count = 1
    print (bit_breakup)

    
    for x in range (len(bit_breakup)+1):
    # while len(bit_breakup) != 0:
        if (bit_breakup[:count] in huff_dict):
            decoded_string += huff_dict[bit_breakup[:count]]
            bit_breakup = bit_breakup[count:]
            count = 1
        count += 1
       

    print ()
    print (decoded_string)


main()