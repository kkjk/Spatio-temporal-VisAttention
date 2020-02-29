import math
import numpy as np
import cv2
import cv2, os
import matplotlib.pyplot as plt
import sys
import re


########### calculate NSS BO Spatial ##############

def NSS(saliency_map, ground_truth):

    #Normalize
    saliency_map_norm = (saliency_map - np.min(saliency_map))/((np.max(saliency_map)-np.min(saliency_map))*1.0)

    #discretize
    gt = ground_truth / 255

    # NSS
    x, y = np.where(gt == 1.0)
   
    s_map_norm = (saliency_map_norm - np.mean(saliency_map_norm))/np.std(saliency_map_norm)

    temp = []
    for i, j in zip(x, y):
        temp.append(s_map_norm[i][j])
    return np.mean(temp)

def normalize_map(s_map):

    # normalize the salience map (as done in MIT code)
    norm_s_map = (s_map - np.min(s_map))/((np.max(s_map)-np.min(s_map))*1.0)
    return norm_s_map


def auc_judd(s_map, gt):

    # ground truth is discrete, s_map is continous and normalized
    gt = gt/255

    s_map = s_map/255

    print('MAx GT:', np.max(gt))
    print('MAx smap:', np.max(s_map))
# thresholds are calculated from the salience map, only at places where fixations are present
    thresholds = []
    for i in range(0, gt.shape[0]):
        for k in range(0, gt.shape[1]):
            if gt[i][k]>0:
                thresholds.append(s_map[i][k])

    num_fixations = np.sum(gt)
    # num fixations is no. of salience map values at gt >0

    thresholds = sorted(set(thresholds))

    # fp_list = []
    # tp_list = []
    area = []
    area.append((0.0, 0.0))
    for thresh in thresholds:
        # in the salience map, keep only those pixels with values above threshold
        temp = np.zeros(s_map.shape)
        temp[s_map >= thresh] = 1.0
        assert np.max(gt) == 1, 'something is wrong with ground truth..not discretized properly max value > 1'
        assert np.max(s_map) == 1, 'something is wrong with salience map..not normalized properly max value > 1'
        num_overlap = np.where(np.add(temp, gt)==2)[0].shape[0]
        tp = num_overlap/(num_fixations*1.0)

    # total number of pixels > threshold - number of pixels that overlap with gt / total number of non fixated pixels
        # this becomes nan when gt is full of fixations..this won't happen
        fp = (np.sum(temp) - num_overlap)/((np.shape(gt)[0] * np.shape(gt)[1]) - num_fixations)
        area.append((round(tp, 4), round(fp, 4)))

    area.append((1.0,1.0))
    area.sort(key = lambda x:x[0])
    tp_list =  [x[0] for x in area]
    fp_list =  [x[1] for x in area]
    return np.trapz(np.array(tp_list),np.array(fp_list))


def auc_borji(s_map, gt, splits=100, stepsize=0.1):
    gt = gt/255
    num_fixations = np.sum(gt)

    print('num_fixations',num_fixations)

    num_pixels = s_map.shape[0]*s_map.shape[1]
    random_numbers = []
    for i in range(0, splits):
        temp_list = []
        for k in range(0, int(num_fixations)):
            temp_list.append(np.random.randint(num_pixels))
        random_numbers.append(temp_list)

    aucs = []
    # for each split, calculate auc
    for i in random_numbers:
        r_sal_map = []
        for k in i:
            r_sal_map.append(s_map[k % s_map.shape[0]-1, int(k/s_map.shape[0])])
        # in these values, we need to find thresholds and calculate auc
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

        r_sal_map = np.array(r_sal_map)

    # once threshs are got
        thresholds = sorted(set(thresholds))
        area = []
        area.append((0.0,0.0))
        for thresh in thresholds:
            # in the salience map, keep only those pixels with values above threshold
            temp = np.zeros(s_map.shape)
            temp[s_map>=thresh] = 1.0
            num_overlap = np.where(np.add(temp, gt)==2)[0].shape[0]
            tp = num_overlap/(num_fixations*1.0)
            fp = len(np.where(r_sal_map>thresh)[0])/(num_fixations*1.0)

            area.append((round(tp,4),round(fp,4)))

        area.append((1.0,1.0))
        area.sort(key = lambda x:x[0])
        tp_list =  [x[0] for x in area]
        fp_list =  [x[1] for x in area]

        aucs.append(np.trapz(np.array(tp_list),np.array(fp_list)))

    return np.mean(aucs)


