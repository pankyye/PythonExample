'''
1.Read pieces of images, which are used to create Mosaic Pic
2.Calculate Avg RGB 
3.Grid the target picture
4.Match the pieces of images with each grid of target picture
5.Composed and create final mosaic picture
'''

import sys,os,random,argparse 
from PIL import Image
import imghdr
import numpy as np 

def getImages(imageDir):
    #given a directory of images, return a list of Images
    files=os.listdir(imageDir)
    images=[]
    for file in files:
        filePath=os.path.abspath(os.path.join(imageDir,file))
        try:
            #explicit load so we don't run into resource crunch
            fp=open(filePath,'rb')
            im=Image.open(fp)
            images.append(im)
            im.load()
            fp.close()
        except:
            print('Invalid image: %s' %(filePath))
    return images  

def getAverageRGB(image):
    #Given PIL image, return average value of color as (r,g,b)
    im=np.array(image)
    w,h,d=im.shape #对应RGB图像的三个单位，分别对应R，G，B
    return tuple(np.average(im.reshape(w*h,d),axis=0))

def getAverageRGBOld(image):
    # no. of pixels in image
    npixels=image.size[0]*image.size[1]
    cols=image.getcolors(npixels)
    sumRGB = [(x[0]*x[1][0], x[0]*x[1][1], x[0]*x[1][2]) for x in cols]
    avg=tuple([int(sum(x)/npixels) for x in zip(*sumRGB)])
    return avg  

def splitImage(image,size):
    '''
    given image and dims(rows,cols) returns an m*n list of images
    '''
    W,H=image.size[0],image.size[1]
    m,n=size 
    w,h=int(W/n),int(H/m)
    imgs=[]
    #generate list of dimensions
    for j in range(m):
        for i in range(n):
            #append cropped image
            imgs.append(image.crop((i*w, j*h, (i+1)*w, (j+1)*h)))
    return imgs 

def getBestMatchIndex(input_avg,avgs):
    '''
    return index of best Image match based on RGB value distance
    '''
    avg=input_avg

    index=0
    min_index=0
    min_dist=0
    for val in avgs:
        dist=((val[0] - avg[0])*(val[0] - avg[0]) +
            (val[1] - avg[1])*(val[1] - avg[1]) +
            (val[2] - avg[2])*(val[2] - avg[2]))
        if dist<min_dist:
            min_dist=dist
            min_index=index 
        index+=1 
    return min_index

def createImageGrid(images,dims):
    '''
    Given a list of images and a grid size (m, n), create 
  a grid of images. 
  '''
    m,n=dims

  #sanity check
    assert m*n==len(images)

    width=max([img.size[0] for img in images])
    height=max([img.size[1] for img in images])

    grid_img=Image.new('RGB',(n*width,m*height))

    #paste images
    for index in range(len(images)):
        row=int(index/n)
        col=index-n*row  
        grid_img.paste(images[index], (col*width, row*height))
    return grid_img


def createPhotomosaic(target_image, input_images, grid_size,
                      reuse_images=True):
    """
    Creates photomosaic given target and input images.
    """

    print('splitting input image...')
    # split target image 
    target_images = splitImage(target_image, grid_size)

    print('finding image matches...')
    # for each target image, pick one from input
    output_images = []
    # for user feedback
    count = 0
    batch_size = int(len(target_images)/10)

    # calculate input image averages
    avgs = []
    for img in input_images:
        avgs.append(getAverageRGB(img))

    for img in target_images:
        # target sub-image average
        avg = getAverageRGB(img)
        # find match index
        match_index = getBestMatchIndex(avg, avgs)
        output_images.append(input_images[match_index])
        # user feedback
        if count > 0 and batch_size > 10 and count % batch_size is 0:
            print('processed %d of %d...' %(count, len(target_images)))
        count += 1
        # remove selected image from input if flag set
        if not reuse_images:
            input_images.remove(match)

    print('creating mosaic...')
    # draw mosaic to image
    mosaic_image = createImageGrid(output_images, grid_size)

    # return mosaic
    return mosaic_image


def main():
    parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')

    parser.add_argument('--target-image', dest='target_image', required=True)
    parser.add_argument('--input-folder', dest='input_folder', required=True)
    parser.add_argument('--grid-size', nargs=2, dest='grid_size', required=True)
    parser.add_argument('--output-file', dest='outfile', required=False)

    args=parser.parse_args()

    #target image
    target_image=Image.open(args.target_image)

    #input images
    print('reading input folder...')
    input_images=getImages(args.input_folder)

    #check if any valid input images found
    if input_images==[]:
        print('No input images found in %s. Exiting.' % (args.input_folder, ))
        exit()

    random.shuffle(input_images)

    grid_size=(int(args.grid_size[0]),int(args.grid_size[1]))

    output_filename='mosaic.png'
    if args.outfile:
        output_filename=args.outfile

    reuse_images=True
    resize_input=True 

    print('starting photomosaic creation...')

    #if images cannot be reused, ensure m*n <= num_of_images
    if not reuse_images:
        if grid_size[0]*grid_size[1]>len(input_images):
            print('grid size less than number of images')
            exit()

    if resize_input:
        print('resizing images...')
        # for given grid size, compute max dims w,h of tiles
        dims=(int(target_image.size[0]/grid_size[1]), 
            int(target_image.size[1]/grid_size[0])) 
        print('max tile dims:%s' %(dims,))
        #resize
        for img in input_images:
            img.thumbnail(dims)

    mosaic_image=createPhotomosaic(target_image, input_images, grid_size,
                                   reuse_images)
    mosaic_image.save(output_filename,'PNG')

    print('saved output to %s' %(output_filename,))
    print('done')

if __name__=='__main__':
    main() 

'''
python MosaicPhoto.py--target-image data/a.jpg --input folder data/folderName/ --grid-size 128 128
'''


















