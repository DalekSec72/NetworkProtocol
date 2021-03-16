// headers
#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

// Close with signal
void closesock (int sig);

// Socket descriptor
int sock_listen; // listen socket
int sock_client; // client socket

int main()
{
	int mode;
	char buff[256]; // send_recv buffer
	int count;
	
	struct sockaddr_in addr;
	struct sigaction act;

	act.sa_handler = closesock;
	sigfillset (&(act.sa_mask));
	sigaction (SIGINT, &act, NULL);

	
	printf("1. Server, 2. Client: ");
	scanf("%d", &mode);
		
	if (mode == 1){ // Server Mode

		/* Server address setup (IPv4, 36007, INADDR_ANY) */
		// here

	
		/* Create listen socket (IPv4, TCP) */
		// here
		

		/* Bind server address to listen socket */
		// here
		

		/* Start listening for client requests (Max 5 requests) */
		// here
		
		while (1) {

			/* Accept client request without saving client address */
			// here
			
			printf("Connection Established.\n");

			/* Receive a message from client */
			// here

			/* Send a message to client */
			// here
		}
	}
	else { // Client Mode
		/* Client address setup (IPv4, 36007, 127.0.0.1) */
		// here
		
		/* Create client socket (IPv4, TCP) */
		// here
		
		/* Connect to server */
		// here

		while (1) {

			// Prepare a message (static or user input)
			// here

			// Send a message to server
			// here


			/* Receive a message from server */
			// here
		}
	}

	close(sock_listen);
	close(sock_client);
	return 0;
}

void closesock (int sig)
{
	close(sock_listen);
	close(sock_client);
	printf ("connection lost\n");
	exit (1);
}
