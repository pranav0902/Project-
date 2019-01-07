from glob import glob
import os
import numpy as np
import thecannon as tc
from astropy.table import Table,vstack
blue_paths = glob('GALAH_median_spectra/T*/g[4-6]*/*_1.csv')
green_paths = glob('GALAH_median_spectra/T*/g[4-6]*/*_2.csv')
red_paths = glob('GALAH_median_spectra/T*/g[4-6]*/*_3.csv')
infrared_paths = glob('GALAH_median_spectra/T*/g[4-6]*/*_4.csv')
all_paths = blue_paths + green_paths + red_paths + infrared_paths

def extract_labels(path):
	filename = os.path.basename(path)
	teff = float(filename[1:5])
	logg = float(filename[6:8])/10
	mettalicity = float(filename[8:11].replace('p','+').replace('m','-'))/10
	
	return teff,logg,mettalicity

#for path in blue_paths:
#	print(path,extract_labels(path))

S = len(all_paths)
L = 3

labels = np.zeros((S,L))
for i,path in enumerate(all_paths):
	labels[i] = extract_labels(path)

labels = Table(data = labels,names = ('teff', 'logg', 'fe_h'))

'''for file in blue_paths:
	with open(file) as data:
		print(file,len(data.readlines()))'''

def load_spectra(blue_path):
	#base = blue_paths[-1][:-6]
	#all_paths = [f'{base}_{i}.csv' for i in range(1,5)]
	#spectra = [Table.read(path,data_start = 2, names = ('lambda','flux')) for path in blue_path]
	spectra2 = Table.read(blue_path,data_start = 2, names = ('lambda','flux'))
	return spectra2
S1 = load_spectra(blue_paths[45])

S2 = load_spectra(blue_paths[597])

P = len(S1)
fluxes = np.zeros((S,P))


for i,path in enumerate(all_paths):
	fluxes[i] = load_spectra(path)['flux']

ivars = 10000*np.ones_like(fluxes)

vectoriser = tc.vectorizer.PolynomialVectorizer(('teff','logg','fe_h'),1)

model = tc.CannonModel(labels,fluxes,ivars,vectoriser)

model.train()
test_labels,test_cov,test_meta=model.test(fluxes,ivars)
labels[57]
model([labels[ln][57] for ln in labels.dtype.names])

wavelengths = np.zeros((S,P))

for i,path in enumerate(blue_paths):
	wavelengths[i] = load_spectra(path)['lambda']




