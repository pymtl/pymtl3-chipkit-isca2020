#=========================================================================
# FullAdderGL
#=========================================================================

from pymtl3 import *

class FullAdderGL( Component ):
  def construct( s ):
    s.a    = InPort()
    s.b    = InPort()
    s.cin  = InPort()
    s.sum  = OutPort()
    s.cout = OutPort()

    # @update
    # def upblk():
    #   s.sum  @= s.cin ^ s.a ^ s.b
    #   s.cout @= ( ( s.a ^ s.b ) & s.cin ) | ( s.a & s.b )

    s.tmp = Wire()

    @update
    def upblkA():
      s.tmp  @= s.a ^ s.b

    @update
    def upblkB():
      s.sum  @= s.tmp ^ s.cin
      s.cout @= ( s.tmp & s.cin ) | ( s.a & s.b )

if __name__ == "__main__":
  dut = FullAdderGL()
  dut.apply( DedutultPassGroup(textwave=True) )
  dut.sim_reset()

  dut.a   @= 0
  dut.b   @= 1
  dut.cin @= 0
  dut.sim_tick()

  dut.a   @= 1
  dut.b   @= 1
  dut.cin @= 1
  dut.sim_tick()

  dut.print_textwave()
