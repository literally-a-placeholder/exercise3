from multiprocessing import Pool, cpu_count
from functools import partial
from run_task_helpers import *
import normalize_results
import evaluation


def main():

    # TODO: this whole workflow need to be adjusted to the new data structure!
    # template from last task still below as a reference...

    # preprocessing

    # list and store some paths and ids
    train_pages, valid_pages = get_train_valid_page_nrs()
    train_img_paths, valid_img_paths = get_img_paths(train_pages, valid_pages)
    keywords = get_keywords()
    valid_img_ids = [path[10:-4] for path in valid_img_paths]

    # featurize ALL images from valid pages and store to use for all keywords
    print('\nFeaturize all valid images...')
    featurized_valid = featurize_list(valid_img_paths)

    # for each keyword compare to all valid words and save results in <keyword>.txt
    print('\nCompute all distances of each keyword to each word of the valid pages...')

    pool = Pool(processes=cpu_count())
    func = partial(multicore_compare, valid=featurized_valid, valid_ids=valid_img_ids)
    pool.map(func, keywords)
    pool.close()
    pool.join()

    # calculate precision/recall
    normalize_results.main()
    evaluation.main()


if __name__ == '__main__':
    main()
