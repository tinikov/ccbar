/**
 * @file fks-ti.cc
 * @author TC (reeft137@gmail.com)
 * @brief F_{KS} (time-independent version)
 * @version 1.0
 * @date 2023-10-11
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
  fprintf(stderr, "F_{KS} (time-independent version)\n");
  fprintf(stderr,
          "USAGE: \n"
          "    %s [OPTIONS] ppotV ppotPS\n",
          name);
  fprintf(stderr,
          "OPTIONS: \n"
          "    -l <LENGTH>:       Array length\n"
          "    -m <MDIFF>:        (M_V - M_PS) (LUnit)\n"
          "    -o <OFNAME>:       ofname of F_KS\n"
          "    [-h, --help]:      Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int array_length = 0;
DOUBLE mdiff = 0;
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

    // -m: mdiff
    if (strcmp(argv[0], "-m") == 0) {
      mdiff = atof(argv[1]);  // atof(): convert ASCII string to float
      if (mdiff == 0) {
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
  if (argc != 2) {
    usage(program_name);
    exit(1);
  }

  // Initialization
  fprintf(stderr, "##  F_{KS} (time-independent)! \n");
  fprintf(stderr, "##  Array length:        %d\n", array_length);

  CVARRAY ppotv(array_length), ppotps(array_length), fks(array_length);
  ppotv = ppotps = fks = 0.0;

  read_bin(argv[0], array_length, ppotv);
  read_bin(argv[1], array_length, ppotps);

  fks = - (ppotv - ppotps) / mdiff;

  write_bin(of_name, array_length, fks);

  return 0;
}
