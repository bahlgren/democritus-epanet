#!/usr/bin/env python

from epanet import toolkit as en
import argparse

node_type_str = { en.JUNCTION: "junction",
                  en.RESERVOIR: "reservoir",
                  en.TANK: "tank" }

def get_node_heads(ph, node_count):
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

    ## Simulation loop
    while True:
        t = en.runH(ph)
        #print(f'time after runH: {t}')

        get_node_heads(ph, node_count)

        hstep = en.nextH(ph)
        #print(f'hstep after nextH: {hstep}')

        if hstep == 0:
            break

    en.closeH(ph)
    #en.saveH(ph)
    #en.report(ph)
    en.deleteproject(ph)
