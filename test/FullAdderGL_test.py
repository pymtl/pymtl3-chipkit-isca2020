#=========================================================================
# FullAdderGL_test
#=========================================================================

from pymtl3 import *
from FullAdderGL import FullAdderGL

def test_exhaustive():

  dut = FullAdderGL()
  dut.apply( DefaultPassGroup(textwave=True) )
  dut.sim_reset()

  tvecs = [
    # a   b   cin sum cout
    [ 0,  0,  0,  0,  0  ],
    [ 0,  0,  1,  1,  0  ],
    [ 0,  1,  0,  1,  0  ],
    [ 0,  1,  1,  0,  1  ],
    [ 1,  0,  0,  1,  0  ],
    [ 1,  0,  1,  0,  1  ],
    [ 1,  1,  0,  0,  1  ],
    [ 1,  1,  1,  1,  1  ],
  ]

  for tvec in tvecs:
    dut.a   @= tvec[0]
    dut.b   @= tvec[1]
    dut.cin @= tvec[2]
    dut.sim_eval_combinational()
    assert dut.sum  == tvec[3]
    assert dut.cout == tvec[4]
    dut.sim_tick()

  dut.print_textwave()

