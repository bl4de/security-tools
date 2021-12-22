/* fixgz attempts to fix a binary file transferred in ascii mode by
 * removing each extra CR when it followed by LF.
 * usage: fixgz  bad.gz fixed.gz

 * Copyright 1998 Jean-loup Gailly <jloup@gzip.org>
 *   This software is provided 'as-is', without any express or implied
 * warranty.  In no event will the author be held liable for any damages
 * arising from the use of this software.

 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely.
 */

#include <stdio.h>
#include <cstdlib>

int main(int argc, char* argv[])
{
    int c1, c2; /* input bytes */
    FILE* in;   /* corrupted input file */
    FILE* out;  /* fixed output file */

    if (argc <= 2) {
        fprintf(stderr, "usage: fixgz bad.gz fixed.gz\n");
        exit(1);
    }
    in = fopen(argv[1], "rb");
    if (in == NULL) {
        fprintf(stderr, "fixgz: cannot open %s\n", argv[1]);
        exit(1);
    }
    out = fopen(argv[2], "wb");
    if (in == NULL) {
        fprintf(stderr, "fixgz: cannot create %s\n", argv[2]);
        exit(1);
    }

    c1 = fgetc(in);

    while ((c2 = fgetc(in)) != EOF) {
        if (c1 != '\r' || c2 != '\n') {
            fputc(c1, out);
        }
        c1 = c2;
    }
    if (c1 != EOF) {
        fputc(c1, out);
    }
    exit(0);
    return 0; /* avoid warning */
}