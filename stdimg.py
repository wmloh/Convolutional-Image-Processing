from PIL import Image
from util import *
from tkinter.filedialog import asksaveasfilename

class StdImg:

    '''
    StdImg object stores image files and enables basic I/O functions.
    '''

    def __init__(self, directory, image=None, stack=True):
        '''
        Str, IMAGE.IMAGE -> StdImg
        
        Creates a StdImg by loading an image from a directory or if image
        argument is passed, then it will store a copy of image.
        If stack=True, then the image can be reverted indefinitely until
        its initialization as every edition is saved.

        Attributes:
        * img - current image of StdImg
        * prev - previous image of StdImg
        * orig - original image of StdImg
        * revertible - Boolean value where image of ConvImg can be reverted
        '''
        if type(image) is Image.Image:
            self.img = copy_img(image)
            self.orig = copy_img(image)
        elif type(directory) is str:
            self.img = Image.open(directory)
            self.orig = Image.open(directory)
        else:
            raise ValueError('The value type of directory passed is incorrect and the optional image parameter is not given')
        
        
        if stack:
            self.enable_stack = True
            self.stack = [self.orig]
            self.history = ['original']
        else:
            self.prev = None
            self.revertible = False

    def __str__(self):
        
        '''
        User-defined print function: prints the stack and stack size.
        '''
        print(self.history)
        return 'stack size: %i' % (len(self.stack))

    def preview(self):

        '''
        Displays the current image of StdImg.
        '''
        self.img.show()        

    def return_image(self, passByRef=False):

        '''
        Bool -> IMAGE.IMAGE

        Returns a new copy of the current image of StdImg.
        If passByRef=True then returns a reference to the
        current image of StdImg.
        '''
        if passByRef:
            return self.img
        return copy_img(self.img)

    def save(self):
        
        '''
        Saves the current image.

        Note: A tkinter filedialog will open for file name and
        file format to be given.
        '''
        directory = asksaveasfilename()
        self.img.save(directory)

    def revert(self, original=False):

        '''
        Bool -> None

        Changes the current image of StdImg to the previous.

        Note: If stack=False, the object can only be reverted to one
              previous image and cannot be reverted when recently initialized.
        '''
        if not self.enable_stack and not self.revertible:
            raise RuntimeError('The object has already been reverted or has recently been initialized')
        if original:
            if self.enable_stack:
                self.stack.append(self.img)
                self.history.append('original')
                self.img = copy_img(self.orig)
            else:
                self.prev = self.img
                self.img = copy_img(self.orig)
        else:
            if self.enable_stack:
                self.img = self.stack.pop()
                self.history.pop()
            else:
                img = copy_img(self.prev)
                self.img = img
                self.revertible = False
