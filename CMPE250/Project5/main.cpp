#include <iostream>
#include <set>
#include <math.h>
#include <cstring>

using namespace std;

long long pow133[1001];

int hashReturn (char word[]){
    long long hash = 0 ;
    int wordNumber = strlen(word);
    for(int i = 0 ; i < wordNumber ; i++){
        hash = (hash + (pow133[i] * word[i]) % 1000000007) % 1000000007;
    }
    return hash;
}

int main(int argc, char* argv[]) {
    freopen(argv[1], "r", stdin);
    freopen(argv[2], "w", stdout);
    char faxMachine[1001] ;
    char words[1001] ;
    int wordNumber;
    set<int> wordHashing;
    scanf("%s" , faxMachine);
    scanf("%d" , &wordNumber);

    pow133[0] = 1;
    for(int i = 1 ; i < 1001 ; i++){
        pow133[i] = (pow133[i-1] * 133) % 1000000007;
    }
    while(wordNumber != 0){
        scanf("%s" , words);
        int hash = 0 ;
        hash = hashReturn(words);
        wordHashing.insert(hash);
        wordNumber--;
    }
    int textLength = strlen(faxMachine);
    int dp[textLength + 1];
    for(int i = 1 ; i <= textLength ; i++){
        dp[i] = 0;
    }
    dp[0] = 1;

    for(int i = 1 ; i <= textLength ; i++){
        long long slideHash = 0;
        int count = 0;
        for( int j = i  ; j <= textLength ; j++){
            slideHash = (slideHash + (faxMachine[j-1] * pow133[count] % 1000000007)) % 1000000007 ;
            if(wordHashing.find(slideHash) !=  wordHashing.end()){
                dp[j] += dp[i-1];
                dp[j] %= 1000000007;
            }
            count++;
        }
    }
    printf("%d" , dp[textLength]);
    return 0;
}
