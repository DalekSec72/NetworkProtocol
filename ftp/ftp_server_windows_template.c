#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <WinSock2.h>
#include <process.h>

#pragma warning(disable:4996)
#pragma comment(lib, "ws2_32.lib")

SOCKET listen_sock, clnt_sock[10], data_sock[10];
int control_port = 36007;
int data_port;
char *username = "np2019";
char *password = "np2019";

void recvThread(void *arg);
int LastIndexof(char *str, char c);
void closedatasocket(int idx);

enum {
	NOTLOGGEDIN,
	NEEDPASSWORD,
	LOGGEDIN
};

int main() {
	int count = 0;
	WSADATA wsaData;
	HANDLE th_recv[10];
	data_port = control_port;

	struct sockaddr_in addr;

	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
		printf("WSA Start Failed\n");
		return 0;
	}

	// 주소 설정 36007

	// 소켓 생성 TCP IPv4

	// 주소 바인딩

	// listen

	while (1) {
		// accept and create client thread
	}

	closesocket(listen_sock);
	WSACleanup();
}

void recvThread(void *arg) {
	int connected = 1;
	int idx = *((int*)arg);

	// get current working folder or directory

	// send 220 message

	// receive command
	while (connected) {

		// 데이터 수신 및 command 처리
		// USER, PASS, CWD, NLST, QUIT, PASV, RETR, TYPE
		// while recv:
		//	commands:
		//		USER: username 비교, PASS 전송
		//		PASS: password 비교
		//		CWD: 폴더 or 디렉토리 변경, 현재 작업 디렉토리 필요 
		//		QUIT: control 소켓 종료
		//		PASV: data 소켓 생성, client에게 data 소켓 정보 전달
		//		RETR: file 읽기, 데이터 전송
		//		TYPE: 파일 읽기 방법 변경
	}
	closesocket(clnt_sock[idx]);
}

int LastIndexof(char *str, char c)
{
	int i, idx = -1;
	for (i = 0; i < strlen(str); i++)
	{
		if (str[i] == c)
			idx = i;
	}

	return idx;
}
void closedatasocket(int idx) {
	closesocket(data_sock[idx]);
	data_sock[idx] = NULL;
}
