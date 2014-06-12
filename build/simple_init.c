#include <sys/types.h>
#include <sys/wait.h>

int
main(int argc, char *argv[])
{
    int status;

    while (1) {
      waitpid(-1, &status,  0);
    }
}
