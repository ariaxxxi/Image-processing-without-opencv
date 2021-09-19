#!/usr/bin/env python3
import copy
import math
from PIL import Image as Image


# NO ADDITIONAL IMPORTS ALLOWED!


def get_pixel(image, x, y): 

    index = x + y*image['width']
    return image['pixels'][index] 


def set_pixel(result, x, y, newcolor):
    
    result['pixels'].append(newcolor)

    return result['pixels']  


def apply_per_pixel(image, func):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    for y in range(image['height']):
        for x in range(image['width']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, x, y, newcolor)
    return result  



def inverted(image):
    return apply_per_pixel(image, lambda c: 255 - c)
     



def correlate(image, kernel):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }

    def get(img, x, y):
        return img['pixels'][int(x + y*img['width'])]

    def set_color(img, x, y, color):
        img['pixels'][x + y*img['width']] = color

    def convolute(img, x, y, kernel):
        val = 0
        mid = math.floor(len(kernel) / 2)
        #edge effect
        for i in range(len(kernel)):
            for j in range(len(kernel)):
                x_offset, y_offset = x + i - mid, y + j - mid
                if x_offset < 0:
                    x_offset = 0
                elif x_offset >= img['width']:
                    x_offset = img['width']-1

                if y_offset < 0:
                    y_offset = 0
                elif y_offset >= img['height']:
                    y_offset = img['height']-1
                #correlated color     
                val += kernel[j][i] * get(img, x_offset, y_offset)
        # print(val)
        return val

    for y in range(image['height']):
        for x in range(image['width']):
            set_pixel(result, x, y, convolute(image, x, y, kernel))
    # print(result)        
    return round_and_clip_image(result)
    # return result


def round_and_clip_image(image):

    
    def round_and_clip_pixel(pixel):
        if pixel < 0:
            return 0
        elif pixel > 255:
            return 255
        else:
            return round(pixel)

    pixels = [round_and_clip_pixel(p) for p in image['pixels']]

    return {'height': image['height'], 'width': image['width'], 'pixels': pixels}




# FILTERS

def blurred(image, n):
 
    k = []
    num = 1/(n*n)
    for i in range(n):
        k.append(num)
    kernel = [k for i in range(n)]
    print(kernel)
    
    return correlate(image,kernel)
    # return image


def sharpened(image, n):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    blurred_image = blurred(image, n)
    for y in range(image['height']):
        for x in range(image['width']):
             blurred_color = get_pixel(blurred_image,x,y)
             original_color = get_pixel(image,x,y)
             sharpened_color = 2*original_color - blurred_color
             set_pixel(result, x, y, sharpened_color)
    return round_and_clip_image(result)

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES
def edges(image):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    k1 = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
        ]
    k2 = [
         [-1, -2, -1],
         [0,  0,  0],
         [1,  2,  1]
         ]
    im1 = correlate(image,k1)
    im2 = correlate(image,k2)

    for y in range(image['height']):
        for x in range(image['width']):
            pix1 = get_pixel(im1,x,y)
            pix2 = get_pixel(im2,x,y)
            edge_color = round(math.sqrt(pix1**2 + pix2**2))
            set_pixel(result, x, y, edge_color)

    return round_and_clip_image(result)

def load_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':

    
    # kernel=[
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0]
    #         ]
    # im1 = load_image('test_images/pigbird.png')
    # result = correlate(im1,kernel)
    # save_image(result, 'pigbird_correlated.png', mode='PNG')


    blur
    im2 = load_image('test_images/cat.png')
    blurred = blurred(im2, 5)
    save_image(blurred, 'cat_blurred.png', mode='PNG')

    sharp
    im3 = load_image('test_images/python.png')
    sharp = sharpened(im3, 11)
    save_image(sharp, 'python_sharp.png', mode='PNG')

    edge
    im4 = load_image('test_images/construct.png')
    edge = edges(im4)
    save_image(edge, 'construct_edges.png', mode='PNG')

    