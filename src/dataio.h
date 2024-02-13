/**
 * @file dataio.h
 * @author Tianchen Zhang
 * @brief Dealing with data (binary and txt files).
 *        Provide 5 functions:
 *        void readBin(): Read data from binary file;
 *        void writeBin(): Write data to binary file;
 *        void bin2txt(): Convert binary file to txt file;
 *        void keepReal(): Keep the real part of the data;
 *        void keepImag(): Keep the imaginary part of the data.
 * @version 1.1
 * @date 2024-02-13
 *
 */

#ifndef IS_INCLUDED_DATAIO_H
#define IS_INCLUDED_DATAIO_H

#include "alias.h"

/**
 * @brief Read from binary file
 *
 * @param ifname Input file name of the data file
 * @param arrayLength Total of double/complex numbers
 * @param data The pointer of the array that contains the data to be read
 */
void readBin(const char *ifname, int arrayLength, DOUBLE *data);
void readBin(const char *ifname, int arrayLength, COMPLX *data);
void readBin(const char *ifname, int arrayLength, DVARRAY &data);
void readBin(const char *ifname, int arrayLength, CVARRAY &data);

/**
 * @brief Write to binary file
 *
 * @param ofname Output file name of the data file
 * @param arrayLength Total of double/complex numbers
 * @param data The pointer of the array that contains the data to be written to
 * file
 */
void writeBin(const char *ofname, int arrayLength, const DOUBLE *data);
void writeBin(const char *ofname, int arrayLength, const COMPLX *data);
void writeBin(const char *ofname, int arrayLength, const DVARRAY &data);
void writeBin(const char *ofname, int arrayLength, const CVARRAY &data);

/**
 * @brief Convert binary file to txt file (only for complex (2-lined) data)
 *
 * @param binfame File name of the binary file
 * @param txt_fname File name of the txt file
 * @param arrayLength Total of complex numbers
 */
void bin2txt(const char *binName, const char *txt_fname, int arrayLength);

/**
 * @brief Keep the real part of the data
 *
 * @param data original data (complex valarray)
 * @param realdata real part of the valarray (double valarray)
 * @param arrayLength Total of complex numbers
 */
void keepReal(CVARRAY &data, DVARRAY &realdata, int arrayLength);

/**
 * @brief Keep the imaginary part of the data
 *
 * @param data original data (complex valarray)
 * @param imagdata imaginary part of the valarray (double valarray)
 * @param arrayLength Total of complex numbers
 */
void keepImag(CVARRAY &data, DVARRAY &imagdata, int arrayLength);

/**
 * @brief Calculate the norm of the complex data
 *
 * @param data original data (complex valarray)
 * @param normdata norm of the valarray (double valarray)
 * @param arrayLength Total of complex numbers
 */
void varryNorm(CVARRAY &data, DVARRAY &normdata, int arrayLength);
#endif
