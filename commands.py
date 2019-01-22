import produce_binary_spectra
from produce_labels import produce_labels

def verify_code():
	i = 0
	teffs = []
	loggs = []
	derived_teffs = []
	derived_loggs = []
	while i in range(0,5):
		i += 1
		stellar_labels_1 = model.training_set_labels[np.random.randint(0,len(model.training_set_labels))]
		stellar_labels_2 = model.training_set_labels[np.random.randint(0,len(model.training_set_labels))]
		rv_1 = np.random.randint(-300,300)
		rv_2 = np.random.randint(-300,300)
		fluxes = create_binary_spectra(dispersion,stellar_labels_1,stellar_labels_2,rv_1,rv_2)
		popt = produce_labels(fluxes,dispersion)
		teffs.append([stellar_labels_1[0],stellar_labels_2[0]])
		loggs.append([stellar_labels_1[1],stellar_labels_2[1]])
		derived_loggs.append([popt[1],popt[7]])
		derived_teffs.append([popt[0],popt[6]])
	fig,ax = plt.subplots(1,2)
	ax[0].scatter(teffs,derived_teffs)
	ax[1].scatter(loggs,derived_loggs)
	a = [4000,6800]
	b = [4000,6800]
	x = [1,5]
	y = [1,5]
	ax[0].plot(x,y,'r')
	ax[1].plot(a,b,'r')
	ax[0].set_title('teffs')
	ax[1].set_title('loggs')
	ax[0].set_xlabel('original teffs')
	ax[1].set_xlabel('derived teffs')
	ax[0].set_ylabel('original loggs')
	ax[1].set_ylabel('derived loggs')
	plt.show()





