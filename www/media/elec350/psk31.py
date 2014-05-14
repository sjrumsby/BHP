#!/usr/bin/env python
from struct import pack

def myVaricodeEncodingFunction(message):
    encoding_tbl = {    
        '\x00' : '1010101011', '\x01' : '1011011011', '\x02' : '1011101101',
        '\x03' : '1101110111', '\x04' : '1011101011', '\x05' : '1101011111',
        '\x06' : '1011101111', '\x07' : '1011111101', '\x08' : '1011111111',
        '\x09' : '11101111'  , '\x0A' : '11101'     , '\x0B' : '1101101111',
        '\x0C' : '1011011101', '\x0D' : '11111'     , '\x0E' : '1101110101',
        '\x0F' : '1110101011', '\x10' : '1011110111', '\x11' : '1011110101',
        '\x12' : '1110101101', '\x13' : '1110101111', '\x14' : '1101011011',
        '\x15' : '1101101011', '\x16' : '1101101101', '\x17' : '1101010111',
        '\x18' : '1101111011', '\x19' : '1101111101', '\x1A' : '1110110111',
        '\x1B' : '1101010101', '\x1C' : '1101011101', '\x1D' : '1110111011',
        '\x1E' : '1011111011', '\x1F' : '1101111111', ' '    : '1'         ,
        '!'    : '111111111' , '"'    : '101011111' , '#'    : '111110101' ,
        '$'    : '111011011' , '%'    : '1011010101', '&'    : '1010111011',
        '\''   : '101111111' , '('    : '11111011'  , ')'    :   '11110111',
        '*'    : '101101111' , '+'    : '111011111' , ','    : '1110101'   ,
        '-'    : '110101'    , '.'    : '1010111'   , '/'    : '110101111' ,
        '0'    : '10110111'  , '1'    : '10111101'  , '2'    : '11101101'  ,
        '3'    : '11111111'  , '4'    : '101110111' , '5'    : '101011011' ,
        '6'    : '101101011' , '7'    : '110101101' , '8'    : '110101011' ,
        '9'    : '110110111' , ':'    : '11110101'  , ';'    : '110111101' ,
        '<'    : '111101101' , '='    : '1010101'   , '>'    : '111010111' ,
        '?'    : '1010101111', '@'    : '1010111101', 'A'    : '1111101'   ,
        'B'    : '11101011'  , 'C'    : '10101101'  , 'D'    : '10110101'  ,
        'E'    : '1110111'   , 'F'    : '11011011'  , 'G'    : '11111101'  ,
        'H'    : '101010101' , 'I'    : '1111111'   , 'J'    : '111111101' ,
        'K'    : '101111101' , 'L'    : '11010111'  , 'M'    : '10111011'  ,
        'N'    : '11011101'  , 'O'    : '10101011'  , 'P'    : '11010101'  ,
        'Q'    : '111011101' , 'R'    : '10101111'  , 'S'    : '1101111'   ,
        'T'    : '1101101'   , 'U'    : '101010111' , 'V'    : '110110101' ,
        'W'    : '101011101' , 'X'    : '101110101' , 'Y'    : '101111011' ,
        'Z'    : '1010101101', '['    : '111110111' , '\\'   : '111101111' ,
        ']'    : '111111011' , '^'    : '1010111111', '_'    : '101101101' ,
        '`'    : '1011011111', 'a'    : '1011'      , 'b'    : '1011111'   ,
        'c'    : '101111'    , 'd'    : '101101'    , 'e'    : '11'        ,
        'f'    : '111101'    , 'g'    : '1011011'   , 'h'    : '101011'    ,
        'i'    : '1101'      , 'j'    : '111101011' , 'k'    : '10111111'  ,
        'l'    : '11011'     , 'm'    : '111011'    , 'n'    : '1111'      ,
        'o'    : '111'       , 'p'    : '111111'    , 'q'    : '110111111' ,
        'r'    : '10101'     , 's'    : '10111'     , 't'    : '101'       ,
        'u'    : '110111'    , 'v'    : '1111011'   , 'w'    : '1101011'   ,
        'x'    : '11011111'  , 'y'    : '1011101'   , 'z'    : '111010101' ,
        '{'    : '1010110111', '|'    : '110111011' , '}'    : '1010110101',
        '~'    : '1011010111', '\x7F' : '1110110101'
	}
    
    print("Encoding user message: " + message[:-1])
    text = "0000000000000000"

    for i in message:
	 text += encoding_tbl[i] + "00"

    text += "111110000000000000000"

    print("Encoded user message as " + text)
    return text

def myDifferentialEncodingFunction(message):
    out = [0, -1.0]

    for i in range(2,len(message)+1):
        if message[i-1] == '1':
	    out.append(out[i-1])
	else:
	    out.append(-1*out[i-1])

    print("Encoded " + message + " as " + ' '.join([str(x) for x in out]))

    return out

if __name__ == "__main__":
    userMsg = raw_input('Message String: ')
    varicodeMsg = myVaricodeEncodingFunction(userMsg + '\n')
    encodedMsg = myDifferentialEncodingFunction(varicodeMsg)
    filename = 'output.dat'
    print('Writing ' + filename + '...')

    try:
        outfile = open(filename, 'w')
    except:
        print('Could not open ' + filename + '.')
        exit(-1)

    outputStr = ''.join([pack('f', x) for x in encodedMsg])
    outfile.write(outputStr)
    outfile.close()
    print('Done.')
