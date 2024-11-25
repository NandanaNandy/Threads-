from PIL import Image
filename="F:\Softcopy _official\AZ_profile.jpg"
img1=Image.open(filename)
# img.show()
# img.save("output.jpg")  
img2=Image.new("RGB",(400,500),"red")
# img.show() 
img=img.resize((int(img.width/2),int(img.height/2)))
img.show()
