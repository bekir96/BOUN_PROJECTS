#include <stdio.h> /* printf, scanf, NULL */
#include <pthread.h>
#include <stdlib.h> /* malloc, free, rand, exit */
#include <string>
#include <string.h>  /* strtok_rs */
#include <iostream>
#include <dispatch/dispatch.h>
#include <typeinfo>
#include <pwd.h>
#include <vector>
#include <sys/wait.h>    /* Needed to use wait() */
#include <unistd.h>     /* UNIX and POSIX constants and functions (fork, pipe) */
#include <fcntl.h>   /* Needed to use strlen() */
#include <errno.h>   /* Needed for errno */
#include <regex>
#include <algorithm>

#define alloca(size) __alloca(size)

// Defining enum Operation 
enum Operation {
    LISTDIR, LISTDIR_A, CURRENT_PATH, PRINT_FILE, MOVE_CONTENT_FILE, LISTDIR_GREP, LISTDIR_A_GREP, BASE_CASE
};

/*
    This function takes parameter 'operation' as pointer to pointer to char and  finds appropriate 
    case to perform required process which is wanted to implement for us. 'Task which is performed 
    by operation writes beside.'
*/
Operation findOperation(char** operation){
    
    if (!strcmp(operation[0], "listdir") and operation[1] == NULL) return LISTDIR; /*  To perform 'ls'   */
    else if (!strcmp(operation[0], "listdir") and !strcmp(operation[1],"-a") and operation[2] == NULL) return LISTDIR_A; /*  To perform 'ls -a'   */
    else if (!strcmp(operation[0],"currentpath") and operation[1] == NULL) return CURRENT_PATH; /*  To perform 'pwd'   */
    else if (!strcmp(operation[0],"printfile") and operation[1] == NULL) return BASE_CASE;   /* To get no segmentation fault error. */
    else if (!strcmp(operation[0],"printfile") and operation[1] != NULL and operation[2] == NULL) return PRINT_FILE; /*  To perform 'cat argv'   */
    else if (!strcmp(operation[0],"printfile") and !strcmp(operation[2],">") and operation[3] != NULL and operation[4] == NULL) return MOVE_CONTENT_FILE; /*  To perform 'cat argv[0] >> argv[1]'   */
    else if (!strcmp(operation[0],"listdir") and !strcmp(operation[1],"|") and operation[2] == NULL) return BASE_CASE;  /* To get no segmentation fault error. */
    else if (!strcmp(operation[0],"listdir") and !strcmp(operation[1],"|") and !strcmp(operation[2],"grep") and operation[3] != NULL and operation[4] == NULL) return LISTDIR_GREP; /*  To perform 'ls | grep argv'   */
    else if (!strcmp(operation[0],"listdir") and !strcmp(operation[1],"-a") and !strcmp(operation[2],"|") and 
                        !strcmp(operation[3],"grep") and operation[4] != NULL and operation[5] == NULL) return LISTDIR_A_GREP; /*  To perform 'ls -a  | grep argv'   */
    else return BASE_CASE; /*  To perform 'argv[0] : command not found'   */
}

/*
    This class and static function provide us to get pc name and return it.
*/
class Env{
    public:
    static std::string getUserName()
    {
        uid_t uid = geteuid ();
        struct passwd *pw = getpwuid (uid);
        if (pw)
        {
            std::string returnpw = std::string(pw->pw_name) + " >>> ";
            return returnpw;
        }
    }
};

/*  
    This function takes a input as pointer to const char. We use the library function 'strtok_r'
    to split the string by the character 'space' and return the array of strings instead. We also
    terminate the array 'NULL'. Currently our command buffer allocates 8 blocks only. If we enter 
    a command which has more than 8 words, our command will not work as expected. But in this
    project, input which is greater than 8 words is invalid input.
*/
char** get_input(char *input, std::string search) {
    char **command = (char**)malloc(8 * sizeof(char *));
    if (command == NULL) { /* It can fail if the OS runs out of memory. We should exit the program. */
        perror("malloc failed");
        exit(1);
    }
    char *separator = (char* )" ";  // seperator
    char *parsed, *brkt, *buffer;    //  used for srttok_r parameter
    int index = 0;  // used for memmove control 

    parsed = strtok_r(input, separator, &brkt);
    // Go through the parsed string and store each argument in command.
    while (parsed) {
        if (parsed[0] == '\"'){
            // Remove last index(if have quota)
            search.pop_back();

            // Find position of '\"' using find() 
            int pos = search.find("\"");

            // Take substring after first quota.
            std::string result = search.substr(pos+1);

            // Make string to form char array.
            buffer = strdup(result.c_str());

            command[index] = buffer;
            index++;
            break;
        } 
        else {
            command[index] = parsed;
            index++;
            parsed = strtok_r(NULL, separator, &brkt);
        }
    }

    command[index] = NULL;
    return command;
}

