# Mol.E-Coder
Mol.E-Coder works to convert text into both octal and hexadecimal in the same way. It is a two part program that encodes text input into monomer code and then takes LC/MS data and converts masses back to the original text that was encoded.

Both octal and hexadecimal work in the same way and are separated into an encode and decode portion

### Mol.E-Coder Usage
The first part of Mol.E-Coder is Mol.E-Coder{Hex/Octal}.py. This program takes a Text Document as an input. The text input is then converted to binary code using a Huffman
Algorithm. This algorithm works by created a binary tree of the characters in the text being encoded and assigns the letters to nodes based on the frequency of their occurance
in the text. 

To run this program the program takes a single input: a text document containing the text to be encoded.

The following is an example input and output for the hexadecimal version:

```bash
run Mol.E-CoderHex.py TxtToBeEncoded.txt
```


```python

If one scheme of happiness fails, human nature turns to another; if the first calculation is wrong, we make a second better: we find comfort somewhere.

binary to hex = ['1f', 'bf', '74', 'bb', 'c7', '4a', '4b', 'de', 'fe', '9a', '69', '82', '93', 'bf', 'db', '00', '9e', '7f', 'd1', '64', 'd5', 'e9', 'b0', 'a6', 'be', '14', 'e9', 'fe', '5f', '6a', 'bc', 'd2', '31', 'dc', '37', 'f3', '4b', 'ec', '0d', 'f3', 'c5', '85', '12', '89', 'b0', '2e', 'b8', '3f', '81', 'dd', '11', '9f', 'e0', 'bc', '9a', '72', 'ed', 'dd', '46', 'e8', '9e', '41', '66', '23', '1b', 'e0', 'be', 'c2', '89', 'f1', 'b9', '6e', 'cf', '3b', 'dc', '94', '34', '8d', '0c']

monomers:  158

combined monomer sequence: 1fbf74bbc74a4bdefe9a698293bfdb009e7fd164d5e9b0a6be14e9fe5f6abcd231dc37f34bec0df3c5851289b02eb83f81dd119fe0bc9a72eddd46e89e4166231be0bec289f1b96ecf3bdc94348d0c

length: 158

monomer_occurange: {'0': 8, '1': 11, '2': 7, '3': 9, '4': 10, '5': 4, '6': 8, '7': 5, '8': 8, '9': 13, 'a': 5, 'b': 17, 'c': 10, 'd': 14, 'e': 16, 'f': 13}

split into 9's: ['1fbf74bbc', '74a4bdefe', '9a698293b', 'fdb009e7f', 'd164d5e9b', '0a6be14e9', 'fe5f6abcd', '231dc37f3', '4bec0df3c', '5851289b0', '2eb83f81d', 'd119fe0bc', '9a72eddd4', '6e89e4166', '231be0bec', '289f1b96e', 'cf3bdc943', '48d0c']
```

### Mol.E-Decoder Usage
The second part of Mol.E-Coder is Mol.E-Decoder{Hex/Octal}.py. This program takes in two inputs, the codes output by the Huffman algorithm that are correlated to characters in 
the encoded text "CharactersToHuffmanCodes.xlsx" and the LC/MS masses entered into our template "DataTemplate.xlsx". 

The program first takes in the masses entered into the template and matches the difference between the parent mass and the subsequent mass to a monomer. 
These monomers that were previously assigned to a hexadecimal symbol by the researcher are then converted into their binary representation. This binary representation 
is then matched to the characters in the CharactersToHuffmanCodes.xlsx and the resulting decoded text is output.

The following is an example input and output for the hexadecimal version:

```bash
run Mol.E-DecoderHex.py CharactersToHuffmanCodes.xlsx ExampleDataTemplate.xlsx 
```

```python
If one scheme of happiness fails, human nature turns to another; if the first calculation is wrong, we make a second better: we find comfort somewhere.
```

