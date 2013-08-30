# Download campaign finance reports
# By Christopher Schnaars, USA TODAY
# Developed with Python 2.7.4
# See README.md for complete documentation

# Import needed libraries
import ftplib
import glob
import multiprocessing
import os
import pickle
import re
import urllib
import urllib2
import zipfile

# Try to import user settings or set them explicitly
try:
    exec(open('usersettings.py').read())
except:
    ARCPROCDIR = 'C:\\data\\FEC\\Archives\\Processed\\'
    ARCSVDIR = 'C:\\data\\FEC\\Archives\\Import\\'
    RPTHOLDDIR = 'C:\\data\\FEC\\Reports\\Hold\\'
    RPTPROCDIR = 'C:\\data\\FEC\\Reports\\Processed\\'
    RPTSVDIR = 'C:\\data\\FEC\\Reports\\Import\\'

# Other user variables
ARCFTP = 'ftp://ftp.fec.gov/FEC/electronic/'
NUMPROC = 10  # Multiprocessing processes to run simultaneously
RPTFTP = 'ftp.fec.gov'
RPTURL = 'http://query.nictusa.com/dcdev/posted/'
RSSURL = 'http://fecapps.nictusa.com/rss/generate?preDefinedFilingType=ALL'


def build_archive_download_list(zipinfo={'mostrecent': '', 'badfiles':
                                         []}, oldarchives=[]):
    ftp = ftplib.FTP(RPTFTP)
    ftp.login()
    ftp.cwd('/FEC/electronic')
    files = []
    try:
        files = ftp.nlst()
    except:
        pass

    # Iterate through available files to see which ones to download
    downloads = []
    for filename in files:
        if not filename.endswith('.zip'):
            continue
        elif filename > zipinfo['mostrecent']:
            if filename not in oldarchives:
                downloads.append(filename)
        elif filename in zipinfo['badfiles']:
            if filename not in oldarchives:
                downloads.append(filename)

    return downloads


def build_prior_archive_list():
    dirs = [ARCSVDIR, ARCPROCDIR]
    archives = []

    for dir in dirs:
        for datafile in glob.glob(os.path.join(dir, '*.zip')):
            archives.append(datafile.replace(dir, ''))

    return archives


def build_prior_report_list():
    dirs = [RPTHOLDDIR, RPTPROCDIR, RPTSVDIR]
    reports = []

    for dir in dirs:
        for datafile in glob.glob(os.path.join(dir, '*.fec')):
            reports.append(
                datafile.replace(dir, '').replace('.fec', ''))

    return reports


def consume_rss():
    regex = re.compile(
        '<link>http://query.nictusa.com/dcdev/posted/([0-9]*)\.fec</link>')
    url = urllib.urlopen(RSSURL)
    rss = url.read()
    matches = []
    for match in re.findall(regex, rss):
        matches.append(match)

    return matches


def download_archive(src, dest):
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


def download_report(download):
    # Construct file url and get length of file
    url = RPTURL + download + '.fec'
    y = 0
    try:
        srclen = float(
            urllib2.urlopen(url).info().get('Content-Length'))
    except:
        y = 5
    filename = RPTSVDIR + download + '.fec'
    while y < 5:
        try:
            urllib.urlretrieve(url, filename)
            destlen = os.path.getsize(filename)

            # Repeat download up to five times if files not same size
            if srclen != destlen:
                os.remove(filename)
                y += 1
                continue
            else:
                y = 6
        except:
            y += 1
    if y == 5:
        print('Report ' + download + ' could not be downloaded.')


def pickle_archives(archives, oldarchives):
    zipinfo = {'mostrecent': '', 'badfiles': []}
    for archive in archives:
        if not archive in oldarchives:
            zipinfo['badfiles'].append(archive)
    # Sort the list
    archives.sort()
    # Set most recent to last element
    if len(archives) == 0:
        zipinfo['mostrecent'] = ''
    else:
        zipinfo['mostrecent'] = archives[-1]

    return zipinfo


def unzip_archive(archive, overwrite=0):
    destdirs = [RPTSVDIR, RPTPROCDIR, RPTHOLDDIR]
    try:
        zip = zipfile.ZipFile(ARCSVDIR + archive)
        for subfile in zip.namelist():
            x = 1
            if overwrite != 1:
                for dir in destdirs:
                    if x == 1:
                        if os.path.exists(dir + subfile):
                            x = 0
            if x == 1:
                zip.extract(subfile, destdirs[0])

        zip.close()

        # If all files extracted correctly, move archive to Processed
        # directory
        os.rename(ARCSVDIR + archive, ARCPROCDIR + archive)

    except:
        print('Files contained in ' + archive + ' could not be '
              'extracted. The file has been deleted so it can be '
              'downloaded again later.\n')
        os.remove(ARCSVDIR + archive)