/*
    This function takes three input, vector as 'pair vector' which hold max 15 input, control 
    as 'bool' which determine vector will be fulfilled or be printed and __input__ as 'pair'.
*/
std::vector<std::pair<int, std::string> > check_list(std::vector<std::pair<int, std::string> > vector, bool control, std::pair<int, std::string> pair /* int hold index, string hold input */){
    if (vector.size() == 15){ /* control vector size to hold at 15 */
        vector.erase(vector.begin()); 
        vector.push_back(pair);
    }    
    else    vector.push_back(pair);
    if(control){    /* print statement */
        std::vector<std::pair<int, std::string> >::iterator it;
        for (it = vector.begin(); it < vector.end(); it++)    printf(" %d %s\n", it->first , (it->second).c_str());
    }
    return vector;
}

/*
    We start off by creating a pipe. Then we fork a child process. The parent will use the pipe for 
    command output. That means it needs to change its standard output 'file descriptor (1)' to the 
    writing end of the 'pipe (pfd[1])'. It does this via the 'dup2' system call: 'dup2(pfd[1], 1)'. 
    Then it executes the command in 'cmd1'.

    The child will use the pipe for command input. It needs to change its standard input 
    'file descriptor (0)' to the reading end of the 'pipe (pfd[0])'. It also does this via the 'dup2' 
    system call: 'dup2(pfd[0], 0)'. Then it executes the command in 'cmd2'.
*/
void runpipe(char** cmd1, char** cmd2){
    // To run pipe work correctly.
    int fds[2]; /* file descriptors */
    int status; /* wait status */
    if (pipe(fds) == -1) {       /* An error has occurred. */
		fprintf(stderr,"Pipe failed");
	}

    pid_t pid;  // will hold process ID; used with fork()
    if (fork() == 0) {  /* child 1 */
        // Connect STDOUT_FILENO to fds[1] end of pipe.
        dup2(fds[1], 1);

        // close all pipes (very important!); end we're using was safely copied
        close(fds[0]);
        close(fds[1]);

        // Execute the first command.
        execvp(cmd1[0], cmd1);

        // exec didn't work, exit
        perror("execvp failed");
        _exit(1);

    } else if ((pid = fork()) == 0) { /* child 2 */
        // Connect STDIN_FILENO to fds[0] end of pipe.
        dup2(fds[0], 0);

        // close all pipes (very important!); end we're using was safely copied
        close(fds[0]);
        close(fds[1]);

        // Execute the second command.
        execvp(cmd2[0], cmd2);
        
        // exec didn't work, exit
        perror("execvp failed");
        _exit(1);

    } else { /* parent */

        // close unused pipes.
        close(fds[0]);
        close(fds[1]);

        // only the parent gets here and waits for 2 children to finish
        // To avoid zombie children.
        for (int i = 0; i < 2; i++)
            wait(&status);
    }
}

/*
    This function takes an array of commands 'cmd' which is parsed to correctly. And, use 
    'execvp' to perform command.
*/
void runexec(char** cmd){
    pid_t pid;  // will hold process ID; used with fork()

    /* 
        If the OS runs out of memory or reaches the maximum number of allowed processes, 
        a child process will not be created and it will return -1. 
    */
    if ((pid = fork()) < 0) /* error */
        perror("Error (pid < 0)");

    else if (pid == 0) {    /* child */
        execvp(cmd[0], cmd);
        
        // exec didn't work, exit
        perror("execvp failed");
        _exit(1);

    } else  /* parent */     
        // To avoid zombie children.
        if (waitpid(pid, NULL, 0) < 0)  perror("Failed to collect child process");
            
}

/*
    This function simply provide command that will take a file name as an argument, read its content
    and write them on the standard output. 
*/
void runredirect(char** cmd, char** file){
    int fds[2]; // file descriptors
    int count;  // used for reading from stdout
    int fd;     // single file descriptor
    char buffer;     // used for writing and reading a character at a time
    pid_t pid;  // will hold process ID; used with fork()
    int status; /* wait status */

    pipe(fds);

    if (fork() == 0) { /* child 1 */
        /*
            'O_CREAT' : If the file does not exist it will be created. The owner (user ID) of the file 
                        is set to the effective user ID of the process.
            'O_RDWR' :  These request opening the file read/write, respectively.
            'O_APPEND' : The file is opened in append mode. Before each write(2), the file offset is 
                         positioned at the end of the file.
        */
        fd = open(file[0], O_RDWR | O_CREAT | O_APPEND, 0666); /* open output files */

        if (fd < 0) {    /* An error has occurred for open(). */
        printf("Error: %s\n", strerror(errno));
        return;
        }

        // Connect STDIN_FILENO to fds[0] end of pipe.
        dup2(fds[0], 0);

        // Don't need STDIN_FILENO and STDOUT_FILENO end of pipe.
        // after finishing reading, child close the read end
        close(fds[0]);
        close(fds[1]);

        // Read from stdout...
        while ((count = read(0, &buffer, 1)) > 0)
            write(fd, &buffer, 1); /* Write to the file. */

        exit(0);

    } else if ((pid = fork()) == 0) {  /* child 2 */
        // Connect STDOUT_FILENO to fds[1] end of pipe.
        dup2(fds[1], 1);

        // Don't need STDIN_FILENO and STDIN_FILENO end of pipe.
        close(fds[0]);
        close(fds[0]);

        // Output contents (command before redirect) of the given file to STDOUT_FILENO.
        execvp(cmd[0], cmd);
        
        // exec didn't work, exit
        perror("execvp failed");
        _exit(1);

    } else {  /* parent */
        // close unused pipes.
        close(fds[0]);
        close(fds[1]);

        // only the parent gets here and waits for 2 children to finish
        // To avoid zombie children.
        for (int i = 0; i < 2; i++)
            wait(&status);
    }
}

