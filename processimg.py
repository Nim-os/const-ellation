from PIL import Image, ImageEnhance

# Secret sauce
BRIGHTNESS = 0.005
CONTRAST = 10000


# Open image
base = Image.open("base.png")
rawBase = base.load()

# Prints value of pixel
#print(rawBase[0,0])

# Apply filters: Contrast 100%, brightness 1%.
brightener = ImageEnhance.Brightness(base)
contraster = ImageEnhance.Contrast(brightener.enhance(BRIGHTNESS))


finalImage = contraster.enhance(CONTRAST)