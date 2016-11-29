# This is a script that takes NiFTI Brainscan images and transforms then to .csv files.
# 1.0 version by mrg -
# Nov. 22,2016.

import os
import numpy as np
import nibabel as nib
import fnmatch


for filename in os.listdir('.'):
    if fnmatch.fnmatch(filename, '*.img'):
        print filename

        img = nib.load(filename)
        array_data = np.arange(24, dtype=np.int16).reshape((2, 3, 4))
        affine = np.diag([1, 2, 3, 1])
        array_img = nib.Nifti1Image(array_data, affine)
        nibabel_data = img.get_data()

        nibabel_data= np.squeeze(nibabel_data)
        x,y,z = nibabel_data.shape

        torch_data = np.zeros((128,128,43))
        #Our copying loop
        for k in range(0,42):
        	if k == z:
        	    break

        	for j in range(0,127):
                    print "j", j
            	    for i in range(0,127):
            	        torch_data[i,j,k] = nibabel_data[i,j,k]
                        print "check i", i
    with file('test2.txt', 'w') as outfile:
    	for index in range(0, 42):
    	    outfile.write('# New Slice \n')
    	    np.savetxt(outfile, torch_data[:,:,index], fmt='%-0d',delimiter=',')
