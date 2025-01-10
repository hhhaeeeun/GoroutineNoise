package main

import (
	"fmt"
	"sync"
	"time"
)

var counter int
var counter_val int = 10000

var mu sync.Mutex // 경쟁 상태 제어를 위한 Mutex

// counter 값을 증가시키는 함수
func increment(wg *sync.WaitGroup) {
	defer wg.Done()

	for i := 0; i < counter_val; i++ {
		counter = counter + 1 // 전역 변수에 경쟁 상태로 접근
	}
}

func runTest(wg *sync.WaitGroup) {
	counter = 0 // 각 테스트 실행 전에 counter 초기화

	wg.Add(2)        // 2개의 고루틴 실행을 대기
	go increment(wg) // 첫 번째 고루틴
	go increment(wg) // 두 번째 고루틴

	wg.Wait() // 모든 고루틴이 끝날 때까지 대기
}

func main() {
	oneKB := 8 * 1024
	numBit := oneKB * 10 // 10KB

	start := time.Now()

	var wg sync.WaitGroup

	// 100만번의 테스트 실행
	for i := 1; i <= oneKB; i++ {
		runTest(&wg)
	}

	duration := time.Since(start).Seconds()
	fmt.Printf("[#] last sum (to check if race condition works well) = %d\n", counter)
	fmt.Printf("- %-20s: %-10d KB\n", "size of noise", numBit/oneKB)
	fmt.Printf("- %-20s: %-10.2f sec\n", "time", duration)
	fmt.Printf("- %-20s: %-10.2f bps\n", "speed", float64(numBit)/duration)
}
