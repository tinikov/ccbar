/**
 * @file dataio.cc
 * @author Tianchen Zhang
 * @brief
 * @version 1.1
 * @date 2024-02-13
 *
 */

#include "dataio.h"

void readBin(const char *ifname, int array_length, DOUBLE *data) {
  FILE *fp = fopen(ifname, "rb");
  if (fp == NULL) {
    perror(ifname);
    exit(1);
  }

  fread(data, sizeof(DOUBLE), array_length, fp);
  fclose(fp);
}
void readBin(const char *ifname, int array_length, COMPLX *data) {
  FILE *fp = fopen(ifname, "rb");
  if (fp == NULL) {
    perror(ifname);
    exit(1);
  }

  fread(data, sizeof(COMPLX), array_length, fp);
  fclose(fp);
}
void readBin(const char *ifname, int array_length, DVARRAY &data) {
  FILE *fp = fopen(ifname, "rb");
  if (fp == NULL) {
    perror(ifname);
    exit(1);
  }

  fread(&data[0], sizeof(DOUBLE), array_length, fp);
  fclose(fp);
}
void readBin(const char *ifname, int array_length, CVARRAY &data) {
  FILE *fp = fopen(ifname, "rb");
  if (fp == NULL) {
    perror(ifname);
    exit(1);
  }

  fread(&data[0], sizeof(COMPLX), array_length, fp);
  fclose(fp);
}

void writeBin(const char *of_name, int array_length, const DOUBLE *data) {
  FILE *fp = fopen(of_name, "wb");
  if (fp == NULL) {
    perror(of_name);
    exit(1);
  }

  fwrite(data, sizeof(DOUBLE), array_length, fp);
  fclose(fp);
}
void writeBin(const char *of_name, int array_length, const COMPLX *data) {
  FILE *fp = fopen(of_name, "wb");
  if (fp == NULL) {
    perror(of_name);
    exit(1);
  }

  fwrite(data, sizeof(COMPLX), array_length, fp);
  fclose(fp);
}
void writeBin(const char *of_name, int array_length, const DVARRAY &data) {
  FILE *fp = fopen(of_name, "wb");
  if (fp == NULL) {
    perror(of_name);
    exit(1);
  }

  fwrite(&data[0], sizeof(DOUBLE), array_length, fp);
  fclose(fp);
}
void writeBin(const char *of_name, int array_length, const CVARRAY &data) {
  FILE *fp = fopen(of_name, "wb");
  if (fp == NULL) {
    perror(of_name);
    exit(1);
  }

  fwrite(&data[0], sizeof(COMPLX), array_length, fp);
  fclose(fp);
}

void bin2txt(const char *bin_fname, const char *txt_fname, int array_length) {
  COMPLX data[array_length];
  for (int i = 0; i < array_length; i++) {
    data[i] = 0.0;
  }

  FILE *ifp = fopen(bin_fname, "rb");
  if (ifp == NULL) {
    perror(bin_fname);
    exit(1);
  }

  fread(data, sizeof(COMPLX), array_length, ifp);
  fclose(ifp);

  FILE *ofp = fopen(txt_fname, "w");
  if (ofp == NULL) {
    perror(txt_fname);
    exit(1);
  }

  for (int i = 0; i < array_length; i++) {
    fprintf(ofp, "%d %1.16e %1.16e\n", i, data[i].real(), data[i].imag());
  }
  fclose(ofp);
}

void keepReal(CVARRAY &data, DVARRAY &realdata, int array_length) {
  for (int i = 0; i < array_length; i++) {
    realdata[i] = data[i].real();
  }
}

void keepImag(CVARRAY &data, DVARRAY &imagdata, int array_length) {
  for (int i = 0; i < array_length; i++) {
    imagdata[i] = data[i].imag();
  }
}

void varryNorm(CVARRAY &data, DVARRAY &normdata, int array_length) {
  for (int i = 0; i < array_length; i++) {
    normdata[i] = sqrt(norm(data[i]));
  }
}
