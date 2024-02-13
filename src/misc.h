/**
 * @file misc.h
 * @author Tianchen Zhang 
 * @brief misc = miscellaneous
 *        Provides 2 functions:
 *        void addPrefix(): Add prefix to a file name;
 *        void changePath(): Change the directory part for a file path.
 * @version 1.1
 * @date 2024-02-01
 *
 */

#ifndef IS_INCLUDED_MISC_H
#define IS_INCLUDED_MISC_H

#include <libgen.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * @brief Add prefix to a file (preserving the original path)
 *
 * @param origPath The original path: "dir/filename"
 * @param prefix The prefix to be added: "prefix"
 * @param newPath The desired file name: "dir/prefix.filename"
 */
void addPrefix(const char *origPath, const char *prefix, char *newPath);

/**
 * @brief Change the directory part for a file name
 *
 * @param origPath The original path: "dir/filename"
 * @param tarDir Target directory: "tarDir"
 * @param newPath The character string generated: "tarDir/filename"
 */
void changePath(const char *origPath, const char *tarDir, char *newPath);

#endif
