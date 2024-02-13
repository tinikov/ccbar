/**
 * @file trev2.cc
 * @author Tianchen Zhang 
 * @brief Time reversal for 2-point correlators
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
  fprintf(stderr, "Time reversal for 2-point correlators\n");
  fprintf(stderr,
          "USAGE: \n"
          "    %s [OPTIONS] ifname1 [ifname2 ...]\n",
          name);
  fprintf(stderr,
          "OPTIONS: \n"
          "    -n <TSIZE>:       Temporal size of lattice\n"
          "    -d <OFDIR>:       Directory of output files\n"
          "    [-p] <PREFIX>:    Prefix for output files\n"
          "    [-t]:             Also save a txt file (add \"txt.\" prefix)\n"
          "    [-h, --help]:     Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Custom functions    |
//     |________________________|

void time_reverse_2pt(char *rawDataList[], char *trdlist[], int n_t, int fileCountTotal);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int n_t = 0;
static const char *ofDir = NULL;
static const char *ofPrefix = NULL;
bool isAddPrefix = false;
bool isSaveTxt = false;
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

    // -n: n_t
    if (strcmp(argv[0], "-n") == 0) {
      n_t = atoi(argv[1]);  // atoi(): convert ASCII string to integer
      if (!n_t) {
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

    // -t: save txt
    if (strcmp(argv[0], "-t") == 0) {
      isSaveTxt = true;
      argc--;
      argv++;
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
  fprintf(stderr, "##  Time reversal! \n");
  fprintf(stderr, "##  Total of data files:  %d\n", fileCountTotal);
  fprintf(stderr, "##  Temporal size:        %d\n", n_t);

  // Create an array to store ofnames
  char *tr_dlist[fileCountTotal];

  if (isAddPrefix) {
    for (int i = 0; i < fileCountTotal; i++) {
      char stmp[2048];
      tr_dlist[i] = (char *)malloc(2048 * sizeof(char));
      addPrefix(argv[i], ofPrefix, stmp);
      changePath(stmp, ofDir, tr_dlist[i]);
    }
  } else {
    for (int i = 0; i < fileCountTotal; i++) {
      tr_dlist[i] = (char *)malloc(2048 * sizeof(char));
      changePath(argv[i], ofDir, tr_dlist[i]);
    }
  }

  // Main part for calculation
  time_reverse_2pt(argv, tr_dlist, n_t, fileCountTotal);

  if (isSaveTxt) {
    for (int i = 0; i < fileCountTotal; i++) {
      char txttmp[2048];
      addPrefix(tr_dlist[i], "txt", txttmp);
      bin2txt(tr_dlist[i], txttmp, n_t);
    }
  }

  // Finalization for the string arrays
  for (int i = 0; i < fileCountTotal; i++) {
    free(tr_dlist[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

void time_reverse_2pt(char *rawDataList[], char *trdlist[], int n_t, int fileCountTotal) {
  for (int i = 0; i < fileCountTotal; i++) {
    COMPLX raw[n_t], data[n_t];
    for (int j = 0; j < n_t; j++) raw[j] = data[j] = 0.0;

    readBin(rawDataList[i], n_t, raw);

    for (int j = 0; j < n_t; j++)
      data[j] = (raw[j] + raw[(n_t - j) % n_t]) * 0.5;

    writeBin(trdlist[i], n_t, data);
  }
}
