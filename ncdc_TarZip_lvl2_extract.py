#!/usr/bin/python

### This program will, for each NCDC Level-II radar data request FTP location (path) in the input .txt file, download the available .tar files and then 
### extract all zipped files (usually .gz or .Z) within each .tar file. The extracted zipped files are then saved in appropriate directories.
###
### Created by: Stephen Castleberry (stephen.castleberry@noaa.gov) - ROC/CIMMS - 10/2014
###

# Import the needed libraries.
import sys, os

# Set constants / adaptable parameters.
n_args = 1

# Show explanatory usage text.
if len(sys.argv) == 1:
	print "\n"
	print """This program will, for each NCDC Level-II radar data request FTP location (path) in the input text file, download the available .tar files 
and then extract all zipped files (usually .gz or .Z) within each .tar file. The extracted zipped files are then saved in appropriate directories.\n"""
	print """Note that it is HIGHLY recommended that this script be run using the "wrapper" ncdcl2 (BASH) script (located in the 'CSH' Scripts directory, 
one directory hierarchy level up from this script's directory).\n"""
	print """EXECUTION METHOD:\n\n"""
	print "For the Python script alone (From this script's directory):\n"
	print "./ncdc_TarZip_lvl2_extract.py lvl2_ftp_locs_file\n"
	print "When using the BASH wrapper program (PREFERRED METHOD):\n"
	print "ncdcl2 lvl2_ftp_locs_file\n\n"
	print """lvl2_ftp_locs_file is a text (usually .txt) file containing output directory paths and the listing of NCEI Level-II radar data location paths 
containing the .tar data files. Note that this text file must NOT contain ANYTHING but the file paths and FTP download location web addresses. All other lines 
MUST be comments (lines preceded by a "#" symbol) or blank lines. The input filename can be just the filename if the file is located in the same directory from 
which this script is executed, or can be a full, absolute, or relative path to the file if it is located in a directory different from where this script is executed.\n"""
	print "\n"
	
	sys.exit()
	
elif len(sys.argv) != n_args + 1:
	print "\n"
	print "ERROR: Incorrect number of input arguments. Program requires "+ str(n_args)+ ", but recieved "+ str(len(sys.argv)-1)+ ".\n"
	sys.exit()
	
# Load input parameters.
ftp_locs_fname = sys.argv[1]

# Read the fields in the input .txt file.
ftp_locs_f = open(ftp_locs_fname, 'rU')
paths_arr = ftp_locs_f.read()
ftp_locs_f.close()
paths_arr = paths_arr.split('\n')
paths_arr[:] = [i for i in paths_arr if i != '']
paths_arr[:] = [i for i in paths_arr if not i.startswith('#')]

# Set all needed parameters and extract save directory paths.
#
temp_ftp_dir = paths_arr[0]
xtract_rad_data_savedir_base = paths_arr[1]

# Extract the NCDC FTP location paths.
locs_arr = paths_arr[2:]

# Remove the trailing '/' from the location paths, if needed.
locs_arr[:] = [i.strip('/') for i in locs_arr]

# Loop across all the available NCDC FTP data request location paths and perform the file extractions.
if len(locs_arr) == 0:
	print "\n"
	print "The input file contains no NCDC FTP data request locations to process.\n"
	print "Program execution terminated!\n"
	sys.exit()
else:
	print "\n"
	print "The input file contains "+ str(len(locs_arr))+ " NCDC FTP data request location(s) to process.\n"

path_count = 1
for p in locs_arr:
	# Download the .tar files from the current FTP location. This step can take a long time, depending on how many .tar files there are, and the file sizes.
	print "Current FTP request path number: "+ str(path_count)+ "\n"
	print "Attempting retrieval of NCDC Level-II radar data from FTP request location: " + p + " ...\n"
	os.system('wget -erobots=off --no-check-certificate -r -l1 --no-parent -q -nd -P '+ temp_ftp_dir+ '/ '+ '-A "*.tar"'+ ' '+ p)
	
	# Find the radar site and date of the current FTP directory's .tar files, and move the downloaded .tar files to the appropriate target save directory location.
	#
	tar_files = os.listdir(temp_ftp_dir); tar_files.sort()
			
	# Check that .tar files were, in fact, downloaded.
	if len(tar_files) == 0:
		print "No .tar files available from FTP request location: "+ p+ "\n"
		path_count += 1
		continue
	
	# Generate the full save directories for the .tar files from the current FTP location and the extracted files, check if they already exist, create them if they don't.
	#
	# Get the radar site ID.
	tfs = tar_files[0]; tfs = tfs.split('_')
	rad_site = tfs[3]
	
	# Find the unique dates in the current .tar file listing.
	unique_dates = set()
	for tf in range(len(tar_files)):
		tfs = tar_files[tf]; tfs = tfs.split('_')
		date_s = tfs[4]; date_s = date_s[0:8]
		unique_dates.add(date_s)		
	unique_datesl = list(unique_dates); unique_datesl.sort()
	
	# Generate the save directories and move the files to the appropriate locations.
	for ud in unique_datesl:
		year_s = ud[0:4]; month_s = ud[4:6]; day_s = ud[6:8]
		site_yr_mn_dir = rad_site + '.' + year_s + '.' + month_s
		
		xtract_rad_data_savedir_full = xtract_rad_data_savedir_base+ '/'+ rad_site+ '/'+ site_yr_mn_dir+ '/'+ day_s
			
		if not os.path.isdir(xtract_rad_data_savedir_full):
			os.makedirs(xtract_rad_data_savedir_full)
			
		for tf in tar_files:
			if ud in tf:	
				# Extract the zipped files from the .tar files.
				os.system('tar -xf '+ temp_ftp_dir+ '/'+ tf+ ' -C '+ temp_ftp_dir)
				
				# Delete the .tar files.
				os.system('rm -f '+ temp_ftp_dir+ '/'+ tf)
	
				# Move the extracted zipped files to their target directory.
				rem_files = os.listdir(temp_ftp_dir); rem_files.sort()
				for rf in rem_files:
					if '.tar' not in rf:
						os.system('mv '+ temp_ftp_dir+ '/'+ rf+ ' '+ xtract_rad_data_savedir_full+ '/.')

		# Notify that the files were extracted / moved.	
		zf = os.listdir(xtract_rad_data_savedir_full)
		print str(len(zf))+ " zipped files extracted to directory: "+ xtract_rad_data_savedir_full+ "\n"
	
	path_count += 1
		
print "Program execution complete.\n"
sys.exit()


