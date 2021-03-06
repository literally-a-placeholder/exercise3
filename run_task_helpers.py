import os
import glob
from tqdm import tqdm
import numpy as np
from Featurize import featurize
from DTW import DTWDistance


def dissimilarity_for_one_user(user_id):
    enrollment_paths, verification_paths = get_signature_paths(user_id)

    result = {}
    print('\nCalculating dissimilarities for user \'{}\'...'.format(user_id))

    for verification_index, verification_path in enumerate(tqdm(verification_paths)):

        distances_to_enrollment = [np.inf] * len(enrollment_paths)
        for i, enrollment_path in enumerate(enrollment_paths):
            distances_to_enrollment[i] = DTWDistance(featurize(verification_path, minmax=True),
                                                     featurize(enrollment_path, minmax=True))

        lowest_dist = min(distances_to_enrollment)
        result[verification_paths[verification_index]] = lowest_dist

    return result


def get_signature_paths(user_id):
    enrollment_ids = glob.glob('signaturedata/enrollment/' + str(user_id) + '*')

    verification_ids = glob.glob('signaturedata/verification/' + str(user_id) + '*')

    return enrollment_ids, verification_ids


def get_user_ids(mode='valid'):
    path = 'signaturedata/users_' + mode + '.txt'
    with open(path, 'r') as f:
        user_ids = []
        for line in f:
            user_ids.append(line.rstrip('\n'))

    return user_ids


def save_results(list_of_distance_dicts, user_ids, target_dir, normalize=False):

    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    postfix = ''
    if normalize:
        postfix = '_norm'

    with open('{}/results{}.txt'.format(target_dir, postfix), 'w') as f:

        for i, user in enumerate(list_of_distance_dicts):

            if normalize:
                user = normalize_dict_values(user)

            user_result_string = user_ids[i]
            for key, value in sorted(user.items(), key=lambda item: item[1], reverse=False):
                user_result_string += ', ' + str(key)[-6:-4] + ', ' + str(value)  # key-indexing -> only signature id

            f.write(user_result_string + '\n')

    return user_result_string


def normalize_dict_values(d, target=1.0):
    factor = target / sum(d.values())
    return {key: value*factor for key, value in d.items()}


# ================================================
# functions of task 2 - keyword spotting:


def get_train_valid_page_nrs():
    with open('task/train.txt', 'r') as f:
        train_pages = []
        for line in f:
            train_pages.append(line.rstrip('\n'))

    with open('task/valid.txt', 'r') as f:
        valid_pages = []
        for line in f:
            valid_pages.append(line.rstrip('\n'))

    return train_pages, valid_pages


def get_img_paths(train_pages, valid_pages):
    train_img_paths = []
    for page_nr in train_pages:
        train_img_paths += glob.glob('binarized/' + page_nr + '*')

    valid_img_paths = []
    for page_nr in valid_pages:
        valid_img_paths += glob.glob('binarized/' + page_nr + '*')

    return train_img_paths, valid_img_paths


def get_keywords():
    with open('task/keywords.txt') as f:
        keywords = []
        for line in f:
            keywords.append(line.rstrip('\n'))

    return keywords


def get_ids_of_keyword(keyword, only_train=False):
    ids = []
    with open('ground-truth/transcription.txt', 'r') as f:
        for line in f:
            if only_train:
                if keyword in line and line.startswith('2'):
                    ids.append(line.strip()[:9])
            else:
                if keyword in line:
                    ids.append(line.strip()[:9])

    return ids


def ids_to_paths(ids):
    paths = [None]*len(ids)
    for i, one_id in enumerate(ids):
        paths[i] = 'binarized/' + one_id + '.png'
    return paths


def featurize_list(img_paths):
    featurized_list = np.zeros((len(img_paths), 4, 100))

    for i, path in enumerate(img_paths):
        featurized_list[i] = featurize(path, minmax=True)

    return featurized_list


def compare_all(keyword, featurized_valid, valid_ids, save_as_txt=False, normalize=False):
    """Compare all found samples of the given keyword against all valid words with dynamic time warping (DTW).
    Output: <keyword>.txt containing all id's of the valid words and their scores, sorted from best to worst"""
    keyword_ids = get_ids_of_keyword(keyword, only_train=True)
    valid_ids = valid_ids
    keyword_paths = ids_to_paths(keyword_ids)
    featurized_keywords = featurize_list(keyword_paths)

    result = {}
    print('\nSearching all valid words for keyword \'{}\'...'.format(keyword))
    for valid_id, valid_word in enumerate(tqdm(featurized_valid, mininterval=3)):

        valid_word_distances = [np.inf] * len(keyword_ids)
        for i, keyword_word in enumerate(featurized_keywords):
            valid_word_distances[i] = DTWDistance(keyword_word, valid_word)

        lowest_dist = min(valid_word_distances)
        result[valid_ids[valid_id]] = lowest_dist

    if save_as_txt:
        target_dir = 'results'
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)

        sort_result_and_save_as_txt(result, keyword, target_dir)

    return result


def sort_result_and_save_as_txt(result, keyword, target_dir):
    with open('{}/{}.txt'.format(target_dir, keyword), 'w') as f:
        for key, value in sorted(result.items(), key=lambda item: item[1], reverse=True):
            f.write('{} {}\n'.format(key, value))


def multicore_compare(keyword, valid, valid_ids):
    compare_all(keyword, valid, valid_ids, save_as_txt=True)
    print('\nResults saved in \'{}.txt\'\n'.format(keyword))
