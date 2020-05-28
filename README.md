
Code Examples for PyMTL3 Talk at CHIPKIT Tutorial 2020
==========================================================================

[![Run on Repl.it](https://repl.it/badge/github/pymtl/pymtl3-chipkit-isca2020)](https://repl.it/github/pymtl/pymtl3-chipkit-isca2020)
[![Build Status](https://travis-ci.com/pymtl/pymtl3-chipkit-isca2020.svg?branch=master)](https://travis-ci.com/pymtl/pymtl3-chipkit-isca2020)

This repo contains the simple code examples used in PyMTL3 talk for the
CHIPKIT tutorial at ISCA 2020. Note that these are simple gate-level
examples with one RTL example. Clearly PyMTL3 is far more powerful, but
we find starting with these simple examples greatly simplifies learning
PyMTL3. Here is a list of the examples in increasing order of complexity
along with the key concept the example is meant to illustrate:

| Code Example         | PyMTL3 Concept                           |
| -------------------- | ---------------------------------------- |
| `FullAdderGL`        | combinational logic modeling             |
| `FlipFlopGL`         | sequential logic modeling                |
| `RippleCarryAdderGL` | structural composition                   |
| `RegGL`              | structural composition                   |
| `RegIncrGL`          | constructor-based parameterization       |
| `NstageRegIncrGL`    | hierarchical parameterization, line/VCD tracing, verilog translation |
| `NstageRegIncrGL_v`  | verilog translation/import via verilator |
| `RegIncrRTL`         | RTL modeling                             |

You can experiment with these examples just by clicking on the _run on
repl.it_ badge above and then click the _run_ button. By default, Repl.it
is setup to just run the ad-hoc main program for `FullAdderGL.py`. You
can change it to run a different ad-hoc main program by editing the `run`
variable in the `.replit` file. So for example, you could change it to
this to run the ad-hoc main program for `FlipFlopGL.py`:

```
 run = "python FlipFlopGL.py"
```

You won't be able to run the ad-hoc main program for
`NstageRegIncrGL_v.py` since it requires Verilator to be installed. You
can also check out the results from using `pytest` to run all the tests
using the TravisCI badge above.

Of course you can also just clone the repo and run the examples in your
own virtual environment like this:

```
 % git clone git@github.com:pymtl/pymtl3-chipkit-isca2020
 % cd pymtl3-chipkit-isca2020
 % TOPDIR=$PWD
 % python3 -m venv pymtl3
 % source pymtl3/activate/bin
 % pip install pymtl3
```

Then you can try experimenting with the fixed-bitwidth `Bits` types like
this:

```
 % cd $TOPDIR
 % python
 >>> from pymtl3 import *
 >>> a = Bits8(6)
 >>> a
 >>> b = Bits8(3)
 >>> b
 >>> a | b
 >>> a << 4
 >>> c = (a << 4) | b
 >>> c
 >>> c[4:8]
 >>> exit()
```

Or you can try simulating a simple full adder component that is
distributed with PyMTL3 like this:

```
 % cd $TOPDIR
 % python
 >>> from pymtl3.examples.ex00_quickstart import FullAdder
 >>> import inspect
 >>> print(inspect.getsource(FullAdder))
 >>> fa = FullAdder()
 >>> fa.apply( DefaultPassGroup(textwave=True) )
 >>> fa.sim_reset()
 >>> fa.a   @= 0
 >>> fa.b   @= 1
 >>> fa.cin @= 0
 >>> fa.sim_tick()
 >>> fa.a   @= 0
 >>> fa.b   @= 1
 >>> fa.cin @= 0
 >>> fa.sim_tick()
 >>> fa.print_textwave()
```

Assuming all of that works, then you can run each of the ad-hoc main
programs like this:

```
 % cd $TOPDIR
 % python FullAdderGL.py
 % python FlipFlopGL.py
 % python RippleCarryAdderGL.py
 % python RegGL.py
 % python RegIncrGL.py
 % python NstageRegIncrGL.py
 % python RegIncrRTL.py
```

And you can run all of the `pytest` tests like this:

```
 % cd $TOPDIR
 % pytest
```

Note that to experiment with `NstageRegIncrGL_v.py` you need to have
a recent version of Verilator installed. Here is an example of how to do
this on a standard Ubuntu system:

```
 % sudo apt-get install git make autoconf g++ libfl-dev bison
 % mkdir -p ${HOME}/src
 % cd ${HOME}/src
 % wget http://www.veripool.org/ftp/verilator-4.026.tgz
 % tar -xzvf verilator-4.026.tgz
 % cd verilator-4.026
 % ./configure
 % make
 % sudo make install
```

Then you can run the ad-hoc main program for `NstageRegIncrGL_v.py` which
will translate the model into Verilog and then compile it using Verilator
for PyMTL3/Verilog co-simulation.

```
 % cd $TOPDIR
 % python NstageRegIncrGL_v.py
```

