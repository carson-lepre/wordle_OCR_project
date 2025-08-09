from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np
import pandas 
import sys as sys
import re

argument_list = sys.argv

image = cv.imread(sys.argv[1])

def display(image, display_text):
    cv.imshow(display_text, image)
    cv.waitKey(0)
    cv.destroyAllWindows() 
    
def filter_out_green_and_grey(image):
    # image = cv.imread("wordle.jpg")
    hsv=cv.cvtColor(image,cv.COLOR_BGR2HSV)
    brown_lo=np.array([40,40,40])
    brown_hi=np.array([70,255,255])
    mask=cv.inRange(hsv,brown_lo,brown_hi)
    image[mask>0]=(0,0,0)
    cv.imwrite("filtered.jpg",image)
    cv.imshow("Filtered", image)
    cv.waitKey(0)
    cv.destroyAllWindows() 
    return image

def scan(image, line_number):
    left_border = 120
    right_border = 170
    counter = 0
    scanned_image = str(pytesseract.image_to_string(image[line_number[0]:line_number[1], left_border:right_border]))

    while scanned_image == "" and right_border < 828:
        counter += 1
        # print(left_border)
        # print(right_border)
        scanned_image = str(pytesseract.image_to_string(image[line_number[0]:line_number[1], left_border:right_border]))
        left_border += 15
        right_border += 15

    # display(image[line_number[0]:line_number[1], left_border:right_border], "Cropped Section")


    if scanned_image == "":
        display(image[line_number[0]:line_number[1], left_border:right_border], "Cropped Section")
        return "Not Found"
    else: 
        display(image[line_number[0]:line_number[1], left_border:right_border], "Cropped Section")
        return scanned_image

def get_number_of_games(image):

    # Load tesseract image data into pandas dataframe
    data = pytesseract.image_to_data(image, output_type='data.frame')
    
    # Create list of values from "text" column in dataframe
    name_list = data['text'].values.tolist()

    # Loop to get index position of "STATISTICS" 
    for i in range(len(name_list)):
        if name_list[i] == "STATISTICS":
            stats_index = i

    # "Number of games" is X number greater than location of "STATISTICS" string
    # This little hack locates the "number of games" number
    
    # Step One - It turns out "NaN" values are float-type objects, so ignore float-type
    # objects while using a regex to filter non-integer chars from each list item.
            
    for i in range(0, len(name_list) -1):
     
        if type(name_list[i]) == float:
            pass
        else:            
            temp = re.sub("[^0-9]","",name_list[i])
            name_list[i] = temp          

    # Step Two - Starting at the index position of the string "STATISTICS", iterate through 
    # the list until the next integer. As of 6/4/2024 this has always been the value for the 
    # number of games played.
            
    flag_for_finding_digit = False
    addend = 0
    while flag_for_finding_digit == False:
        try:
            int(name_list[stats_index + addend])
            flag_for_finding_digit = True
            addend += 1
        except:
            addend += 1
            pass
           
    num = "".join(char for char in name_list[stats_index + addend - 1] if char.isdigit())
    return num

number_of_games = get_number_of_games(image)

print(number_of_games)

files_to_test = ["wordle100.jpg",
        "wordle143.jpg",
        "wordle144.jpg",
        "wordle145CL.jpg",
        "wordle145JD.jpg"]
    

def TEST_number_of_games(image, files_to_test):

    list_of_answers = []

    for i in files_to_test:
        list_of_answers.append(get_number_of_games(i))

    return list_of_answers

print(TEST_number_of_games)
    



line_one = (712, 745)
line_two = (758, 788)
line_three = (800, 830)
line_four = (847, 872)
line_five = (885, 918)
line_six = (930, 968)

line = sys.argv[2]

if line == "1":
    line = line_one
elif line == "2":
    line = line_two
elif line == "3":
    line = line_three
elif line == "4":
    line = line_four
elif line == "5":
    line = line_five
elif line == "6":
    line = line_six


# print(scan(image, line))





# print(scan(image, line_one))


# display(image, "Original Screenshot")

# cropped_image = image[712:745, 100:1000]
# left_border = 10
# right_border = 35


# # Display cropped image
# cv.imshow("cropped", cropped_image)

# # # pytesseract.pytesseract.tesseract_cmd = r'/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/pytesseract'
# 828 pixels wide

# image = cv.cvtColor(image, cv.COLOR_BGR2GRAY) 

# time = 0:100, 0:180 
# 1 = 712:745, 100:1000
# 2 = 
# 3 = [800:830] GOOD left to right
# 4 = [847:872, 550:620] GOOD left to right
# 5 = [885:918, 290:350] GOOD left to right
# 6 = 
# full = 710:975, 100:1000
# For three digits, let's say 60 pixels wide is the right 'width.' What's the right 'stride'?

# display(image[712:745, 125:1000], "sample")
# left_border = 798
# right_border = 828
# counter = 0
# scanned_image = str(pytesseract.image_to_string(image[758:786, left_border:right_border]))

# while scanned_image == "" and left_border > 0:
#     counter += 1
#     print(left_border)
#     print(right_border)
#     scanned_image = str(pytesseract.image_to_string(image[758:786, left_border:right_border]))
#     left_border -= 30
#     right_border -= 30
   
# print(scanned_image, type(scanned_image))

# blorp = pytesseract.image_to_string(image, config="-c tessedit_char_whitelist=0123456789")
# text = pytesseract.image_to_data(image, config="-c tessedit_char_whitelist=0123456789")
# print(text)
# print(blorp)
#image = cv.imread('/Users/carsonlepre/projects/wordle/OCR_proj/wordle.jpg')
# cv.imshow("image", image)


# cv.waitKey(0)
# cv.destroyAllWindows()

 
# Save the cropped image
# cv.imwrite("Cropped_Image.jpg", image)
# display(image, "cropped")
# cv.waitKey(0)
# cv.destroyAllWindows()


