from ezc3d import c3d

import numpy as np
import matplotlib.pyplot as plt
from pykalman import KalmanFilter

import sys, os


#
# I make no appologies for using hard tabs to indent. %$*# the Python style guide,
# hard-tabs are the _right_ approach.
#



#
# Function to plot a track
#
def Plot( points, resids ):
	x = points[0,:,:]
	y = points[1,:,:]
	z = points[2,:,:]
	w = resids[0,:,:]
	
	print(x.shape)
	for jc in range( x.shape[0] ):
		plt.subplot(4,1,1)
		plt.plot( x[jc,:] )
		plt.subplot(4,1,2)
		plt.plot( y[jc,:] )
		plt.subplot(4,1,3)
		plt.plot( z[jc,:] )
		plt.subplot(4,1,4)
		plt.plot( w[jc,:] )
	plt.show()



#
# Function to run a Kalman smoother given noise estimates.
#

def KalmanSmoothTrack( trk, tNoise, mNoise ):
	tm = np.array( [ [1,0,0,  1,0,0,  1,0,0],
	                 [0,1,0,  0,1,0,  0,1,0],
	                 [0,0,1,  0,0,1,  0,0,1],
	                 
	                 [0,0,0,  1,0,0,  1,0,0],
	                 [0,0,0,  0,1,0,  0,1,0],
	                 [0,0,0,  0,0,1,  0,0,1],
	                 
	                 [0,0,0,  0,0,0,  1,0,0],
	                 [0,0,0,  0,0,0,  0,1,0],
	                 [0,0,0,  0,0,0,  0,0,1] ]  )
	
	iState = [ trk[0,0],
	           trk[0,1],
	           trk[0,2],
	           trk[1,0] - trk[0,0],
	           trk[1,1] - trk[0,1],
	           trk[1,2] - trk[0,2],
	           0,
	           0,
	           0                    ]
	
	kf = None
	if tNoise < 0 and mNoise < 0:
		kf = KalmanFilter(transition_matrices=tm,
		                  em_vars=['transition_covariance', 'observation_covariance'], 
		                  initial_state_mean = iState,
		                  n_dim_obs=3)
		kf.em(trk)
	elif tNoise < 0 and mNoise >= 0:
		mCov = mNoise * np.eye(3, dtype=np.float32)
		kf = KalmanFilter(transition_matrices=tm,
		                  em_vars=['transition_covariance'], 
		                  observation_covariance = mCov,
		                  initial_state_mean = iState,
		                  n_dim_obs=3)
		kf.em(trk)
	elif tNoise >= 0 and mNoise < 0:
		tCov = tNoise * np.eye(9, dtype=np.float32)
		kf = KalmanFilter(transition_matrices=tm,
		                  em_vars=['observation_covariance'], 
		                  transition_covariance = tCov,
		                  initial_state_mean = iState,
		                  n_dim_obs=3)
		kf.em(trk)
	else:
		tCov = tNoise * np.eye(9, dtype=np.float32)
		mCov = mNoise * np.eye(3, dtype=np.float32)
		kf = KalmanFilter(transition_matrices=tm,
		                  transition_covariance = tCov,
		                  observation_covariance = mCov,
		                  initial_state_mean = iState,
		                  n_dim_obs=3)
	
	
	#print( kf.transition_covariance  )
	#print( kf.observation_covariance )
	
	
	
	
	
	res = kf.smooth( trk )
	
	print(res[0].shape)
	
	#plt.plot(trk[:,2], label="trk")
	#plt.plot(res[0][:,2], label="res")
	#plt.legend()
	#plt.show()
	#exit(0)
	
	return res[0]



#
# Linearly interpolate if we're missing values.
#
def HandleMissing( points, resids ):
	
	print( points.shape, resids.shape )
	npoints = points.copy()
	nresids = resids.copy()
	firstValid = 0
	finalValid  = points.shape[2]
	for kpc in range( points.shape[1] ):
		
		# find the first valid frame
		minfc = 0
		while resids[0, kpc, minfc] <= 0:
			minfc += 1
		
		firstValid = max(firstValid, minfc)
		
		lastValid = minfc
		invalid = False
		for fc in range( minfc, points.shape[2] ):
			if resids[0,kpc,fc] > 0:
				if invalid:
					for ifc in range( lastValid+1, fc ):
						v = (ifc-lastValid) / (fc-lastValid)
						for k in range(3):
							npoints[k,kpc,ifc] = points[k, kpc, lastValid] + v * (points[k,kpc,fc] - points[k,kpc,lastValid])
						npoints[3,kpc,ifc] = 1.0
						nresids[0,kpc,ifc] = 1.0
				lastValid = fc
				invalid = False
			else:
				invalid = True
		
		finalValid = min( finalValid, lastValid )
	
	
	return (npoints, nresids, firstValid, finalValid )

def FindFiles(path):
	print(f"[INFO] - Searching for files beneath: {path}")
	retFiles = []
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith(".c3d") and file.find("-filled") < 0 and file.find("-smoothed") < 0:
				pth = os.path.join(root,file)
				retFiles.append(pth)
	return retFiles


if len(sys.argv) < 2:
	print("This is a tool to fill, smooth and plot a .c3d file using a Kalman filter.")
	print("Usage: ")
	print(sys.argv[0], " True ")
	print(sys.argv[0], " False <trans noise> <obs noise> < file00.c3d > [ file01.c3d] ... [ file##.c3d ] ")
	print(" - or - ")
	print("output will be to:")
	print("file00.c3d -> (file00-filled.c3d, file00-smoothed.c3d)")
	exit(0)

assert( sys.argv[1] == "True" or sys.argv[1] == "False" )

files = []
tNoise = 0.01
obsNoise = 15.0
if sys.argv[1] == "True":
	import config
	files = FindFiles( config.PATH )
	tNoise = config.KALMAN_TRANS_NOISE
	obsNoise = config.KALMAN_OBS_NOISE
else:
	assert( len(sys.argv) > 4 )
	tNoise = float( sys.argv[2] )
	obsNoise = float( sys.argv[3] )
	files = sys.argv[4:]
	
print(f"[INFO] - Got: {len(files)} files")
for f in files:
	
	print(f"[INFO] - Processing: {f}")
	track = c3d( f )
	
	points = track['data']['points']
	resids = track['data']['meta_points']['residuals']
	
	(fpoints, fresids, firstValid, lastValid) = HandleMissing( points, resids )
	
	track['data']['points'] = fpoints
	track['data']['meta_points']['residuals'] = fresids
	
	a = f.rfind('.c3d')
	filledFilename = f[:a] + "-filled.c3d"
	
	print("writing: ", filledFilename )
	track.write( filledFilename )
	
	kpoints = fpoints.copy()
	for kpc in range( points.shape[1] ):
		trk = kpoints[:3,kpc,firstValid:lastValid].transpose()
		trkSmooth = KalmanSmoothTrack( trk, tNoise, obsNoise )
		kpoints[:3,kpc,firstValid:lastValid] = trkSmooth.transpose()[:3,:]
	
	smoothedFilename = f[:a] + "-smoothed.c3d"
	
	track['data']['points'] = kpoints
	track['data']['meta_points']['residuals'] = fresids
	
	print("writing: ", smoothedFilename )
	track.write( smoothedFilename )
	
	#Plot( points, resids  )
	#Plot( fpoints, fresids )
	#Plot( kpoints, fresids )
	#exit(0)
	
	
