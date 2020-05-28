#=========================================================================
# FlipFlopGL_test
#=========================================================================

from pymtl3 import *
from FlipFlopGL import FlipFlopGL

def test_exhaustive():

  dut = FlipFlopGL()
  dut.apply( DefaultPassGroup(textwave=True) )
  dut.sim_reset()

  tvecs = [
    # d  q
    [ 0, 0 ],
    [ 0, 0 ],
    [ 1, 0 ],
    [ 1, 1 ],
    [ 0, 1 ],
    [ 0, 0 ],
    [ 0, 0 ],
  ]

  for tvec in tvecs:
    dut.d @= tvec[0]
    dut.sim_eval_combinational()
    assert dut.q == tvec[1]
    dut.sim_tick()

  dut.print_textwave()

