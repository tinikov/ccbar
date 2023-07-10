/**
 * @file a1plus.cc
 * @author TC (reeft137@gmail.com)
 * @brief A1+ projection for 4-point correlators
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
  fprintf(stderr, "A1+ projection for 4-point correlators\n");
  fprintf(stderr, "USAGE: \n"
                  "    %s [OPTIONS] ifname1 ifname2 [ifname3 ...]\n", name);
  fprintf(stderr, "OPTIONS: \n"
                  "    -s <SPACE>:       Space length\n"
                  "    -d <OFDIR>:       Directory of output files\n"
                  "    [-p] <PREFIX>:    Prefix for output files\n"
                  "    [-h, --help]:     Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Custom functions    |
//     |________________________|

void a1_plus(char *rawdlist[], char *a1list[], int spacelength, int N_df);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int n_xyz = 0;
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

    // -s: n_xyz
    if (strcmp(argv[0], "-s") == 0)
    {
      n_xyz = atoi(argv[1]); // atoi(): convert ASCII string to integer
      if (!n_xyz)
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
  if (n_xyz == 0 || ofdir == NULL)
  {
    usage(program_name);
    exit(1);
  }

  // Initialization
  const int N_df = argc; // # of data files
  fprintf(stderr, "##  A1+ projection! \n");
  fprintf(stderr, "##  Total of data files: %d\n", N_df);
  fprintf(stderr, "##  Space length:        %d\n", n_xyz);

  // Create an arrary to store ofnames
  char *a1_dlist[N_df];

  if (is_add_prefix)
  {
    for (int i = 0; i < N_df; i++)
    {
      char stmp[2048];
      a1_dlist[i] = (char *)malloc(2048 * sizeof(char));
      add_prefix(argv[i], of_prefix, stmp);
      change_path(stmp, ofdir, a1_dlist[i]);
    }
  }
  else
  {
    for (int i = 0; i < N_df; i++)
    {
      a1_dlist[i] = (char *)malloc(2048 * sizeof(char));
      change_path(argv[i], ofdir, a1_dlist[i]);
    }
  }

  // Main part for calculation
  a1_plus(argv, a1_dlist, n_xyz, N_df);

  // Finalization for the string arrays
  for (int i = 0; i < N_df; i++)
  {
    free(a1_dlist[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

inline DOUBLE sphere_sym(DOUBLE *data, int x, int y, int z, int spacelength)
{
  return (CORR(data, x, y, z, spacelength) + CORR(data, y, z, x, spacelength) + CORR(data, z, x, y, spacelength) + CORR(data, x, z, y, spacelength) + CORR(data, z, y, x, spacelength) + CORR(data, y, x, z, spacelength)) / 6.0;
}

inline DOUBLE a1_sym(DOUBLE *data, int x, int y, int z, int spacelength)
{
  return (sphere_sym(data, x, y, z, spacelength) + sphere_sym(data, x, y, spacelength - z, spacelength) + sphere_sym(data, x, spacelength - y, z, spacelength) + sphere_sym(data, x, spacelength - y, spacelength - z, spacelength) + sphere_sym(data, spacelength - x, y, z, spacelength) + sphere_sym(data, spacelength - x, y, spacelength - z, spacelength) + sphere_sym(data, spacelength - x, spacelength - y, z, spacelength) + sphere_sym(data, spacelength - x, spacelength - y, spacelength - z, spacelength)) / 8.0;
}

void a1_plus(char *rawdlist[], char *a1list[], int spacelength, int N_df)
{
  int array_length = int(pow(spacelength, 3));

  for (int i = 0; i < N_df; i++)
  {
    DOUBLE tmp[array_length], result[array_length];

    for (int j = 0; j < array_length; j++) // Initialize the empty arrays
    {
      tmp[j] = result[j] = 0.0;
    }

    read_bin(rawdlist[i], array_length, tmp);

#pragma omp parallel for
    for (int ix = 0; ix < spacelength; ix++)
#pragma omp parallel for
      for (int iy = 0; iy < spacelength; iy++)
#pragma omp parallel for
        for (int iz = 0; iz < spacelength; iz++)
        {
          CORR(result, ix, iy, iz, spacelength) = a1_sym(tmp, ix, iy, iz, spacelength);
        }

    write_bin(a1list[i], array_length, result);
  }
}