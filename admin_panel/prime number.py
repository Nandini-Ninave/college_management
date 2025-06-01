num = 10
for i in range(1, num):
    for count in range(2, num-1):
        if(i % count == 0):
            print(i, "is not a prime number")
            break;
    if(i == count):
        print(i, "is a prime number")