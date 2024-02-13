/**
 * @file jre.cc
 * @author Tianchen Zhang 
 * @brief Jackknife resampling for raw data
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
  fprintf(stderr, "Jackknife resampling for raw data\n");
  fprintf(stderr,
          "USAGE: \n"
          "    %s [OPTIONS] ifname1 ifname2 [ifname3 ...]\n",
          name);
  fprintf(stderr,
          "OPTIONS: \n"
          "    -l <LENGTH>:      Length of data arrays\n"
          "    -d <OFDIR>:       Directory of output files\n"
          "    [-p] <PREFIX>:    Prefix for output files\n"
          "    [-v]:             Calculate variance for each sample\n"
          "    [-t]:             Also save a txt file (add \"txt.\" prefix)\n"
          "    [-h, --help]:     Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Custom functions    |
//     |________________________|

void jackknife_resample(char *rawDataList[], char *samdlist[], int arrayLength,
                        int fileCountTotal);
void jackknife_resample_var(char *rawDataList[], char *samdlist[],
                            int arrayLength, int fileCountTotal);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int arrayLength = 0;
static const char *ofdir = NULL;
static const char *ofPrefix = NULL;
bool isAddPrefix = false;
bool is_cal_var = false;
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

    // -d: directory for output file
    if (strcmp(argv[0], "-d") == 0) {
      ofdir = argv[1];
      if (ofdir == NULL) {
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

    // -v: calculate the variance
    if (strcmp(argv[0], "-v") == 0) {
      is_cal_var = true;
      argc--;
      argv++;
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
  if (fileCountTotal < 2) {
    usage(programName);
    exit(1);
  }
  fprintf(stderr, "##  Jackknife resampling! \n");
  fprintf(stderr, "##  Total of data files:  %d\n", fileCountTotal);
  fprintf(stderr, "##  Array length:         %d\n", arrayLength);

  // Create an array to store ofnames
  char *jre_dlist[fileCountTotal];

  if (isAddPrefix) {
    for (int i = 0; i < fileCountTotal; i++) {
      char stmp[2048];
      jre_dlist[i] = (char *)malloc(2048 * sizeof(char));
      addPrefix(argv[i], ofPrefix, stmp);
      changePath(stmp, ofdir, jre_dlist[i]);
    }
  } else {
    for (int i = 0; i < fileCountTotal; i++) {
      jre_dlist[i] = (char *)malloc(2048 * sizeof(char));
      changePath(argv[i], ofdir, jre_dlist[i]);
    }
  }

  // Main part for calculation
  if (is_cal_var) {
    jackknife_resample_var(argv, jre_dlist, arrayLength, fileCountTotal);
  } else {
    jackknife_resample(argv, jre_dlist, arrayLength, fileCountTotal);
  }

  if (isSaveTxt) {
    for (int i = 0; i < fileCountTotal; i++) {
      char txttmp[2048];
      addPrefix(jre_dlist[i], "txt", txttmp);
      bin2txt(jre_dlist[i], txttmp, arrayLength);
    }
  }

  // Finalization for the string arrays
  for (int i = 0; i < fileCountTotal; i++) {
    free(jre_dlist[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

void jackknife_resample(char *rawDataList[], char *samdlist[], int arrayLength,
                        int fileCountTotal) {
  CVARRAY sum(arrayLength), value(arrayLength);
  sum = value = 0.0;

  // First round: Get sum of all data
  for (int i = 0; i < fileCountTotal; i++) {
    CVARRAY tmp(arrayLength);
    tmp = 0.0;
    readBin(rawDataList[i], arrayLength, tmp);

    sum += tmp;
  }

  // Second round: Generate jackknife resampled data and save files
  for (int i = 0; i < fileCountTotal; i++) {
    CVARRAY tmp(arrayLength);
    tmp = 0.0;
    readBin(rawDataList[i], arrayLength, tmp);

    value = (sum - tmp) / (fileCountTotal - 1.0);

    writeBin(samdlist[i], arrayLength, value);
  }
}

void jackknife_resample_var(char *rawDataList[], char *samdlist[],
                            int arrayLength, int fileCountTotal) {
  DVARRAY sum(arrayLength), sum_square(arrayLength), value(arrayLength),
      var(arrayLength);
  sum = sum_square = value = var = 0.0;

  // First round: Get sum and sum^2 of all data
  for (int i = 0; i < fileCountTotal; i++) {
    CVARRAY tmp(arrayLength);
    tmp = 0.0;
    readBin(rawDataList[i], arrayLength, tmp);

    DVARRAY rtmp(arrayLength);
    rtmp = 0.0;
    keepReal(tmp, rtmp, arrayLength);
    // varryNorm(tmp, rtmp, arrayLength);

    sum += rtmp;
    sum_square += rtmp * rtmp;
  }

  // Second round: Generate the Jackknife sampled data and calculate the
  // variance
  // Also, save files to samdlist[]
  for (int i = 0; i < fileCountTotal; i++) {
    CVARRAY tmp(arrayLength);
    tmp = 0.0;
    readBin(rawDataList[i], arrayLength, tmp);

    DVARRAY rtmp(arrayLength);
    rtmp = 0.0;
    keepReal(tmp, rtmp, arrayLength);
    // varryNorm(tmp, rtmp, arrayLength);

    value = (sum - rtmp) / (fileCountTotal - 1.0);
    // About this variance, please refer to eq.(7.37) on P.383, Montvay LQCD
    // book
    var =
        sqrt(((sum_square - rtmp * rtmp) / DOUBLE(fileCountTotal - 1.0) - value * value) /
             DOUBLE(fileCountTotal - 2.0));

    CVARRAY result(arrayLength);
    result = 0.0;

    for (int j = 0; j < arrayLength; j++) {
      result[j].real(value[j]);
      result[j].imag(var[j]);
    }

    writeBin(samdlist[i], arrayLength, result);
  }
}
