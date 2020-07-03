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

    err = EN_solveH(ph);
    if (err !=0) epanet_error_exit(err);

    err = EN_deleteproject(ph);
    if (err !=0) epanet_error_exit(err);
}
