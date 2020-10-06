#!/usr/bin/env python

from epanet import toolkit as en
import argparse
import csv

node_type_str = { en.JUNCTION: "junction",
                  en.RESERVOIR: "reservoir",
                  en.TANK: "tank" }


class NodeValueCSVWriter:
    def __init__(self, csv_filename, project_handle, node_value):
        self._csv_filename = csv_filename
        self._ph = project_handle
        self._node_value = node_value
        node_count = en.getcount(self._ph, en.NODECOUNT)
        self._node_range = range(1, node_count+1)

    def __enter__(self):
        self._f = open(self._csv_filename, 'w', newline='')
        self._cw = csv.writer(self._f, delimiter=';')
        self._cw.writerow(['time'] + [i for i in self._node_range])
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if (exc_type != None):
            print(exc_type, exc_value, traceback)
        self._f.close()
        return False

    def __call__(self, time):
        self._cw.writerow([time] +
                          [en.getnodevalue(self._ph, i, self._node_value)
                           for i in self._node_range])


def print_node_heads(ph, time, node_count):
    print(f'Time: {time}')
    for i in range(1, node_count+1):
        node_type = en.getnodetype(ph, i)
        head = en.getnodevalue(ph, i, en.HEAD)
        pressure = en.getnodevalue(ph, i, en.PRESSURE)
        demand = en.getnodevalue(ph, i, en.DEMAND)
        print(f'Node: {i:2}, type: {node_type_str[node_type]},',
              f'head: {head:8g}, pressure: {pressure:8g}, demand: {demand:8g}')
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run an EPANET simulation.')
    parser.add_argument('input_filename',
                        help='An EPANET input file describing the system.')
    parser.add_argument('report_filename', nargs='?', default='',
                        help='Report log file from the simulation run.')
    parser.add_argument('binary_filename', nargs='?', default='',
                        help='Hydraulic analysis results file (binary).')
    parser.add_argument('--hstep', metavar='seconds', type=int, default=3600,
                        help='Hydraulic time step (default 3600s=1h).')

    args = parser.parse_args()

    ph = en.createproject()
    en.open(ph, args.input_filename, args.report_filename, args.binary_filename)

    en.openH(ph)

    ## Set time step
    hstep = en.gettimeparam(ph, en.HYDSTEP)
    print(f'Hydraulic time step was: {hstep}', end='')
    hstep = args.hstep
    en.settimeparam(ph, en.HYDSTEP, hstep)
    print(f', setting to: {hstep}')

    ## Other initialisation
    en.setstatusreport(ph, en.NORMAL_REPORT)
    en.initH(ph, en.SAVE)
    #en.setreport(ph, 'SUMMARY YES')
    #en.setreport(ph, 'NODES ALL')
    #en.setreport(ph, 'LINKS ALL')
    #en.settimeparam(ph, en.REPORTSTEP, 600)
    node_count = en.getcount(ph, en.NODECOUNT)
    link_count = en.getcount(ph, en.LINKCOUNT)

    print(f'Node count: {node_count}, link count: {link_count}')

    ## XXX - rewrite with contextlib.ExitStack
    with NodeValueCSVWriter('pressure.csv', ph, en.PRESSURE) as pressure_wrt, \
         NodeValueCSVWriter('head.csv', ph, en.HEAD) as head_wrt, \
         NodeValueCSVWriter('demand.csv', ph, en.DEMAND) as demand_wrt:

        ## Simulation loop
        while True:
            t = en.runH(ph)
            #print(f'time after runH: {t}')

            #get_node_heads(ph, t, node_count)
            pressure_wrt(t)
            head_wrt(t)
            demand_wrt(t)

            hstep = en.nextH(ph)
            #print(f'hstep after nextH: {hstep}')

            if hstep == 0:
                break

    en.closeH(ph)
    #en.saveH(ph)
    #en.report(ph)
    en.deleteproject(ph)
