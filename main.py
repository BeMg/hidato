from random import randint


class hidato:
    def __init__(self, h, w):
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

def random_hidato_generator(h, w, remove_rate=0.4):
    table = [[-1 for i in range(w)] for j in range(h)]
    curr_x = randint(0, h-1)
    curr_y = randint(0, w-1)

    step = [(i,j) for i in [1, 0, -1] for j in [1, 0 ,-1]]
    step.remove((0,0))
    cnt = 1

    while True:
        table[curr_x][curr_y] = cnt if randint(1, 100) > remove_rate*100 or cnt == 1 else 0
        cnt += 1

        next_point = [(curr_x+i, curr_y+j) for i, j in step]
        safe_step = []
        for i, j in next_point:
            if i < 0 or i > h-1 or j < 0 or j > w-1:
                continue
            else:
                if table[i][j] == -1:
                    safe_step.append((i, j))

        if len(safe_step) == 0:
            break
        else:
            target = randint(0, len(safe_step)-1)
            curr_x, curr_y = safe_step[target]

    rst = hidato(h, w)

    for i in range(h):
        for j in range(w):
            rst.set_point(i, j, table[i][j])

    return rst

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
    # a.print_table()
    # print(a.n)
    # print(a.start_point)
    # print(a.check_solution([2, 6 ,4]))

    b = random_hidato_generator(10, 14)

    b.print_table()