def verify_reports(rpts, downloaded):
    downloads = []
    for rpt in rpts:
        if rpt not in downloaded:
            downloads.append(rpt)
        else:
            srclen = float(urllib2.urlopen(RPTURL + rpt + '.fec').info()
                           .get('Content-Length'))
            destlen = 0
            childdirs = [RPTSVDIR, RPTPROCDIR, RPTHOLDDIR]
            for child in childdirs:
                try:
                    destlen = os.path.getsize(child + rpt + '.fec')
                except:
                    pass
            if srclen != destlen:
                downloads.append(rpt)
                os.remove(child + rpt + '.fec')

    return downloads


if __name__ == '__main__':
    # Attempt to fetch data specifying missing .zip files and most
    # recent .zip file downloaded
    print('Attempting to retrieve information for previously '
          'downloaded archives...')
    try:
        zipinfo = pickle.load(open("zipinfo.p", "rb"))
        print('Information retrieved successfully.\n')
    except:
        zipinfo = {'mostrecent': '', 'badfiles': []}
        print('zipinfo.p not found. Starting from scratch...\n')

    # IF YOU DON'T WANT TO DOWNLOAD ALL ARCHIVES BACK TO 2001 OR
    # OTHERWISE WANT TO MANUALLY CONTROL WHAT IS DOWNLOADED, YOU CAN
    # UNCOMMENT THE TWO LINES OF CODE BELOW AND EXPLICITLY SET THE
    # VALUES.
    # Set mostrecent to the last date you DON'T want, so if you want
    # everything since Jan. 1, 2013, set mostrecent to: '20121231.zip'
    # zipinfo['mostrecent'] = '20121231.zip' # YYYYMMDD.zip
    # zipinfo['badfiles'] = [] # You probably want to leave this blank

    # Build a list of previously downloaded archives
    print('Building a list of previously downloaded archive files...')
    oldarchives = build_prior_archive_list()
    print('Done!\n')

    # Go to FEC site and fetch a list of .zip files available
    print('Compiling a list of archives available for download...')
    archives = build_archive_download_list(zipinfo, oldarchives)
    if len(archives) == 0:
        print('No new archives found.\n')
    # If any files returned, download them using multiprocessing
    else:
        print('Done!\n')
        print('Downloading ' + str(len(archives))
              + ' new archive(s)...')
        pool = multiprocessing.Pool(processes=NUMPROC)
        for archive in archives:
            pool.apply_async(download_archive(ARCFTP + archive,
                                              ARCSVDIR + archive))
        pool.close()
        pool.join()
        print('Done!\n')

        # Open each archive and extract new reports
        print('Extracting files from archives...')
        pool = multiprocessing.Pool(processes=NUMPROC)
        for archive in archives:
            # Make sure archive was downloaded
            if os.path.isfile(ARCSVDIR + archive):
                pool.apply_async(unzip_archive(archive, 0))
        pool.close()
        pool.join()
        print('Done!\n')

        # Rebuild list of downloaded archives
        print('Rebuilding list of downloaded archives...')
        oldarchives = build_prior_archive_list()
        print('Done!\n')

        # Rebuild zipinfo and save with pickle
        print('Repickling the archives. Adding salt and vinegar...')
        zipinfo = pickle_archives(archives, oldarchives)
        pickle.dump(zipinfo, open('zipinfo.p', 'wb'))
        print('Done!\n')

    # Build a list of previously downloaded reports
    print('Building a list of previously downloaded reports...')
    downloaded = build_prior_report_list()
    print('Done!\n')

    # Consume FEC's RSS feed to get a list of files posted in the past
    # seven days
    print('Consuming FEC RSS feed to find new reports...')
    rpts = consume_rss()
    print('Done! ' + str(len(rpts)) + ' reports found.\n')

    # See whether each file flagged for download already has been
    # downloaded.  If it has, verify the downloaded file is the correct
    # length.
    print('Compiling list of reports to download...')
    newrpts = verify_reports(rpts, downloaded)
    print('Done! ' + str(len(newrpts)) + ' reports flagged for '
          'download.\n')

    # Download each of these reports
    print('Downloading new reports...')
    pool = multiprocessing.Pool(processes=NUMPROC)
    for rpt in newrpts:
        pool.apply_async(download_report(rpt))
    pool.close()
    pool.join()
    print('Done!\n')
    print('Process completed.')
