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

void time_reverse_2pt(char *rawdlist[], char *trdlist[], int n_t, int N_df);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int n_t = 0;
static const char *of_dir = NULL;
static const char *of_prefix = NULL;
bool is_add_prefix = false;
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

    // -n: n_t
    if (strcmp(argv[0], "-n") == 0) {
      n_t = atoi(argv[1]);  // atoi(): convert ASCII string to integer
      if (!n_t) {
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
  if (N_df < 1) {
    usage(program_name);
    exit(1);
  }
  fprintf(stderr, "##  Time reversal! \n");
  fprintf(stderr, "##  Total of data files:  %d\n", N_df);
  fprintf(stderr, "##  Temporal size:        %d\n", n_t);

  // Create an array to store ofnames
  char *tr_dlist[N_df];

  if (is_add_prefix) {
    for (int i = 0; i < N_df; i++) {
      char stmp[2048];
      tr_dlist[i] = (char *)malloc(2048 * sizeof(char));
      addPrefix(argv[i], of_prefix, stmp);
      changePath(stmp, of_dir, tr_dlist[i]);
    }
  } else {
    for (int i = 0; i < N_df; i++) {
      tr_dlist[i] = (char *)malloc(2048 * sizeof(char));
      changePath(argv[i], of_dir, tr_dlist[i]);
    }
  }

  // Main part for calculation
  time_reverse_2pt(argv, tr_dlist, n_t, N_df);

  if (is_save_txt) {
    for (int i = 0; i < N_df; i++) {
      char txttmp[2048];
      addPrefix(tr_dlist[i], "txt", txttmp);
      bin2txt(tr_dlist[i], txttmp, n_t);
    }
  }

  // Finalization for the string arrays
  for (int i = 0; i < N_df; i++) {
    free(tr_dlist[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

void time_reverse_2pt(char *rawdlist[], char *trdlist[], int n_t, int N_df) {
  for (int i = 0; i < N_df; i++) {
    COMPLX raw[n_t], data[n_t];
    for (int j = 0; j < n_t; j++) raw[j] = data[j] = 0.0;

    readBin(rawdlist[i], n_t, raw);

    for (int j = 0; j < n_t; j++)
      data[j] = (raw[j] + raw[(n_t - j) % n_t]) * 0.5;

    writeBin(trdlist[i], n_t, data);
  }
}
