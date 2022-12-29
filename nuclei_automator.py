arr = [1000000001, 1000000002, 1000000003, 1000000004, 1000000005]

def aVeryBigSum(arr):
    remover = -1
    for i in range(1,len(str(arr[1]))):
        remover = -i
        all = True
        for j in range(len(arr)):
            if str(arr[0])[0:remover] != str(arr[j])[0:remover]:
                all = False
                break
        if all:
            break
    remover -= 1
    sum_last = 0
    sum_first = 0
    for i in arr:
        sum_first += int(str(i)[len(str(i))+remover::])
    for j in arr:
        sum_last += int(str(j)[0:remover])
    print(f"{sum_last}{sum_first}")

        
aVeryBigSum(arr)