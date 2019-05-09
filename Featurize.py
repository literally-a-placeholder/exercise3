import numpy as np
from sklearn import preprocessing


def main():
    fet = featurize('signaturedata/enrollment/001-g-01.txt')
    print(fet)


def featurize(filename, minmax=False):

    signature_data = np.loadtxt(filename)

    feature_mat = signature_data

    if minmax:
        feature_mat = min_max_normalize(feature_mat)

    return feature_mat


# __________ feature calculations __________
def lower_contour(img_col):
    result = 0
    zeros_indices = np.where(img_col == 0)[0]
    if zeros_indices.size != 0:
        result = np.amax(zeros_indices)
    return result


def upper_contour(img_col):
    result = img_col.size
    zeros_indices = np.where(img_col == 0)[0]
    if zeros_indices.size != 0:
        result = np.amin(zeros_indices)
    return result


def bw_transitions(img_col):
    old_val = img_col[0]
    transitions = 0
    for val in img_col:
        if val != old_val:
            transitions += 1
        old_val = val
    return transitions


def fraction_of_bw_between_uclc(img_col):
    result = 0
    upp = upper_contour(img_col)
    low = lower_contour(img_col)
    between_uclc = img_col[upp:low+1]
    if between_uclc.size != 0:
        result = np.count_nonzero(between_uclc) / between_uclc.size * 100
    return result
# __________________________________________


def min_max_normalize(feature_mat):
    minmax_scale = preprocessing.MinMaxScaler().fit(feature_mat)
    df_minmax = minmax_scale.transform(feature_mat)
    return df_minmax


if __name__ == '__main__':
    main()
