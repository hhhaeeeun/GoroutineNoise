#include <stdio.h>
#include <time.h>
#include <omp.h>


#define N 20000
int sum = 0;

int run_sum_with_omp();
int measure_time();

int main() {
    printf("# OMP based Noise Generator\n");

    //run_sum_with_omp();
    //printf("- sum = %d\n", sum);

    measure_time();
    return 0;
}

int run_sum_with_omp() {
    sum = 0;

#pragma omp parallel for num_threads(2)
    for(int i=0; i<N; i++) {
        sum++;
    }
    return 0;
}

int measure_time() {

    clock_t start, finish;
    double duration;

    //  byte --> KB --> MB
    int one_KB = 8*1024;
    int num_bit = one_KB*10;    // 10KB

    start = clock();

    for(int i=0; i<num_bit; i++) {
        run_sum_with_omp();
    }

    finish = clock();

    duration = (double)(finish - start) / CLOCKS_PER_SEC;
    printf("[#] last sum (to check if race condition works well) = %d\n", sum);
    printf("- %-20s: %-10d KB\n", "size of noise", num_bit / one_KB);
    printf("- %-20s: %-10.2f sec\n", "time", duration);
    printf("- %-20s: %-10.2f bps\n", "speed", (double) num_bit / duration);
}
