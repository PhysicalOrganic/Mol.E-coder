#!/usr/bin/env
"""
Takes a txt file, performs a huffman compression to output binary codes that
are stored in CharactersToHuffmanCodes.xlsx.This binary is the converted to 
its hexadecimal equivalent and printed out in the terminal as well as being
written to OutputCodes.xlsx as snippets that can be assigned to monomers
to storage in oligomers.
"""
from sys import argv
from heapq import heappush, heappop, heapify
import xlsxwriter


def encode(symb2freq):
    """Takes in dictionary of letter frequencies and returns a list of huffman codes."""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)

    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = "0" + pair[1]
        for pair in hi[1:]:
            pair[1] = "1" + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def main():
    # get name of csv to read in and write out
    script, txt_file_name = argv

    letter_frequency = {}
    txt_to_compress = open(txt_file_name, "r", encoding="utf-8-sig")

    # create workbook and sheet
    workbook = xlsxwriter.Workbook("HexData/CharactersToHuffmanCodes.xlsx")
    worksheet = workbook.add_worksheet()

    # get letter frequency
    cleaned_up_txt = ""
    for line in txt_to_compress:
        line = line.strip()
        for char in line:
            cleaned_up_txt += char
            if char not in letter_frequency.keys():
                letter_frequency[char] = 1
            else:
                letter_frequency[char] += 1

    # get huffman encoding for each letter and add to dict
    huff = encode(letter_frequency)
    huff_codes = {}

    print()
    print(cleaned_up_txt)
    print()

    # adding huffcodes to dictionary
    for p in huff:
        huff_codes[p[0]] = p[1]

    # creating the bitstring using the huff codes dictionary
    bitcode = ""
    for char in cleaned_up_txt:
        bitcode += huff_codes[char]

    # determining amount of padding the bitcode with zeros so the number of monomers works out
    hex_padded = 0

    # determining amount of padding hex bitcode
    hex_padded_bitcode = bitcode
    while len(hex_padded_bitcode) % 8 != 0:
        hex_padded_bitcode += "0"
        hex_padded += 1

    binary_hex = {}

    hex_padding = "0000000"

    # creating binary to hex dict
    for i in range(256):
        oct_num = str(hex(i))[2:]
        if len(oct_num) == 1:
            oct_num = "0" + oct_num
        binary_hex[hex_padding[len(str(bin(i))[2:]) - 1 :] + str(bin(i))[2:]] = oct_num

    hex_monomer_code = []

    compress = hex_padded_bitcode
    while len(compress) != 0:
        byte = compress[:8]
        hex_monomer_code.append(binary_hex[byte])
        compress = compress[8:]

    row = 0
    col = 0

    #### CHANGE DEPENDING ON HEX_PADDED OR OCT_PADDED ##########
    worksheet.write(row, col, "padding")
    worksheet.write(row, col + 1, hex_padded)
    row += 1

    # GET NUMBER OF INDIVIDUAL MONOMERS === hex_occur
    total_monomer_string = ""
    hex_chars = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
    ]
    hex_occur = {}

    for z in hex_monomer_code:
        total_monomer_string += z

    for p in hex_chars:
        occurance = total_monomer_string.count(p)
        hex_occur[p] = occurance

    total_chars_check = 0
    for p in hex_occur:
        total_chars_check += hex_occur[p]

    # BREAK INTO PIECES OF 9
    monomer_split_9 = []
    single_well = []

    separate_monomers_to_9 = total_monomer_string
    temp_string = ""
    while len(separate_monomers_to_9) != 0:
        if len(separate_monomers_to_9) >= 9:
            single_well = separate_monomers_to_9[:9]
            monomer_split_9.append(single_well)
            separate_monomers_to_9 = separate_monomers_to_9[9:]
            single_well = []

        else:
            single_well = separate_monomers_to_9
            monomer_split_9.append(single_well)
            separate_monomers_to_9 = ""

    # PRINT OUT INFO
    print("binary to hex =", hex_monomer_code)
    print()
    print("monomers: ", len(hex_monomer_code) * 2)
    print()
    print("combined monomer sequence:", total_monomer_string)
    print()
    print("length:", len(total_monomer_string))
    print()
    print("monomer_occurange:", hex_occur)
    print()
    print("split into 9's:", monomer_split_9)

    for letter in huff_codes:
        worksheet.write(row, col, letter)
        worksheet.write(row, col + 1, huff_codes[letter])
        row += 1

    workbook.close()

    # create workbook and sheet
    workbook1 = xlsxwriter.Workbook("HexData/OutputCodes.xlsx")
    worksheet1 = workbook1.add_worksheet()

    row = 0
    col = 0

    for letter in hex_monomer_code:
        worksheet1.write(row, col, letter)
        row += 1

    workbook1.close()


main()
