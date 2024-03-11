/**
 * @file correlator.h
 * @author Tianchen Zhang
 * @brief
 * @version 1.1
 * @date 2024-02-13
 *
 */

#ifndef IS_INCLUDED_CORRELATOR_H
#define IS_INCLUDED_CORRELATOR_H

#include "alias.h"

inline DOUBLE&
CORR(DOUBLE* data, int x, int y, int z, int xyzSize)
{
  x = (x + xyzSize) % xyzSize;
  y = (y + xyzSize) % xyzSize;
  z = (z + xyzSize) % xyzSize;
  DOUBLE& corrReturn = data[x + xyzSize * (y + xyzSize * z)];
  return corrReturn;
}

inline COMPLX&
CORR(COMPLX* data, int x, int y, int z, int xyzSize)
{
  x = (x + xyzSize) % xyzSize;
  y = (y + xyzSize) % xyzSize;
  z = (z + xyzSize) % xyzSize;
  COMPLX& corrReturn = data[x + xyzSize * (y + xyzSize * z)];
  return corrReturn;
}

inline DOUBLE&
CORR(DVARRAY& data, int x, int y, int z, int xyzSize)
{
  x = (x + xyzSize) % xyzSize;
  y = (y + xyzSize) % xyzSize;
  z = (z + xyzSize) % xyzSize;
  DOUBLE& corrReturn = data[x + xyzSize * (y + xyzSize * z)];
  return corrReturn;
}

inline COMPLX&
CORR(CVARRAY& data, int x, int y, int z, int xyzSize)
{
  x = (x + xyzSize) % xyzSize;
  y = (y + xyzSize) % xyzSize;
  z = (z + xyzSize) % xyzSize;
  COMPLX& corrReturn = data[x + xyzSize * (y + xyzSize * z)];
  return corrReturn;
}

#endif
