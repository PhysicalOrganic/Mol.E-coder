#!/usr/bin/env python3

from sys import argv
import xlrd
global hex_codes
global huff_dict


def HexToDecimal(hex_string):
    # using int () to convert to hexadecimal string
    n = int(hex_string, 16)
    bStr = ""
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    res = bStr

    return res


def MassToHex(value1, value2):
    mass_match = float(value1) - float(value2)
    for i in hex_codes.values():
        if (i[0] + 1.5 >= mass_match and i[0] - 1.5 <= mass_match) or (
            i[1] + 1.5 >= mass_match and i[1] - 1.5 <= mass_match
        ):
            print(value1, value2, mass_match)
            return list(hex_codes.keys())[list(hex_codes.values()).index(i)]
    print(mass_match, "NOT MATCHED")


def MakeBitstring(sheet):
    encoded_bitstring = ""
    hex_padding = "000"
    for i in range(sheet.nrows):
        for j in range(sheet.ncols):
            if len(sheet.cell_value(i, j)) > 3:
                cells = sheet.cell_value(i, j).strip(" ")
                cells = sheet.cell_value(i, j).split(",")
                for k in range(0, len(cells)):
                    value1 = cells[k]
                    if k == len(cells) - 1:
                        value2 = 0
                    else:
                        value2 = cells[k + 1]
                    hex_value = str(MassToHex(value1, value2))[0]
                    if hex_value == "e" and k == 0:
                        continue
                    else:
                        if hex_value == "0":
                            num = "0000"
                        else:
                            num = HexToDecimal(str(hex_value))
                        print(hex_value, hex_padding[len(str(num)) - 1 :] + str(num))
                        encoded_bitstring += hex_padding[len(str(num)) - 1 :] + str(num)

    return encoded_bitstring


def HuffmanDecodeBinaryString(bitstring, huff_dict):
    # break up bitstring into into huffman codes
    decoded_string = ""
    bit_breakup = bitstring
    count = 1
    for x in range(len(bit_breakup) + 1):
        if bit_breakup[:count] in huff_dict:
            decoded_string += huff_dict[bit_breakup[:count]]
            bit_breakup = bit_breakup[count:]
            count = 1
        count += 1

    return decoded_string


if __name__ == "__main__":

    # get name of csv to read in and write out
    script, huff_codes, hex_code, LCMS_template = argv

    ### MONOMER TO HEX CODES ####
    # open workbook with hex_codes
    codes_workbook = xlrd.open_workbook(hex_code)
    sheet1 = codes_workbook.sheet_by_index(0)
    sheet1.cell_value(0, 0)
    hex_codes = {}

    for j in range(1, sheet1.nrows):
        hex_codes[(sheet1.cell_value(j, 0))] = (
            sheet1.cell_value(j, 1),
            sheet1.cell_value(j, 2),
        )

    #### END MONOMER TO HEX CODE READIN ####

    #### HUFFMAN CODES ####
    # open document that contains the letters and their corresponding huffman codings
    wb = xlrd.open_workbook(huff_codes)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    padding = int(sheet.cell_value(0, 1))

    # create dictionary of the huffman codes
    huff_dict = {}
    for i in range(1, sheet.nrows):
        huff_dict[str(sheet.cell_value(i, 1))] = sheet.cell_value(i, 0)

    print(huff_dict, hex_codes)

    #### END HUFFMAN CODE READ IN ####

    #### READ IN EXCEL LCMS DATA FROM TEMPLATE ####
    template_workbook = xlrd.open_workbook(LCMS_template)
    LCMSsheet = template_workbook.sheet_by_index(0)

    # convert hex codes to binary representation
    encoded_bitstring = MakeBitstring(LCMSsheet)
    #### END LCMS DATA READIN ####

    # remove 0 at the end of the bitstring according to how much padding their is
    bit_breakup = encoded_bitstring[: len(encoded_bitstring) - padding]
    print("bit_breakup", bit_breakup)
    print()
    print()

    decoded_string = HuffmanDecodeBinaryString(bit_breakup, huff_dict)

    print()
    print(decoded_string)
