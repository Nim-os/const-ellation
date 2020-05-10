from PIL import Image, ImageEnhance

# Prepares image for FindStars
def PrepImage(img):
    # Secret sauce
    BRIGHTNESS = 0.005
    CONTRAST = 10000

    # Apply filters: Contrast 100%, brightness 1%.
    brightener = ImageEnhance.Brightness(img)
    contraster = ImageEnhance.Contrast(brightener.enhance(BRIGHTNESS))
    finalImage = contraster.enhance(CONTRAST)
    
    return finalImage


# Find bright spots in image with brightness at least threshold. Star positions will not expand past low
def FindStars(rawImg=[(0,0,0)], threshold=50, low=40):

    # Optimization, will only check every LINESKIP + 1 lines
    LINESKIP = 2

    stars = []

    for x in len(rawImg[0]):
        for y in len(rawImg):
            
            brightness = sum(rawImg[x * LINESKIP, y * LINESKIP])/3

            if(brightness > threshold):
                stars.append(GetStarArea(rawImg, low, (x * LINESKIP, y * LINESKIP)))


    return 0

def GetStarArea(rawImg, low, pos):
    x,y = pos[0],pos[1]

    print("Star found at %d, %d" % x % y)

    # Go in a cross to find max radius of point

    return 0