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
    # Kinda misses a lot tho. Generally you'll get 100/2^(LINESKIP - 1)% stars
    LINESKIP = 1

    sizeX,sizeY = int(img.size[0]/LINESKIP),int(img.size[1]/LINESKIP)

    # Filled with tuples of (starLeft, starUp, starRight, starDown)
    stars = []

    for x in range(0,sizeX):
        for y in range(0,sizeY):

            brightness = CalculateBrightness(rawImg[x * LINESKIP, y * LINESKIP])

            if(brightness > threshold):

                # Have to check if star is already in list
                newStar = GetStarBounds(rawImg, low, (x * LINESKIP, y * LINESKIP), (sizeX, sizeY))

                collided = False

                # Chck coll in for loop
                # Maybe also check if pixel is already inside another star before making it a star to optimize?

                # Check list of stars backwards to find any collisions faster
                for star in reversed(stars):
                    if(CheckCollision(star,newStar)):
                        collided = True
                        break
                    
                if not (collided):
                    stars.append(newStar)

                    # Potential time save as well
                    y = newStar[3] + 1

    #print(len(stars)) # Debugging

    return 0

# What is that photoshop thing that determines if it should grab the surrounding pixel ??
def GetStarBounds(rawImg, low, pos, size):
    pX,pY = pos[0],pos[1]

    # Go in a cross to find max radius of point

    # (x1, y1, x2, y2)
    # (starLeft, starUp, starRight, starDown)

    # Tuples are immutable
    starLeft,starUp,starRight,starDown = 0,0,0,0

    # Marches pos in x and y direction individually by inc
    def MarchPoint(pos, inc):
        x,y = pos[0],pos[1]

        while CalculateBrightness(rawImg[x, pY]) > low:
            x += inc
            if(x < 0 or x >= size[0]):
                x -= inc
                break


        while CalculateBrightness(rawImg[pX, y]) > low:
            y += inc
            if(y < 0 or y >= size[1]):
                y -= inc
                break

        return (x,y)

    # Get right and up

    bounds = MarchPoint(pos, 1)

    starRight,starUp = bounds[0],bounds[1]

    # Get left and down

    bounds = MarchPoint(pos, -1)

    starLeft,starDown = bounds[0],bounds[1]
    
    return (starLeft,starUp,starRight,starDown)

def CheckCollision(starA, starB):

    # star = left,up,right,down

    for i in range(0,2):
        # On i = 0, check if BLeft if between ALeft and ARight
        # Then check if BRight is between ALeft and ARight

        if((starA[i] < starB[i] & starB[i] < starA[i+2])
        | (starA[i] < starB[i+2] & starB[i+2] < starA[i+2])):
            return True

    return False

def CalculateBrightness(pixel=(0,0,0)):
    return sum(pixel)/3