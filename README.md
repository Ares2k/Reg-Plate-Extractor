# Reg-Plate-Extractor
Extracts the registration plate contents from a car image and overlays it highlighting the reg plate location.<br><br>

Before             |  After
:-------------------------:|:-------------------------:
![car1](https://user-images.githubusercontent.com/40499701/153950583-8630a554-2c5c-4b61-aebd-9f6aa40dcc20.png) | ![image](https://user-images.githubusercontent.com/40499701/153951154-88618a14-7516-4021-99e6-1ea089a266f5.png)



Before             |  After
:-------------------------:|:-------------------------:
![car3](https://user-images.githubusercontent.com/40499701/153952570-023ffec9-0f9c-4bbf-86d0-9f008d846f11.png) | ![image](https://user-images.githubusercontent.com/40499701/153951764-447f7e93-091d-43c8-88c2-afd35da8e4e3.png)


## How the program works
#### 1. Edge Detection
This is required since the only logical approach in extracting the number from a license plate is to identify the region where it is located in. This will make it easier as approximately 95% of the image will be cropped out making our lives easier. The result of this process can be seen below:

![image](https://user-images.githubusercontent.com/40499701/153949352-aa5263c8-2da8-4ae2-8b3b-21d079e7ff9a.png)<br>


#### 2. Locating Contours
The next step is to identify the contours on the image. This would help identify curves and points where lines meet. The result of identifying contours can be seen on another image (clearer demonstration):

![image](https://user-images.githubusercontent.com/40499701/153949698-6df3909a-52f0-498d-82f3-ee6868b44651.png)<br>

#### 3. Identifying Polygons
Now that we have our contoured image, it's important to identify polygons so that a particular shape could be identified (a rectangle with 4 points), which is our license plate. Once the contours have been identified (stored in the format of a sorted array), we go through the contours and look for a rectangle of length 4 (since rectangle is 4 sided). We iterate over the contours and grab all the points. As notable from the image below, we have each corner of the license plate with its corresponding coordinate on the image, so now we can crop it and create a mask:

![image](https://user-images.githubusercontent.com/40499701/153950113-3898d557-7ea2-44ff-aa97-fc510da9dabc.png)<br>

#### 4. Creating a contoured mask
Once the coordinates of the license plate have been identified, we can simply create a contoured mask, turn it into a gray scaled image and use the EasyOCR library to extract the text:

![image](https://user-images.githubusercontent.com/40499701/153953053-c739991d-bc6d-421e-b0f2-cc151bad803a.png)

#### 5. Overlay our final product
All that's left is to overlay the extracted registration plate contents over our original image. Job done!

![image](https://user-images.githubusercontent.com/40499701/153953359-5b6d125b-5c7c-4261-84ec-8b2f1f43d3e4.png)



