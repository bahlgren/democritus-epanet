#!/usr/bin/env python3

from epanet import toolkit as en
import argparse
import csv
import contextlib


node_type_str = { en.JUNCTION: "junction",
                  en.RESERVOIR: "reservoir",
                  en.TANK: "tank" }

link_type_str = { en.CVPIPE: "cvpipe",
                  en.PIPE: "pipe",
                  en.PUMP: "pump",
                  en.PRV: "prv",
                  en.PSV: "psv",
                  en.PBV: "pbv",
                  en.FCV: "fcv",
                  en.TCV: "tcv",
                  en.GPV: "gpv" }


def create_value_filename_list(value_list):
    if value_list == None:
        return []
    else:
        value_filenames = []
        for v in value_list:
            en_constant = getattr(en, v.upper())
            if not isinstance(en_constant, int):
                raise AttributeError(f"'{v.upper()}' is not an EPANET constant")
            value_filenames.append( (en_constant, v.lower()+'.csv') )
        return value_filenames


class NodeValueCSVWriter:
    """Generic class for writing node values to a csv-formatted data file.

    An instance of this class is initialised with a file name to write
    the csv-formatted data to, an EPANET project handle, and a node
    value that can be passed to en.getnodevalue().  On each call to
    the object, the configured node values are retrieved for all
    nodes, and one data row is written to the files with the following
    structure:

    <time>;<node 1 value>;<node 2 value>;...

    """

    def __init__(self, csv_filename, project_handle, node_value):
        self._csv_filename = csv_filename
        self._ph = project_handle
        self._node_value = node_value
        node_count = en.getcount(self._ph, en.NODECOUNT)
        self._node_range = range(1, node_count+1)

    def __enter__(self):
        self._f = open(self._csv_filename, 'w', newline='')
        self._cw = csv.writer(self._f, delimiter=';')
        self._cw.writerow(['time'] +
                          [f'{node_type_str[en.getnodetype(self._ph, i)]}{i}'
                           for i in self._node_range])
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


class LinkValueCSVWriter:
    """Generic class for writing link values to a csv-formatted data file.

    An instance of this class is initialised with a file name to write
    the csv-formatted data to, an EPANET project handle, and a link
    value that can be passed to en.getlinkvalue().  On each call to
    the object, the configured link values are retrieved for all
    links, and one data row is written to the files with the following
    structure:

    <time>;<link 1 value>;<link 2 value>;...

    """

    def __init__(self, csv_filename, project_handle, link_value):
        self._csv_filename = csv_filename
        self._ph = project_handle
        self._link_value = link_value
        link_count = en.getcount(self._ph, en.LINKCOUNT)
        self._link_range = range(1, link_count+1)

    def __enter__(self):
        self._f = open(self._csv_filename, 'w', newline='')
        self._cw = csv.writer(self._f, delimiter=';')
        self._cw.writerow(['time'] +
                          [f'{link_type_str[en.getlinktype(self._ph, i)]}{i}'
                           for i in self._link_range])
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if (exc_type != None):
            print(exc_type, exc_value, traceback)
        self._f.close()
        return False

    def __call__(self, time):
        self._cw.writerow([time] +
                          [en.getlinkvalue(self._ph, i, self._link_value)
                           for i in self._link_range])


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
    parser.add_argument('-n', '--node-value-csv', action='append', metavar='VALUE',
                        help='Create csv file for specified node attribute VALUE.')
    parser.add_argument('-l', '--link-value-csv', action='append', metavar='VALUE',
                        help='Create csv file for specified link attribute VALUE.')

    args = parser.parse_args()

    nodevalue_filename_list = create_value_filename_list(args.node_value_csv)
    linkvalue_filename_list = create_value_filename_list(args.link_value_csv)

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

    with contextlib.ExitStack() as ctx_stack:
        nodevalue_wrts = [ ctx_stack.enter_context(NodeValueCSVWriter(fn, ph, nv))
                           for nv, fn in nodevalue_filename_list ]
        linkvalue_wrts = [ ctx_stack.enter_context(LinkValueCSVWriter(fn, ph, lv))
                           for lv, fn in linkvalue_filename_list ]

        ## Simulation loop
        while True:
            t = en.runH(ph)
            #print(f'time after runH: {t}')

            #get_node_heads(ph, t, node_count)
            for nv_wrt in nodevalue_wrts:
                nv_wrt(t)
            for lv_wrt in linkvalue_wrts:
                lv_wrt(t)

            hstep = en.nextH(ph)
            #print(f'hstep after nextH: {hstep}')

            if hstep == 0:
                break

    en.closeH(ph)
    #en.saveH(ph)
    #en.report(ph)
    en.deleteproject(ph)
