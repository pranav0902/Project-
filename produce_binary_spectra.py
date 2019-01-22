import thecannon as tc
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import speed_of_light as c
from scipy.interpolate import interp1d

np.random.seed(0)

dispersion = np.hstack([
    np.arange(4715.94, 4896.00, 0.046), # ab lines 4716.3 - 4892.3
    np.arange(5650.06, 5868.25, 0.055), # ab lines 5646.0 - 5867.8
    np.arange(6480.52, 6733.92, 0.064), # ab lines 6481.6 - 6733.4
    np.arange(7693.50, 7875.55, 0.074), # ab lines 7691.2 - 7838.5

])

model = tc.CannonModel.read('galah.model')


def create_binary_spectrum(pixels,stellar_labels_1,stellar_labels_2,rv_1,rv_2): 
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


def plot_binary_spectrum(rv_1,new_fluxes):
	new_wavelengths = [wavelength*(1+(rv_1/c)) for wavelength in dispersion]
	fig,ax = plt.subplots(4,1)
	ax[0].plot(new_wavelengths,new_fluxes,'b',label = 'blue arm')
	ax[1].plot(new_wavelengths,new_fluxes,'g',label = 'green arm')
	ax[2].plot(new_wavelengths,new_fluxes,'r',label = 'red arm')
	ax[3].plot(new_wavelengths,new_fluxes,'k',label = 'infrared arm')
	ax[0].set_xlim([4710,4900])
	ax[1].set_xlim([5600,5900])
	ax[2].set_xlim([6450,6800])
	ax[3].set_xlim([7650,7900])
	fig.legend()
	return ax
	




