from PIL import Image
from util import *
from stdimg import StdImg

class ConvImg(StdImg):

    '''
    ConvImg object stores image files that can be editted using
    the following convolution and standard image processing
    techniques.

    By default, most image processing operations return a RGB image.
    '''
    
    def __init__(self, directory, image=None, stack=True):

        '''
        Str, IMAGE.IMAGE -> ConvImg
        
        Creates a ConvImg by loading an image from a directory or if image
        argument is passed, then it will store a copy of image.
        If stack=True, then the image can be reverted indefinitely until
        its initialization as every edition is saved.

        Attributes:
        * img - current image of ConvImg
        * prev - previous image of ConvImg
        * orig - original image of ConvImg
        * revertible - Boolean value where image of ConvImg can be reverted
        '''

        super().__init__(directory, image, stack)

    def box_blur(self, deg, original=False):

        '''
        Int, Bool -> None

        Sets the current image to be a box blur version of the current
        image. If original=True then the current image is set using the
        original image.

        Deg indicates the intensity of the bluriness.
        '''
        if original:
            img = copy_img(self.orig, excess=deg * 2)
        else:
            img = copy_img(self.img,  excess=deg * 2)
        pixels = img.load()
        canvas = Image.new('RGB', (img.size[0] - deg*2, img.size[1] - deg*2), '#808080')
        length = 1 + 2 * deg
        size = length ** 2
        
        tup_fnc = lambda x, y: tup_mult(tuple(conv_box(pixels,
                                                       (x+length-2,y+length-2),
                                                       [1 for i in range(size)],
                                                       oneD_lst=True)), 1/size)
        for i in range(img.size[0] - deg * 2):
            for j in range(img.size[1] - deg * 2):
                pix_tup = tup_fnc(i,j)
                canvas.putpixel((i,j), pix_tup)
        if self.enable_stack:
            self.stack.append(self.img)
            self.history.append('box_blur')
        else:
            self.prev = self.img
            self.revertible = True
        self.img = canvas
        

    def edge_detection(self, original=False):

        '''
        Bool -> None

        Sets the current image to be the coloured outline of the current
        image with a black background. If original=True then the current
        image is set using the original image.
        '''
        if original:
            img = copy_img(self.orig, 2)
        else:
            img = copy_img(self.img, 2)
        pixels = img.load()
        canvas = Image.new('RGB', (img.size[0], img.size[1]), 'black')
        tup_fnc = lambda x, y : conv_box(pixels, (x+1,y+1), [[-1,-1,-1],
                                                             [-1,8,-1],
                                                             [-1,-1,-1]])
        for i in range(img.size[0] - 2):
            for j in range(img.size[1] - 2):
                t = tuple(tup_fnc(i,j))
                canvas.putpixel((i,j), t)

        if self.enable_stack:
            self.stack.append(self.img)
            self.history.append('edge_detection')
        else:
            self.prev = self.img
            self.revertible = True
        self.img = canvas
        

    def silhouette(self, relative=False, original=False):

        '''
        Bool, Bool -> None

        Sets the current image to be a monotonic silhouette of the current
        image. If original=True then the current image is set using the
        original image.

        If relative=True, then the benchmark will be set to the average
        pixel value of the image. Then any pixel value lower than the
        benchmark will be set to 0 and any pixel value higher than the
        benchmark will be set to 255.
        If relative=False, then the benchmark will be set to 128.

        Note: Returns a 1-bit pixels image
        '''
        if original:
            img = copy_img(self.orig)
        else:
            img = copy_img(self.img)
        pixels = img.load()
        canvas = Image.new('1', (img.size[0], img.size[1]), "black")
        benchmark = 128
        if relative:
            total = 0
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                   total += sum(pixels[i,j]) // 3
            benchmark = total / (img.size[0] * img.size[1])
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                weight = sum(pixels[i,j]) / 3
                if weight >= benchmark:
                    canvas.putpixel((i,j), 1)
                else:
                    canvas.putpixel((i,j), 0)

        if self.enable_stack:
            self.stack.append(self.img)
            self.history.append('silhouette')
        else:
            self.prev = self.img
            self.revertible = True
        self.img = canvas
        

    def black_white(self, original=False):

        '''
        Bool -> None

        Sets the current image to be a black and white version of
        the current image. If original=True then the current image
        is set using the original image.
        '''
        if original:
            img = copy_img(self.orig)
        else:
            img = copy_img(self.img)
        pixels = img.load()
        canvas = Image.new('RGB', (img.size[0], img.size[1]), "black")

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                weight = int(sum(pixels[i,j]) / 3)
                canvas.putpixel((i,j), (weight, weight, weight))

        if self.enable_stack:
            self.stack.append(self.img)
            self.history.append('black_white')
        else:
            self.prev = self.img
            self.revertible = True
        self.img = canvas
        

    def negative(self, original=False):

        '''
        Bool -> None

        Sets the current image to be a negative version of the current
        image. If original=True then the current image is set using the
        original image.
        '''
        if original:
            img = copy_img(self.orig)
        else:
            img = copy_img(self.img)
        pixels = img.load()
        canvas = Image.new('RGB', (img.size[0], img.size[1]), "black")

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                x = (255 - pixels[i,j][0], 255 - pixels[i,j][1], 255 - pixels[i,j][2])
                canvas.putpixel((i,j), x)

        if self.enable_stack:
            self.stack.append(self.img)
            self.history.append('negative')
        else:
            self.prev = self.img
            self.revertible = True
        self.img = canvas
        

    def contrast(self, deg, original=False):

        '''
        Float, Bool -> None

        Requires:
        * 0 < deg < 1
        
        Sets the current image to be a high contrast, clean version of
        the current image. If original=True then the current image is
        set using the original image. Higher deg leads to higher
        augmentation.
        '''
        if original:
            img = copy_img(self.orig)
        else:
            img = copy_img(self.img)
        pixels = img.load()
        canvas = Image.new('RGB', (img.size[0], img.size[1]), 'black')

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if sum(pixels[i,j])/3 < 128:
                    canvas.putpixel((i,j), min(tup_mult(pixels[i,j], 1 - deg), (255,255,255)))
                else:
                    canvas.putpixel((i,j), max(tup_mult(pixels[i,j], 1 + deg), (0,0,0)))

        if self.enable_stack:
            self.stack.append(self.img)
            self.history.append('contrast')
        else:
            self.prev = self.img
            self.revertible = True
        self.img = canvas
        

    def sharpen(self, deg, original=False):

        '''
        Int, Bool -> None

        Requires:
        * deg >= 1

        Sets the current image to be a sharper version of the current
        image. If original=True then the current image is set using the
        original image.

        Note: Passing negative deg values leads to an unfocussed image.
        '''
        if original:
            img_new = copy_img(self.orig, 2)
        else:
            img_new = copy_img(self.img, 2)
        pixels = img_new.load()
        x_size = self.img.size[0]
        y_size = self.img.size[1]
        
        canvas = Image.new('RGB', (x_size, y_size), 'black')
        deg = int(deg)

        factor_fnc = lambda x, y: conv_box(pixels, (x+1,y+1), [[0,-deg,0,-deg],
                                                               [4 * deg + 1,-deg],
                                                               [0,-deg,0]])
        
        for i in range(x_size):
            for j in range(y_size):
                factor = tuple(factor_fnc(i,j))
                canvas.putpixel((i,j), factor)

        if self.enable_stack:
            self.stack.append(self.img)
            self.history.append('sharpen')
        else:
            self.prev = self.img
            self.revertible = True
        self.img = canvas
        

