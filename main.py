
class hidato:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.n = w*h
        self.start_point = (-1, -1)
        self.table = [[0 for i in range(w)] for j in range(h)]

    def print_table(self):
        for i in range(self.h):
            print("\t".join([str(j) for j in self.table[i]]))

    # -1 represent this grid is unavailable, and 1~n can't be repeat between the grid.
    # handle by user.
    def set_point(self, x, y, value):
        # if we set some grid unavailable, we need update new target in
        if self.table[x][y] >= 0 and value < 0:
            self.n -= 1
        elif self.table[x][y] < 0 and value >= 0:
            self.n += 1
        else:
            pass

        if value == 1:
            self.start_point = (x, y)

        self.table[x][y] = value

    # Maybe can use fitness function to check the solution.
    # But here is use simulation the game rule to check solution.
    def check_solution(self, solution):
        if self.start_point == (-1, -1):
            return False

        curr_table = [[0 for i in range(self.w)] for j in range(self.h)]
        cnt = 0

        for i in range(self.h):
            for j in range(self.w):
                if self.table[i][j] == 0:
                    curr_table[i][j] = solution[cnt]
                    cnt += 1
                else:
                    curr_table[i][j] = self.table[i][j]

        curr_point = self.start_point

        while curr_table[curr_point[0]][curr_point[1]] != self.n:
            next_point = [(curr_point[0]+i, curr_point[1]+j) for i, j in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]]
            tmp_point = None
            for i, j in next_point:
                if i < 0 or i>self.h-1 or j<0 or j>self.w-1:
                    continue
                else:
                    if curr_table[i][j] == curr_table[curr_point[0]][curr_point[1]]+1:
                        tmp_point = (i, j)
                        break
                    else:
                        continue
            if tmp_point == None:
                return False
            else:
                curr_point = tmp_point
        return True

class GA:
    pass


if __name__=='__main__':
    a = hidato(3, 3)
    a.set_point(0, 0, 1)
    # a.set_point(0, 1, 2)
    a.set_point(0, 2, 3)
    # a.set_point(1, 0, 6)
    a.set_point(1, 1, 5)
    # a.set_point(1, 2, 4)
    a.set_point(2, 0, 7)
    a.set_point(2, 1, 8)
    a.set_point(2, 2, 9)
    a.print_table()
    print(a.n)
    print(a.start_point)
    print(a.check_solution([2, 6 ,4]))