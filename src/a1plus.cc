/**
 * @file a1plus.cc
 * @author Tianchen Zhang 
 * @brief A1+ projection for 4-point correlators
 * @version 1.0
 * @date 2023-05-03
 *
 */

#include "correlator.h"
#include "data_process.h"
#include "misc.h"
#include "type_alias.h"
// __________________________________
//     .________|______|________.
//     |                        |
//     |     Usage function     |
//     |________________________|

void usage(char *name) {
  fprintf(stderr, "A1+ projection for 4-point correlators\n");
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

void a1_plus(char *rawdlist[], char *a1list[], int n_xyz, int N_df);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int n_xyz = 0;
static const char *of_dir = NULL;
static const char *of_prefix = NULL;
bool is_add_prefix = false;
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

    // -n: n_xyz
    if (strcmp(argv[0], "-n") == 0) {
      n_xyz = atoi(argv[1]);  // atoi(): convert ASCII string to integer
      if (!n_xyz) {
        usage(program_name);
        exit(1);
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    // -d: directory for output file
    if (strcmp(argv[0], "-d") == 0) {
      of_dir = argv[1];
      if (of_dir == NULL) {
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

    fprintf(stderr, "Error: Unknown option '%s'\n", argv[0]);
    usage(program_name);
    exit(1);
  }

  // Initialization
  const int N_df = argc;  // # of data files
  if (N_df < 1) {
    usage(program_name);
    exit(1);
  }
  fprintf(stderr, "##  A1+ projection! \n");
  fprintf(stderr, "##  Total of data files:  %d\n", N_df);
  fprintf(stderr, "##  Spacial size:         %d\n", n_xyz);

  // Create an array to store ofnames
  char *a1_dlist[N_df];

  if (is_add_prefix) {
    for (int i = 0; i < N_df; i++) {
      char stmp[2048];
      a1_dlist[i] = (char *)malloc(2048 * sizeof(char));
      addPrefix(argv[i], of_prefix, stmp);
      changePath(stmp, of_dir, a1_dlist[i]);
    }
  } else {
    for (int i = 0; i < N_df; i++) {
      a1_dlist[i] = (char *)malloc(2048 * sizeof(char));
      changePath(argv[i], of_dir, a1_dlist[i]);
    }
  }

  // Main part for calculation
  a1_plus(argv, a1_dlist, n_xyz, N_df);

  // Finalization for the string arrays
  for (int i = 0; i < N_df; i++) {
    free(a1_dlist[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

inline COMPLX sphere_sym(COMPLX *data, int x, int y, int z, int n_xyz) {
  return (CORR(data, x, y, z, n_xyz) + CORR(data, y, z, x, n_xyz) +
          CORR(data, z, x, y, n_xyz) + CORR(data, x, z, y, n_xyz) +
          CORR(data, z, y, x, n_xyz) + CORR(data, y, x, z, n_xyz)) /
         6.0;
}

inline COMPLX a1_sym(COMPLX *data, int x, int y, int z, int n_xyz) {
  return (sphere_sym(data, x, y, z, n_xyz) +
          sphere_sym(data, x, y, n_xyz - z, n_xyz) +
          sphere_sym(data, x, n_xyz - y, z, n_xyz) +
          sphere_sym(data, x, n_xyz - y, n_xyz - z, n_xyz) +
          sphere_sym(data, n_xyz - x, y, z, n_xyz) +
          sphere_sym(data, n_xyz - x, y, n_xyz - z, n_xyz) +
          sphere_sym(data, n_xyz - x, n_xyz - y, z, n_xyz) +
          sphere_sym(data, n_xyz - x, n_xyz - y, n_xyz - z, n_xyz)) /
         8.0;
}

void a1_plus(char *rawdlist[], char *a1list[], int n_xyz, int N_df) {
  int array_length = int(pow(n_xyz, 3));

  for (int i = 0; i < N_df; i++) {
    COMPLX tmp[array_length], result[array_length];
    for (int j = 0; j < array_length; j++)  // Initialize the empty arrays
    {
      tmp[j] = result[j] = 0.0;
    }

    readBin(rawdlist[i], array_length, tmp);

    for (int ix = 0; ix < n_xyz; ix++)
      for (int iy = 0; iy < n_xyz; iy++)
        for (int iz = 0; iz < n_xyz; iz++) {
          CORR(result, ix, iy, iz, n_xyz) = a1_sym(tmp, ix, iy, iz, n_xyz);
        }

    writeBin(a1list[i], array_length, result);
  }
}
