# Download zipped FEC master files
# By Christopher Schnaars, USA TODAY
# Developed with Python 2.7.4
# See README.md for complete documentation

# Import needed libraries
from datetime import datetime, timedelta
import glob
import multiprocessing
import os
import urllib
import urllib2
import zipfile

# Try to import user settings or set them explicitly
try:
    import usersettings
    MASTERDIR = usersettings.MASTERDIR
except:
    MASTERDIR = 'C:\\data\\FEC\\Master\\'

# Other user variables
ARCHIVEFILES = 1 # Set to 0 if you don't want to archive the weekly master files each week.
MASTERFTP = 'ftp://ftp.fec.gov/FEC/'
MASTERFILES = ['add', 'ccl', 'chg', 'cm', 'cn', 'delete', 'indiv', 'oth', 'pas2']
NUMPROC = 10 # Multiprocessing processes to run simultaneously
STARTCYCLE = 2002 # Oldest election cycle for which you want to download master files


def archive_master_files(archivedate):
    """
    Moves current weekly master files to archive directory. The
    archivedate parameter specifies the most recent Sunday date. If the
    archive directory does not exist, this subroutine creates it.
    """
    # Create timestamp
    timestamp = archivedate.strftime("%Y%m%d")

    # Create archive directory if it doesn't exist
    savedir = MASTERDIR + 'Archive\\' + timestamp + '\\'
    if not os.path.isdir(savedir):
        try:
            os.mkdir(savedir)
        except:
            pass

    # Move all the files
    for datafile in glob.glob(os.path.join(MASTERDIR, '*.zip')):
        os.rename(datafile, datafile.replace(MASTERDIR, savedir))


def delete_files(dir, ext):
    """
    Deletes all files in the specified directory with the specified
    file extension. In this module, it is used to delete all text files
    extracted from the previous week's archives prior to downloading
    the new archives. These files are housed in the directory
    specified by MASTERDIR.

    When ARCHIVEFILES is set to 0, this subroutine also is used
    to delete all archive files from the MASTERDIR directory.
    """
    # Remove asterisks and periods from specified extension
    ext = '*.' + ext.lstrip('*.')

    # Delete all files
    for datafile in glob.glob(os.path.join(dir, ext)):
        os.remove(datafile)


def download_file(src, dest):
    """
    Downloads a single master file (src) and saves it as dest. After
    downloading a file, this subroutine compares the length of the
    downloaded file with the length of the source file and will try to
    download a file up to five times when the lengths don't match.
    """
    y = 0
    try:
        srclen = float(
            urllib2.urlopen(src).info().get('Content-Length'))
    except:
        y = 5
    while y < 5:
        try:
            urllib.urlretrieve(src, dest)
            destlen = os.path.getsize(dest)

            # Repeat download up to five times if files not same size
            if srclen != destlen:
                os.remove(dest)
                y += 1
                continue
            else:
                y = 6
        except:
            y += 1
    if y == 5:
        print(src + ' could not be downloaded.')


def unzip_master_file(masterfile):
    """
    Extracts the data file from a single weekly master file archive.
    If the extracted file does not include a year reference, this
    subroutine appends a two-digit year to the extracted filename.
    """
    fileyear = masterfile[masterfile.find('.zip')-2:masterfile.find('.zip')]

    try:
        zip = zipfile.ZipFile(masterfile)
        for subfile in zip.namelist():
            zip.extract(subfile, MASTERDIR)
            # Rename the file if it does not include the year
            if subfile.find(fileyear + '.') == -1:
                savefile = MASTERDIR + subfile
                os.rename(savefile, savefile.replace('.', fileyear + '.'))

    except:
        print('Files contained in ' + masterfile + ' could not be extracted.')


if __name__=='__main__':
    
    # Delete text files extracted from the prior week's archives
    print('Deleting old data...')
    delete_files(MASTERDIR, 'txt')

    # Delete last week's archives if they're still in the working
    # directory. These files are moved to another directory
    # (archived) below when ARCHIVEFILES is set to 1.
    delete_files(MASTERDIR, 'zip')
    print('Done!\n')

    # Use multiprocessing to download weekly files
    print('Downloading weekly master files...\n')
    pool = multiprocessing.Pool(processes=NUMPROC)

    # Determine most recent Sunday's date
    maxdate = datetime.now()
    x = -(maxdate.weekday()%6)-1
    maxdate = maxdate + timedelta(days=x)

    # Parse year
    maxyear = maxdate.year
    # Add one if it's not even
    if maxyear/2*2 < maxyear: maxyear += 1
        
    # Create loop to iterate through FEC ftp directories
    for x in range(STARTCYCLE, maxyear + 2, 2):
        fecdir = MASTERFTP + str(x) + '/'

        for thisfile in MASTERFILES:
            currfile = thisfile + str(x)[2:] + '.zip'
            fecfile = fecdir + currfile
            savefile = MASTERDIR + currfile
            pool.apply_async(download_file(fecfile, savefile))
    pool.close()
    pool.join()
    print('Done!\n')

    # Use multiprocessing to extract data files from the archives
    print('Unzipping files...')
    pool = multiprocessing.Pool(processes=NUMPROC)

    for fecfile in glob.glob(os.path.join(MASTERDIR, '*.zip')):
        pool.apply_async(unzip_master_file(fecfile))
    pool.close()
    pool.join()
    print('Done!\n')

    # Archive files when ARCHIVEFILES == 1
    # Otherwise delete files
    if ARCHIVEFILES == 1:
	    print('Archiving data files...')
	    archive_master_files(maxdate)
	    print('Done!\n')

    print('Process complete.')

