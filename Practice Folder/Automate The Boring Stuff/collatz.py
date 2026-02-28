print('Enter a number')
number = int(input())  # Convert input to integer

if number % 2 == 0:  # Check if the number is even
    answer = number // 2
    print(answer)
else:
    answer = number * 3 + 1
    print(answer)

    


