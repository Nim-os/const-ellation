from PIL import Image
import Process

base = Image.open("base.png")

prepIMG = Process.PrepImage(base)

Process.FindStars(prepIMG)