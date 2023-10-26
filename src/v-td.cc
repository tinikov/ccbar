/**
 * @file v-td.cc
 * @author TC (reeft137@gmail.com)
 * @brief Vcc and Vspin (time-dependent version)
 * @version 1.0
 * @date 2023-05-03
 *
 */

#include "data_process.h"
#include "misc.h"
#include "type_alias.h"
// __________________________________
//     .________|______|________.
//     |                        |
//     |     Usage function     |
//     |________________________|

void usage(char *name) {
  fprintf(stderr, "F_{KS} (time-dependent version)\n");
  fprintf(stderr,
          "USAGE: \n"
          "    %s [OPTIONS] CV(t-1) CV(t+1) CPS(t-1) CPS(t+1) ppotV ppotPS\n",
          name);
  fprintf(stderr,
          "OPTIONS: \n"
          "    -l <LENGTH>:       Array length\n"
          "    -mc <MASS>:        Kinetic mass of charm quark\n"
          "    -oc <OFDIR>:       ofname of Vcc\n"
          "    -os <OFDIR>:       ofname of Vspin\n"
          "    [-h, --help]:      Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int array_length = 0;
DOUBLE mc = 0.0;
static const char *vcc_name = NULL;
static const char *vspin_name = NULL;
// __________________________________
//     .________|______|________.
//     |                        |
//     |      Main Function     |
//     |________________________|

int main(int argc, char *argv[]) {
  char program_name[128];
  strncpy(program_name, basename(argv[0]), 127);
  argc--;
  argv++;
  // ________________________________
  //    .________|______|________.
  //    |                        |
  //    |  Dealing with Options  |
  //    |________________________|

  while (argc > 0 &&
         argv[0][0] == '-')  // deal with all options regardless of their order
  {
    // -h and --help: show usage
    if (strcmp(argv[0], "-h") == 0 || strcmp(argv[0], "--help") == 0) {
      usage(program_name);
      exit(0);
    }

    // -l: array_length
    if (strcmp(argv[0], "-l") == 0) {
      array_length = atoi(argv[1]);  // atoi(): convert ASCII string to integer
      if (!array_length) {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -mc: charm quark mass
    if (strcmp(argv[0], "-mc") == 0) {
      mc = atof(argv[1]);
      if (!mc) {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -oc: ofname of Vcc
    if (strcmp(argv[0], "-oc") == 0) {
      vcc_name = argv[1];
      if (vcc_name == NULL) {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -os: ofname of Vspin
    if (strcmp(argv[0], "-os") == 0) {
      vspin_name = argv[1];
      if (vspin_name == NULL) {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    fprintf(stderr, "Error: Unknown option '%s'\n", argv[0]);
    usage(program_name);
    exit(1);
  }

  // Make sure of all needed syntax
  if (argc != 6) {
    usage(program_name);
    exit(1);
  }

  // Initialization
  fprintf(stderr, "##  F_{KS} (time-dependent)! \n");
  fprintf(stderr, "##  Array length:        %d\n", array_length);

  CVARRAY cv_m(array_length), cv_p(array_length), cps_m(array_length),
      cps_p(array_length), ppotv(array_length), ppotps(array_length),
      ddt(array_length), fks(array_length);
  cv_m = cv_p = cps_m = cps_p = ppotv = ppotps = ddt = fks = 0.0;

  read_bin(argv[0], array_length, cv_m);
  read_bin(argv[1], array_length, cv_p);
  read_bin(argv[2], array_length, cps_m);
  read_bin(argv[3], array_length, cps_p);
  read_bin(argv[4], array_length, ppotv);
  read_bin(argv[5], array_length, ppotps);

  ddt = (log(cv_p / cps_p) - log(cv_m / cps_m)) / 2.0;
  fks = (ppotv - ppotps) / ddt;

  write_bin(vspin_name, array_length, ddt);
  write_bin(vcc_name, array_length, fks);

  return 0;
}
