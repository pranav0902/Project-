from astropy.io import fits

filename = "GALAH_DR2.1_catalog.fits"

with fits.open(filename) as hdu_list:
	table = hdu_list[1].data
	for star in table:
		list_of_stars = []
		for i in range(0,len(table)):
			star = table[i]
			if cannon_flag is 0:
				if star.field('logg') > 4 and star.field('snr_c1') > 100:
					if 0 < star.field('rv_obst') < 20:
						list_of_stars.append(star.field('star_id'))
	print(len(list_of_stars))

	
	