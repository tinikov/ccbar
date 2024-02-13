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

#include "type_alias.h"

/**
 * @brief Read from binary file
 *
 * @param if_name Input file name of the data file
 * @param array_length Total of double/complex numbers
 * @param data The pointer of the array that contains the data read
 */
void readBin(const char *if_name, int array_length, DOUBLE *data);
void readBin(const char *if_name, int array_length, COMPLX *data);
void readBin(const char *if_name, int array_length, DVARRAY &data);
void readBin(const char *if_name, int array_length, CVARRAY &data);

/**
 * @brief Write to binary file
 *
 * @param of_name Output file name of the data file
 * @param array_length Total of double/complex numbers
 * @param data The pointer of the array that contains the data to be written to
 * file
 */
void writeBin(const char *of_name, int array_length, const DOUBLE *data);
void writeBin(const char *of_name, int array_length, const COMPLX *data);
void writeBin(const char *of_name, int array_length, const DVARRAY &data);
void writeBin(const char *of_name, int array_length, const CVARRAY &data);

/**
 * @brief Convert binary file to txt file (only for complex (2-lined) data)
 *
 * @param bin_fname File name of the binary file
 * @param txt_fname File name of the txt file
 * @param array_length Total of complex numbers
 */
void bin2txt(const char *bin_fname, const char *txt_fname, int array_length);

/**
 * @brief Keep the real part of the data
 *
 * @param data original data (complex valarray)
 * @param realdata real part of the valarray (double valarray)
 * @param array_length Total of complex numbers
 */
void keepReal(CVARRAY &data, DVARRAY &realdata, int array_length);

/**
 * @brief Keep the imaginary part of the data
 *
 * @param data original data (complex valarray)
 * @param imagdata imaginary part of the valarray (double valarray)
 * @param array_length Total of complex numbers
 */
void keepImag(CVARRAY &data, DVARRAY &imagdata, int array_length);

/**
 * @brief Calculate the norm of the complex data
 *
 * @param data original data (complex valarray)
 * @param normdata norm of the valarray (double valarray)
 * @param array_length Total of complex numbers
 */
void varryNorm(CVARRAY &data, DVARRAY &normdata, int array_length);
#endif
