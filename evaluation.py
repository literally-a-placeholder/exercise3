import glob
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from tqdm import tqdm


def main():
    ################################################

    file = np.genfromtxt('results/results_norm.txt', delimiter=',', dtype=str)
    score = []

    #reate an array, that has the same structure as gf
    result_gf = np.zeros([ len(file[0])//2*len(file) , 2], object)

    precision_mean = []

    # file with key
    gt = np.loadtxt('signaturedata/gt.txt', dtype=str)

    threshold = []
    precision_all = []


    #go through different thresholds i
    for i in tqdm(np.arange(0, 0.1, 0.00001)):

        tp = 0
        fp = 0


        # user: genuine (g) and forgeries (f) signatures
        # user1, signature_ID11, dissimilarity11, signature_ID12, dissimilarity12, ...
        # example:
        # 051, 46, 6.40341144, 21, 7.62949846, 17, 9.18516724, 03, 10.47132116, […]
        for k, user in enumerate(file):

            #go through every single signature: if score is below threshold (i) --> genuined(g); otherwise --> foreeriesed (f)
            for e in range(len(user)//2):
                #create first column:
                row = k*(len(user)//2) + e
                id_text = user[0] + "-" + user[e*2 + 1]
                result_gf[row, 0] = id_text.replace(" ", "")

                #create second column:
                #if score is below threshold (i) --> genuined(g); otherwise --> foreeriesed (f)
                if float(user[e*2+2]) < i:
                    result_gf[row, 1] = "g"
                else:
                    result_gf[row, 1] = "f"


        result_gf = np.array(result_gf, dtype='str')
        result_gf = result_gf[np.argsort(result_gf[:, 0])[::]]

        for k1, line in enumerate(result_gf):
            if line[1] == gt[k1,1]:
                tp +=1
            else:
                fp +=1

        precision = tp/ (tp + fp)

        threshold.append(i)
        precision_all.append(precision)

        #precision_mean.append(np.mean(precision_all))



    # print(np.mean(recall_mean), np.mean(precision_mean))
    #
    # auc = metrics.auc(recall_mean, precision_mean)
    plt.plot(threshold, precision_all)
    plt.xlabel('threshold')
    plt.ylabel('precision')
    plt.title("Precision with different thresholds")
    plt.ylim(0,1.2)

    ymax = max(precision_all)
    xpos = precision_all.index(ymax)
    xmax = threshold[xpos]
    plt.annotate('maximum precision: {} \n with threshold = {}'.format(ymax, xmax), xy=(xmax, ymax), xytext=(xmax, ymax + 0.1),
                arrowprops=dict(facecolor='black', shrink=0.05),
                )


    plt.show()


if __name__ == '__main__':
    main()