# epanet-stepwise.py

is a test program that can run an EPANET simulation with a specified
(short) time step, and produce csv data files for the desired node and
link attributes.  One row of data is produced at each time step.

## Requirements

The program needs the "owa-epanet" python wrapper for the EPANET
library.  As it contains the EPANET C library, it has to be compiled
for a particular platform (CPU and OS).  "owa-epanet" is part of the
[OpenWaterAnalytics](https://github.com/OpenWaterAnalytics)/[epanet-python](https://github.com/OpenWaterAnalytics/epanet-python)
repository.

## How to run

Example EPANET simulation configurations can, for example, be found in
the
[OpenWaterAnalytics](https://github.com/OpenWaterAnalytics)/[EPANET](https://github.com/OpenWaterAnalytics/EPANET)
repository under "example-networks".

Run a simualation producing csv data files for pressure, quality and
flow using the example "Net1.inp":

    $ python3 epanet-stepwise.py --hstep 10 -n pressure -n quality -l flow Net1.inp rep.txt
    Hydraulic time step was: 3600, setting to: 10
    Node count: 11, link count: 13
    $

Print the help text:

    $ python3 epanet-stepwise.py --help
    usage: epanet-stepwise.py [-h] [--hstep seconds] [-n VALUE] [-l VALUE]
			      input_filename [report_filename] [binary_filename]

    Run an EPANET simulation.

    positional arguments:
      input_filename        An EPANET input file describing the system.
      report_filename       Report log file from the simulation run.
      binary_filename       Hydraulic analysis results file (binary).

    optional arguments:
      -h, --help            show this help message and exit
      --hstep seconds       Hydraulic time step (default 3600s=1h).
      -n VALUE, --node-value-csv VALUE
			    Create csv file for specified node attribute VALUE.
      -l VALUE, --link-value-csv VALUE
			    Create csv file for specified link attribute VALUE.
## Node and link attributes

Please see the EPANET documentation for possible node and link
properties.  Just remove the "EN_" prefix.  The specified property
names ("VALUE" above) will be converted to upper case, that is,
"pressure" will become "EN_PRESSURE" in the call to the EPANET
toolkit, but when used to create the csv file name, it will be
converted to lower case.
