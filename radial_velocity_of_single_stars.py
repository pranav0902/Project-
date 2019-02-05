import numpy as np
from PyAstronomy import pyasl
import thecannon as tc
from scipy.constants import speed_of_light as c
from scipy.interpolate import interp1d

model = tc.CannonModel.read('galah.model')
def shifting_the_stellar_spectrum(labels,rv):
	if labels.shape == (6,):
		flux_of_star = model(labels)
		wavelength_of_star = np.linspace(4715.94,7875.55,len(flux_of_star))
		function = interp1d(wavelength_of_star,flux_of_star,bounds_error=False,fill_value='extrapolate')
		shifted_wavelength_of_star = np.array([wavelength*(1+((rv*1000)/c)) for wavelength in wavelength_of_star])
		shifted_flux_of_star = function(shifted_wavelength_of_star)
		return [shifted_flux_of_star,shifted_wavelength_of_star,wavelength_of_star,flux_of_star]
	else:
		return "The number of labels entered is incorrect. There should be 6 labels."

def get_rv(shifted_flux_of_star,shifted_wavelength_of_star,flux_of_star,wavelength_of_star):
	rv,cc = pyasl.crosscorrRV(wavelength_of_star,flux_of_star,wavelength_of_star,shifted_flux_of_star,-300.,300.,5.,skipedge = 40)
	return rv[np.argmax(cc)]