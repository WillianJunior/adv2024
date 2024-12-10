package main
// package day6

import (
	"fmt"
	"sync"
	"bufio"
	"os"

	// reader "../../utils"
)

type State struct {
	goneUp    bool
	goneDown  bool
	goneRight bool
	goneLeft  bool
}

func main() {
	// Part1()
	// Part2()
	Part2sync()
}

func GetScanner(path string) *bufio.Scanner {
	f, err := os.Open(path)

	if err != nil {
		panic(err)
	}

	s := bufio.NewScanner(f)

	return s
}

func Part2sync() {
	s := GetScanner("input.txt")
	ans := 0

	areaMap := [][]byte{}
	for s.Scan() != false {
		line := make([]byte, len(s.Bytes()))
		for _, b := range s.Bytes() {
			line = append(line, b)
		}
		areaMap = append(areaMap, line)
	}

	// go routine will do stuff below

	// get guard position
	initialGuardPosition := make([]int, 2)
	for y, row := range areaMap {
		for x, column := range row {
			if column == '^' {
				initialGuardPosition[0] = y
				initialGuardPosition[1] = x
			}
		}
	}

	for y, row := range areaMap {
		for x, column := range row {
			if column != '.' {
				continue
			}
			// create state
			state := make([][]State, len(areaMap))
			for i := 0; i < len(areaMap); i++ {
				state[i] = make([]State, len(areaMap[i]))
			}

			guardPosition := []int{initialGuardPosition[0], initialGuardPosition[1]}
			direction := "up"
			for {
				if direction == "up" {
					// left the map area
					if guardPosition[0]-1 < 0 {
						break
					}
					if areaMap[guardPosition[0]-1][guardPosition[1]] == '#' || (guardPosition[0]-1 == y && guardPosition[1] == x) {
						direction = "right"
						continue
					}
					guardPosition[0] -= 1

					if !state[guardPosition[0]][guardPosition[1]].goneUp {
						state[guardPosition[0]][guardPosition[1]].goneUp = true
						continue
					}

					ans += 1
					break
				}
				if direction == "down" {
					// left the map area
					if guardPosition[0]+1 >= len(areaMap) {
						break
					}
					if areaMap[guardPosition[0]+1][guardPosition[1]] == '#' || (guardPosition[0]+1 == y && guardPosition[1] == x) {
						direction = "left"
						continue
					}
					guardPosition[0] += 1
					if !state[guardPosition[0]][guardPosition[1]].goneDown {
						state[guardPosition[0]][guardPosition[1]].goneDown = true
						continue
					}

					// LOOP
					ans += 1
					break
				}
				if direction == "left" {
					// left the map area
					if guardPosition[1]-1 < 0 {
						break
					}
					if areaMap[guardPosition[0]][guardPosition[1]-1] == '#' || (guardPosition[0] == y && guardPosition[1]-1 == x) {
						direction = "up"
						continue
					}
					guardPosition[1] -= 1
					if !state[guardPosition[0]][guardPosition[1]].goneLeft {
						state[guardPosition[0]][guardPosition[1]].goneLeft = true
						continue
					}

					// LOOP
					ans += 1
					break
				}
				if direction == "right" {
					// left the map area
					if guardPosition[1]+1 >= len(areaMap[0]) {
						break
					}
					if areaMap[guardPosition[0]][guardPosition[1]+1] == '#' || (guardPosition[0] == y && guardPosition[1]+1 == x) {
						direction = "down"
						continue
					}
					guardPosition[1] += 1
					if !state[guardPosition[0]][guardPosition[1]].goneRight {
						state[guardPosition[0]][guardPosition[1]].goneRight = true
						continue
					}

					// LOOP
					ans += 1
					break
				}
			}
		}
	}

	fmt.Println(ans)
}
func Part2() {
	s := GetScanner("input.txt")
	ans := 1

	areaMap := [][]byte{}
	for s.Scan() != false {
		line := make([]byte, len(s.Bytes()))
		for _, b := range s.Bytes() {
			line = append(line, b)
		}
		areaMap = append(areaMap, line)
	}

	// go routine will do stuff below

	// get guard position
	guardPosition := make([]int, 2)
	for y, row := range areaMap {
		for x, column := range row {
			if column == '^' {
				guardPosition[0] = y
				guardPosition[1] = x
			}
		}
	}

	var wg sync.WaitGroup
	result := make(chan int, len(areaMap)*len(areaMap[0]))
	for y, row := range areaMap {
		for x, column := range row {
			if column == '.' {
				wg.Add(1)
				go func(guardPosition []int, x, y int) {
					defer wg.Done()
					// create state
					state := make([][]State, len(areaMap))
					for i := 0; i < len(areaMap); i++ {
						state[i] = make([]State, len(areaMap[i]))
					}

					direction := "up"
					for {
						if direction == "up" {
							// left the map area
							if guardPosition[0]-1 < 0 {
								break
							}
							if areaMap[guardPosition[0]-1][guardPosition[1]] == '#' || (guardPosition[0]-1 == y && guardPosition[1] == x) {
								direction = "right"
								continue
							}
							guardPosition[0] -= 1

							if !state[guardPosition[0]][guardPosition[1]].goneUp {
								state[guardPosition[0]][guardPosition[1]].goneUp = true
								continue
							}

							fmt.Println("lol c")
							result <- 1
							break
						}
						if direction == "down" {
							// left the map area
							if guardPosition[0]+1 >= len(areaMap) {
								break
							}
							if areaMap[guardPosition[0]+1][guardPosition[1]] == '#' || (guardPosition[0]+1 == y && guardPosition[1] == x) {
								direction = "left"
								continue
							}
							guardPosition[0] += 1
							if !state[guardPosition[0]][guardPosition[1]].goneDown {
								state[guardPosition[0]][guardPosition[1]].goneDown = true
								continue
							}

							// LOOP
							fmt.Println("lol c")
							result <- 1
							break
						}
						if direction == "left" {
							// left the map area
							if guardPosition[1]-1 < 0 {
								break
							}
							if areaMap[guardPosition[0]][guardPosition[1]-1] == '#' || (guardPosition[0] == y && guardPosition[1]-1 == x) {
								direction = "up"
								continue
							}
							guardPosition[1] -= 1
							if !state[guardPosition[0]][guardPosition[1]].goneLeft {
								state[guardPosition[0]][guardPosition[1]].goneLeft = true
								continue
							}

							// LOOP
							fmt.Println("lol c")
							result <- 1
							break
						}
						if direction == "right" {
							// left the map area
							if guardPosition[1]+1 >= len(areaMap[0]) {
								break
							}
							if areaMap[guardPosition[0]][guardPosition[1]+1] == '#' || (guardPosition[0] == y && guardPosition[1]+1 == x) {
								direction = "down"
								continue
							}
							guardPosition[1] += 1
							if !state[guardPosition[0]][guardPosition[1]].goneRight {
								state[guardPosition[0]][guardPosition[1]].goneRight = true
								continue
							}

							// LOOP
							fmt.Println("lol c")
							result <- 1
							break
						}
					}
				}(guardPosition, x, y)
			}
		}
	}

	go func() {
		wg.Wait()
		close(result)
	}()

	for v := range result {
		fmt.Println(v)
		ans += v
	}

	fmt.Println(ans)
}

