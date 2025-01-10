package main

import (
	"encoding/binary"
	"flag"
	"fmt"
	"os"
	"sync"
)

var counter int

// 전역 변수 선언
// var counter_val int = 10000
var counter_val int
var Trials int

// counter 값을 증가시키는 함수
func increment(wg *sync.WaitGroup) {
	defer wg.Done()

	for i := 0; i < counter_val; i++ {
		counter = counter + 1 // 전역 변수에 경쟁 상태로 접근
	}
}

func runTest(iteration int, wg *sync.WaitGroup, results *[]int) {
	counter = 0 // 각 테스트 실행 전에 counter 초기화

	wg.Add(2)        // 2개의 고루틴 실행을 대기
	go increment(wg) // 첫 번째 고루틴
	go increment(wg) // 두 번째 고루틴

	wg.Wait() // 모든 고루틴이 끝날 때까지 대기
	*results = append(*results, counter)
}

func saveResultsAsBinary(filename string, results []int, wg *sync.WaitGroup) {
	defer wg.Done()

	file, err := os.Create(filename)
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer file.Close()

	for _, value := range results {
		if err := binary.Write(file, binary.LittleEndian, int32(value)); err != nil {
			fmt.Println("Error writing int to file:", err)
			return
		}
	}
}

func main() {

	// 플래그 정의
	j := flag.Int("j", 0, "An integer value for the flag -j")
	counterval := flag.Int("counterval", 0, "Value of counter_val")
	trial := flag.Int("trial", 0, "Number of trials")
	flag.Parse()
	counter_val = *counterval
	Trials = *trial
	// 입력받은 값 출력
	fmt.Printf("Received value for -j: %d\n", *j)

	var wg sync.WaitGroup
	results := make([]int, 0)

	// 100만번의 테스트 실행
	for i := 1; i <= Trials; i++ {
		runTest(i, &wg, &results)
		if i%10000 == 0 {
			fmt.Printf("진행 상황: %d 완료 counter : %d \n", i, counter)
		}
		//fmt.Printf("진행 상황: %d 완료 counter : %d \n", i, counter)
	}

	// 파일 이름 생성
	fileName := fmt.Sprintf("results_%d_%d_%d.bin", counter_val, Trials/10000, *j)
	wg.Add(1)
	go saveResultsAsBinary(fileName, results, &wg)

	wg.Wait() // 모든 고루틴이 종료될 때까지 대기
	fmt.Printf("결과가 %s에 바이너리 형식으로 저장되었습니다.\n", fileName)
	results = results[:0]

}
