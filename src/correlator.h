/**
 * @file correlator.h
 * @author TC (reeft137@gmail.com)
 * @brief 
 * @version 1.0
 * @date 2023-05-03
 *
 */

#ifndef IS_INCLUDED_CORRELATOR_H
#define IS_INCLUDED_CORRELATOR_H

#include "type_alias.h"

// inline DOUBLE &CORR(DOUBLE *data, int x, int y, int z, int spacelength)
// {
//   x = (x + spacelength) % spacelength;
//   y = (y + spacelength) % spacelength;
//   z = (z + spacelength) % spacelength;
//   DOUBLE &corr_r = data[x + spacelength * (y + spacelength * z)];
//   return corr_r;
// }

inline COMPLX &CORR(COMPLX *data, int x, int y, int z, int spacelength)
{
  x = (x + spacelength) % spacelength;
  y = (y + spacelength) % spacelength;
  z = (z + spacelength) % spacelength;
  COMPLX &corr_r = data[x + spacelength * (y + spacelength * z)];
  return corr_r;
}

// inline DOUBLE &CORR(DVARRAY &data, int x, int y, int z, int spacelength)
// {
//   x = (x + spacelength) % spacelength;
//   y = (y + spacelength) % spacelength;
//   z = (z + spacelength) % spacelength;
//   DOUBLE &corr_r = data[x + spacelength * (y + spacelength * z)];
//   return corr_r;
// }

// inline COMPLX &CORR(CVARRAY &data, int x, int y, int z, int spacelength)
// {
//   x = (x + spacelength) % spacelength;
//   y = (y + spacelength) % spacelength;
//   z = (z + spacelength) % spacelength;
//   COMPLX &corr_r = data[x + spacelength * (y + spacelength * z)];
//   return corr_r;
// }

#endif
