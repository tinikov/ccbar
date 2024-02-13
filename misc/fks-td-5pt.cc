/**
 * @file fks-td.cc
 * @author Tianchen Zhang 
 * @brief F_{KS} (time-dependent version) (5-point stencil)
 * @version 1.0
 * @date 2023-05-03
 *
 */
#include <vector>

#include "dataio.h"
#include "misc.h"
#include "alias.h"
// __________________________________
//     .________|______|________.
//     |                        |
//     |     Usage function     |
//     |________________________|

void usage(char *name) {
  fprintf(stderr, "F_{KS} (time-dependent pro version)\n");
  fprintf(stderr,
          "USAGE: \n"
          "    %s [OPTIONS] CV(t-2) CV(t-1) CV(t+1) CV(t+2) CPS(t-2) CPS(t-1) "
          "CPS(t+1) CPS(t+2) ppotV ppotPS\n",
          name);
  fprintf(stderr,
          "OPTIONS: \n"
          "    -l <LENGTH>:       Array length\n"
          "    -o <OFNAME>:        ofname of F_KS\n"
          "    [-h, --help]:      Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int arrayLength = 0;
static const char *ofname = NULL;
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

    // -o: ofname
    if (strcmp(argv[0], "-o") == 0) {
      ofname = argv[1];
      if (ofname == NULL) {
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
  if (argc != 10) {
    usage(programName);
    exit(1);
  }

  // Initialization
  fprintf(stderr, "##  F_{KS} (time-dependent)! \n");
  fprintf(stderr, "##  Array length:        %d\n", arrayLength);

  CVARRAY ddt(arrayLength), fks(arrayLength);

  std::vector<CVARRAY> data;

  for (int i = 0; i < 10; i++) {
    CVARRAY tmp(arrayLength);
    tmp = 0.0;

    read_bin(argv[i], arrayLength, tmp);
    data.push_back(tmp);
  }

  ddt = (-log(data[3] / data[7]) + 8 * log(data[2] / data[6]) -
         8 * log(data[1] / data[5]) + log(data[0] / data[4])) /
        12.0;
  fks = (data[8] - data[9]) / ddt;

  write_bin(ofname, arrayLength, fks);

  return 0;
}
