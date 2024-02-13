/**
 * @file effmass.cc
 * @author Tianchen Zhang 
 * @brief Effective masses for charmonium
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
  fprintf(stderr,
          "Effective masses for charmonium (ofname: exp.xxx and csh.xxx)\n");
  fprintf(stderr,
          "USAGE: \n"
          "    %s [OPTIONS] ifname1 [ifname2 ...]\n",
          name);
  fprintf(stderr,
          "OPTIONS: \n"
          "    -n <TSIZE>:       Temporal size of lattice\n"
          "    -d <OFDIR>:       Directory of output files\n"
          "    [-t]:             Also save a txt file (add \"txt.\" prefix)\n"
          "    [-h, --help]:     Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Custom functions    |
//     |________________________|

void exp_mass(char *rawdlist[], char *explist[], int n_t, int N_df);
void csh_mass(char *rawdlist[], char *cshlist[], int n_t, int N_df);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int n_t = 0;
static const char *of_dir = NULL;
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
  fprintf(stderr, "##  Effective mass! \n");
  fprintf(stderr, "##  Total of data files: %d\n", N_df);
  fprintf(stderr, "##  Temporal size:       %d\n", n_t);

  // Create an array to store ofnames
  char *exp_dlist[N_df], *csh_dlist[N_df];

  for (int i = 0; i < N_df; i++) {
    char stmp[2048];

    exp_dlist[i] = (char *)malloc(2048 * sizeof(char));
    addPrefix(argv[i], "exp", stmp);
    changePath(stmp, of_dir, exp_dlist[i]);

    csh_dlist[i] = (char *)malloc(2048 * sizeof(char));
    addPrefix(argv[i], "csh", stmp);
    changePath(stmp, of_dir, csh_dlist[i]);
  }

  // Main part for calculation
  exp_mass(argv, exp_dlist, n_t, N_df);
  csh_mass(argv, csh_dlist, n_t, N_df);

  if (is_save_txt) {
    for (int i = 0; i < N_df; i++) {
      char txttmp[2048];

      addPrefix(exp_dlist[i], "txt", txttmp);
      bin2txt(exp_dlist[i], txttmp, n_t);

      addPrefix(csh_dlist[i], "txt", txttmp);
      bin2txt(csh_dlist[i], txttmp, n_t);
    }
  }

  // Finalization for the string arrays
  for (int i = 0; i < N_df; i++) {
    free(exp_dlist[i]);
    free(csh_dlist[i]);
  }

  return 0;
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |  Custom Functions DEF  |
//     |________________________|

void exp_mass(char *rawdlist[], char *explist[], int n_t, int N_df) {
  for (int i = 0; i < N_df; i++) {
    COMPLX raw[n_t], effmass[n_t];
    for (int j = 0; j < n_t; j++) {
      raw[j] = 0.0;
      effmass[j] = 0.0;
    }
    readBin(rawdlist[i], n_t, raw);

    for (int j = 0; j < n_t; j++) {
      effmass[j].real(log(raw[j].real() / raw[(j + 1) % n_t].real()));
    }

    writeBin(explist[i], n_t, effmass);
  }
}

DOUBLE coshtype_mass(int t1, int t2, DOUBLE corr1, DOUBLE corr2, int n_t) {
#define JMAX 100
#define M0 0.001
#define M1 10.0
#define MACC 1.0e-12
#define coshtype(m) \
  (corr1 / corr2 - cosh((m) * (n_t / 2.0 - t1)) / cosh((m) * (n_t / 2.0 - t2)))

  DOUBLE dm, f, fmid, mmid, mass;

  f = coshtype(M0);
  fmid = coshtype(M1);
  if (f * fmid >= 0.0) {
    fprintf(stderr, "Root must be bracketed for bisection in RTBIS\n");
    return NAN;
  }
  mass = f < 0.0 ? (dm = M1 - M0, M0) : (dm = M0 - M1, M1);
  for (int j = 1; j <= JMAX; j++) {
    mmid = mass + (dm *= 0.5);
    fmid = coshtype(mmid);
    if (fmid <= 0.0) mass = mmid;
    if (fabs(dm) < MACC || fmid == 0.0) return mass;
  }
  fprintf(stderr, "Too many bisections in RTBIS");
  return 0.0;
}

void csh_mass(char *rawdlist[], char *cshlist[], int n_t, int N_df) {
  for (int i = 0; i < N_df; i++) {
    COMPLX raw[n_t], effmass[n_t];
    for (int j = 0; j < n_t; j++) {
      raw[j] = 0.0;
      effmass[j] = 0.0;
    }
    readBin(rawdlist[i], n_t, raw);

    for (int j = 0; j < n_t; j++) {
      int t1 = j;
      int t2 = (j + 1) % n_t;
      effmass[j].real(
          coshtype_mass(t1, t2, raw[t1].real(), raw[t2].real(), n_t));
    }

    writeBin(cshlist[i], n_t, effmass);
  }
}
