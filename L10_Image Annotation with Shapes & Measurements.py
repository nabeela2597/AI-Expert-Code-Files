1 import cv2
2 import matplotlib.pyplot as plt
3
4 # Step 1: Load the Image
5 image_path = 'sample.jpg' # User-provided image path
6 image_rgb = cv2.imread(image_path)
7
8 # Convert BGR to RGB for correct color display with matplotlib
9 image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB)
10
11 # Get image dimensions
12 height, width, _ = image_rgb.shape
13
14 # Step 2: Draw Two Rectangles Around Interesting Regions
15 # Rectangle 1: Top-Left Region
16 rect1_width, rect1_height = 150, 150
17 top_left1 = (20, 20) # Fixed 20 pixels padding from top-left
18 bottom_right1 = (top_left1[0] + rect1_width, top_left1[1] + rect1_height)
19 cv2.rectangle(image_rgb, top_left1, bottom_right1, (0, 255, 255), 3) # Yellow rectangle
20
21 # Rectangle 2: Bottom-Right Region
22 rect2_width, rect2_height = 200, 150
23 top_left2 = (width - rect2_width - 20, height - rect2_height - 20) # 20 pixels padding
24 bottom_right2 = (top_left2[0] + rect2_width, top_left2[1] + rect2_height)
25 cv2.rectangle(image_rgb, top_left2, bottom_right2, (255, 0, 255), 3) # Magenta rectangle
26
27 # Step 3: Draw Circles at the Centers of Both Rectangles
28 center1_x = top_left1[0] + rect1_width // 2
29 center1_y = top_left1[1] + rect1_height // 2
30 center2_x = top_left2[0] + rect2_width // 2
31 center2_y = top_left2[1] + rect2_height // 2
32 cv2.circle(image_rgb, (center1_x, center1_y), 15, (0, 255, 0), -1) # Filled green circle
33 cv2.circle(image_rgb, (center2_x, center2_y), 15, (0, 0, 255), -1) # Filled red circle
34
35 # Step 4: Draw Connecting Lines Between Centers of Rectangles
36 cv2.line(image_rgb, (center1_x, center1_y), (center2_x, center2_y), (0, 255, 0), 3)
37
38 # Step 5: Add Text Labels for Regions and Centers
39 font = cv2.FONT_HERSHEY_SIMPLEX
40 cv2.putText(image_rgb, 'Region 1', (top_left1[0], top_left1[1] - 10), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
41 cv2.putText(image_rgb, 'Region 2', (top_left2[0], top_left2[1] - 10), font, 0.7, (255, 0, 255), 2, cv2.LINE_AA)
42 cv2.putText(image_rgb, 'Center 1', (center1_x - 40, center1_y + 40), font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
43 cv2.putText(image_rgb, 'Center 2', (center2_x - 40, center2_y + 40), font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
44
45 # Step 6: Add Bi-Directional Arrow Representing Height
46 arrow_start = (width - 50, 20) # Start near the top-right
47 arrow_end = (width - 50, height - 20) # End near the bottom right
48
49 # Draw arrows in both directions
50 cv2.arrowedLine(image_rgb, arrow_start, arrow_end, (255, 255, 0), 3, tipLength=0.05) # Downward arrow
51 cv2.arrowedLine(image_rgb, arrow_end, arrow_start, (255, 255, 0), 3, tipLength=0.05) # Upward arrow
52
53 # Annotate the height value
54 height_label_position = (arrow_start[0] - 150, (arrow_start[1] + arrow_end[1]) // 2)
55 cv2.putText(image_rgb, 'H=' + str(height) + 'px', height_label_position, font, 0.8, (255, 255, 0), 2, cv2.LINE_AA)
56
57 # Step 7: Display the Annotated Image
58 plt.figure(figsize=(12, 8))
59 plt.imshow(image_rgb)
60 plt.title('Annotated Image with Regions, Centers, and Bi-Directional Height Arrow')
61 plt.axis('off')
62 plt.show()
