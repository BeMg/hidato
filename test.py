from main import GA, hidato, random_hidato_generator
import json


if __name__=='__main__':
    # hidato size
    n = 25
    group_size = 10000
    round = 1000
    record = []
    for i in [x+5 for x in range(n-5+1)]: # size
        for j in [50+50*x for x in range(20)]: # round
            for k in [0.2*x for x in range(11)]: # alive rate
                for l in [0.2*x for x in range(11)]: # mutation rate
                    for m in [1000+100*x for x in range(20)]: # group size
                        cnt = 0
                        best = random_hidato_generator(i, i)
                        while True and cnt < 100:
                            cnt += 1
                            tmp = random_hidato_generator(i, i)
                            if tmp.n > best.n:
                                best = tmp
                        g = GA()
                        g.set_alive_rate(float(k))
                        g.set_group_size(int(m))
                        g.set_mutation_rate(float(l))
                        g.set_round(int(j))
                        rst = g.run(best)
                        record.append(rst)
                        with open('data.json', 'w') as f:
                            json.dump(record, f, ensure_ascii=False)