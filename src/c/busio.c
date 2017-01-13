/*
 * peek_poke.c
 * Attempt to R/W arbitrary MicroZed memory from Linux command line
 * wja 2014-12-17
 */

#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include <sys/mman.h>

typedef unsigned long u32;

int busio(int argc, char **argv)
{
  int i = 0, rc = 0;
  int wr = 0;
  assert(argc>1);   // need command + at least 1 argument
  u32 addr = 0, data = 0;
  rc = sscanf(argv[1], "%x", &addr);
  assert(rc==1);
  if (!strcmp(argv[0], "rd")) {
    wr = 0;
  } else if (!strcmp(argv[0], "wr")) {
    wr = 1;
    assert(argc>2);
    rc = sscanf(argv[2], "%x", &data);
    assert(rc==1);
  } else {
    fprintf(stderr, "busio: unknown command '%s'\n", argv[0]);
    return 1;
  }
  // Xilinx uses u32, while mmap uses size_t
  assert(sizeof(u32)==sizeof(size_t));
  // It seems that mmap wants base address to lie on a page boundary
  u32 base = 0x43c00000;
  // Map 4096 bytes (which is presumably a page or power-of-two pages)
  u32 mlen = 0x00001000;
  int memfd = 0;
  void *mapped_base = 0;
  memfd = open("/dev/mem", O_RDWR | O_SYNC);
  assert(memfd != -1);
  mapped_base = mmap(0, mlen,
		     PROT_READ|PROT_WRITE, MAP_SHARED,
		     memfd, base);
  assert(mapped_base != MAP_FAILED);
  size_t *r = (size_t *) mapped_base;
  if (wr) {
    // "bus" write operation
    r[2] = 0;                        // all PS strobes should already be 0
    assert((r[3] & 1)==0);           // PL strobe should already be 0
    r[1] = ((data & 0xffff) << 16) | (addr & 0xffff);
    r[2] = 2;                        // raise PS write strobe
    assert(r[3] & 1);                // PL strobe should be 1 now
    r[2] = 0;                        // lower PS write strobe
    printf("busio: wr %04x := %04x\n", r[5] & 0xffff, r[4] & 0xffff);
  } else {
    // "bus" read operation
    r[2] = 0;                        // all PS strobes should already be 0
    assert((r[3] & 1)==0);           // PL strobe should already be 0
    r[1] = addr & 0xffff;
    r[2] = 1;                        // raise PS read strobe
    assert(r[3] & 1);                // PL strobe should be 1 now
    data = r[4] & 0xffff;            // latch in data from read cycle
    r[2] = 0;                        // lower PS read strobe
    printf("busio: rd %04x ==> %04x\n", r[5] & 0xffff, data);
  }
  return 0;
}
