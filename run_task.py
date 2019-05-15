from multiprocessing import Pool, cpu_count
from functools import partial
from run_task_helpers import *
import normalize_results
import evaluation


def main():

    # TODO: this whole workflow need to be adjusted to the new data structure!
    # template from last task still below as a reference...

    # list and store some paths and ids
    user_ids = get_user_ids()

    # for each user, compare all verification signatures to all genuine enrollment signatures
    # and save sorted results (dissimilarity measures)
    print('\nCompute all dissimilarities between verification and enrollment for each user...\n')

    ### REMOVE LINE BELOW WHEN DONE WITH TESTING!
    user_ids = user_ids[:1]

    result = []
    for user_id in user_ids:
        result.append(dissimilarity_for_one_user(user_id))

    ### REMOVE LINES BELOW WHEN DONE WITH TESTING!
    for user in result:
        for signature, dist in user.items():
            print(signature, dist, sep='\t')

    # save results in specified format (see README) in txt file
    save_results(result, user_ids, 'results/')

    # calculate precision/recall
    # normalize_results.main()
    # evaluation.main()


if __name__ == '__main__':
    main()
