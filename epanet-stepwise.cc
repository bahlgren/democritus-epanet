#include <iostream>

#include "utility.h"
#include "epanet2_2.h"


int main(int argc, char *argv[])
{
    int err;
    char *file;

    program = argv[0];

    if (argc != 2) {
        usage();
        exit(1);
    }

    file = argv[1];

    EN_Project ph;
    EN_createproject(&ph);

    err = EN_open(ph, file, "", "");
    if (err !=0) epanet_error_exit(err);

    err = EN_openH(ph);
    if (err !=0) epanet_error_exit(err);

    long t, tstep;

    err = EN_gettimeparam(ph, EN_HYDSTEP, &tstep);
    if (err !=0) epanet_error_exit(err);
    std::cout << "Hydraulic time step was: " << tstep;

    tstep = 10;
    err = EN_settimeparam(ph, EN_HYDSTEP, tstep);
    if (err !=0) epanet_error_exit(err);
    std::cout << ", setting to: " << tstep << std::endl;

    err = EN_setstatusreport(ph, EN_NORMAL_REPORT);
    if (err !=0) epanet_error_exit(err);

    err = EN_initH(ph, EN_NOSAVE);
    if (err !=0) epanet_error_exit(err);

    for (int i = 0; ; i++) {
        //std::cout << std::endl << "Iteration: " << i;

        err = EN_runH(ph, &t);
        if (err !=0) epanet_error_exit(err);
        //std::cout << "time after runH: " << t;

        err = EN_nextH(ph, &tstep);
        if (err !=0) epanet_error_exit(err);

        //std::cout << ", tstep after nextH: " << tstep << std::endl;

        if (tstep == 0.0) break;
    }

    err = EN_closeH(ph);
    if (err !=0) epanet_error_exit(err);

    err = EN_deleteproject(ph);
    if (err !=0) epanet_error_exit(err);
}
