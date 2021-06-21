### Project1 
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def change_gamma(image, gamma=0.1):
   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")
   return cv2.LUT(image, table)

def color_histo(image):
    b,g,r = cv2.split(image)
    equhist_b = cv2.equalizeHist(b)
    equhist_g = cv2.equalizeHist(g)
    equhist_r = cv2.equalizeHist(r)
    equhist = cv2.merge((equhist_b, equhist_g, equhist_r))
    return equhist

def show_save(title, image):
    #cv2.putText(image, title, (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)
    cv2.imshow(title, image)
    cv2.imwrite('fig/'+title+'.jpg', image)
    
def image_scale(image):
    scale_factor = np.max(image)/255 
    image = (image/scale_factor).astype(np.uint8) 
    return image

def threshold_mask(image, thr1, thr2):
    binary_output = np.zeros_like(image)
    binary_output[(image >= thr1) & (image <= thr2)] = 255  
    return binary_output
    
# read and show orginal and gray image
img = mpimg.imread('1.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
show_save('1 Original image',img)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
show_save('2 gray image',gray)

hist,bins = np.histogram(img.flatten(),256,[0,256])
plt.hist(img.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.show()


## gray histogram equalization
show_save('3 Histogram Equalization - gray normal', cv2.equalizeHist(gray))

#change brithnessand apply histogram equalization                              
extreme_dark = change_gamma(gray, gamma=0.1)  # change the gamma value here to get different result
show_save('4 gray extreme_dark', extreme_dark)
show_save('5 Histogram Equalization - gray extreme_dark', cv2.equalizeHist(extreme_dark))

medium_dark = change_gamma(gray, gamma=0.7)
show_save('6 gray medium_dark', medium_dark)
show_save('7 Histogram Equalization -gray  medium_dark', cv2.equalizeHist(medium_dark))

extreme_ligth = change_gamma(gray, gamma=2.5)
show_save('8 gray xtreme_ligth', extreme_ligth)
show_save('9 Histogram Equalization - gray extreme_ligth', cv2.equalizeHist(extreme_ligth))


## color histogram equalization
show_save('10 Histogram Equalization - color normal', color_histo(img))

#change brithnessand apply histogram equalization   
extreme_dark = change_gamma(img, gamma=0.1)
show_save('11 color extreme_dark', extreme_dark)
show_save('12 Histogram Equalization - color extreme_dark', color_histo(extreme_dark))

medium_dark = change_gamma(img, gamma=0.7)
show_save('13color medium_dark', medium_dark)
show_save('14 Histogram Equalization - color medium_dark', color_histo(medium_dark))

extreme_ligth = change_gamma(img, gamma=2.5)
show_save('15 color extreme_ligth', extreme_ligth)
show_save('16 Histogram Equalization - color extreme_ligth', color_histo(extreme_ligth))


#Gradient
gX = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=1, dy=0)
gY = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=0, dy=1)
mag = np.sqrt((gX ** 2) + (gY ** 2))
orientation = np.arctan2(gY, gX) * (180 / np.pi) % 180

show_save("17 gradient x", image_scale(gX))
show_save("18 gradient y", image_scale(gY))
show_save("19 gradient magnitude", image_scale(mag))

# create a binary image of ones where threshold is met, zeros otherwise
show_save("20 gradient magnitude_threshold 25", threshold_mask(image_scale(mag), 0, 25))
show_save("20 gradient magnitude_threshold 50", threshold_mask(image_scale(mag), 0, 50))
show_save("20 gradient magnitude_threshold 100", threshold_mask(image_scale(mag), 0, 100))
show_save("20 gradient magnitude_threshold 150", threshold_mask(image_scale(mag), 0, 150))


cv2.waitKey(0)
cv2.destroyAllWindows()