/*
    This function provide the code to enter proper place according to 'operation' which is finded in 'main' 
    function. Also takes 'command' as pointer to pointer to char and 'pipefd' as int array which will useful 
    for other functions.
*/
void switch_case(Operation operation, char** cmd){
    if (operation == LISTDIR) {                  /* Enter if input is format of 'listdir' */
        char *argv[] = {(char*)"ls", NULL};
        runexec(argv);
    } else if (operation == LISTDIR_A) {         /* Enter if input is format of 'listdir -a' */
        char *argv[] = {(char*)"ls", (char*)"-a", NULL}; 
        runexec(argv);
    } else if (operation == CURRENT_PATH) {      /* Enter if input is format of 'currentpath' */
        char *argv[] = {(char*)"pwd",  NULL};
        runexec(argv);
    } else if (operation == PRINT_FILE) {        /* Enter if input is format of 'printfile argv' */
        char *argv[] = {(char*)"cat", cmd[1], NULL};
        runexec(argv);
    } else if (operation == MOVE_CONTENT_FILE) { /* Enter if input is format of 'printfile argv[0] > argv[1]' */
        char *argv[] = {(char*)"cat",cmd[1],NULL};
        char *file[]= {cmd[3]};
        runredirect(argv, file);
    } else if (operation == LISTDIR_GREP) {
        char* cmd1[] = {(char*)"ls", NULL};     /* Enter if input is format of 'listdir | grep argv' */
        char* cmd2[] = {(char*)"grep", cmd[3], NULL};
        runpipe(cmd1, cmd2);
    } else if (operation == LISTDIR_A_GREP) {     /* Enter if input is format of 'listdir -a | grep argv' */
        char* cmd1[] = {(char*)"ls", (char*)"-a", NULL};
        char* cmd2[] = {(char*)"grep", cmd[4], NULL};
        runpipe(cmd1, cmd2);
    } else if (operation == BASE_CASE) {         /* Enter if input is format of 'non above' */
        printf("%s: %s", cmd[0], "command not found\n");
    } 
}

/*
    In 'main' function, we get input from the user, and pass it to 'get input' to fulfill the purpose
    which is mentioned above. Once the input has been parsed, we call 'fork' with switch statement
    which detects child, parent or error process and call 'switch_case' to find which operations is 
    required. When the 'fork' command completes, the child is an exact copy of the parent process. 
    However, when we invoke 'execvp', it replaces the current program with the program passed to it in 
    the arguments. What this means is that although the current text, data, heap and stack segments of 
    the process are replaced, the process id still remains unchanged, but the program gets overwritten 
    completely. If the invocation is successful, then 'execvp' never returns, and any code in the child 
    after this will not be executed.
*/
int main() {
    // Takes user input until they quit the shell, and passes that input as
    // arguments to be run.
    char **cmd;
    const char* __user_name__;
    std::string __input__;
    
    // To hold max 15 command and index of it.
    std::vector<std::pair<int, std::string> > vector;
    std::pair<int, std::string> pair;
    int history = 0;

    // Takes pc name.
    __user_name__ = (Env().getUserName()).c_str();

    // Keep returning the user to the prompt ad infinitum unless they enter 'exit' (without quotes).
    while (1) {
        // Display a prompt.
        std::cout << __user_name__;

        // Read in a command from the user.
        std::getline(std::cin, __input__);

        // Make string to form char array.
        char cstr[__input__.size()+1];
        strcpy(cstr, __input__.c_str());

        // Decipher the command we just read in and split it.
        cmd = get_input(cstr, __input__);

        // Detect if user enter or not press just enter.
        if(!strcmp(__input__.c_str(), "")) continue;
        /* 
            If we fork this if-else statement, vector changes in child process not in parent process.
            As a result, we do not get desired result. That is, we also need to ensure that, if the
            command entered by the user is 'footprint', we will not 'fork' the process at all. 
        */
        else if (!strcmp(cmd[0], "footprint") and cmd[1] == NULL) {
            history++;
            pair.first = history;
            pair.second = __input__;
            vector = check_list(vector, 1 /* print vector */, pair); /* Detect if input is format of 'footprint'. */
        } 
        else {
            history++;
            pair.first = history;
            pair.second = __input__;
            vector = check_list(vector, 0 /* fulfill vector */, pair);
            if (strcmp(cmd[0], "exit") == 0)  /* is it an "exit"?     */
                exit(0);

            // Determine how to handle the user's command(s) and returns enum 'Operation'.
            Operation operation = findOperation(cmd);
            switch_case(operation, cmd);
        }
        free(cmd);
    }

    // Let the OS know everything is a-okay.
    exit(0);
}