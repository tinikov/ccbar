/**
 * @file misc.cc
 * @author TC (reeft137@gmail.com)
 * @brief
 * @version 1.0
 * @date 2023-05-03
 *
 */

#include "misc.h"

void add_prefix(const char *raw_name, const char *prefix, char *new_name)
{
  char stmp[1024], dir[1024], base[512], pre[512];

  strncpy(stmp, raw_name, 1023);
  strncpy(dir, dirname(stmp), 1023);

  strncpy(pre, prefix, 511);
  
  strncpy(stmp, raw_name, 1023);
  strncpy(base, basename(stmp), 511);

  snprintf(new_name, 2048, "%s/%s.%s", dir, pre, base);
}

void change_path(const char *raw_name, const char *new_dir, char *new_name)
{
  char stmp[1024], ndir[1024], base[1024];

  strncpy(ndir, new_dir, 1023);

  strncpy(stmp, raw_name, 1023);
  strncpy(base, basename(stmp), 1023);

  snprintf(new_name, 2048, "%s/%s", ndir, base);
}
