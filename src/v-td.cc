/**
 * @file v-td.cc
 * @author Tianchen Zhang 
 * @brief Vcc and Vspin (time-dependent version)
 * @version 1.0
 * @date 2023-05-03
 *
 */

#include "dataio.h"
#include "misc.h"
#include "alias.h"
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

int arrayLength = 0;
DOUBLE mc = 0.0;
static const char *vcc_name = NULL;
static const char *vspin_name = NULL;
// __________________________________
//     .________|______|________.
//     |                        |
//     |      Main Function     |
//     |________________________|

int main(int argc, char *argv[]) {
  char programName[128];
  strncpy(programName, basename(argv[0]), 127);
  argc--;
  argv++;
  // ________________________________
  //    .________|______|________.
  //    |                        |
  //    |  Dealing with Options  |
  //    |________________________|

  while (argc > 0 &&
         argv[0][0] == '-')
  {
    // -h and --help: show usage
    if (strcmp(argv[0], "-h") == 0 || strcmp(argv[0], "--help") == 0) {
      usage(programName);
      exit(0);
    }

    // -l: arrayLength
    if (strcmp(argv[0], "-l") == 0) {
      arrayLength = atoi(argv[1]);  // atoi(): convert ASCII string to integer
      if (!arrayLength) {
        usage(programName);
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
        usage(programName);
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
        usage(programName);
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
        usage(programName);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    fprintf(stderr, "Error: Unknown option '%s'\n", argv[0]);
    usage(programName);
    exit(1);
  }

  // Make sure of all needed syntax
  if (argc != 6) {
    usage(programName);
    exit(1);
  }

  // Initialization
  fprintf(stderr, "##  F_{KS} (time-dependent)! \n");
  fprintf(stderr, "##  Array length:        %d\n", arrayLength);

  CVARRAY cv_m(arrayLength), cv_p(arrayLength), cps_m(arrayLength),
      cps_p(arrayLength), ppotv(arrayLength), ppotps(arrayLength),
      ddt(arrayLength), fks(arrayLength);
  cv_m = cv_p = cps_m = cps_p = ppotv = ppotps = ddt = fks = 0.0;

  readBin(argv[0], arrayLength, cv_m);
  readBin(argv[1], arrayLength, cv_p);
  readBin(argv[2], arrayLength, cps_m);
  readBin(argv[3], arrayLength, cps_p);
  readBin(argv[4], arrayLength, ppotv);
  readBin(argv[5], arrayLength, ppotps);

  ddt = (log(cv_p / cps_p) - log(cv_m / cps_m)) / 2.0;
  fks = (ppotv - ppotps) / ddt;

  writeBin(vspin_name, arrayLength, ddt);
  writeBin(vcc_name, arrayLength, fks);

  return 0;
}
