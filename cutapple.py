# use labelImg to label VOC Format, then use this to cut target object. 

import cv2 
import numpy as np
import os

import xml.etree.ElementTree as Et
from xml.etree.ElementTree import Element, ElementTree

def parseAndGenerateImg():
	path = os.getcwd() + "/Labels"
	print("curpath: ", path)
	(dir_path, dir_names, filenames) = next(os.walk(os.path.abspath(path)))

	boxCount = 0
	for filename in filenames:
		xmlPath = os.path.join(dir_path, filename)
		xml = open(xmlPath, "r")
		tree = Et.parse(xml)
		root = tree.getroot()

		imagePath = root.find("path").text

		xml_size = root.find("size")
		size = {
			"width": xml_size.find("width").text,
			"height": xml_size.find("height").text,
			"depth": xml_size.find("depth").text
		}

		objects = root.findall("object")
		if len(objects) == 0:
			return False, "number object zero"

		obj = {
			"num_obj": len(objects)
		}

		print("filename", imagePath)

		obj_index = 0
		imageInfo = cv2.imread(imagePath)
		for _object in objects:
			tmp={
	            "name": _object.find("name").text
	        }

			xml_bndbox = _object.find("bndbox")
			bndbox = {
				"xmin": int(xml_bndbox.find("xmin").text),
				"ymin": int(xml_bndbox.find("ymin").text),
				"xmax": int(xml_bndbox.find("xmax").text),
				"ymax": int(xml_bndbox.find("ymax").text)
			}
			tmp["bndbox"] = bndbox
			obj[str(obj_index)] = tmp
			
			obj_index += 1
			print("bndbox", bndbox)

			imgBox = imageInfo[bndbox["ymin"]:bndbox["ymax"], bndbox["xmin"]:bndbox["xmax"]]
			if not os.path.exists('objects/scale'):
				os.makedirs('objects/scale')

			cv2.imwrite("objects/"+filename+str(obj_index)+".jpg", imgBox)
	
			resized_image = cv2.resize(imgBox, (50, 50))
			cv2.imwrite("objects/scale/object"+str(boxCount)+".jpg", resized_image)

			boxCount += 1



parseAndGenerateImg()