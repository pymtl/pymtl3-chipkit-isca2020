#=========================================================================
# RegGL
#=========================================================================

from pymtl3 import *
from FlipFlopGL import FlipFlopGL

class RegGL( Component ):
  def construct( s, nbits=4 ):
    s.in_ = InPort (nbits)
    s.out = OutPort(nbits)

    s.ffs = [ FlipFlopGL() for _ in range(nbits) ]

    for i in range(nbits):
      s.in_[i] //= s.ffs[i].d
      s.out[i] //= s.ffs[i].q

#-------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------

if __name__ == "__main__":

  dut = RegGL()
  dut.apply( DefaultPassGroup(textwave=True) )
  dut.sim_reset()

  dut.in_ @= 0
  dut.sim_tick()

  dut.in_ @= 4
  dut.sim_tick()

  dut.in_ @= 6
  dut.sim_tick()
  dut.sim_tick()

  dut.print_textwave()

