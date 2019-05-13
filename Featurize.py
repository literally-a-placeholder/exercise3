import numpy as np
from sklearn import preprocessing


def main():
    fet = featurize('signaturedata/enrollment/001-g-01.txt')
    fet_norm = featurize('signaturedata/enrollment/001-g-01.txt', minmax=True)
    print(fet)
    print(fet_norm)


def featurize(filename, minmax=False):

    # load and transpose
    signature_data = np.loadtxt(filename).T

    # get dt, the time interval/step between each measurement
    time_step = signature_data[0, 1] - signature_data[0, 0]

    # calculate 2 new features, the velocity in x and y respectively with respect to dt
    vx = np.diff(signature_data[2], prepend=signature_data[2, 0]) / time_step
    vy = np.diff(signature_data[2], prepend=signature_data[2, 0]) / time_step

    # combine to one feature matrix and remove index 0 (the discrete time point measure)
    feature_mat = np.vstack((signature_data, vx, vy))[1:]

    if minmax:
        feature_mat = min_max_normalize(feature_mat)

    return feature_mat


def min_max_normalize(feature_mat):
    minmax_scale = preprocessing.MinMaxScaler().fit(feature_mat)
    df_minmax = minmax_scale.transform(feature_mat)
    return df_minmax


if __name__ == '__main__':
    main()