func Part1() {
	s := GetScanner("input.txt")
	ans := 1

	areaMap := [][]byte{}
	for s.Scan() != false {
		line := make([]byte, len(s.Bytes()))
		for _, b := range s.Bytes() {
			line = append(line, b)
		}
		// fmt.Println(string(line))
		areaMap = append(areaMap, line)
	}

	guardPosition := make([]int, 2)
	for y, row := range areaMap {
		for x, column := range row {
			if column == '^' {
				guardPosition[0] = y
				guardPosition[1] = x
			}
		}
	}

	// fmt.Println(guardPosition)
	direction := "up"
	for {
		// printAreaMap(areaMap)
		if direction == "up" {
			// left the map area
			if guardPosition[0]-1 < 0 {
				break
			}
			if areaMap[guardPosition[0]-1][guardPosition[1]] == '#' {
				direction = "right"
				continue
			}
			if areaMap[guardPosition[0]-1][guardPosition[1]] != 'X' {
				ans += 1
			}
			areaMap[guardPosition[0]][guardPosition[1]] = 'X'
			guardPosition[0] -= 1
			areaMap[guardPosition[0]][guardPosition[1]] = '^'
		}
		if direction == "down" {
			// left the map area
			if guardPosition[0]+1 >= len(areaMap) {
				break
			}
			if areaMap[guardPosition[0]+1][guardPosition[1]] == '#' {
				direction = "left"
				continue
			}
			if areaMap[guardPosition[0]+1][guardPosition[1]] != 'X' {
				ans += 1
			}
			areaMap[guardPosition[0]][guardPosition[1]] = 'X'
			guardPosition[0] += 1
			areaMap[guardPosition[0]][guardPosition[1]] = 'V'
		}
		if direction == "left" {
			// left the map area
			if guardPosition[1]-1 < 0 {
				break
			}
			if areaMap[guardPosition[0]][guardPosition[1]-1] == '#' {
				direction = "up"
				continue
			}
			if areaMap[guardPosition[0]][guardPosition[1]-1] != 'X' {
				ans += 1
			}
			areaMap[guardPosition[0]][guardPosition[1]] = 'X'
			guardPosition[1] -= 1
			areaMap[guardPosition[0]][guardPosition[1]] = '<'
		}
		if direction == "right" {
			// left the map area
			if guardPosition[1]+1 >= len(areaMap[0]) {
				break
			}
			if areaMap[guardPosition[0]][guardPosition[1]+1] == '#' {
				direction = "down"
				continue
			}
			if areaMap[guardPosition[0]][guardPosition[1]+1] != 'X' {
				ans += 1
			}
			areaMap[guardPosition[0]][guardPosition[1]] = 'X'
			guardPosition[1] += 1
			areaMap[guardPosition[0]][guardPosition[1]] = '>'
		}
	}

	fmt.Println(ans)
}

func printAreaMap(areaMap [][]byte) {
	for _, y := range areaMap {
		for _, x := range y {
			fmt.Printf("%s", string(x))
		}
		fmt.Println()
	}
	fmt.Println()
}