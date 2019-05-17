from run_task_helpers import *
import normalize_results
import evaluation


def main():

    # list and store some paths and ids
    user_ids = get_user_ids()

    # for each user, compare all verification signatures to all genuine enrollment signatures
    # and save sorted results (dissimilarity measures)
    print('\nCompute all dissimilarities between verification and enrollment for each user...\n')

    result = []
    for user_id in user_ids[:3]:
        result.append(dissimilarity_for_one_user(user_id))

    # save results in specified format (see README) in txt file
    save_results(result, user_ids, 'results/', normalize=True)

    # calculate precision/recall
    # normalize_results.main()
    # evaluation.main()


if __name__ == '__main__':
    main()
