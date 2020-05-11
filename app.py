from PIL import Image
import Process

base = Image.open("base.png")

prepIMG = Process.PrepImage(base)

stars = Process.FindStars(prepIMG)

Process.DrawStars(base,stars)