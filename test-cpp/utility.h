#ifndef _EPANET_TEST_UTILITY_
#define _EPANET_TEST_UTILITY_

#define CHECK_ERR(err) if (err !=0) epanet_error_exit(err)

extern char *program;
void usage();
void epanet_error_exit(int err);

#endif
