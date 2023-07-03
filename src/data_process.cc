/**
 * @file data_process.cc
 * @author TC (reeft137@gmail.com)
 * @brief
 * @version 1.0
 * @date 2023-05-03
 *
 */

#include "data_process.h"

void read_bin(const char *ifname, int array_length, DOUBLE *data)
{
  FILE *fp = fopen(ifname, "rb");
  if (fp == NULL)
  {
    perror(ifname);
    exit(1);
  }

  fread(data, sizeof(DOUBLE), array_length, fp);
  fclose(fp);
}
void read_bin(const char *ifname, int array_length, COMPLX *data)
{
  FILE *fp = fopen(ifname, "rb");
  if (fp == NULL)
  {
    perror(ifname);
    exit(1);
  }

  fread(data, sizeof(COMPLX), array_length, fp);
  fclose(fp);
}
void read_bin(const char *ifname, int array_length, DVARRAY &data)
{
  FILE *fp = fopen(ifname, "rb");
  if (fp == NULL)
  {
    perror(ifname);
    exit(1);
  }

  fread(&data[0], sizeof(DOUBLE), array_length, fp);
  fclose(fp);
}
void read_bin(const char *ifname, int array_length, CVARRAY &data)
{
  FILE *fp = fopen(ifname, "rb");
  if (fp == NULL)
  {
    perror(ifname);
    exit(1);
  }

  fread(&data[0], sizeof(COMPLX), array_length, fp);
  fclose(fp);
}

void write_bin(const char *ofname, int array_length, const DOUBLE *data)
{
  FILE *fp = fopen(ofname, "wb");
  if (fp == NULL)
  {
    perror(ofname);
    exit(1);
  }

  fwrite(data, sizeof(DOUBLE), array_length, fp);
  fclose(fp);
}
void write_bin(const char *ofname, int array_length, const COMPLX *data)
{
  FILE *fp = fopen(ofname, "wb");
  if (fp == NULL)
  {
    perror(ofname);
    exit(1);
  }

  fwrite(data, sizeof(COMPLX), array_length, fp);
  fclose(fp);
}
void write_bin(const char *ofname, int array_length, const DVARRAY &data)
{
  FILE *fp = fopen(ofname, "wb");
  if (fp == NULL)
  {
    perror(ofname);
    exit(1);
  }

  fwrite(&data[0], sizeof(DOUBLE), array_length, fp);
  fclose(fp);
}
void write_bin(const char *ofname, int array_length, const CVARRAY &data)
{
  FILE *fp = fopen(ofname, "wb");
  if (fp == NULL)
  {
    perror(ofname);
    exit(1);
  }

  fwrite(&data[0], sizeof(COMPLX), array_length, fp);
  fclose(fp);
}

void bin2txt(const char *bin_fname, const char *txt_fname, int array_length)
{
  COMPLX data[array_length];
#pragma omp parallel for
  for (int i = 0; i < array_length; i++)
  {
    data[i] = 0.0;
  }

  FILE *ifp = fopen(bin_fname, "rb");
  if (ifp == NULL)
  {
    perror(bin_fname);
    exit(1);
  }

  fread(data, sizeof(COMPLX), array_length, ifp);
  fclose(ifp);

  FILE *ofp = fopen(txt_fname, "w");
  if (ofp == NULL)
  {
    perror(txt_fname);
    exit(1);
  }

  for (int i = 0; i < array_length; i++)
  {
    fprintf(ofp, "%d %1.16e %1.16e\n", i, data[i].real(), data[i].imag());
  }
  fclose(ofp);
}

void keep_real(CVARRAY &data, DVARRAY &realdata, int array_length)
{
#pragma omp parallel for
  for (int i = 0; i < array_length; i++)
  {
    realdata[i] = data[i].real();
  }
}

void keep_imag(CVARRAY &data, DVARRAY &imagdata, int array_length)
{
#pragma omp parallel for
  for (int i = 0; i < array_length; i++)
  {
    imagdata[i] = data[i].imag();
  }
}
