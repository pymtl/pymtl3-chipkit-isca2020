#=========================================================================
# RegIncrRTL
#=========================================================================

from pymtl3 import *

class RegIncrRTL( Component ):
  def construct( s, nbits=4, incr_value=1 ):
    s.in_  = InPort (nbits)
    s.out  = OutPort(nbits)

    s.tmp  = Wire( nbits )

    @update_ff
    def upblk_ff():
      if s.reset:
        s.tmp <<= 0
      else:
        s.tmp <<= s.in_

    @update
    def upblk_comb():
      s.out @= s.tmp + incr_value

  def line_trace( s ):
    return f"{s.in_}(){s.out}"

#-------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------

if __name__ == "__main__":

  dut = RegIncrRTL(incr_value=2)
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

