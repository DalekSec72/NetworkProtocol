# NetworkProtocol
4-1 Network Protocol class practice

1. echo server
  TCP 통신을 이용하여 클라이언트가 서버에 메시지를 전송하면 서버가 그대로 돌려주는 기능 구현.
  
2. TCP chat server/client
  TCP 소켓 프로그래밍으로 한 서버에 다중 클라이언트가 접속하여 서로 메시지를 보내고 받을 수 있는 기능 구현.
  
  멀티 스레드 구현으로 서버 송/수신 스레드를 각각 생성하도록 구현.
  
3. FTP server/client
  FTP(File Transfer Protocol)를 이용한 파일 전송 서버/클라이언트 구현.
  
  다양한 FTP 명령어와 응답코드를 구현하여 소켓을 통해 FTP 통신.

4. Pub/Sub Middleware
  토픽 기반 pub/sub 방식을 통한 데이터 송수신 구현.

  publisher, subscriber 역할을 수행하는 client와 중간에서 요청을 처리하는 broker 구현.
