"""
# Lisence
This project is licensed under the MIT License, see the LICENSE.txt file for details
https://github.com/teddokano/bitbang_SPI_controller_MicroPython
"""
from	machine	import	Pin

class bbSPI:
	MSB	= 1
	LSB	= 0
	
	def __init__( self, *, polarity = 0, phase = 0, bits = 8, first_bit = MSB, sck = None, mosi = None, miso = None, cs = None ):
	
		#	pin definitions
		self.sclk, self.mosi, self.miso, self.cs	= sck, mosi, miso, cs
		
		self.mosi.init( Pin.IN )
		self.miso.init( Pin.IN )
		self.sclk.init( Pin.OUT )
		
		if self.cs:
			self.cs.init( Pin.OUT )
			self.cs.value( 1 )

		#	mode settings
		self.pol	= polarity
		self.pha	= phase
		
		self.sclk.value( self.pol )
		
		if first_bit == self.MSB:
			self.bit_order	= tuple( n for n in range( bits - 1, -1, -1 ) )
		else:
			self.bit_order	= tuple( n for n in range( bits ) )
		
	def write_readinto( self, send, receive ):
		if self.cs:
			self.cs.value( 0 )

		self.mosi.init( Pin.OUT )
	
		if self.pha:
			pol	= not self.pol
			self.sclk.value( pol )
		else:
			pol	= self.pol

		for n, outdata in enumerate( send ):
			r	= 0
			for i in self.bit_order:
				self.mosi.value( (outdata >> i) & 1 )
				self.sclk.value( not pol )
				r	|= self.miso.value() << i
				self.sclk.value( pol )
			
			receive[ n ]	= r

		#if not self.pha:
		self.sclk.value( self.pol )

		self.mosi.init( Pin.IN )
			
		if self.cs:
			self.cs.value( 1 )
			
def main():
	spi	= bbSPI( sck = Pin( 10 ), mosi = Pin( 11 ), miso = Pin( 12 ), cs = Pin( 13 ) )

	while True:
		data	= [ 0xAA, 0x55 ]
		spi.write_readinto( data, data )
		print( data )
		sleep_ms( 100 )
		
if __name__ == "__main__":
	from	utime	import	sleep_ms
	main()
