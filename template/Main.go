package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

var scanner *bufio.Scanner = bufio.NewScanner(os.Stdin)
var writer *bufio.Writer = bufio.NewWriter(os.Stdout)

type Int64Slice []int64

func (slice Int64Slice) Len() int           { return len(slice) }
func (slice Int64Slice) Less(i, j int) bool { return slice[i] < slice[j] }
func (slice Int64Slice) Swap(i, j int)      { slice[i], slice[j] = slice[j], slice[i] }

func main() {
	defer writer.Flush()
	scanner.Split(bufio.ScanWords)

	fmt.Printf("%v", 12345)
}

func Demo() {
	var n, m int64 = ReadInt64(), ReadInt64()
	PrintInt64s(n, m)
	writer.WriteByte('\n')
	slice := []int64{1, 2, 3, 4, 5}
	PrintInt64s(slice...)

	// sortDemo
	//slice := []int64{5, 3, 4, 2, 1}
	sort.Sort(Int64Slice(slice))

	//s := strconv.FormatBool(true)
	//s := strconv.FormatFloat(3.1415, 'E', -1, 64)
	//s := strconv.FormatInt(-42, 16)
	//s := strconv.FormatUint(42, 16)

}

func Min(a int64, b int64) int64 {
	if a < b {
		return a
	}
	return b
}

func MinInt(a int, b int) int {
	if a < b {
		return a
	}
	return b
}

func MinFloat64(a float64, b float64) float64 {
	if a < b {
		return a
	}
	return b
}

func MaxInt64(a int64, b int64) int64 {
	if a < b {
		return a
	}
	return b
}

func MaxInt(a int, b int) int {
	if a < b {
		return a
	}
	return b
}

func MaxFloat64(a float64, b float64) float64 {
	if a < b {
		return a
	}
	return b
}

func ReadInt32() int {
	scanner.Scan()
	ans, _ := strconv.Atoi(scanner.Text())
	return ans
}

func ReadInt64() int64 {
	scanner.Scan()
	ans, _ := strconv.ParseInt(scanner.Text(), 10, 64)
	return ans
}

func ReadFloat64() float64 {
	scanner.Scan()
	ans, _ := strconv.ParseFloat(scanner.Text(), 64)
	return ans
}

func PrintInt64s(ints ...int64) {
	for _, value := range ints {
		writer.WriteString(strconv.Itoa(int(value)))
		writer.WriteByte(' ')
	}
}
