#!/usr/bin/env 

'''
Script takes TWO arguments: the FIRST is the txttobeencoded in a text doc and
the second is the name of the output file!!!
'''
from sys import argv
from heapq import heappush, heappop, heapify
from collections import defaultdict
import xlsxwriter
import csv

def encode(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def main():
    # get name of csv to read in and write out
    script, txt_file_name, csv_name = argv

    letter_frequency = {}
    txt_to_compress = open(txt_file_name, "r", encoding="utf-8-sig")

    # create workbook and sheet
    workbook = xlsxwriter.Workbook("HuffmanEncodeCharacterBinary.xlsx")
    worksheet = workbook.add_worksheet()

    '''
    # create workbook and sheet for octal code
    workbook_binarytooct = xlsxwriter.Workbook("Encoded.xlsx")
    worksheet_oct = workbook_binarytooct.add_worksheet()
    '''

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

    print ()
    print (cleaned_up_txt)
    print ()

    # adding huffcodes to dictionary
    for p in huff:
        huff_codes[p[0]] = p[1]

    # creating the bitstring using the huff codes dictionary
    bitcode = ""
    for char in cleaned_up_txt:
        bitcode += huff_codes[char]


    # determining amount of padding the bitcode with zeros so the number of monomers works out
    oct_padded = 0
    hex_padded = 0

    oct_padded_bitcode = bitcode
    while len(oct_padded_bitcode) % 6 != 0:
        oct_padded_bitcode += "0"
        oct_padded += 1

    # determining amount of padding hex bitcode
    hex_padded_bitcode = bitcode
    while len(hex_padded_bitcode) % 8 != 0:
        hex_padded_bitcode += "0"
        hex_padded += 1

    # adding padding to bitcodes
    print ("octal padded bitcode =", oct_padded_bitcode)
    print ("padded =", oct_padded)
    print ()

    # adding padding to bitcodes
    print ("hex padded bitcode =", hex_padded_bitcode)
    print ("padded =", hex_padded)

    binary_oct = {}
    binary_hex = {}

    oct_padding = "00000"
    hex_padding = "0000000"

    # creating binary to octal dict
    for i in range (64):
        dec_num = str(oct(i))[2:]
        if (len(dec_num)==1):
            dec_num = "0"+dec_num
        binary_oct[oct_padding[len(str(bin(i))[2:]) - 1:] + str(bin(i))[2:]] = dec_num
        # print (i, str(oct(i))[2:], oct_padding[len(str(bin(i))[2:]) - 1:] + str(bin(i))[2:])

    # print (binary_oct)

    # creating binary to hex dict
    for i in range (256):
        oct_num = str(hex(i))[2:]
        if (len(oct_num)==1):
            oct_num = "0"+oct_num
        binary_hex[hex_padding[len(str(bin(i))[2:]) - 1:] + str(bin(i))[2:]]= oct_num
        
    print (binary_hex)

    octal_monomer_code = []
    hex_monomer_code = []

    compress = oct_padded_bitcode
    while len(compress) != 0:
        byte = compress[:6]
        octal_monomer_code.append(binary_oct[byte])
        compress = compress[6:]
            

    compress = hex_padded_bitcode
    while len(compress) != 0:
        byte = compress[:8]
        hex_monomer_code.append(binary_hex[byte])
        compress = compress[8:]

    row = 0
    col = 0

    #### CHANGE DEPENDING ON HEX_PADDED OR OCT_PADDED ##########
    worksheet.write(row, col, "padding")
    worksheet.write(row, col+1, hex_padded)
    row+=1
    
    # GET NUMBER OF INDIVIDUAL MONOMERS === hex_occur
    total_monomer_string = "" 
    hex_chars = ["0", "1","2","3","4","5","6","7","8","9", "a","b","c","d","e","f"]
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
    while (len(separate_monomers_to_9) != 0):
        if (len(separate_monomers_to_9)>=9):
            single_well = separate_monomers_to_9[:9]
            monomer_split_9.append(single_well)
            separate_monomers_to_9 = separate_monomers_to_9[9:]
            single_well = []
            
        else:
            single_well = separate_monomers_to_9
            monomer_split_9.append(single_well)
            separate_monomers_to_9 = ""
    
            
        
    #PRINT OUT INFO

    print ("binary to octal =", octal_monomer_code)
    print ("monomers: ", len(octal_monomer_code) *2)
    print ()
    print ()
    print ("binary to hex =", hex_monomer_code)
    print ("monomers: ", len(hex_monomer_code)*2)
    print ("combined monomer sequence:", total_monomer_string)
    print ("length:", len(total_monomer_string))
    print ("monomer_occurange:", hex_occur)
    print ("check:", total_chars_check)
    print ("Split into 9's:", monomer_split_9)

    for letter in huff_codes:
        worksheet.write(row, col, letter)
        worksheet.write(row, col+1, huff_codes[letter])
        row +=1

    workbook.close()
    '''
    for pair in octal_monomer_code:
        worksheet_oct.write(row, col, pair)
        row += 1

    workbook_binarytooct.close()
    '''
    
    # create workbook and sheet
    workbook1 = xlsxwriter.Workbook("OutputCodes.xlsx")
    worksheet1 = workbook1.add_worksheet()
    
    row = 0
    col = 0
    
    for letter in hex_monomer_code:
        worksheet1.write(row, col, letter)
        row +=1

    workbook1.close()
    
    '''
    
    with open(csv_name +"Octal", 'w', newline='') as csvfile:
        cody_codecodes = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for i in octal_monomer_code:
            cody_codecodes.writerow([i])
    
    '''
            
    with open(csv_name +"Hex", 'w', newline='') as csvfile:
        hexcody_codecodes = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for i in hex_monomer_code:
            hexcody_codecodes.writerow([i])


main ()