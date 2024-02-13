/**
 * @file v-ti.cc
 * @author Tianchen Zhang
 * @brief Central potential (time-independent version)
 * @version 1.0
 * @date 2023-10-11
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
  fprintf(stderr, "Central potential (time-independent version)\n");
  fprintf(stderr,
          "USAGE: \n"
          "    %s [OPTIONS] ppotV ppotPS\n",
          name);
  fprintf(stderr,
          "OPTIONS: \n"
          "    -l <LENGTH>:       Array length\n"
          "    -mbar <MBAR>:      1/4(3M_V + M_PS) (LUnit)\n"
          "    -mdiff <MDIFF>:    (M_V - M_PS) (LUnit)\n"
          "    -mc <MC>:          charm quark mass (LUnit)\n"
          "    -ov0 <OFNAMEV0>:   ofname of v0\n"
          "    -ovs <OFNAMEVS>:   ofname of vs\n"
          "    [-h, --help]:      Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int array_length = 0;
DOUBLE mbar = 0;
DOUBLE mdiff = 0;
DOUBLE mc = 0;
static const char *of_name_v0 = NULL;
static const char *of_name_vs = NULL;
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

  while (argc > 0 && argv[0][0] == '-')  // read options (order irrelevant)
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

    // -mbar
    if (strcmp(argv[0], "-mbar") == 0) {
      mbar = atof(argv[1]);  // atof(): convert ASCII string to float
      if (mbar == 0) {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -mdiff
    if (strcmp(argv[0], "-mdiff") == 0) {
      mdiff = atof(argv[1]);  // atof(): convert ASCII string to float
      if (mdiff == 0) {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -mc: charm quark mass
    if (strcmp(argv[0], "-mc") == 0) {
      mc = atof(argv[1]);  // atof(): convert ASCII string to float
      if (mc == 0) {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -ov0: of_name_v0
    if (strcmp(argv[0], "-ov0") == 0) {
      of_name_v0 = argv[1];
      if (of_name_v0 == NULL) {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -ovs: of_name_vs
    if (strcmp(argv[0], "-ovs") == 0) {
      of_name_vs = argv[1];
      if (of_name_vs == NULL) {
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
  if (argc != 2) {
    usage(program_name);
    exit(1);
  }

  // Initialization
  fprintf(stderr, "##  Central potential (time-independent)! \n");
  fprintf(stderr, "##  Array length:        %d\n", array_length);

  CVARRAY ppotv(array_length), ppotps(array_length), v0(array_length),
      vs(array_length);
  ppotv = ppotps = v0 = vs = 0.0;

  readBin(argv[0], array_length, ppotv);
  readBin(argv[1], array_length, ppotps);

  v0 = 1 / (4.0 * mc) * (3 * ppotv + ppotps) + 1 / 4.0 * mbar - 2.0 * mc;
  vs = 1 / mc * (ppotv - ppotps) + mdiff;

  writeBin(of_name_v0, array_length, v0);
  writeBin(of_name_vs, array_length, vs);

  return 0;
}
