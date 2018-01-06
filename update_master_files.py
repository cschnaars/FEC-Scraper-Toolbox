# Download zipped FEC master files
# By Christopher Schnaars, USA TODAY
# Developed with Python 2.7.4
# See README.md for complete documentation

# WARNING:
# --------
# If you automate the execution of this script, you should set it to
# run in the late evening to make sure you don't download any master
# files before the FEC has a chance to update them. At the time of this
# writing, the FEC was updating the candidate, committee and
# candidate-committee linkage files daily around 7:30 a.m. while
# other weekly files were updated a little before 4 p.m. on Sundays.

# Development Notes:
# ------------------
# 4/7/2014: Updated code so files can be downloaded daily. The FEC began
# publishing daily updates to the candidate, committee and
# candidate-committee linkage files. Other master files continue
# to be updated weekly on Sundays.

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
ARCHIVEFILES = 1 # Set to 0 if you don't want to archive the master files each week.
MASTERFTP = 'https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/'
MASTERFILES = ['ccl', 'cm', 'cn', 'indiv', 'oth', 'pas2', 'oppexp']
NUMPROC = 10 # Multiprocessing processes to run simultaneously
STARTCYCLE = 2002 # Oldest election cycle for which you want to download master files
OMITNONSUNDAYFILES = 1 # Set to 0 to download all files regardless of day of week


def archive_master_files():
    """
    Moves current master files to archive directory. The
    archivedate parameter specifies the most recent Sunday date. If the
    archive directory does not exist, this subroutine creates it.
    """
    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d")

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

        
def create_timestamp():
    filetime = datetime.datetime.now()
    return filetime.strftime('%Y%m%d')


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
        # Add a header to the request.
        request = urllib2.Request(src, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'})
        srclen = float(urllib2.urlopen(request).info().get('Content-Length'))
    except:
        y = 5
    while y < 5:
        try:
            urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
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
            if subfile.find(fileyear + '.txt') == -1:
                savefile = MASTERDIR + subfile
                os.rename(savefile, savefile.replace('.txt', fileyear + '.txt'))

    except:
        print('Files contained in ' + masterfile + ' could not be extracted.')


if __name__=='__main__':
    
    # Delete text files extracted from an earlier archive
    print('Deleting old data...')
    delete_files(MASTERDIR, 'txt')

    # Delete old archives if they're still in the working
    # directory. These files are moved to another directory
    # (archived) below when ARCHIVEFILES is set to 1.
    delete_files(MASTERDIR, 'zip')
    print('Done!\n')

    # Use multiprocessing to download master files
    print('Downloading master files...\n')
    pool = multiprocessing.Pool(processes=NUMPROC)

    # Determine whether today is Sunday
    sunday = False
    if datetime.now().weekday() == 6:
        sunday = True

    # Remove all files but cn, cm and ccl from MASTERFILES
    if sunday == False and OMITNONSUNDAYFILES == 1:
        files = []
        for fecfile in ['ccl', 'cm', 'cn']:
            if fecfile in MASTERFILES:
                files.append(fecfile)
        MASTERFILES = files

    # Calculate current election cycle
    maxyear = datetime.now().year
    # Add one if it's not an even-numbered year
    if maxyear / 2 * 2 < maxyear: maxyear += 1
        
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
	    archive_master_files()
	    print('Done!\n')

    print('Process complete.')

