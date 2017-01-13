/*
 * util.c
 * MicroZed Linux application to collect together misc utilities
 * begun 2014-12-17 by wja
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// external function prototypes
int dumb_gpio(int argc, char **argv);

int main(int argc, char **argv)
{
  int rc = 0;  // return status code
  if (0) printf("util.c starting: argc=%d\n", argc);
  if (argc>1) {
    // if command-line argument is present, treat first argument as command
    char *cmd = argv[1];
    if (!strcmp(cmd, "dumb")) {
      rc = dumb_gpio(argc-1, argv+1);
    } else if (!strcmp(cmd, "peek") || !strcmp(cmd, "poke")) {
      rc = peek_poke(argc-1, argv+1);
    } else if (!strcmp(cmd, "rd") || !strcmp(cmd, "wr")) {
      rc = busio(argc-1, argv+1);
    } else {
      fprintf(stderr, "command '%s' unknown\n", cmd);
      rc = 1;
    }
  }
  if (0) printf("util.c done: rc=%d\n", rc);
  return rc;
}
