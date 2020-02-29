import cv2, os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import sys

def GaussianMask(sizex,sizey, sigma=33, center=None,fix=1):
  """
  sizex  : mask width
  sizey  : mask height
  sigma  : gaussian Sd
  center : gaussian mean
  fix    : gaussian max
  return gaussian mask
  """

  x = np.arange(0, sizex, 1, float)
  y = np.arange(0, sizey, 1, float)
  x, y = np.meshgrid(x,y)
  
  if center is None:
    x0 = sizex // 2
    y0 = sizey // 2
  
  else:
    if np.isnan(center[0])==False and np.isnan(center[1])==False:           
      x0 = center[0]
      y0 = center[1]        

    else:
      return np.zeros((sizey,sizex))

  return fix*np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / sigma**2)

def Fixpos2Densemap(fix_arr, width, height, imgfile, alpha=0.5, threshold=10):

  """
  fix_arr   : fixation array number of subjects x 3(x,y,fixation)
  width     : output image width
  height    : output image height
  imgfile   : image file (optional)
  alpha     : marge rate imgfile and heatmap (optional)
  threshold : heatmap threshold(0~255)
  return heatmap 
  """

  heatmap = np.zeros((H,W), np.float32)
  for n_subject in tqdm(range(fix_arr.shape[0])):
    heatmap += GaussianMask(W, H, 64, (fix_arr[n_subject,0],fix_arr[n_subject,1]), fix_arr[n_subject,2])
  
  # Normalization
  heatmap = heatmap/np.amax(heatmap)
  heatmap = heatmap*255
  heatmap = heatmap.astype("uint8")
  # heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
  return heatmap
  if imgfile.any():
    # Resize heatmap to imgfile shape 
    h, w, _ = imgfile.shape
    heatmap = cv2.resize(heatmap, (w, h))
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Create mask
    mask = np.where(heatmap<=threshold, 1, 0)
    mask = np.reshape(mask, (h, w, 1))
    mask = np.repeat(mask, 3, axis=2)
    
    # Marge images
    marge = imgfile*mask + heatmap_color*(1-mask)
    marge = marge.astype("uint8")
    marge = cv2.addWeighted(imgfile, 1-alpha, marge,alpha,0)

    return marge, mask, heatmap_color

  else:
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    return heatmap

if __name__ == '__main__':
  # Load image file
  
  imdir = sys.argv[1]
  outdir = sys.argv[2]
  if not os.path.exists(outdir):
    os.makedirs(outdir)

  for sFile in os.listdir(imdir):
  
    if sFile.endswith(".png"):
      path = os.path.join(imdir, sFile)
      print(path)
      
      img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
      result = np.where(img == 255)
      # y = np.array(result[0])[::-1]
      y = np.array(result[0])
      x = np.array(result[1])
      z = np.ones(x.shape)
      fix_arr = np.column_stack([x, y, z])
      H, W = img.shape 
      heatmap = Fixpos2Densemap(fix_arr, W, H, img, 0.7, 5)
      cv2.imwrite(os.path.join(outdir, sFile), heatmap)
      #os.remove(os.path.join(imdir, sFile))

#os.rmdir(imdir)

