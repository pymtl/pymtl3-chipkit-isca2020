#=========================================================================
# RegIncrGL_test
#=========================================================================

from pymtl3 import *
from RegIncrGL import RegIncrGL

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

def test_basic():

  dut = RegIncrGL()
  dut.apply( DefaultPassGroup(textwave=True) )
  dut.sim_reset()

  tvecs = [
    # in_  out
    [ 0x0, 0x1 ],
    [ 0x0, 0x1 ],
    [ 0x1, 0x1 ],
    [ 0x1, 0x2 ],
    [ 0x0, 0x2 ],
    [ 0x0, 0x1 ],
    [ 0x0, 0x1 ],
  ]

  for tvec in tvecs:
    dut.in_ @= tvec[0]
    dut.sim_eval_combinational()
    assert dut.out == tvec[1]
    dut.sim_tick()

  dut.print_textwave()

#-------------------------------------------------------------------------
# test_values
#-------------------------------------------------------------------------

def test_values():

  dut = RegIncrGL()
  dut.apply( DefaultPassGroup(textwave=True) )
  dut.sim_reset()

  tvecs = [
    # in_  out
    [ 0x8, 0x1 ],
    [ 0xf, 0x9 ],
    [ 0x1, 0x0 ],
    [ 0xa, 0x2 ],
    [ 0x0, 0xb ],
    [ 0x0, 0x1 ],
  ]

  for tvec in tvecs:
    dut.in_ @= tvec[0]
    dut.sim_eval_combinational()
    assert dut.out == tvec[1]
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

  incr_value = data.draw( pst.bits(nbits) )

  values  = data.draw( st.lists( pst.bits(nbits), min_size=1, max_size=8 ) )
  inputs  = values + [0]
  outputs = [ 0+incr_value ] + [ v+incr_value for v in values ]

  print(f"\nTrying +{incr_value} {values}")

  dut = RegIncrGL( nbits=nbits, incr_value=incr_value )
  dut.apply( DefaultPassGroup() )
  dut.sim_reset()

  for input,output in zip(inputs,outputs):
    dut.in_ @= input
    dut.sim_eval_combinational()
    assert dut.out == output
    dut.sim_tick()

