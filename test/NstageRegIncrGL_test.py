#=========================================================================
# NstageRegIncrGL_test
#=========================================================================

from pymtl3 import *
from NstageRegIncrGL import NstageRegIncrGL

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

def test_basic():

  dut = NstageRegIncrGL()
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

  dut = NstageRegIncrGL()
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
# test_values
#-------------------------------------------------------------------------

def test_2stage():

  dut = NstageRegIncrGL(nstages=2)
  dut.apply( DefaultPassGroup(textwave=True) )
  dut.sim_reset()

  tvecs = [
    # in_  out
    [ 0x8, 0x2 ],
    [ 0xf, 0x2 ],
    [ 0x1, 0xa ],
    [ 0xa, 0x1 ],
    [ 0x0, 0x3 ],
    [ 0x0, 0xc ],
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
@hypothesis.given( nbits=st.integers(4,64),
                   nstages=st.integers(1,8), data=st.data() )
def test_hypothesis( nbits, nstages, data ):

  values  = data.draw( st.lists( pst.bits(nbits), min_size=1, max_size=8 ) )
  inputs  = values + [0]*nstages
  outputs = ['?']*nstages + [ v+nstages for v in values ]

  print(f"\nTrying {values}")

  dut = NstageRegIncrGL( nbits=nbits, nstages=nstages )
  dut.apply( DefaultPassGroup() )
  dut.sim_reset()

  for input,output in zip(inputs,outputs):
    dut.in_ @= input
    dut.sim_eval_combinational()
    if output != '?':
      assert dut.out == output
    dut.sim_tick()

