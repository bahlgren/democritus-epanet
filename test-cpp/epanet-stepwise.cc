#include <iostream>

#include "utility.h"
#include "epanet2_2.h"


const char *node_type_str[] =
    { [EN_JUNCTION] = "junction",
      [EN_RESERVOIR] = "reservoir",
      [EN_TANK] = "tank" };


void get_node_heads(EN_Project ph, int node_count)
{
    int err, node_type;
    double head, pressure, demand;

    for (int i = 1; i <= node_count; i++) {
        err = EN_getnodetype(ph, i, &node_type); CHECK_ERR(err);
        err = EN_getnodevalue(ph, i, EN_HEAD, &head); CHECK_ERR(err);
        err = EN_getnodevalue(ph, i, EN_PRESSURE, &pressure); CHECK_ERR(err);
        err = EN_getnodevalue(ph, i, EN_DEMAND, &demand); CHECK_ERR(err);

        std::cout << "Node: " << i << ", type: " << node_type_str[node_type]
                  << ", head: " << head
                  << ", pressure: " << pressure
                  << ", demand: " << demand << std::endl;
    }
}


int main(int argc, char *argv[])
{
    int err;
    char _empty[] = "";
    char *inp_file;
    char *rep_file = _empty;
    char *bin_file = _empty;

    program = argv[0];

    if ((argc < 2) || (argc > 4)) {
        usage();
        exit(1);
    }

    inp_file = argv[1];
    if (argc > 2) rep_file = argv[2];
    if (argc > 3) bin_file = argv[3];

    EN_Project ph;
    EN_createproject(&ph);

    err = EN_open(ph, inp_file, rep_file, bin_file);
    CHECK_ERR(err);

    err = EN_openH(ph);
    CHECK_ERR(err);

    long t, tstep;

    err = EN_gettimeparam(ph, EN_HYDSTEP, &tstep);
    CHECK_ERR(err);
    std::cout << "Hydraulic time step was: " << tstep;

    tstep = 10;
    err = EN_settimeparam(ph, EN_HYDSTEP, tstep);
    CHECK_ERR(err);
    std::cout << ", setting to: " << tstep << std::endl;

    err = EN_setstatusreport(ph, EN_NORMAL_REPORT);
    CHECK_ERR(err);

    err = EN_initH(ph, EN_NOSAVE);
    CHECK_ERR(err);

    int node_count, link_count;

    err = EN_getcount(ph, EN_NODECOUNT, &node_count);
    CHECK_ERR(err);
    err = EN_getcount(ph, EN_LINKCOUNT, &link_count);
    CHECK_ERR(err);

    std::cout << std::endl << "Node count: " << node_count
              << ", link count: " << link_count << std::endl;

    for (int i = 0; ; i++) {
        //std::cout << std::endl << "Iteration: " << i;

        err = EN_runH(ph, &t);
        CHECK_ERR(err);
        //std::cout << "time after runH: " << t;

        get_node_heads(ph, node_count);

        err = EN_nextH(ph, &tstep);
        CHECK_ERR(err);

        //std::cout << ", tstep after nextH: " << tstep << std::endl;

        if (tstep == 0) break;
    }

    err = EN_closeH(ph);
    CHECK_ERR(err);

    err = EN_deleteproject(ph);
    CHECK_ERR(err);
}
