/**
 * @file ppot.cc
 * @author TC (reeft137@gmail.com)
 * @brief Pre-potential: [▽^2 C(r,t)]/C(r,t)
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
  fprintf(stderr, "Pre-potential: [▽^2 C(r,t)]/C(r,t)\n");
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

void pre_potential(char *rawdlist[], char *ppotlist[], int n_xyz, int N_df);
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
  fprintf(stderr, "##  Pre-potential! \n");
  fprintf(stderr, "##  Total of data files: %d\n", N_df);
  fprintf(stderr, "##  Space length:        %d\n", n_xyz);

  // Create an array to store ofnames
  char *ppot_dlist[N_df];

  if (is_add_prefix)
  {
    for (int i = 0; i < N_df; i++)
    {
      char stmp[2048];
      ppot_dlist[i] = (char *)malloc(2048 * sizeof(char));
      add_prefix(argv[i], of_prefix, stmp);
      change_path(stmp, ofdir, ppot_dlist[i]);
    }
  }
  else
  {
    for (int i = 0; i < N_df; i++)
    {
      ppot_dlist[i] = (char *)malloc(2048 * sizeof(char));
      change_path(argv[i], ofdir, ppot_dlist[i]);
    }
  }

  // Main part for calculation
  pre_potential(argv, ppot_dlist, n_xyz, N_df);

  // Finalization for the string arrays
  for (int i = 0; i < N_df; i++)
  {
    free(ppot_dlist[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

void pre_potential(char *rawdlist[], char *ppotlist[], int n_xyz, int N_df)
{
  int array_length = int(pow(n_xyz, 3));

#pragma omp parallel for
  for (int i = 0; i < N_df; i++)
  {
    COMPLX tmp[array_length], result[array_length];
#pragma omp parallel for
    for (int j = 0; j < array_length; j++) // Initialize the empty arrays
    {
      tmp[j] = result[j] = 0.0;
    }

    read_bin(rawdlist[i], array_length, tmp);

#pragma omp parallel for
    for (int ix = 0; ix < n_xyz; ix++)
#pragma omp parallel for
      for (int iy = 0; iy < n_xyz; iy++)
#pragma omp parallel for
        for (int iz = 0; iz < n_xyz; iz++)
        {
          CORR(result, ix, iy, iz, n_xyz) = (CORR(tmp, ix + 1, iy, iz, n_xyz) + CORR(tmp, ix - 1, iy, iz, n_xyz) + CORR(tmp, ix, iy + 1, iz, n_xyz) + CORR(tmp, ix, iy - 1, iz, n_xyz) + CORR(tmp, ix, iy, iz + 1, n_xyz) + CORR(tmp, ix, iy, iz - 1, n_xyz) - 6.0 * CORR(tmp, ix, iy, iz, n_xyz)) / CORR(tmp, ix, iy, iz, n_xyz);
        }

    write_bin(ppotlist[i], array_length, result);
  }
}