# Modules:
## enviroment:
import random as rd
import numpy as np

## local:


def genCigar(R1, R2, c, n_points, rot_angle=0.0):
	'''
	Generate cigar shape cluster with:
		r1 :: max radius
		r2 :: min radius
		theta :: inclination angle
		c :: center
		'''

	# rotation matrix
	rotation = getRotationMatrix(rot_angle)

	points = np.empty([n_points,2])
	for i in range(n_points):
		r1 = rd.uniform(0, R1)
		r2 = rd.uniform(0, R2)
		theta = rd.uniform(0, 2*np.pi)
		points[i] = rotation @ np.array([
			r1*np.cos(theta),
			r2*np.sin(theta)]) + c
	
	return points

def genDisk(R, c, n_points):

	return genCigar(R, R, c, n_points, rot_angle=0.0)

def genAnnulus(
	R1, R2, c, n_points, 
	theta_start=0, theta_stop=2*np.pi):
	'''
	Generate an annulus cluster of points in [0,1]^2 with:
		c :: ring center
		R1 :: inner radius
		R2 :: outer radius
	'''
	points = np.empty([n_points,2])
	for i in range(n_points):
		r = rd.uniform(R1, R2)
		theta = rd.uniform(theta_start, theta_stop)
		points[i] = np.array([
			r*np.cos(theta) + c[0],
			r*np.sin(theta) + c[1]])

	return points


def genCross(w, h, t, c, n_points, rot_angle=0.0):
	'''
	Generate a cross with
		w :: width
		h :: height
		t :: thickness
		c :: center (2-tuple)
	'''

	# rotation matrix
	rotation = getRotationMatrix(rot_angle)

	c2 = (c[0],c[1]+(h+t)/4)
	c3 = (c[0],c[1]-(h+t)/4)

	Vol = w*t + (h-t)*t
	f1 = w*t/Vol
	f2 = 0.5*t*(h-t)/Vol

	n2 = int(f2*n_points)
	n1 = n_points - 2*n2

	points = np.concatenate(
		(genRect(w,t,c,n1), 
			genRect(t,(h-t)/2,c2,n2),
			genRect(t,(h-t)/2,c3,n2)),
		axis=0)

	for i in range(n_points):
		points[i] = rotation @ (points[i]-c) + c

	return points


def genRect(w, h, c, n_points):
	'''
	Generate a rectange, with
		w :: width
		h :: height
		c :: center
	'''
	points = np.empty([n_points,2])

	for i in range(n_points):
		x = rd.uniform(c[0]-0.5*w, c[0]+0.5*w)
		y = rd.uniform(c[1]-0.5*h, c[1]+0.5*h)

		points[i] = [x,y]

	return points

def genS(h, t, c, n_points):
	'''
	Generate S shape with:
		w :: width
		h :: height
		t :: thickness
		c :: center
	'''

	w = 0.5*h

	ctop = (c[0],c[1]+(h-t)/4)
	cbot = (c[0],c[1]-(h-t)/4)

	n1 = int(0.5*n_points)
	n2 = n_points - n1

	points = np.concatenate(
		(
			genAnnulus((h-3*t)/4,(h+t)/4,ctop,n1, theta_start=0, theta_stop=1.5*np.pi),
			genAnnulus((h-3*t)/4,(h+t)/4,cbot,n2, theta_start=np.pi, theta_stop=2.5*np.pi)), 
		axis=0)

	return points

def genEight(h, t, c, n_points):
	'''
	Generate figure 8 with:
		w :: width
		h :: height
		t :: thickness
		c :: center
	'''

	w = 0.5*h

	ctop = (c[0],c[1]+(h-t)/4)
	cbot = (c[0],c[1]-(h-t)/4)

	n1 = int(0.5*n_points)
	n2 = n_points - n1

	points = np.concatenate(
		(
			genAnnulus((h-3*t)/4,(h+t)/4,ctop,n1, theta_start=-0.77*np.pi, theta_stop=1.5*np.pi),
			genAnnulus((h-3*t)/4,(h+t)/4,cbot,n2, theta_start=0.75*np.pi, theta_stop=2.5*np.pi)), 
		axis=0)

	return points

def genGauss(c, st0, st1, n_points, rot_angle=0.0):

	points = np.empty([n_points,2])

	points[:,0] = np.random.normal(c[0],st0,n_points)
	points[:,1] = np.random.normal(c[1],st1,n_points)

	# rotation matrix
	rotation = getRotationMatrix(rot_angle)
	for i in range(n_points):
		points[i] = rotation @ (points[i]-c) + c

	return points
	


def getRotationMatrix(rot_angle):
	# rotation matrix
	return np.array(
		[[np.cos(rot_angle), np.sin(rot_angle)],
		[-np.sin(rot_angle), np.cos(rot_angle)]])