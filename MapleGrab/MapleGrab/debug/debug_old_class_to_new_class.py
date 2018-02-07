import os


path = './Arrow/'
dir = 'up_'
full = 0
empty = 0

for i in range(500):
    try:
        os.rename(path+"full_"+dir+str(i)+'.bmp', path+"full_"+dir+str(full)+'.bmp')
        full+=1
        print(str(i))
    except FileNotFoundError:
        try:
            os.rename(path+"empty_"+dir+str(i)+'.bmp', path+"empty_"+dir+str(empty)+'.bmp')
            print(str(i))
            empty+=1
        except FileNotFoundError:
            exit(0)
    