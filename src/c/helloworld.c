

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define NEL(x) ((sizeof((x))/sizeof((x)[0])))

int main()
{
  printf("Hello World -- this is MicroZed!\n");
  int sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
  if (sockfd==-1) {
	  perror("socket");
	  exit(1);
  }
  struct sockaddr_in srvaddr;
  memset(&srvaddr, 0, sizeof(srvaddr));
  srvaddr.sin_family = AF_INET;
  srvaddr.sin_addr.s_addr = htonl(INADDR_ANY);
  srvaddr.sin_port = htons(31416);
  int rc = bind(sockfd, &srvaddr, sizeof(srvaddr));
  if (rc==-1) {
	  perror("bind");
	  exit(1);
  }
  int count = 0;
  printf("listening on UDP port %d\n", ntohs(srvaddr.sin_port));
  while (1) {
	  struct sockaddr_in cliaddr;
	  memset(&cliaddr, 0, sizeof(cliaddr));
	  int clen = sizeof(cliaddr);
	  char recvbuf[1024];
	  memset(recvbuf, 0, sizeof(recvbuf));
	  rc = recvfrom(sockfd, recvbuf, sizeof(recvbuf), 0, &cliaddr, &clen);
	  if (rc==-1) {
		  perror("recvfrom");
		  exit(1);
	  }
	  count++;
	  printf("received datagram from %s:%d (rc=%d, count=%d)\n",
			  inet_ntoa(cliaddr.sin_addr),
			  ntohs(cliaddr.sin_port), rc, count);
	  recvbuf[NEL(recvbuf)-1] = 0;  // temporary: ensure recvbuf is a null-terminated string
	  printf("content: %s\n", recvbuf);
	  char sendbuf[NEL(recvbuf)];
	  memset(sendbuf, 0, sizeof(sendbuf));
	  sprintf(sendbuf, "ok: count=%d", count);
	  sendto(sockfd, sendbuf, sizeof(sendbuf), 0, &cliaddr, sizeof(cliaddr));
  }
  close(sockfd);
  return 0;
}
