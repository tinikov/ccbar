/**
 * @file cart2sphr.cc
 * @author TC (reeft137@gmail.com)
 * @brief From Cartesian coordinate to Spherical coordinate
 * @version 1.0
 * @date 2023-05-03
 *
 */

#include "correlator.h"
#include "data_process.h"
#include "misc.h"
// __________________________________
//     .________|______|________.
//     |                        |
//     |     Usage function     |
//     |________________________|

void usage(char *name)
{
  fprintf(stderr, "From Cartesian coordinate to Spherical coordinate\n");
  fprintf(stderr, "USAGE: \n"
                  "    %s [OPTIONS] ifname1 [ifname2 ...]\n",
          name);
  fprintf(stderr, "OPTIONS: \n"
                  "    -s <LENGTH>:      Space length\n"
                  "    -d <OFDIR>:       Directory of output files\n"
                  "    [-p] <PREFIX>:    Prefix for output files\n"
                  "    [-h, --help]:     Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Custom functions    |
//     |________________________|

void cartesian_to_spherical(char *rawdlist[], char *sphrdlist[], int space_length, int N_df);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int space_length = 0;
static const char *ofdir = NULL;
static const char *of_prefix = NULL;
bool is_add_prefix = false;
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

    // -l: space_length
    if (strcmp(argv[0], "-s") == 0)
    {
      space_length = atoi(argv[1]); // atoi(): convert ASCII string to integer
      if (!space_length)
      {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -d: directory for output file
    if (strcmp(argv[0], "-d") == 0)
    {
      ofdir = argv[1];
      argc -= 2;
      argv += 2;
      continue;
    }

    // -p: prefix for output file
    if (strcmp(argv[0], "-p") == 0)
    {
      of_prefix = argv[1];
      is_add_prefix = true;
      argc -= 2;
      argv += 2;
      continue;
    }

    fprintf(stderr, "Error: Unknown option '%s'\n", argv[0]);
    usage(program_name);
    exit(1);
  }

  // Make sure of all needed syntax
  if (space_length == 0 || ofdir == NULL)
  {
    usage(program_name);
    exit(1);
  }

  // Initialization
  const int N_df = argc; // # of data files
  fprintf(stderr, "##  Cartesian to Spherical! \n");
  fprintf(stderr, "##  Total of data files: %d\n", N_df);
  fprintf(stderr, "##  Space length:        %d\n", space_length);

  // Create an arrary to store ofnames
  char *sphr_dlist[N_df];

  if (is_add_prefix)
  {
    for (int i = 0; i < N_df; i++)
    {
      char stmp[2048];
      sphr_dlist[i] = (char *)malloc(2048 * sizeof(char));
      add_prefix(argv[i], of_prefix, stmp);
      change_path(stmp, ofdir, sphr_dlist[i]);
    }
  }
  else
  {
    for (int i = 0; i < N_df; i++)
    {
      sphr_dlist[i] = (char *)malloc(2048 * sizeof(char));
      change_path(argv[i], ofdir, sphr_dlist[i]);
    }
  }

  // Main part for calculation
  cartesian_to_spherical(argv, sphr_dlist, space_length, N_df);

  // Finalization for the string arrays
  for (int i = 0; i < N_df; i++)
  {
    free(sphr_dlist[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

void cartesian_to_spherical(char *rawdlist[], char *sphrdlist[], int space_length, int N_df)
{
  int array_length = pow(space_length, 3);

  for (int i = 0; i < N_df; i++)
  {
    COMPLX tmp[array_length];

#pragma omp parallel for
    for (int j = 0; j < array_length; j++) // Initialize the empty arrays
    {
      tmp[j] = 0.0;
    }
    read_bin(rawdlist[i], array_length, tmp);

    FILE *fp = fopen(sphrdlist[i], "w");
    if (fp == NULL)
    {
      perror(sphrdlist[i]);
      exit(1);
    }
#pragma omp parallel for
    for (int i = 0; i < space_length / 2 + 1; i++)
#pragma omp parallel for
      for (int j = i; j < space_length / 2 + 1; j++)
#pragma omp parallel for
        for (int k = j; k < space_length / 2 + 1; k++)
        { 
          DOUBLE re, im, distance = 0.0;

          distance = sqrt(pow(DOUBLE(i), 2) + pow(DOUBLE(j), 2) + pow(DOUBLE(k), 2));
          re = CORR(tmp, i, j, k, space_length).real();
          im = CORR(tmp, i, j, k, space_length).imag();

          fprintf(fp, "%1.16e %1.16e %1.16e\n", distance, re, im);
        }

    fclose(fp);
  }
}
