#ifndef SD_LIB_H
#define SD_LIB_H

#include "fatfs.h"

void save_sd(int id, const char* value, const char* timestamp);

#endif
