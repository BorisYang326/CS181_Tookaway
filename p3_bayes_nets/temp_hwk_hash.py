# input = [24,14,35,54,55,98,17]
# candidate = [i for i in range(1, 100)]
# output = []
# output2 = []
# index = [k for k in range(0, 11)]
# for j in candidate:
#     output = []
#     output2 = []
#     for i in input:
#         x = ((11 * i + 4) % j) % 10
#         output.append(x)
#         output2.append((x,i))
#     print(j)
#     print('Load Factor=' + str(10.00 / len(set(output))))
#     if (10.00 / len(list(set(output))) == 1):
#         print('True')
#         print list(set(output))
#         print (output2)
#         print('\n')
#     else:
#         print('False')
#         print('\n')
# output3=[]
# for k in input:
#     output3.append((((k+7)*(k+6)/16+k)%10,k))
# print (output3)

def function(a,b,c):
    return (a+b+c)%27

print function(13,5,2)
print function(9,10,13)
print function(1,2,10)