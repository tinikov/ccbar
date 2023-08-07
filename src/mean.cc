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
// __________________________________
//     .________|______|________.
//     |                        |
//     |     Usage function     |
//     |________________________|

void usage(char *name)
{
  fprintf(stderr, "Mean for raw data (Optional: jackknife variance)\n");
  fprintf(stderr, "USAGE: \n"
                  "    %s [OPTIONS] ifname1 ifname2 [ifname3 ...]\n",
          name);
  fprintf(stderr, "OPTIONS: \n"
                  "    -l <LENGTH>:      Length of data arrays\n"
                  "    -o <OFNAME>:      Name of output file\n"
                  "    [-j]:             Calculate jackknife variance\n"
                  "    [-t]:             Also save a txt file\n"
                  "    [-h, --help]:     Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Custom functions    |
//     |________________________|

void arithmetic_mean(char *rawdlist[], const char *result, int array_length, int N_df);
void jackknife_mean(char *rawdlist[], const char *result, int array_length, int N_df);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int array_length = 0;
static const char *ofname = NULL;
bool is_jackknife = false;
bool is_save_txt = false;
// __________________________________
//     .________|______|________.
//     |                        |
//     |      Main Function     |
//     |________________________|

int main(int argc, char *argv[])
{
  char program_name[128];
  strncpy(program_name, basename(argv[0]), 127);
  argc--;
  argv++;
  // ________________________________
  //    .________|______|________.
  //    |                        |
  //    |  Dealing with Options  |
  //    |________________________|

  while (argc > 0 && argv[0][0] == '-') // deal with all options regardless of their order
  {
    // -h and --help: show usage
    if (strcmp(argv[0], "-h") == 0 || strcmp(argv[0], "--help") == 0)
    {
      usage(program_name);
      exit(0);
    }

    // -l: array_length
    if (strcmp(argv[0], "-l") == 0)
    {
      array_length = atoi(argv[1]); // atoi(): convert ASCII string to integer
      if (!array_length)
      {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -o: ofname
    if (strcmp(argv[0], "-o") == 0)
    {
      ofname = argv[1];
      if (ofname == NULL)
      {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -j: jackknife variance
    if (strcmp(argv[0], "-j") == 0)
    {
      is_jackknife = true;
      argc--;
      argv++;
      continue;
    }

    // -t: save txt
    if (strcmp(argv[0], "-t") == 0)
    {
      is_save_txt = true;
      argc--;
      argv++;
      continue;
    }

    fprintf(stderr, "Error: Unknown option '%s'\n", argv[0]);
    usage(program_name);
    exit(1);
  }

  // Make sure of all needed syntax
  if (argc < 2)
  {
    usage(program_name);
    exit(1);
  }

  if (is_jackknife)
  {
    // Initialization
    const int N_df = argc; // # of data files
    fprintf(stderr, "##  Mean with JK-var! \n");
    fprintf(stderr, "##  Total of data files:  %d\n", N_df);
    fprintf(stderr, "##  Array length:         %d\n", array_length);

    jackknife_mean(argv, ofname, array_length, N_df);

    if (is_save_txt)
    {
      char txtfname[2048];
      add_prefix(ofname, "txt", txtfname);
      bin2txt(ofname, txtfname, array_length);
    }
  }
  else
  {
    // Initialization
    const int N_df = argc; // # of data files
    fprintf(stderr, "##  Naive mean! \n");
    fprintf(stderr, "##  Total of data files:  %d\n", N_df);
    fprintf(stderr, "##  Array length:         %d\n", array_length);

    arithmetic_mean(argv, ofname, array_length, N_df);

    if (is_save_txt)
    {
      char txtfname[2048];
      add_prefix(ofname, "txt", txtfname);
      bin2txt(ofname, txtfname, array_length);
    }
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

// Jackknife average
void jackknife_mean(char *rawdlist[], const char *result, int array_length, int N_df)
{
  DVARRAY mean(array_length), var(array_length);
  mean = var = 0.0;

#pragma omp parallel for
  for (int i = 0; i < N_df; i++)
  {
    CVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);

    DVARRAY rtmp(array_length);
    rtmp = 0.0;
    keep_real(tmp, rtmp, array_length);

    mean += rtmp / DOUBLE(N_df);
  }

#pragma omp parallel for
  for (int i = 0; i < N_df; i++)
  {
    CVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);
    
    DVARRAY rtmp(array_length);
    rtmp = 0.0;
    keep_real(tmp, rtmp, array_length);

    var += pow((rtmp - mean), 2);
  }

  var = sqrt(var * DOUBLE(N_df - 1) / DOUBLE(N_df));

  CVARRAY out(array_length);
  out = 0.0;

#pragma omp parallel for
  for (int i = 0; i < array_length; i++)
  {
    out[i].real(mean[i]);
    out[i].imag(var[i]);
  }

  write_bin(result, array_length, out);
}

void arithmetic_mean(char *rawdlist[], const char *result, int array_length, int N_df)
{
  CVARRAY mean(array_length);
  mean = 0.0;

#pragma omp parallel for
  for (int i = 0; i < N_df; i++)
  {
    CVARRAY tmp(array_length);
    tmp = 0.0;
    read_bin(rawdlist[i], array_length, tmp);

    mean += tmp / DOUBLE(N_df);
  }

  write_bin(result, array_length, mean);
}