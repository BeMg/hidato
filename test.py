from main import GA, hidato, random_hidato_generator
import json


if __name__=='__main__':
    # hidato size

    # 5*5 -> 50*50 with step equal to 5
    for i in range(10):
        n = (i+1)*5
        group_size = 10000
        muation_rate = 1
        alive_rate = 0.3
        round = 30

        cnt = 0
        best = random_hidato_generator(n, n)
        while True and cnt < n*50:
            cnt += 1
            tmp = random_hidato_generator(n, n)
            if tmp.n > best.n:
                best = tmp

        # every setting run 200 time get the average
        result = []
        for j in range(200):
            g = GA()
            g.set_round(round)
            g.set_mutation_rate(muation_rate)
            g.set_group_size(group_size)
            g.set_alive_rate(alive_rate)
            rst = g.run(best)
            result.append(rst)

        with open('hidato_{}.json'.format(n), 'w') as f:
            json.dump(result, f, ensure_ascii=False)