def similarity(saliency_map, ground_truth):
    # here gt is not discretized nor normalized

    ground_truth = normalize_map(ground_truth)
    saliency_map = normalize_map(saliency_map)
    ground_truth = ground_truth/(np.sum(ground_truth)*1.0)
    x,y = np.where(ground_truth>0.0)
    sim = 0.0
    for i in zip(x, y):
        sim = sim + min(ground_truth[i[0], i[1]], saliency_map[i[0], i[1]])
    return sim


def cc(saliency_map, ground_truth):
    s_map_norm = (saliency_map - np.mean(saliency_map))/np.std(saliency_map)
    gt_norm = (ground_truth - np.mean(ground_truth))/np.std(ground_truth)
    a = s_map_norm
    b = gt_norm
    corr = (a*b).sum() / math.sqrt((a*a).sum() * (b*b).sum())
    #r = np.corrcoef(s_map_norm, gt_norm)
    return corr
	
	
	## NSS, AUC - location based metric,i.e. gt is discrete with fixation points
	## Similarity, Correlation coefficient - distribution based metric,i.e. gt is continuous fixation map
	############# change directories of ground truth and prediction

gtdir = os.path.abspath(sys.argv[1])
pdir = os.path.abspath(sys.argv[2])
resultFileDir = os.path.abspath(sys.argv[3])


print(gtdir)
print(pdir)

if not os.path.exists(gtdir):
    print("Error, folder doesn't exist")
    sys.exit(1)

if not os.path.exists(pdir):
    print("Error, folder doesn't exist")
    sys.exit(1)

nss = []
sim = []
correlation = []
aucJ = []
aucB = []

### range for filenames: SPATIAL- stepsize is 340, TEMPORAL - stepsize is 1
for sFile in os.listdir(gtdir):
    numberString = re.findall(r'\d+', sFile) # through regular expression
    numberList = list(map(int, numberString))
    print(numberList)
    timeIndex = numberList[0]
    userName = sFile.split(".")[0]
    predFile = userName.split("_")[0]+"_Prediction_"+str(timeIndex)+".png"
    print(predFile)
    predPath = os.path.join(pdir, predFile)
    print(predPath)
    gtPath = os.path.join(gtdir, sFile)
    predsaliencyMap = cv2.imread(predPath, cv2.IMREAD_GRAYSCALE)
    gtsaliencyMap = cv2.imread(gtPath, cv2.IMREAD_GRAYSCALE)
    predsaliencyMapNorm = normalize_map(predsaliencyMap)

    score = NSS(predsaliencyMapNorm, gtsaliencyMap)
    simi = similarity(predsaliencyMap, gtsaliencyMap)
    corr = cc(predsaliencyMap, gtsaliencyMap)
    aucj = auc_judd(predsaliencyMap, gtsaliencyMap)
    aucb = auc_borji(predsaliencyMap, gtsaliencyMap)
    nss.append((score))
    sim.append((simi))
    correlation.append((corr))
    aucJ.append((aucj))
    aucB.append((aucb))
    
nssVal =  np.mean(np.array(nss))
simVal = np.mean(np.array(simi))
corrVal = np.mean(np.array(corr))
aucJudVal = np.mean(np.array(aucj))
aucBorjVal = np.mean(np.array(aucb))

print('NSS:', nssVal)
print('Similarity:',simVal)
print('Correlation:',corrVal)
print('AUC JUDD:',aucJudVal)
print('AUC BORJI:',aucBorjVal)

resultantFile = os.path.join(resultFileDir, "SalienceMericResults.txt")
finalWriteStr = "NSS: "+ str(nssVal) + "\n\r" + "Similarity: "+ str(simVal) + "\n\r" + "Correlation: "+ str(corrVal) + "\n\r" + "AUC JUDD: "+ str(aucJudVal) + "\n\r" + "AUC BORJI: "+ str(aucBorjVal) + "\n\r" 
f = open(resultantFile, "w")
f.write("Saliency Metrics Calculated\n\r")
f.write(finalWriteStr)
f.close()
