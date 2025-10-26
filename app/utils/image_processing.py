import cv2 as cv
from PIL import Image

def img_proc(path, size =(200, 200), quality=70):
    img=cv.imread(path)
    rgb_img=cv.cvtColor(img, cv.COLOR_BGR2RGB)
    resized_img = cv.resize(rgb_img, size, interpolation=cv.INTER_AREA) #resize
    
    pil_img = Image.fromarray(resized_img)
    pil_img.save(path, optimize=True, quality=quality) #compress
    
