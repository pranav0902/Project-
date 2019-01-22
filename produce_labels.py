import thecannon as tc
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import speed_of_light as c
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import pickle

np.random.seed(0)

dispersion = np.hstack([
    np.arange(4715.94, 4896.00, 0.046), # ab lines 4716.3 - 4892.3
    np.arange(5650.06, 5868.25, 0.055), # ab lines 5646.0 - 5867.8
    np.arange(6480.52, 6733.92, 0.064), # ab lines 6481.6 - 6733.4
    np.arange(7693.50, 7875.55, 0.074), # ab lines 7691.2 - 7838.5

])

model = tc.CannonModel.read('galah.model')

def generate_spectra(pixels,a1,b1,c1,d1,e1,f1,a2,b2,c2,d2,e2,f2,rv_1,rv_2): 
	stellar_labels_1 = np.array([a1,b1,c1,d1,e1,f1])
	stellar_labels_2 = np.array([a2,b2,c2,d2,e2,f2])
	model_flux_1 = model(stellar_labels_1).flatten()
	model_flux_2 = model(stellar_labels_2).flatten()
	pixels = dispersion
	pixels_of_1 = [wavelength*(1+(rv_1/c)) for wavelength in pixels]
	pixels_of_2 = [wavelength*(1+(rv_2/c)) for wavelength in pixels]
	f = interp1d(pixels_of_2,model_flux_2,bounds_error = False, fill_value = 'extrapolate')
	model_flux_2 = f(pixels_of_1)
	new_fluxes = model_flux_1*model_flux_2
	new_wavelengths = pixels_of_1
	return new_fluxes

def produce_labels(fluxes,pixels):
	pixels_of_1 = [wavelength*(1+(-100/c)) for wavelength in pixels]
	popt,pcov = curve_fit(generate_spectra,pixels_of_1,fluxes,bounds = ([4006,0.65,-2.23,0.94,3.06,0.0,4006,0.65,-2.23,0.94,3.06,0.0,-300,-300],[7431,4.74,0.52,2.64,29.45,0.4,7431,4.74,0.52,2.64,29.45,0.4,300,300]))
	return popt


