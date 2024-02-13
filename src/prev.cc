/**
 * @file prev.cc
 * @author Tianchen Zhang 
 * @brief Pre-potential: [▽^2 C(r,t)]/C(r,t)
 * @version 1.0
 * @date 2023-05-03
 *
 */

#include "correlator.h"
#include "dataio.h"
#include "misc.h"
#include "alias.h"
// __________________________________
//     .________|______|________.
//     |                        |
//     |     Usage function     |
//     |________________________|

void usage(char *name) {
  fprintf(stderr, "Pre-potential: [▽^2 C(r,t)]/C(r,t)\n");
  fprintf(stderr,
          "USAGE: \n"
          "    %s [OPTIONS] ifname1 [ifname2 ...]\n",
          name);
  fprintf(stderr,
          "OPTIONS: \n"
          "    -n <XYZSIZE>:     Spacial size of lattice\n"
          "    -d <OFDIR>:       Directory of output files\n"
          "    [-p] <PREFIX>:    Prefix for output files\n"
          "    [-h, --help]:     Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Custom functions    |
//     |________________________|

void pre_potential(char *rawDataList[], char *ppotlist[], int xyzSize, int fileCountTotal);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int xyzSize = 0;
static const char *ofDir = NULL;
static const char *ofPrefix = NULL;
bool isAddPrefix = false;
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

    // -n: xyzSize
    if (strcmp(argv[0], "-n") == 0) {
      xyzSize = atoi(argv[1]);  // atoi(): convert ASCII string to integer
      if (!xyzSize) {
        usage(programName);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -d: directory for output file
    if (strcmp(argv[0], "-d") == 0) {
      ofDir = argv[1];
      if (ofDir == NULL) {
        usage(programName);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -p: prefix for output file
    if (strcmp(argv[0], "-p") == 0) {
      ofPrefix = argv[1];
      isAddPrefix = true;
      argc -= 2;
      argv += 2;
      continue;
    }

    fprintf(stderr, "Error: Unknown option '%s'\n", argv[0]);
    usage(programName);
    exit(1);
  }

  // Initialization
  const int fileCountTotal = argc;  // # of data files
  if (fileCountTotal < 1) {
    usage(programName);
    exit(1);
  }
  fprintf(stderr, "##  Pre-potential! \n");
  fprintf(stderr, "##  Total of data files:  %d\n", fileCountTotal);
  fprintf(stderr, "##  Spacial size:         %d\n", xyzSize);

  // Create an array to store ofnames
  char *prev_dlist[fileCountTotal];

  if (isAddPrefix) {
    for (int i = 0; i < fileCountTotal; i++) {
      char stmp[2048];
      prev_dlist[i] = (char *)malloc(2048 * sizeof(char));
      addPrefix(argv[i], ofPrefix, stmp);
      changePath(stmp, ofDir, prev_dlist[i]);
    }
  } else {
    for (int i = 0; i < fileCountTotal; i++) {
      prev_dlist[i] = (char *)malloc(2048 * sizeof(char));
      changePath(argv[i], ofDir, prev_dlist[i]);
    }
  }

  // Main part for calculation
  pre_potential(argv, prev_dlist, xyzSize, fileCountTotal);

  // Finalization for the string arrays
  for (int i = 0; i < fileCountTotal; i++) {
    free(prev_dlist[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

void pre_potential(char *rawDataList[], char *ppotlist[], int xyzSize, int fileCountTotal) {
  int array_length = int(pow(xyzSize, 3));

  for (int i = 0; i < fileCountTotal; i++) {
    COMPLX tmp[array_length], result[array_length];
    for (int j = 0; j < array_length; j++)  // Initialize the empty arrays
    {
      tmp[j] = result[j] = 0.0;
    }

    readBin(rawDataList[i], array_length, tmp);

    for (int ix = 0; ix < xyzSize; ix++)
      for (int iy = 0; iy < xyzSize; iy++)
        for (int iz = 0; iz < xyzSize; iz++) {
          CORR(result, ix, iy, iz, xyzSize) =
              (CORR(tmp, ix + 1, iy, iz, xyzSize) +
               CORR(tmp, ix - 1, iy, iz, xyzSize) +
               CORR(tmp, ix, iy + 1, iz, xyzSize) +
               CORR(tmp, ix, iy - 1, iz, xyzSize) +
               CORR(tmp, ix, iy, iz + 1, xyzSize) +
               CORR(tmp, ix, iy, iz - 1, xyzSize) -
               6.0 * CORR(tmp, ix, iy, iz, xyzSize)) /
              CORR(tmp, ix, iy, iz, xyzSize);
        }

    writeBin(ppotlist[i], array_length, result);
  }
}
