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

int array_length = 0;
static const char *of_name = NULL;
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

    // -o: of_name
    if (strcmp(argv[0], "-o") == 0) {
      of_name = argv[1];
      if (of_name == NULL) {
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
  if (argc != 10) {
    usage(program_name);
    exit(1);
  }

  // Initialization
  fprintf(stderr, "##  F_{KS} (time-dependent)! \n");
  fprintf(stderr, "##  Array length:        %d\n", array_length);

  CVARRAY ddt(array_length), fks(array_length);

  std::vector<CVARRAY> data;

  for (int i = 0; i < 10; i++) {
    CVARRAY tmp(array_length);
    tmp = 0.0;

    read_bin(argv[i], array_length, tmp);
    data.push_back(tmp);
  }

  ddt = (-log(data[3] / data[7]) + 8 * log(data[2] / data[6]) -
         8 * log(data[1] / data[5]) + log(data[0] / data[4])) /
        12.0;
  fks = (data[8] - data[9]) / ddt;

  write_bin(of_name, array_length, fks);

  return 0;
}
