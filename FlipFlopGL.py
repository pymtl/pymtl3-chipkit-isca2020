#=========================================================================
# FlopFlopGL
#=========================================================================

from pymtl3 import *

class FlipFlopGL( Component ):
  def construct( s ):
    s.d = InPort()
    s.q = OutPort()

    @update_ff
    def upblk():
      s.q <<= s.d

#-------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------

if __name__ == "__main__":

  dut = FlipFlopGL()
  dut.apply( DefaultPassGroup(textwave=True) )
  dut.sim_reset()

  dut.d   @= 0
  dut.sim_tick()

  dut.d   @= 1
  dut.sim_tick()

  dut.d   @= 0
  dut.sim_tick()
  dut.sim_tick()

  dut.print_textwave()

