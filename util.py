from PIL import Image
import math

def conv_box(pix, pos, coeff_lst, returnSum=False, oneD_lst=False):

    '''
    PIXELACCESS, tuple(Int, Int), list(list(Int))/list(Int), Bool, Bool
        -> List/Int

    Requires:
    * len(coeff_lst) must be a square number
    * pix is a RGB PixelAccess object

    Performs a box convolution operation of pixel <pos> on PixelAccess
    object <pix> with coefficients specified in coeff_lst.
    
    If returnSum=True then it will return the sum of all RGB values,
    otherwise, a list of values of RGB.

    If 1D_lst=True, then coeff_lst is a 1D list (no nested list),
    otherwise, coeff_lst has to be 2D list(1 level nested).
    '''
    if not oneD_lst:
        coeff_lst = [i for sublst in coeff_lst for i in sublst]
    length = int(math.sqrt(len(coeff_lst)))
    
    s = [0,0,0]
    x = pos[0] - length + 2
    y = pos[1] - length + 2
    
    for index, val in enumerate(coeff_lst):
        s[0] += (pix[x + (index % length), y + (index // length)])[0] * val
        s[1] += (pix[x + (index % length), y + (index // length)])[1] * val
        s[2] += (pix[x + (index % length), y + (index // length)])[2] * val

    if returnSum:
        return sum(s)

    return s

def tup_mult(t, c):

    '''
    Tuple, Num -> Tuple

    Returns tuple <t> such that each element is multipled by <c>.
    '''
    x = list()
    for i in range(len(t)):
        x.append(int(t[i] * c))

    return tuple(x)

def copy_img(img, excess=0, center=True):

    '''
    IMAGE.IMAGE, Int, Bool -> IMAGE.IMAGE

    Requires:
    * excess >= 0

    Returns a copy of <img> (not a reference). The excess parameter
    specifies the additional black spaces added to the border. For
    symmetry, it is recommended <excess> is an even number.
    
    If center=True then the returned image will be centralized,
    otherwise, it will be at the top left corner.
    '''
    if excess == 0:
        return img.copy()
    pixels = img.load()
    canvas = Image.new('RGB', (img.size[0] + excess, img.size[1] + excess), "black")
    if center:
        pad = excess // 2
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                canvas.putpixel((i + pad, j + pad), pixels[i,j])
    else:
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                canvas.putpixel((i,j), pixels[i,j])

    return canvas
