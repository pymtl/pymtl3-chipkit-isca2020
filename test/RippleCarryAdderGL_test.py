#=========================================================================
# RippleCarryAdderGL_test
#=========================================================================

from pymtl3 import *
from RippleCarryAdderGL import RippleCarryAdderGL

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

def test_basic():

  dut = RippleCarryAdderGL()
  dut.apply( DefaultPassGroup(textwave=True) )
  dut.sim_reset()

  tvecs = [
    # in0  in1  sum
    [ 0x0, 0x0, 0x0 ],
    [ 0x1, 0x1, 0x2 ],
    [ 0x2, 0x3, 0x5 ],
    [ 0x3, 0x2, 0x5 ],
    [ 0x7, 0x7, 0xe ],
  ]

  for tvec in tvecs:
    dut.in0 @= tvec[0]
    dut.in1 @= tvec[1]
    dut.sim_eval_combinational()
    assert dut.out == tvec[2]
    dut.sim_tick()

  dut.print_textwave()

#-------------------------------------------------------------------------
# test_overflow
#-------------------------------------------------------------------------

def test_overflow():

  dut = RippleCarryAdderGL()
  dut.apply( DefaultPassGroup(textwave=True) )
  dut.sim_reset()

  tvecs = [
    # in0  in1  sum
    [ 0x8, 0x8, 0x0 ],
    [ 0xf, 0x1, 0x0 ],
    [ 0x1, 0xf, 0x0 ],
    [ 0x8, 0x9, 0x1 ],
    [ 0x9, 0x8, 0x1 ],
    [ 0xa, 0xa, 0x4 ],
  ]

  for tvec in tvecs:
    dut.in0 @= tvec[0]
    dut.in1 @= tvec[1]
    dut.sim_eval_combinational()
    assert dut.out == tvec[2]
    dut.sim_tick()

  dut.print_textwave()

#-------------------------------------------------------------------------
# test_hypothesis
#-------------------------------------------------------------------------

import hypothesis

from hypothesis       import strategies as st
from pymtl3.datatypes import strategies as pst

@hypothesis.settings( max_examples=25, deadline=None )
@hypothesis.given( nbits=st.integers(1,64), data=st.data() )
def test_hypothesis( nbits, data ):

  a = data.draw(pst.bits(nbits))
  b = data.draw(pst.bits(nbits))
  c = a + b

  print(f"Trying {a} + {b} = {c}")

  dut = RippleCarryAdderGL(nbits)
  dut.apply( DefaultPassGroup() )
  dut.sim_reset()

  dut.in0 @= a
  dut.in1 @= b
  dut.sim_eval_combinational()
  assert dut.out == c

