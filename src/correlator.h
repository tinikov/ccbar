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

// inline DOUBLE &CORR(DOUBLE *data, int x, int y, int z, int n_xyz)
// {
//   x = (x + n_xyz) % n_xyz;
//   y = (y + n_xyz) % n_xyz;
//   z = (z + n_xyz) % n_xyz;
//   DOUBLE &corr_r = data[x + n_xyz * (y + n_xyz * z)];
//   return corr_r;
// }

inline COMPLX &CORR(COMPLX *data, int x, int y, int z, int n_xyz)
{
  x = (x + n_xyz) % n_xyz;
  y = (y + n_xyz) % n_xyz;
  z = (z + n_xyz) % n_xyz;
  COMPLX &corr_r = data[x + n_xyz * (y + n_xyz * z)];
  return corr_r;
}

// inline DOUBLE &CORR(DVARRAY &data, int x, int y, int z, int n_xyz)
// {
//   x = (x + n_xyz) % n_xyz;
//   y = (y + n_xyz) % n_xyz;
//   z = (z + n_xyz) % n_xyz;
//   DOUBLE &corr_r = data[x + n_xyz * (y + n_xyz * z)];
//   return corr_r;
// }

// inline COMPLX &CORR(CVARRAY &data, int x, int y, int z, int n_xyz)
// {
//   x = (x + n_xyz) % n_xyz;
//   y = (y + n_xyz) % n_xyz;
//   z = (z + n_xyz) % n_xyz;
//   COMPLX &corr_r = data[x + n_xyz * (y + n_xyz * z)];
//   return corr_r;
// }

#endif
