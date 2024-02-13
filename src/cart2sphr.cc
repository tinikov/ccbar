/**
 * @file cart2sphr.cc
 * @author Tianchen Zhang
 * @brief From Cartesian coordinate to Spherical coordinate
 * @version 1.1
 * @date 2024-02-13
 *
 */

#include "correlator.h"
#include "dataio.h"
#include "misc.h"

void usage(char *name) {
  fprintf(stderr, "From Cartesian coordinate to Spherical coordinate\n");
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

// Custom function declaration
void cart2sphr(char *rawDataList[], char *sphrList[], int xyzSize,
               int fileCountTotal);

// Main function
int main(int argc, char *argv[]) {
  // Global Variables
  int xyzSize = 0;
  static const char *ofDir = NULL;
  static const char *ofPrefix = NULL;
  bool isAddPrefix = false;
  char programName[128];
  strncpy(programName, basename(argv[0]), 127);
  argc--;
  argv++;

  // read options (order irrelevant)
  while (argc > 0 && argv[0][0] == '-') {
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

  // Create an array to store ofnames
  char *ofnameArr[fileCountTotal];
  if (isAddPrefix) {
    for (int i = 0; i < fileCountTotal; i++) {
      char stmp[2048];
      ofnameArr[i] = (char *)malloc(2048 * sizeof(char));
      addPrefix(argv[i], ofPrefix, stmp);
      changePath(stmp, ofDir, ofnameArr[i]);
    }
  } else {
    for (int i = 0; i < fileCountTotal; i++) {
      ofnameArr[i] = (char *)malloc(2048 * sizeof(char));
      changePath(argv[i], ofDir, ofnameArr[i]);
    }
  }

  // Main part for calculation
  cart2sphr(argv, ofnameArr, xyzSize, fileCountTotal);

  // Finalization for the string arrays
  for (int i = 0; i < fileCountTotal; i++) {
    free(ofnameArr[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

void cart2sphr(char *rawDataList[], char *sphrList[], int xyzSize,
               int fileCountTotal) {
  int array_length = pow(xyzSize, 3);

  for (int i = 0; i < fileCountTotal; i++) {
    COMPLX tmp[array_length];
    for (int j = 0; j < array_length; j++)  // Initialize the empty arrays
    {
      tmp[j] = 0.0;
    }
    readBin(rawDataList[i], array_length, tmp);

    FILE *fp = fopen(sphrList[i], "w");
    if (fp == NULL) {
      perror(sphrList[i]);
      exit(1);
    }

    for (int i = 0; i < xyzSize / 2 + 1; i++)
      for (int j = i; j < xyzSize / 2 + 1; j++)
        for (int k = j; k < xyzSize / 2 + 1; k++) {
          DOUBLE re, im, distance = 0.0;

          distance =
              sqrt(pow(DOUBLE(i), 2) + pow(DOUBLE(j), 2) + pow(DOUBLE(k), 2));
          re = CORR(tmp, i, j, k, xyzSize).real();
          im = CORR(tmp, i, j, k, xyzSize).imag();

          fprintf(fp, "%1.16e %1.16e %1.16e\n", distance, re, im);
        }

    fclose(fp);
  }
}
