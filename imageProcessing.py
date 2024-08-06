import cv2
from rembg import remove
from PIL import Image 

def imagOperation(filename, operation):
    img = cv2.imread(f"uploads/{filename}")
    
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        
        case "cwebp":
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "rbg":
            newFilename = imagOperation(filename, 'cpng')
            input_image = Image.open(f"{newFilename}")
            output_image = remove(input_image)
            output_image.save(f"{newFilename}")
            return newFilename