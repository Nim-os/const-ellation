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

    for x in range(sizeX):
        for y in range(sizeY):

            brightness = CalculateBrightness(rawImg[x * LINESKIP, y * LINESKIP])

            if(brightness > threshold):

                # Have to check if star is already in list
                newStar = GetStarBounds(rawImg, (sizeX, sizeY), low, (x * LINESKIP, y * LINESKIP))

                collided = False

                # Check coll in for loop
                # Maybe also check if pixel is already inside another star before making it a star to optimize?

                # Check list of stars backwards to find any collisions faster
                for star in reversed(stars):
                    if(CheckCollision(star,(x * LINESKIP, y * LINESKIP))):
                        collided = True
                        break
                
                if not (collided):
                    stars.append(newStar)

                    # Potential time save as well
                    # print("Star down: " + str(newStar[3]) + "  |  Before: ", x, " , ", y)
                    y = newStar[3]
                    # print(y)

    #print(len(stars)) # Debugging

    #img.show()

    return stars

# What is that photoshop thing that determines if it should grab the surrounding pixel ??
def GetStarBounds(rawImg, size, low, pos):
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

    # Get right and down

    bounds = MarchPoint(pos, 1)

    starRight,starDown = bounds[0],bounds[1]

    # Get left and up

    bounds = MarchPoint(pos, -1)

    starLeft,starUp = bounds[0],bounds[1]
    
    return (starLeft,starUp,starRight,starDown)

def CheckCollision(star, pixel):

    # star = left,up,right,down
    # pixel = x,y

    if((pixel[0] > star[0] and pixel[0] < star[2])
        and (pixel[1] > star[1] and pixel[1] < star[3])):
            return True
    
    return False


    # DEAD CODE
    #for i in range(2):
        # On i = 0, check if BLeft if between ALeft and ARight
        # Then check if BRight is between ALeft and ARight

        # TO SELF: Only check if chosen pixel is inside star. Faster to calculate. Also prevents false positives!!



        #if((starA[i] < starB[i] and starA[i+2] > starB[i])
        #or (starA[i] < starB[i+2] and starA[i+2] > starB[i])):
        #    if(star[]):
        #        return True


def CalculateBrightness(pixel=(0,0,0)):
    return sum(pixel)/3

## Functions given Stars ##

def DrawStars(img, stars, colour=(255,0,0)):

    rawImg = img.load()
    
    for star in stars:

        for x in range(star[0],star[2]+1):
            for y in range(star[1],star[3]+1):
                if((x == star[0] or x == star[2]) and (y == star[1] or y == star[3])): # Make a bit more circular
                    continue

                rawImg[x,y] = colour
    
    img.save("redStars.png")

    return 0
