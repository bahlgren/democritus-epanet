#include <iostream>

#include "utility.h"
#include "epanet2_2.h"

char *program;

void usage()
{
    std::cerr << "Usage: " << program << " file.inp" << std::endl;
}

void epanet_error_exit(int err)
{
    char error_msg[300];

    int geterr_err = EN_geterror(err, error_msg, sizeof(error_msg));
    std::cerr << "Epanet error: " << error_msg << std::endl;

    if (geterr_err != 0)
        std::cerr << "geterror() error " << geterr_err << std::endl;

    exit(1);
}
