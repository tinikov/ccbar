/**
 * @file effmass.cc
 * @author TC (reeft137@gmail.com)
 * @brief Effective masses for charmonium
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
  fprintf(stderr, "Effective masses for charmonium (ofname: exp.xxx and csh.xxx)\n");
  fprintf(stderr, "USAGE: \n"
                  "    %s [OPTIONS] ifname1 [ifname2 ...]\n",
          name);
  fprintf(stderr, "OPTIONS: \n"
                  "    -l <TSITES>:      Temporal length\n"
                  "    -d <OFDIR>:       Directory of output files\n"
                  "    [-t]:             Also save a txt file (add \"txt.\" prefix)\n"
                  "    [-h, --help]:     Print help\n");
}
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Custom functions    |
//     |________________________|

void exp_mass(char *rawdlist[], char *explist[], int T_length, int N_df);
void csh_mass(char *rawdlist[], char *cshlist[], int T_length, int N_df);
// __________________________________
//     .________|______|________.
//     |                        |
//     |    Global Variables    |
//     |________________________|

int T_length = 0;
static const char *ofdir = NULL;
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

    // -l: T_length
    if (strcmp(argv[0], "-l") == 0)
    {
      T_length = atoi(argv[1]); // atoi(): convert ASCII string to integer
      if (!T_length)
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
  if (T_length == 0 || ofdir == NULL)
  {
    usage(program_name);
    exit(1);
  }

  // Initialization
  const int N_df = argc; // # of data files
  fprintf(stderr, "##  Effective mass! \n");
  fprintf(stderr, "##  Total of data files: %d\n", N_df);
  fprintf(stderr, "##  Temporal length:     %d\n", T_length);

  // Create an arrary to store ofnames
  char *exp_dlist[N_df], *csh_dlist[N_df];

  for (int i = 0; i < N_df; i++)
  {
    char stmp[2048];

    exp_dlist[i] = (char *)malloc(2048 * sizeof(char));
    add_prefix(argv[i], "exp", stmp);
    change_path(stmp, ofdir, exp_dlist[i]);

    csh_dlist[i] = (char *)malloc(2048 * sizeof(char));
    add_prefix(argv[i], "csh", stmp);
    change_path(stmp, ofdir, csh_dlist[i]);
  }

  // Main part for calculation
  exp_mass(argv, exp_dlist, T_length, N_df);
  csh_mass(argv, csh_dlist, T_length, N_df);

  if (is_save_txt)
  {
    for (int i = 0; i < N_df; i++)
    {
      char txttmp[2048];

      add_prefix(exp_dlist[i], "txt", txttmp);
      bin2txt(exp_dlist[i], txttmp, T_length);

      add_prefix(csh_dlist[i], "txt", txttmp);
      bin2txt(csh_dlist[i], txttmp, T_length);
    }
  }

  // Finalization for the string arrays
  for (int i = 0; i < N_df; i++)
  {
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

void exp_mass(char *rawdlist[], char *explist[], int T_length, int N_df)
{
#pragma omp parallel for
  for (int i = 0; i < N_df; i++)
  {
    COMPLX raw[T_length], effmass[T_length];
#pragma omp parallel for
    for (int j = 0; j < T_length; j++)
    {
      raw[j] = 0.0;
      effmass[j] = 0.0;
    }
    read_bin(rawdlist[i], T_length, raw);

#pragma omp parallel for
    for (int j = 0; j < T_length; j++)
    {
      effmass[j].real(log(raw[j].real() / raw[(j + 1) % T_length].real()));
    }

    write_bin(explist[i], T_length, effmass);
  }
}

DOUBLE coshtype_mass(int t1, int t2, DOUBLE corr1, DOUBLE corr2, int T_length)
{
#define JMAX 100
#define M0 0.001
#define M1 10.0
#define MACC 1.0e-12
#define coshtype(m) (corr1 / corr2 - cosh((m) * (T_length / 2.0 - t1)) / cosh((m) * (T_length / 2.0 - t2)))

  DOUBLE dm, f, fmid, mmid, mass;

  f = coshtype(M0);
  fmid = coshtype(M1);
  if (f * fmid >= 0.0)
  {
    fprintf(stderr, "Root must be bracketed for bisection in RTBIS\n");
    return NAN;
  }
  mass = f < 0.0 ? (dm = M1 - M0, M0) : (dm = M0 - M1, M1);
  for (int j = 1; j <= JMAX; j++)
  {
    mmid = mass + (dm *= 0.5);
    fmid = coshtype(mmid);
    if (fmid <= 0.0)
      mass = mmid;
    if (fabs(dm) < MACC || fmid == 0.0)
      return mass;
  }
  fprintf(stderr, "Too many bisections in RTBIS");
  return 0.0;
}

void csh_mass(char *rawdlist[], char *cshlist[], int T_length, int N_df)
{
#pragma omp parallel for
  for (int i = 0; i < N_df; i++)
  {
    COMPLX raw[T_length], effmass[T_length];
#pragma omp parallel for
    for (int j = 0; j < T_length; j++)
    {
      raw[j] = 0.0;
      effmass[j] = 0.0;
    }
    read_bin(rawdlist[i], T_length, raw);

#pragma omp parallel for
    for (int j = 0; j < T_length; j++)
    {
      int t1 = j;
      int t2 = (j + 1) % T_length;
      effmass[j].real(coshtype_mass(t1, t2, raw[t1].real(), raw[t2].real(), T_length));
    }

    write_bin(cshlist[i], T_length, effmass);
  }
}