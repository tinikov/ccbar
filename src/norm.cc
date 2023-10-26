/**
 * @file norm.cc
 * @author TC (reeft137@gmail.com)
 * @brief Normalizaion for 4-point correlators
 * @version 1.0
 * @date 2023-07-10
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
  fprintf(stderr, "Normalizaion for 4-point correlators\n");
  fprintf(stderr,
          "USAGE: \n"
          "    %s [OPTIONS] ifname1 [ifname2 ...]\n",
          name);
  fprintf(stderr,
          "OPTIONS: \n"
          "    -n <XYZSIZE>:     Spacial size of lattice\n"
          "    -d <OFDIR>:       Directory of output files\n"
          "    [-h, --help]:     Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Custom functions    |
//     |________________________|

void naive_norm(char *rawdlist[], char *nnlist[], int n_xyz, int N_df);
void l2_norm(char *rawdlist[], char *l2list[], int n_xyz, int N_df);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int n_xyz = 0;
static const char *of_dir = NULL;
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
  fprintf(stderr, "##  Normalization! \n");
  fprintf(stderr, "##  Total of data files: %d\n", N_df);
  fprintf(stderr, "##  Spacial size:        %d\n", n_xyz);

  // Create arrays to store ofnames
  char *nn_dlist[N_df], *l2_dlist[N_df];

  for (int i = 0; i < N_df; i++) {
    char nn_stmp[2048], l2_stmp[2048];
    nn_dlist[i] = (char *)malloc(2048 * sizeof(char));
    l2_dlist[i] = (char *)malloc(2048 * sizeof(char));

    add_prefix(argv[i], "nn", nn_stmp);
    change_path(nn_stmp, of_dir, nn_dlist[i]);
    add_prefix(argv[i], "l2", l2_stmp);
    change_path(l2_stmp, of_dir, l2_dlist[i]);
  }

  // Main part for calculation
  naive_norm(argv, nn_dlist, n_xyz, N_df);
  l2_norm(argv, l2_dlist, n_xyz, N_df);

  // Finalization for the string arrays
  for (int i = 0; i < N_df; i++) {
    free(nn_dlist[i]);
    free(l2_dlist[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

void naive_norm(char *rawdlist[], char *nnlist[], int n_xyz, int N_df) {
  int array_length = int(pow(n_xyz, 3));

  for (int i = 0; i < N_df; i++) {
    COMPLX tmp[array_length], result[array_length];

    for (int j = 0; j < array_length; j++)  // Initialize the empty arrays
    {
      tmp[j] = result[j] = 0.0;
    }

    read_bin(rawdlist[i], array_length, tmp);

    for (int j = 0; j < array_length; j++)  // Compute C_n(t) = C(t)/C(0)
    {
      result[j] = tmp[j] / tmp[0];
    }

    write_bin(nnlist[i], array_length, result);
  }
}

void l2_norm(char *rawdlist[], char *l2list[], int n_xyz, int N_df) {
  int array_length = int(pow(n_xyz, 3));

  for (int i = 0; i < N_df; i++) {
    COMPLX tmp[array_length], result[array_length];
    DOUBLE norm_fact = 0.0;

    for (int j = 0; j < array_length; j++)  // Initialize the empty arrays
    {
      tmp[j] = result[j] = 0.0;
    }

    read_bin(rawdlist[i], array_length, tmp);

    for (int j = 0; j < array_length; j++) {
      norm_fact += norm(tmp[j]);
    }

    norm_fact = sqrt(norm_fact);

    for (int j = 0; j < array_length;
         j++)  // Compute C_n(t) = C(t)/\sqrt(\sum_{C^2})
    {
      result[j] = tmp[j] / norm_fact;
    }

    write_bin(l2list[i], array_length, result);
  }
}
