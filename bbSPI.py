from	machine	import	Pin
from	utime	import	sleep_ms

class bbSPI:
	MSB	= 1
	LSB	= 0
	
	def __init__( self, *, sck = 3, mosi = 4, miso = 5, cs = None, polarity = 0, phase = 0, bits = 8, first_bit = MSB ):
	
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
		self.pol	= polarity
		self.pha	= phase
		
		self.sck.value( self.pol )
		
		if first_bit == MSB:
			self.bit_order	= tuple( n for n in range( bits - 1, -1, -1 ) )
		else:
			self.bit_order	= tuple( n for n in range( bits ) )
		
	def send_receive_chunks( self, send, receive ):
		if self.cs:
			self.cs.value( 0 )

		self.mosi	= Pin( mosi, Pin.OUT )
	
		if self.pha:
			pol	= not self.pol
			self.sck.value( pol )
	
		for i, (ourdata, indata) in enumerate( zip( send, receive ) ):
			r	= 0
			for i in self.bit_order:
				self.sck.value( not pol )
				self._mosi.value( (outchunk >> i) & 1 )
				self.sck.value( pol )
				r	|= self._miso.value() << i
			
			receive[ i ]	= r

		if not self.pha:
			self.sck.value( pol )

		if self.cs:
			self.cs.value( 1 )
			
		self.mosi	= Pin( mosi, Pin.IN )
			
def main():
	spi	= bbSPI( sck = 10, mosi = 11, miso = 12, cs = 13 )

	while True:
		spi.write( [ 0x00, 0xFF ] + [ n for n in range( 8 ) ], [ 0xFF for _ in range( 10 ) ] )
		sleep_ms( 100 )
		
if __name__ == "__main__":
	main()
