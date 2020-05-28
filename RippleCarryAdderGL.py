#=========================================================================
# RippleCarryAdderGL
#=========================================================================

from pymtl3 import *
from FullAdderGL import FullAdderGL

class RippleCarryAdderGL( Component ):
  def construct( s, nbits=4 ):
    s.in0 = InPort (nbits)
    s.in1 = InPort (nbits)
    s.out = OutPort(nbits)

    s.fas = [ FullAdderGL() for _ in range(nbits) ]

    for i in range(nbits):
      s.in0[i] //= s.fas[i].a
      s.in1[i] //= s.fas[i].b
      s.out[i] //= s.fas[i].sum

    s.fas[0].cin //= 0
    for i in range(nbits-1):
      s.fas[i].cout //= s.fas[i+1].cin

#-------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------

if __name__ == "__main__":

  dut = RippleCarryAdderGL()
  dut.apply( DefaultPassGroup(textwave=True) )
  dut.sim_reset()

  dut.in0 @= 6
  dut.in1 @= 3
  dut.sim_tick()

  dut.in0 @= 4
  dut.in1 @= 4
  dut.sim_tick()

  dut.in0 @= 0xf
  dut.in1 @= 0x1
  dut.sim_tick()
  dut.sim_tick()

  dut.print_textwave()

