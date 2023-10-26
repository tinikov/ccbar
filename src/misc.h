/**
 * @file misc.h
 * @author TC (reeft137@gmail.com)
 * @brief misc = miscellaneous
 *        Provides 2 functions:
 *        void add_prefix(): Add prefix to a file name;
 *        void change_path(): Change the directory part for a file name.
 * @version 1.0
 * @date 2023-05-03
 *
 */

#ifndef IS_INCLUDED_MISC_H
#define IS_INCLUDED_MISC_H

#include <libgen.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * @brief Add prefix to a file name (preserving the original path)
 *
 * @param raw_name The original file name: "dir/FILENAME"
 * @param prefix The prefix to be added: "PREFIX"
 * @param new_name The desired file name: "dir/PREFIX.FILENAME"
 */
void add_prefix(const char *raw_name, const char *prefix, char *new_name);

/**
 * @brief Change the directory part for a file name
 *
 * @param raw_name The original file name: "dir/FILENAME"
 * @param new_dir Target directory: "newdir"
 * @param new_name The character string generated: "newdir/FILENAME"
 */
void change_path(const char *raw_name, const char *new_dir, char *new_name);

#endif
