# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import numpy as np
import pandas as pd
from PIL import Image, ImageOps
import caffe

def white_bg_square(img):
    "return a white-background-color image having the img in exact center"
    size = (max(img.size),)*2
    layer = Image.new('RGB', size, (255,255,255))
    layer.paste(img, tuple(map(lambda x:(x[0]-x[1])/2, zip(size, img.size))))
    return layer

def init_caffe():
    caffe.set_mode_cpu()                
    model = "VGG_FACE_deploy.prototxt"
    weights = "VGG_FACE.caffemodel"    
    net = caffe.Net(model,
                weights,
                caffe.TEST)
    return net

def alter_image(fotoLink, size, averageImg):
    im = Image.open(fotoLink)
    square_im = white_bg_square(im)
    square_im = ImageOps.fit(square_im, size, Image.ANTIALIAS)
    im_input = np.asarray(square_im)
    r = im_input[:,:,0] - averageImg[0]
    g = im_input[:,:,1] - averageImg[1]
    b = im_input[:,:,2] - averageImg[2]
    im_input = np.asarray([b,g,r])
    return im_input
    
    
if __name__ == "__main__":    
    size = 224,224
    averageImg = [129.1863,104.7624,93.5940] ;
    net = init_caffe()    
    
    with open("personsVectors.csv", "w") as procFile:                
        dt = pd.read_csv("personsData.csv", sep=';', header=0)
        for i in range(0,len(dt.pid)):
            print(dt.pid[i])
            idPerson = dt.pid[i]
            fotoLink = "foto/"+str(idPerson)+".jpg"
            try:
                im_input = alter_image(fotoLink,size,averageImg)
                im_input = im_input[np.newaxis, :, :, :]
                net.blobs['data'].data[...] = im_input

                out = net.forward()
                #print(net.blobs['fc7'].data.tolist())
                #print(out['prob'].tolist()[0:len(out['prob'].tolist())])
                #print(net.blobs['fc8'].data.shape)
                #res = [str(i) for i in net.blobs['fc8'].data[0,:]]
                res = [str(i) for i in out['prob'][0,:]]
                vector = ";".join(res)
                procFile.write(str(idPerson)+";"+vector+"\n")
                
            except:            
                print("Error" + str(i))
            
    