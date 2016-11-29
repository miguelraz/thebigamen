#NifTI to .txt 128x128x43 matrix converter python script by Miguel Raz
# Nov.23, 2016
#V1.0

#Script explained:
#This script will use the NiBabel pythod module to open up .img files using their respective
# .hdr files, read their dimension, skim off an extra empty one, and copy them into
# a Comma Separated Value matrix in a .txt file.

#Note1:Since some of the files from the whole trove we used sometimes threw an error,
#I hacked a conditional when reading the filenames so as to not start from scratch.
#Be mindful of uncommenting said block (mentioned below) or reassigning folder names
#to make the hack workable. The files were called oddballs and I put them into a different
#directory where the whole tar ball will also be uploaded.


#Modules for importing our nifty functions
import os
import numpy as np
import nibabel as nib
import fnmatch

#Begin a huge loop in Python considering all files in the current directory
for filename in os.listdir('.'):
    #Iterate over filenames if they start with '*.img', or if they are in a files already looped over
    if fnmatch.fnmatch(filename, '*.img') and filename not in os.listdir('donefiles'):

        #Sanity check
        print filename
#         Note1: This is the little hack loop. We open the folder 'donefiles', write
#               the name of the file, and pop out again. This will make the if conditional
#               above not process the same files again.
#        os.chdir('donefiles')
#        FILE = open(filename,"w")
#        FILE.close()
#        os.chdir('..')

        #Standard Nibabel commands to read basic data from the .img files from its header
        img = nib.load(filename)
        array_data = np.arange(24, dtype=np.int16).reshape((2, 3, 4))
        affine = np.diag([1, 2, 3, 1])
        array_img = nib.Nifti1Image(array_data, affine)

        #This handily reads the data of the .img specifications
        nibabel_data = img.get_data()

        #Trim off the extra empty dimension
        nibabel_data= np.squeeze(nibabel_data)

        x,y,z = nibabel_data.shape

        torch_data = np.zeros((128,128,43))

        #Our copying loop
        for k in range(0,42):
            if k == z:
                break

            for j in range(0,127):
                for i in range(0,127):
                    torch_data[i,j,k] = nibabel_data[i,j,k]

        #We have to remember to rename the files as they were originally, but preserving
        #the '.txt' ending, and we do so with the next string manipulations
        filename = filename[:-4]
        filename = filename + '.txt'

        #Our Writing loop, which handily uses the [:,:, index] construct. Thanks Kuba Karpierz!
        with file(filename, 'w') as outfile:
            for index in range(0, 42):
                outfile.write('# New Slice \n')
                np.savetxt(outfile, torch_data[:,:,index], fmt='%-0d',delimiter=',')
