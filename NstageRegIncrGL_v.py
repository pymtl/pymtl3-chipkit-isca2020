#=========================================================================
# NstageRegIncrGL_v
#=========================================================================

from pymtl3 import *
from RegIncrGL import RegIncrGL

class NstageRegIncrGL( Component ):
  def construct( s, nbits=4, nstages=2 ):
    s.in_ = InPort (nbits)
    s.out = OutPort(nbits)

    s.rincrs = [ RegIncrGL(nbits) for _ in range(nstages) ]

    s.in_ //= s.rincrs[0].in_
    for rincr, rincr_next in zip(s.rincrs,s.rincrs[1:]):
      rincr.out //= rincr_next.in_
    s.out //= s.rincrs[-1].out

  def line_trace( s ):
    return " ".join([ rincr.line_trace() for rincr in s.rincrs ])

#-------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------

from pymtl3.passes.backends.verilog import *
from pymtl3.passes.tracing.VcdGenerationPass import VcdGenerationPass

if __name__ == "__main__":

  dut = NstageRegIncrGL(nstages=2)

  # Use hierarchical parameter system

  dut.set_param( "top.rincrs*.construct", incr_value=2 )

  # Turn on VCD waveform dumping

  dut.set_metadata( VcdGenerationPass.vcd_file_name, "dump" )

  # Turn on Verilog translation/import and apply corresponding passes

  dut.set_metadata( VerilogTranslationImportPass.enable, True )
  dut.apply( VerilogPlaceholderPass() )
  dut = VerilogTranslationImportPass()( dut )

  # Apply default pass group and simulate

  dut.apply( DefaultPassGroup(textwave=True) )
  dut.sim_reset()

  dut.in_ @= 0
  dut.sim_tick()

  dut.in_ @= 4
  dut.sim_tick()

  dut.in_ @= 6
  dut.sim_tick()
  dut.sim_tick()
  dut.sim_tick()
  dut.sim_tick()

  dut.print_textwave()

