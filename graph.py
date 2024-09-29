import matplotlib.pyplot as plt

# 결과 파일에서 데이터 읽기
with open("results.txt", "r") as file:
    results = [int(line.strip()) for line in file]

# 그래프 출력
plt.figure(figsize=(10, 6))
plt.hist(results, bins=30, color='skyblue', edgecolor='black')
plt.title("Race Condition Simulation Results (1000 Iterations with Goroutines)")
plt.xlabel("Final Counter Value")
plt.ylabel("Frequency")
plt.grid(True)

plt.show()
