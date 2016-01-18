# Made by : Anshuman Suri

import numpy as np
import cv2
import sys

if len(sys.argv) < 4:
	print "Format : python self_flow.py <image1> <image2> window_size"
	exit()

try:
	img_in = cv2.imread(sys.argv[1])
	img2_in = cv2.imread(sys.argv[2])
except:
	print "Error reading files"
	exit()

img = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2_in, cv2.COLOR_BGR2GRAY)

def window_flow(window,window2):
	Ix = np.zeros(window.shape)
	Iy = np.zeros(window.shape)
	It = np.zeros(window.shape)
	Ix[:,1:] = window[:,1:] - window[:,:-1]
	Iy[1:,] = window[1:,:] - window[-1:,:]
	It = window2 - window
	Ix_Ix = np.sum(np.square(Ix))
	Iy_Iy = np.sum(np.square(Iy))
	Ix_Iy = np.sum(Ix*Iy)
	Ix_It = np.sum(Ix*It)
	Iy_It = np.sum(Iy*It)
	mat1 = np.matrix([[Ix_Ix,Ix_Iy],[Ix_Iy,Iy_Iy]])
	mat2 = np.matrix([[-Ix_It],[-Iy_It]])
	try:
		ans = np.linalg.inv(mat1) * mat2
	except:
		# Singular matrix : assuming negligible motion 
		ans = [0,0]
	return ans
		# u is along X axis,v is along Y axis

def pyramid_transition(imag,imag2,initial,iters=10):
	# print "Error",np.sum((imag-imag2)**2)
	iterations = 0
	u,v = initial
	while iterations < iters:
		ret = window_flow(imag,imag2)
		u,v = u+ret[0],v+ret[1]
		print u,v
		temp = imag
		if(int(round(u))>0):
			temp[:,int(round(u)):] = imag[:,:-int(round(u))]
		elif(int(round(u))<0):
			temp[:,:int(round(u))] = imag[:,-int(round(u)):]
		if(int(round(v))>0):
			temp[int(round(v)):,:] = imag[:-int(round(v)),:]
		elif(int(round(v))<0):
			temp[:int(round(v)),:] = imag[-int(round(v)):,:]
		imag = temp
		# print "Error",np.sum((imag-imag2)**2)
		iterations += 1
	return [u/2,v/2]


def pyramid(l1_1,l1_2):
	l2_1,l2_2 = l1_1[::2,::2],l1_2[::2,::2]
	l3_1,l3_2 = l2_1[::2,::2],l2_2[::2,::2]
	l4_1,l4_2 = l3_1[::2,::2],l3_2[::2,::2]
	l5_1,l5_2 = l4_1[::2,::2],l4_2[::2,::2]
	x = [0,0]
	x = pyramid_transition(l5_1,l5_2,x)
	x = pyramid_transition(l4_1,l4_2,x)
	x = pyramid_transition(l3_1,l3_2,x)
	x = pyramid_transition(l2_1,l2_2,x)
	x = pyramid_transition(l1_1,l1_2,x)
	return x

# Main :
f_x,f_y = pyramid(img,img2)	
print "Flow is ",f_x," , ",f_y
	
# i=0
# j=0
# window_size = sys.argv[3]
# template = img2_in
# x = window_flow(img,img2)
# print x

# Uncomment to calculate flow on whole image
# threshold = 10
# abs_error = np.sum((img-img2)**2)
# iterations = 0
# while abs_error > threshold:
# while iterations < 100:
# 	u,v = window_flow(img,img2)
# 	print u,v
# 	temp = img
# 	if(int(round(u))>0):
# 		temp[:,int(round(u)):] = img[:,:-int(round(u))]
# 	elif(int(round(u))<0):
# 		temp[:,:int(round(u))] = img[:,-int(round(u)):]
# 	if(int(round(v))>0):
# 		temp[int(round(v)):,:] = img[:-int(round(v)),:]
# 	elif(int(round(v))<0):
# 		temp[:int(round(v)),:] = img[-int(round(v)):,:]
# 	img = temp
# 	abs_error = np.sum((img-img2)**2)
# 	iterations += 1

# point1 = (c/2 , r/2)
# point2 = (int(round(c/2+u)) , int(round(r/2+v)))
# cv2.arrowedLine(template,point1,point2,(255,0,0),3)
# cv2.imwrite('Optical Flow.jpg',template)
# exit()

# Uncomment to calculate flow on windows
# flow_x = np.zeros((r/window_size+1,c/window_size+1))
# flow_y = np.zeros((r/window_size+1,c/window_size+1))

# for i in range(r/window_size):
# 	for j in range(c/window_size):
# 		flow_x[i,j],flow_y[i,j] = window_flow(img[window_size*i:window_size*i+window_size,window_size*j:window_size*j+window_size],img2[window_size*i:window_size*i+window_size,window_size*j:window_size*j+window_size])

# img_x = np.zeros(img.shape)
# img_y = np.zeros(img.shape)
# for i in range(r):
# 	for j in range(c):
# 		img_x[i,j] = flow_x[i/window_size,j/window_size]
# 		img_y[i,j] = flow_y[i/window_size,j/window_size]			

# for i in range(r/window_size):
# 	for j in range(c/window_size):
# 		point1 = (j*window_size+(window_size/2) , i*window_size+(window_size/2))
# 		point2 = (int(round(j*window_size+(window_size/2)+flow_x[i,j])) , int(round(i*window_size+(window_size/2)+flow_y[i,j])))
# 		cv2.arrowedLine(template,point1,point2,(255,0,0))
# cv2.imwrite('Optical Flow(5x5).jpg',template)