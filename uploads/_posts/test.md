


value:  P   A   H   N   A   P   L   S   I   I   G   Y   I   R
oldidx: 0   4   8   12  1   3   5   7   9   11  13  2   6   10
zlinen: 0   0   0   0   1   1   1   1   1   1   1   2   2   2



class Solution(object):
    def convert(self, s, numRows):
        if numRows == 1:
            return s
        tmp = [ '' for i in range(numRows) ]
        for i, value in enumerate(list(s)):
            print i % 4
            index = (numRows-1)-abs(numRows-1-i%(2*numRows-2))
            tmp[index] += value
        return "".join(tmp)

if __name__ == '__main__':
    s = Solution()
    #print s.convert("ABCDEFGHIJKLMN", 4)
    print s.convert("PAYPALISHIRING", 3)
