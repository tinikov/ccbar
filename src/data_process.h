/**
 * @file data_process.h
 * @author TC (reeft137@gmail.com)
 * @brief Dealing with data (binary and txt files).
 *        Provide 5 functions:
 *        void read_bin(): Read data from binary file;
 *        void write_bin(): Write data to binary file;
 *        void bin2txt(): Convert binary file to txt file;
 *        void keep_real(): Keep the real part of the data;
 *        void keep_imag(): Keep the imaginary part of the data.
 * @version 1.0
 * @date 2023-05-03
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
void read_bin(const char *if_name, int array_length, DOUBLE *data);
void read_bin(const char *if_name, int array_length, COMPLX *data);
void read_bin(const char *if_name, int array_length, DVARRAY &data);
void read_bin(const char *if_name, int array_length, CVARRAY &data);

/**
 * @brief Write to binary file
 *
 * @param of_name Output file name of the data file
 * @param array_length Total of double/complex numbers
 * @param data The pointer of the array that contains the data to be written to
 * file
 */
void write_bin(const char *of_name, int array_length, const DOUBLE *data);
void write_bin(const char *of_name, int array_length, const COMPLX *data);
void write_bin(const char *of_name, int array_length, const DVARRAY &data);
void write_bin(const char *of_name, int array_length, const CVARRAY &data);

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
 * @param rdata real part of the valarray (double valarray)
 * @param array_length
 */
void keep_real(CVARRAY &data, DVARRAY &realdata, int array_length);

/**
 * @brief Keep the imaginary part of the data
 *
 * @param data original data (complex valarray)
 * @param rdata imaginary part of the valarray (double valarray)
 * @param array_length
 */
void keep_imag(CVARRAY &data, DVARRAY &imagdata, int array_length);

#endif
