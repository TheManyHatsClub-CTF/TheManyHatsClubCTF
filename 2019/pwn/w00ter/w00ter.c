#include <stdio.h>
#include <netdb.h>
#include <time.h>
#include <unistd.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>


#define MAX 80
#define MAX_TIME 10
#define PORT 1337
#define SA struct sockaddr



void gadgets() {
    __asm__(
        "pop %rax\n\tpop %rsi\n\tret\n\tpop %rdi\n\tpop %rdx\n\tpop %rbx\n\tret\n\t"
        "mov %rbx, (%rdi)\n\tret\n\tsyscall\n\tret\n\t"
    );
}

void test_func(int sockfd) {

    char output[512] = {'\0'};
    snprintf(output, sizeof(output), "Dump of %p\n", (gadgets+2));
    send(sockfd, output, strlen(output), 0);
    send(sockfd, (unsigned char *)(gadgets+2), 19, 0);

}

void getUsername(char *username_buf) {
    struct stat st;
    stat("./.score", &st);
    int total = st.st_size;

    int fd = open("./.score", O_RDONLY);
    read(fd, username_buf, total);
    close(fd);
}

void checkBestScore(int sockfd) {
    int fd;
    char buf[64] = {'\0'};
    getUsername(buf);

    int len=0;
    char *pos = buf;

    while (*(pos++) != '\0') {
        len++;
    }

    send(sockfd, "The best player is ", 19, 0);
    send(sockfd, buf, len, 0);
    send(sockfd, "\n", 1, 0);

}

void check_win(int sockfd, unsigned int pts) {

    char buf[512] = {'\0'};
    char output[1024];

    if (pts > 10) {
        send(sockfd, "We have a new winer!\n", 21, 0);
        send(sockfd, "Please enter your name: ", 24, 0);
        int length = recv(sockfd, buf, sizeof(buf), 0);
        snprintf(output, sizeof(output), "Congratz %s, you're our new champion!\nYou're now the best player\0", buf);
        send(sockfd, output, strlen(output), 0);
        int fd = open("./.score", O_WRONLY | O_TRUNC);
        write(fd, buf, length);
        close(fd);
    }

}

int eq(int sockfd) {

    int result = 0;

    int left = rand() % 10;
    int right = rand() % 10;
    int op = rand() % 4;
    char str[64];
    char ans[64] = {'\0'};

    switch (op) { // ADD
        case 0:
            result = left+right;
            snprintf(str, sizeof(str),"%d%c%d ?\n\0", left, '+', right);
            break;
        case 1:
            result = left-right;
            snprintf(str, sizeof(str),"%d%c%d ?\n\0", left, '-', right);
            break;
        case 2:
            result = left*right;
            snprintf(str, sizeof(str),"%d%c%d ?\n\0", left, '*', right);
            break;
        case 3:
            while (right == 0)
                right = rand() % 10;

            result = left/right;
            snprintf(str, sizeof(str), "%d%c%d ?\n\0", left, '/', right);
            break;
        default:
            result=0;
    }
    send(sockfd, str, strlen(str), 0);

    recv(sockfd, ans, sizeof(ans), 0);
    int ansint = atoi(ans);


    return ansint == result;

}

void play(int sockfd) {

    time_t t0 = time(NULL);
    unsigned int pts = 0;

    send(sockfd, "Ready...\n", 9, 0);
    //sleep(1);
    send(sockfd, "Set...\n", 7, 0);
    //sleep(1);
    send(sockfd, "Go!\n", 4, 0);

    for (;;) {
        if (eq(sockfd)) {
            send(sockfd, "Good job!\n", 10, 0);
            pts += 1;
        } else {
            send(sockfd, "Failed!\n", 8, 0);
            pts += 1;
        }

        if ((time(NULL) - t0) >= MAX_TIME)
            break;
    }

    send(sockfd, "Bzzzzz! It's over!\n", 19, 0);

    char ptsstr[64];
    snprintf(ptsstr, sizeof(ptsstr), "You managed to get %d points.\n\0", pts);
    send(sockfd, ptsstr, strlen(ptsstr), 0);

    check_win(sockfd, pts);

}

void debug(int sockfd) {

    char output[512] = {'\0'};
    snprintf(output, sizeof(output), "the test func is at %p\n", test_func);
    send(sockfd, output, strlen(output), 0);

}

void worker(int sockfd) {

    char buff[2];
    char answer = '\0';


    char intro[] = "Welcome, dear friend, to the w00ter!\n\n";
    char menu[] = "-- MAIN MENU --\n\n1. Check best score\n2. Play!\n3. Debug [To be removed in prod!]\n\n";

    send(sockfd, intro, sizeof(intro), 0);

    for(;;) {

        buff[0] = '\0';
        send(sockfd, menu, sizeof(menu), 0);
        recv(sockfd, buff, sizeof(buff), 0);
        answer = buff[0];

        if (answer == '1')
            checkBestScore(sockfd);
        else if (answer == '2')
            play(sockfd);
        else if (answer == '3')
            debug(sockfd);
        else
            break;
    }

    close(sockfd);
}

int main()
{
    int sockfd, connfd, len;
    int opt = 1;
    struct sockaddr_in servaddr, cli;

    srand(time(NULL));

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("socket creation failed...\n");
        exit(0);
    }

    if ( setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
        &opt, sizeof(opt)) ) {
        printf("setsockopt failed...\n");
        exit(0);
    }

    bzero(&servaddr, sizeof(servaddr));

    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(PORT);

    if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) {
        printf("socket bind failed...\n");
        exit(0);
    }

    if ((listen(sockfd, 50)) != 0) {
        printf("Listen failed...\n");
        exit(0);
    }
    len = sizeof(cli);

    printf("[+] Server started on port %d\n", PORT);

    for (;;) {
        connfd = accept(sockfd, (SA*)&cli, &len);
        if (connfd < 0) {
            printf("server acccept failed...\n");
            exit(0);
        }

        printf("[*] Client %d connected!\n", connfd);

        if (!fork())
            worker(connfd);

        close(connfd);

    }
}
