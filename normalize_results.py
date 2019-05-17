from run_task_helpers import normalize_dict_values


def main():
    results_norm = ''
    with open('results/results.txt', 'r') as f:
        for line in f:
            one_user_result = line.strip().split(', ')

            user = one_user_result[0]

            # make dict out of list, alternating key and value
            i = iter(one_user_result[1:])
            res_dict = dict(zip(i, i))
            for keys in res_dict:
                res_dict[keys] = float(res_dict[keys])
            res_dict = normalize_dict_values(res_dict)

            results_norm += user
            for key, value in sorted(res_dict.items(), key=lambda item: item[1], reverse=False):
                results_norm += ', ' + str(key) + ', ' + str(value)

            results_norm += '\n'

    with open('results/results_norm.txt', 'w') as r:
        r.write(results_norm)


if __name__ == '__main__':
    main()
