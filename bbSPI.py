from	machine	import	Pin

class bbSPI:
	MSB	= 1
	LSB	= 0
	
	def __init__( self, *, mode = None, polarity = 0, phase = 0, bits = 8, first_bit = MSB, sck = 3, mosi = 4, miso = 5, cs = None ):
	
		#	pin definitions
		self.sck	= Pin( sck, Pin.OUT )
		self.mosi	= Pin( mosi, Pin.IN )
		self.miso	= Pin( miso, Pin.IN )
		
		if cs:
			self.cs	= Pin( cs, Pin.OUT )
			self.cs.value( 1 )
		else:
			self.cs	= None

		#	mode settings
		if mode:
			self.pol	= (mode >> 1) & 0x1
			self.pha	=  mode & 0x1
		else:
			self.pol	= polarity
			self.pha	= phase
		
		self.sck.value( self.pol )
		
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
			self.sck.value( pol )
		else:
			pol	= self.pol

		for n, ourdata in enumerate( send ):
			r	= 0
			for i in self.bit_order:
				self.mosi.value( (ourdata >> i) & 1 )
				self.sck.value( not pol )
				r	|= self.miso.value() << i
				self.sck.value( pol )
			
			receive[ n ]	= r

		#if not self.pha:
		self.sck.value( self.pol )

		self.mosi.init( Pin.IN )
			
		if self.cs:
			self.cs.value( 1 )
			
def main():
	spi	= bbSPI( sck = 10, mosi = 11, miso = 12, cs = 13 )
	
	send_data		= [ 0x00, 0xFF ] + [ n for n in range( 8 ) ]
	receive_data	= [ 0xFF for _ in range( 10 ) ]
	
	while True:
		spi.write_readinto( send_data, receive_data )
		print( receive_data )
		sleep_ms( 100 )
		
if __name__ == "__main__":
	from	utime	import	sleep_ms
	main()
