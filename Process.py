from PIL import Image, ImageEnhance

# Prepares image by highlighting bright spots
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
def FindStars(img, threshold=50, low=40):

    rawImg = img.load()

    # Optimization, will only check every LINESKIP + 1 lines
    LINESKIP = 1

    sizex,sizey = int(img.size[0]/LINESKIP),int(img.size[1]/LINESKIP)

    # Filled with tuples of (starLeft, starUp, starRight, starDown)
    stars = []

    for x in range(0,sizex):
        for y in range(0,sizey):
            
            #brightness = sum(rawImg[x * LINESKIP, y * LINESKIP])/3

            brightness = CalculateBrightness(rawImg[x * LINESKIP, y * LINESKIP])

            if(brightness > threshold):

                # Have to check if star is already in list
                stars.append(GetStarArea(rawImg, low, (x * LINESKIP, y * LINESKIP)))

                #rawImg[x * LINESKIP, y * LINESKIP] = (255,0,0) # Check that stars are correctly being selected

    print(stars)

    return 0

# What is that photoshop thing that determines if it should grab the surrounding pixel ??
def GetStarArea(rawImg, low, pos):
    pX,pY = pos[0],pos[1]

    #print("Star found at %d, %d" % (pX, pY))

    # Go in a cross to find max radius of point
    # Go up until not apart of the star, multiply by -1 to flip to other side. And find the edge further down or up.
    # Do same for right

    x,y = pX,pY

    # (x1, y1, x2, y2)
    # (starLeft, starUp, starRight, starDown)
    star = (0,0,0,0)

    # Check vertical
    
        
    # Check horizontal

    return 0

def CalculateBrightness(pixel=(0,0,0)):
    return sum(pixel)/3