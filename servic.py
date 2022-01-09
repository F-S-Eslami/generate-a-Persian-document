#creating dateset for 992 computer vision project
import pandas as pd
import cv2
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import ImageFont, Image, ImageDraw
import os
from random import randint
from sys import exit
from openpyxl import Workbook, load_workbook

#<functions>----------------------------------------------------------------------------------------
def change_color(img_src, color_bgr):
	img_copy = img_src.copy()
	for i in range(img_copy.shape[0]):
		for j in range(img_copy.shape[1]):
			img_copy[i][j] = color_bgr

	return img_copy

#---------------------------------------------------------------------
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename),1)
        img = cv2.resize(img, (170, 240))
        if img is not None:
            images.append(img)

    return images	
#---------------------------------------------------------------------
def gen_date(lower_year, upper_year):
	year = str(randint(lower_year, upper_year))
	month = str(randint(1, 12))
	day = str(randint(1, 30))

	date = ""
	date += year + " / " + month + " / " + day

	return date
#---------------------------------------------------------------------
def gen_code(upper_range):
	passno = ""
	passno += str(randint(1, 9))
	for i in range(upper_range-1):
		passno += str(randint(0, 9))

	return passno
#--------------------------------------------------------------------


#<reading img>
img = cv2.imread("templet/ghadim.jpg", 1)
# print(img.shape)


#<file handling>
faces_folder = "men/"
faces_list = load_images_from_folder(faces_folder)
print(len(faces_list))

#<excel>
wb = Workbook()
row_excel = wb.active
page_excel = [( "filename", "data", "x", "y", "w",'h')]


#<face>
for i in range(1):
	
	individual = faces_list[i]
	
	individual_gray = cv2.cvtColor(individual, cv2.COLOR_BGR2GRAY)
	
	
	for row in range(individual.shape[0]):
		for col in range(individual.shape[1]):
			if individual[row][col][0] != 255 and individual[row][col][1] != 255 and individual[row][col][2] != 255:
			
				img[row+150][col+50] = individual[row][col]
	

#<fonts>
fontaddress_2compset =  """fonts/SCOMPSET.TTF"""
font_2compset = ImageFont.truetype(fontaddress_2compset, 26)

fontaddress_2koodak =  """fonts/SKOODKBD.TTF"""
font_2koodak = ImageFont.truetype(fontaddress_2koodak, 46)

#<reading information from txt file>

#<city>

cities = open("inputFile/cities.txt", "r", encoding="utf8")
cities_list = cities.readlines()


#<surnames>
file = "inputFile/lname.xlsx" 
df = pd.read_excel(file)
surnames_list = list(df['name'])

file = "inputFile/rank.xlsx" 
df = pd.read_excel(file)
rank = list(df['name'])


#<names men>
file = "inputFile/pesar.xlsx" 
df = pd.read_excel(file)
names_men_list= list(df['name'])

j=0
for i in range(1):
	# j=j+1
	# i=i+1

	#<CV to PTL>
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = Image.fromarray(img)
	#</CV to PTL>
	
	file_name=f"img1#{j}"

#<text farsi>

#<surname farsi>
	surname =surnames_list[randint(0, len(surnames_list)-1)]

	reshaped_surname = arabic_reshaper.reshape(surname)
	bidi_text = get_display(reshaped_surname)

	draw_surname = ImageDraw.Draw(img)
	draw_surname.text((560, 225), bidi_text, (1, 2, 3), font=font_2compset)

#------------------------------------------------------------------------------------------------
	row_info = (file_name,  surname ,560, 225, 60,25)
	page_excel.append(row_info)
#------------------------------------------------------------------------------------------------



#<name farsi>
	name = names_men_list[randint(0, len(names_men_list)-1)]


	reshaped_name = arabic_reshaper.reshape(name)
	bidi_text = get_display(reshaped_name)

	draw_name = ImageDraw.Draw(img)
	draw_name.text((610, 170), bidi_text, (1, 2, 3), font=font_2compset)

#------------------------------------------------------------------------------------------------
	row_info = (file_name,  name, 610, 170 ,60 , 25)
	page_excel.append(row_info)
#------------------------------------------------------------------------------------------------



#<father name farsi>
	father = names_men_list[randint(0, len(names_men_list)-1)]

	reshaped_father = arabic_reshaper.reshape(father)
	bidi_text = get_display(reshaped_father)

	draw_father = ImageDraw.Draw(img)
	draw_father.text((630, 264), bidi_text, (1, 2, 3), font=font_2compset)

#------------------------------------------------------------------------------------------------
	row_info = (file_name, father, 630, 264, 60 , 25)
	page_excel.append(row_info)
#------------------------------------------------------------------------------------------------


	passno = gen_code(10)

	reshaped_passno = arabic_reshaper.reshape(passno)
	bidi_text = get_display(reshaped_passno)

	draw = ImageDraw.Draw(img)
	draw.text((570, 350), bidi_text, (1, 2, 3), font=font_2compset)

#------------------------------------------------------------------------------------------------
	row_info = (file_name, passno, 570, 350, 160, 25)
	page_excel.append(row_info)
#------------------------------------------------------------------------------------------------

#<birth date farsi>
	birthdate = gen_date(1320, 1390)


	reshaped_birthdate = arabic_reshaper.reshape(birthdate)
	bidi_text = get_display(reshaped_birthdate)

	draw_birthdate = ImageDraw.Draw(img)
	draw_birthdate.text((520, 285), bidi_text, (1, 2, 3), font=font_2compset)

#------------------------------------------------------------------------------------------------
	row_info = (file_name, birthdate, 520, 285 ,150 , 25)
	page_excel.append(row_info)
#------------------------------------------------------------------------------------------------



#/<text farsi>

#<PTL to CV>
	img = np.array(img)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#</PTL to CV>

	for new_i, (file_name,info, x, y,w,h) in enumerate(page_excel):
	    	row_excel[f"A{new_i+1}"] = file_name
	    	row_excel[f"B{new_i+1}"] = info
	    	row_excel[f"C{new_i+1}"] = x
	    	row_excel[f"D{new_i+1}"] = y
	    	row_excel[f"E{new_i+1}"] = w
	    	row_excel[f"F{new_i+1}"] = h

	
	cv2.imwrite(f"saves/img1#{j}.jpg", img)


#<save excel>
wb.save(filename="Book1.xlsx")


