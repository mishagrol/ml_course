import sys
size = int(sys.argv[1])+1
for i in range(1, size):
    print(' '*(size-i-1)+'#'*i)
