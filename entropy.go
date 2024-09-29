package main

import (
	"fmt"
	"os"
	"sync"
)

var counter int

// counter 값을 증가시키는 함수
func increment(wg *sync.WaitGroup) {
	defer wg.Done()

	for i := 0; i < 1000000; i++ {
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
func main() {
	var wg sync.WaitGroup
	results := make([]int, 0)

	// 1000번의 테스트 실행
	for i := 1; i <= 1000; i++ {
		runTest(i, &wg, &results)
		fmt.Printf("진행 상황: %d 완료\n", i)
	}

	// 결과를 파일로 저장
	file, err := os.Create("results.txt")
	if err != nil {
		fmt.Println("파일 생성 에러:", err)
		return
	}
	defer file.Close()

	for _, result := range results {
		file.WriteString(fmt.Sprintf("%d\n", result))
	}

	fmt.Println("결과가 results.txt에 저장되었습니다.")
}
