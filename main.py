from random import randint, shuffle


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

    def get_init_soluation(self):
        already_have = set()
        all_have = set(range(1, self.n+1))
        for i in range(self.h):
            for j in range(self.w):
                if self.table[i][j] <= 0:
                    pass
                else:
                    already_have.add(self.table[i][j])

        need_have = all_have - already_have

        return list(need_have)

    def get_full_table(self, soluation):
        cnt = 0
        rst_table = [[0 for i in range(self.w)] for j in range(self.h)]
        for i in range(self.h):
            for j in range(self.w):
                if self.table[i][j] == 0:
                    rst_table[i][j] = soluation[cnt]
                    cnt += 1
                else:
                    rst_table[i][j] = self.table[i][j]
        return rst_table

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
    def __init__(self):
        self.pool = []
        self.group_size = 0
        self.round = 0
        self.mutation_rate = 0
        self.alive_rate = 0

    def set_group_size(self, size):
        self.group_size = size

    def set_round(self, n_round):
        self.round = n_round

    def set_mutation_rate(self, rate):
        self.mutation_rate = rate

    def set_alive_rate(self, rate):
        self.alive_rate = rate

    def mutation(self, target):
        if randint(1, 100) > self.mutation_rate*100:
            pass
        else:
            r = len(target)
            if r-1 == 0:
                pass
            else:
                x = randint(0, r-1)
                y = randint(0, r-1)
                target[x], target[y] = target[y], target[x]
        return target

    def crossover(self, p1, p2):

        length = len(p1)

        slice_p1 = p1[length // 4: length // 4 + length // 2]
        slice_p2 = p2[length // 4: length // 4 + length // 2]

        map1 = dict()
        map2 = dict()

        need_map1 = list(set(slice_p1) - set(slice_p2))
        need_map2 = list(set(slice_p2) - set(slice_p1))

        for i in range(len(need_map1)):
            map1[need_map2[i]] = need_map1[i]
            map2[need_map1[i]] = need_map2[i]


        o1 = [0] * length
        o2 = [0] * length

        for i in range(length):
            if p1[i] in map1:
                o1[i] = map1[p1[i]]
            else:
                o1[i] = p1[i]

            if p2[i] in map2:
                o2[i] = map2[p2[i]]
            else:
                o2[i] = p2[i]

        o1[length // 4: length // 4 + length // 2] = slice_p2
        o2[length // 4: length // 4 + length // 2] = slice_p1

        return (o1, o2)

    def fitness(self, table):
        step = [(i, j) for i in [1, 0, -1] for j in [1, 0, -1]]
        step.remove((0,0))

        score = 0
        for i in range(len(table)):
            for j in range(len(table[0])):
                need_check = [(i+x, j+y) for x, y in step if not (i+x < 0 or i+x >= len(table) or j+y < 0 or j+y >= len(table[0]))]
                for x, y in need_check:
                    if table[x][y] == table[i][j] + 1 or table[x][y] == table[i][j] - 1:
                        score += 1
        return score

    def run(self, hidato):

        self.pool.append(hidato.get_init_soluation())

        for i in range(self.round):
            print("Round {}".format(i+1))
            while len(self.pool) < self.group_size:
                tmp = self.pool[-1].copy()
                shuffle(tmp)
                self.pool.append(tmp)

            for i in range(self.group_size // 2):
                x = randint(0, len(self.pool)-1)
                y = randint(0, len(self.pool)-1)
                o1, o2 = self.crossover(self.pool[x], self.pool[y])
                o1 = self.mutation(o1)
                o2 = self.mutation(o2)
                self.pool.append(o1)
                self.pool.append(o2)

            pool_and_score = []

            for i in range(len(self.pool)):
                pool_and_score.append((self.fitness(hidato.get_full_table(self.pool[i])), self.pool[i]))

            pool_and_score.sort(reverse=True)

            print(pool_and_score[0])

            self.pool = [pool_and_score[i][1] for i in range(int(len(pool_and_score)*self.alive_rate))]

        return self.pool[0]


if __name__=='__main__':
    # a = hidato(3, 3)
    # a.set_point(0, 0, 1)
    # # a.set_point(0, 1, 2)
    # a.set_point(0, 2, 3)
    # # a.set_point(1, 0, 6)
    # a.set_point(1, 1, 5)
    # # a.set_point(1, 2, 4)
    # a.set_point(2, 0, 7)
    # a.set_point(2, 1, 8)
    # a.set_point(2, 2, 9)
    # # a.print_table()
    # # print(a.n)
    # # print(a.start_point)
    # # print(a.check_solution([2, 6 ,4]))

    b = random_hidato_generator(10, 10)

    g = GA()
    g.set_alive_rate(0.1)
    g.set_group_size(1000)
    g.set_mutation_rate(0.5)
    g.set_round(50)

    rst = g.run(b)

    b.print_table()
    print(rst)

    print(b.check_solution(rst))