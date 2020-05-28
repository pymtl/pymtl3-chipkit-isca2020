#=========================================================================
# RegIncrGL
#=========================================================================

from pymtl3 import *
from RippleCarryAdderGL import RippleCarryAdderGL
from RegGL              import RegGL

class RegIncrGL( Component ):
  def construct( s, nbits=4, Adder=RippleCarryAdderGL, incr_value=1 ):
    s.in_  = InPort (nbits)
    s.out  = OutPort(nbits)

    s.reg  = RegGL(nbits)
    s.incr = Adder(nbits)

    s.reg.in_ //= s.in_
    s.incr.in0 //= s.reg.out
    s.incr.in1 //= incr_value
    s.out      //= s.incr.out

  def line_trace( s ):
    return f"{s.in_}(){s.out}"

#-------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------

if __name__ == "__main__":

  dut = RegIncrGL(incr_value=2)
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

