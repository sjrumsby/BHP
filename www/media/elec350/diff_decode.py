from sys import argv
from binascii import unhexlify, hexlify

class rds():
	gen_decimal = 1465;
	d_x = {0 : "0011111100", 1 : "0110011000", 2 : "0101101000", 3 : "0110110100"}

	def checksum(self, bits, check, block):
		print "%s - %s - %s" % (bits, check, block)
		bits_dec = int(bits, 2)
		check_dec = int(check, 2)
		block_dec = int(self.d_x[i], 2)
		checksum = block_dec + (bits_dec*1024/self.gen_decimal)%self.gen_decimal
		print "Decimal of checksum: %s" % checksum
		print "Binary string of checksum %s" % bin(checksum)

def checksum(bits, d_x):
	checksum = int(d_x,2) + (1024*int(bits,2) + 1024*int(bits,2)/1465)%1465
	print str(bin(checksum))[2:].zfill(10)

#Convert the hex callsign into a binary string
lfsr = ""
if len(argv[1]) == 4:
	callsign = argv[1]
	for i in range(0,4):
		lfsr += bin(int(callsign[i],16))[2:].zfill(4)
else:
	print "Invalid callsign"
	exit()

f = open('data.dmp', 'rb')
bin_data = ""
text_data = ""

print "Grabbing bits from data file..."

i = 0
while i<100000:
	data = f.read(1)
	if data == "":
		break
	else:
		bin_data += '{0:08b}'.format(ord(data))
		bin_data += f.read(1)
	i += 1
f.close()

print "Acquired %s bits of data" % len(bin_data)
print "Differential Encoding..."

for i in range(0,len(bin_data)-1):
	if bin_data[i] == bin_data[i+1]:
		text_data += "1"
	else:
		text_data += "0"

print "Acquired %s of encoded data." % len(text_data)

lfsr_check = lfsr + "0101001110"

r = rds()
start = text_data.index(lfsr)

for i in range(0,4):
	data_start = start + 26*i
	bits = text_data[data_start:data_start+16]
	check = text_data[data_start+16:data_start+26]
#	r.checksum(bits, check, i)

checksum("0000000000000001", "0101101000")
checksum("1111111111111111", "0101101000")



