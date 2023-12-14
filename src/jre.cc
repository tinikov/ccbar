/**
 * @file jre.cc
 * @author TC (reeft137@gmail.com)
 * @brief Jackknife resampling for raw data
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

void jackknife_resample(char *rawdlist[], char *samdlist[], int array_length,
                        int N_df);
void jackknife_resample_var(char *rawdlist[], char *samdlist[],
                            int array_length, int N_df);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int array_length = 0;
static const char *ofdir = NULL;
static const char *of_prefix = NULL;
bool is_add_prefix = false;
bool is_cal_var = false;
bool is_save_txt = false;
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

    // -d: directory for output file
    if (strcmp(argv[0], "-d") == 0) {
      ofdir = argv[1];
      if (ofdir == NULL) {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -p: prefix for output file
    if (strcmp(argv[0], "-p") == 0) {
      of_prefix = argv[1];
      is_add_prefix = true;
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
      is_save_txt = true;
      argc--;
      argv++;
      continue;
    }

    fprintf(stderr, "Error: Unknown option '%s'\n", argv[0]);
    usage(program_name);
    exit(1);
  }

  // Initialization
  const int N_df = argc;  // # of data files
  if (N_df < 2) {
    usage(program_name);
    exit(1);
  }
  fprintf(stderr, "##  Jackknife resampling! \n");
  fprintf(stderr, "##  Total of data files:  %d\n", N_df);
  fprintf(stderr, "##  Array length:         %d\n", array_length);

  // Create an array to store ofnames
  char *jre_dlist[N_df];

  if (is_add_prefix) {
    for (int i = 0; i < N_df; i++) {
      char stmp[2048];
      jre_dlist[i] = (char *)malloc(2048 * sizeof(char));
      add_prefix(argv[i], of_prefix, stmp);
      change_path(stmp, ofdir, jre_dlist[i]);
    }
  } else {
    for (int i = 0; i < N_df; i++) {
      jre_dlist[i] = (char *)malloc(2048 * sizeof(char));
      change_path(argv[i], ofdir, jre_dlist[i]);
    }
  }

  // Main part for calculation
  if (is_cal_var) {
    jackknife_resample_var(argv, jre_dlist, array_length, N_df);
  } else {
    jackknife_resample(argv, jre_dlist, array_length, N_df);
  }

  if (is_save_txt) {
    for (int i = 0; i < N_df; i++) {
      char txttmp[2048];
      add_prefix(jre_dlist[i], "txt", txttmp);
      bin2txt(jre_dlist[i], txttmp, array_length);
    }
  }

  // Finalization for the string arrays
  for (int i = 0; i < N_df; i++) {
    free(jre_dlist[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

void jackknife_resample(char *rawdlist[], char *samdlist[], int array_length,
                        int N_df) {
  CVARRAY sum(array_length), value(array_length);
  sum = value = 0.0;

  // First round: Get sum of all data
  for (int i = 0; i < N_df; i++) {
    CVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);

    sum += tmp;
  }

  // Second round: Generate jackknife resampled data and save files
  for (int i = 0; i < N_df; i++) {
    CVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);

    value = (sum - tmp) / (N_df - 1.0);

    write_bin(samdlist[i], array_length, value);
  }
}

void jackknife_resample_var(char *rawdlist[], char *samdlist[],
                            int array_length, int N_df) {
  DVARRAY sum(array_length), sum_square(array_length), value(array_length),
      var(array_length);
  sum = sum_square = value = var = 0.0;

  // First round: Get sum and sum^2 of all data
  for (int i = 0; i < N_df; i++) {
    CVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);

    DVARRAY rtmp(array_length);
    rtmp = 0.0;
    keep_real(tmp, rtmp, array_length);
    // varry_norm(tmp, rtmp, array_length);

    sum += rtmp;
    sum_square += rtmp * rtmp;
  }

  // Second round: Generate the Jackknife sampled data and calculate the
  // variance
  // Also, save files to samdlist[]
  for (int i = 0; i < N_df; i++) {
    CVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);

    DVARRAY rtmp(array_length);
    rtmp = 0.0;
    keep_real(tmp, rtmp, array_length);
    // varry_norm(tmp, rtmp, array_length);

    value = (sum - rtmp) / (N_df - 1.0);
    // About this variance, please refer to eq.(7.37) on P.383, Montvay LQCD
    // book
    var =
        sqrt(((sum_square - rtmp * rtmp) / DOUBLE(N_df - 1.0) - value * value) /
             DOUBLE(N_df - 2.0));

    CVARRAY result(array_length);
    result = 0.0;

    for (int j = 0; j < array_length; j++) {
      result[j].real(value[j]);
      result[j].imag(var[j]);
    }

    write_bin(samdlist[i], array_length, result);
  }
}
