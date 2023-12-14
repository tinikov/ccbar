/**
 * @file mean.cc
 * @author TC (reeft137@gmail.com)
 * @brief Mean for raw data (Optional: jackknife variance)
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
  fprintf(stderr, "Mean for raw data (Optional: jackknife variance)\n");
  fprintf(stderr,
          "USAGE: \n"
          "    %s [OPTIONS] ifname1 ifname2 [ifname3 ...]\n",
          name);
  fprintf(stderr,
          "OPTIONS: \n"
          "    -l <LENGTH>:      Length of data arrays\n"
          "    -o <OFNAME>:      Name of output file\n"
          "    [-j]:             Calculate jackknife variance\n"
          "    [-jd]:            Calculate jackknife variance (input: DOUBLE)\n"
          "    [-t]:             Also save a txt file\n"
          "    [-h, --help]:     Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Custom functions    |
//     |________________________|

void arithmetic_mean(char *rawdlist[], const char *result, int array_length,
                     int N_df);
void jackknife_mean(char *rawdlist[], const char *result, int array_length,
                    int N_df);
void jackknife_mean_double(char *rawdlist[], const char *result,
                           int array_length, int N_df);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int array_length = 0;
static const char *of_name = NULL;
bool is_jackknife = false;
bool is_jackknife_double = false;
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

    // -j: jackknife variance
    if (strcmp(argv[0], "-j") == 0) {
      is_jackknife = true;
      argc--;
      argv++;
      continue;
    }

    // -jd: jackknife variance (on DOUBLE)
    if (strcmp(argv[0], "-jd") == 0) {
      is_jackknife_double = true;
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

  const int N_df = argc;  // # of data files
  if (N_df < 2) {
    usage(program_name);
    exit(1);
  }

  if (is_jackknife) {
    // Initialization
    fprintf(stderr, "##  Mean with JK-var! \n");
    fprintf(stderr, "##  Total of data files:  %d\n", N_df);
    fprintf(stderr, "##  Array length:         %d\n", array_length);

    jackknife_mean(argv, of_name, array_length, N_df);
  } else if (is_jackknife_double) {
    // Initialization
    fprintf(stderr, "##  Mean with JK-var! (DOUBLE)\n");
    fprintf(stderr, "##  Total of data files:  %d\n", N_df);
    fprintf(stderr, "##  Array length:         %d\n", array_length);

    jackknife_mean_double(argv, of_name, array_length, N_df);
  } else {
    // Initialization
    fprintf(stderr, "##  Naive mean! \n");
    fprintf(stderr, "##  Total of data files:  %d\n", N_df);
    fprintf(stderr, "##  Array length:         %d\n", array_length);

    arithmetic_mean(argv, of_name, array_length, N_df);
  }

  if (is_save_txt) {
    char txtfname[2048];
    add_prefix(of_name, "txt", txtfname);
    bin2txt(of_name, txtfname, array_length);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

// Jackknife average
void jackknife_mean(char *rawdlist[], const char *result, int array_length,
                    int N_df) {
  DVARRAY mean(array_length), var(array_length);
  mean = var = 0.0;

  for (int i = 0; i < N_df; i++) {
    CVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);

    DVARRAY rtmp(array_length);
    rtmp = 0.0;
    keep_real(tmp, rtmp, array_length);
    // varry_norm(tmp, rtmp, array_length);

    mean += rtmp / DOUBLE(N_df);
  }

  for (int i = 0; i < N_df; i++) {
    CVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);

    DVARRAY rtmp(array_length);
    rtmp = 0.0;
    keep_real(tmp, rtmp, array_length);
    // varry_norm(tmp, rtmp, array_length);

    var += (rtmp - mean) * (rtmp - mean);
  }

  var = sqrt(var * DOUBLE(N_df - 1) / DOUBLE(N_df));

  CVARRAY out(array_length);
  out = 0.0;

  for (int i = 0; i < array_length; i++) {
    out[i].real(mean[i]);
    out[i].imag(var[i]);
  }

  write_bin(result, array_length, out);
}

void jackknife_mean_double(char *rawdlist[], const char *result,
                           int array_length, int N_df) {
  DVARRAY mean(array_length), var(array_length);
  mean = var = 0.0;

  for (int i = 0; i < N_df; i++) {
    DVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);

    mean += tmp / DOUBLE(N_df);
  }

  for (int i = 0; i < N_df; i++) {
    DVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);

    var += (tmp - mean) * (tmp - mean);
  }

  var = sqrt(var * DOUBLE(N_df - 1) / DOUBLE(N_df));

  CVARRAY out(array_length);
  out = 0.0;

  for (int i = 0; i < array_length; i++) {
    out[i].real(mean[i]);
    out[i].imag(var[i]);
  }

  write_bin(result, array_length, out);
}

void arithmetic_mean(char *rawdlist[], const char *result, int array_length,
                     int N_df) {
  CVARRAY mean(array_length);
  mean = 0.0;

  for (int i = 0; i < N_df; i++) {
    CVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);

    mean += tmp / COMPLX(N_df, 0.0);
  }

  write_bin(result, array_length, mean);
}
