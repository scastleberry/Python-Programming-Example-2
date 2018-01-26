# Python-Programming-Example-2

# This repository contains a more simplistic example Python script example that I created to download a set of radar data files from a web URL.

In this Python example (using the script file ncdc_TarZip_lvl2_extract.py), the user will go to the NCEI website (https://www.ncdc.noaa.gov/has/HAS.FileAppRouter?datasetname=6500&subqueryby=STATION&applname=&outdest=FILE), request a set of radar data files, set up their output paths accordingly (such as in the text file ncdc_lvl2_data_ftp_locs_GEN.txt), and then copy the download URL to that same file once the request is complete and the special download URL is emailed to the user.

The script is then run from the Linux command line using the text file, containing the paths and URL, as its one input. 

For example, you could run the script like so: ./ncdc_TarZip_lvl2_extract.py ncdc_lvl2_data_ftp_locs_GEN.txt

The radar data files will then be downloaded from the download URL that was specified in the text file, and then un-tarred and sorted into output directories based on their dates.

