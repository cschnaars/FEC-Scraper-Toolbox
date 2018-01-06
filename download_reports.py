# Download campaign finance reports
# By Christopher Schnaars, USA TODAY
# Developed with Python 2.7.4
# See README.md for complete documentation

# Import needed libraries
import datetime
import glob
import multiprocessing
import os
import pickle
import re
import sys
import urllib
import urllib2
import zipfile

# Try to import user settings or set them explicitly
try:
    import usersettings

    ARCPROCDIR = usersettings.ARCPROCDIR
    ARCSVDIR = usersettings.ARCSVDIR
    RPTHOLDDIR = usersettings.RPTHOLDDIR
    RPTPROCDIR = usersettings.RPTPROCDIR
    RPTSVDIR = usersettings.RPTSVDIR
except:
    ARCPROCDIR = 'C:\\data\\FEC\\Archives\\Processed\\'
    ARCSVDIR = 'C:\\data\\FEC\\Archives\\Import\\'
    RPTHOLDDIR = 'C:\\data\\FEC\\Reports\\Hold\\'
    RPTPROCDIR = 'C:\\data\\FEC\\Reports\\Processed\\'
    RPTSVDIR = 'C:\\data\\FEC\\Reports\\Import\\'

# Other user variables
ARCFTP = 'https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/electronic/'
NUMPROC = 1  # Multiprocessing processes to run simultaneously
RPTURL = 'http://docquery.fec.gov/dcdev/posted/'
RSSURL = 'http://efilingapps.fec.gov/rss/generate?preDefinedFilingType=ALL'


def build_archive_download_list(zipinfo):
    """
    On 1/8/2018, the FEC shut down its FTP server and moved their
    bulk files to an Amazon S3 bucket. Rather than try to hack the
    JavaScript, this function now looks for files dated after the
    mostrecent element of the zipinfo.p pickle up to the current
    system date. I'm adding a try_again_later property to the
    pickle for .zip files that fail to download.
    """

    # Generate date range to look for new files
    start_date = datetime.datetime.strptime(zipinfo['mostrecent'], '%Y%m%d').date()
    add_day = datetime.timedelta(days=1)
    start_date += add_day
    end_date = datetime.datetime.now().date()

    # Create dictionary to house list of files to attempt to download
    downloads = []

    # Add recent archive files
    while start_date < end_date:
        downloads.append(datetime.date.strftime(start_date, '%Y%m%d') + '.zip')
        start_date += add_day

    # Add try_again files
    for fec_file in zipinfo['try_again_later']:
        if fec_file not in downloads:
            downloads.append(datetime.datetime.strftime(fec_file, '%Y%m%d'))

    # Remove any bad files from the list
    for fec_file in zipinfo['badfiles']:
        if fec_file in downloads:
            downloads.remove(fec_file)

    return downloads


def build_prior_report_list():
    """
    Returns a list of reports housed in the directories specified by
    RPTHOLDDIR, RPTPROCDIR and RPTSVDIR.
    """
    dirs = [RPTHOLDDIR, RPTPROCDIR, RPTSVDIR]
    reports = []

    for dir in dirs:
        for datafile in glob.glob(os.path.join(dir, '*.fec')):
            reports.append(
                datafile.replace(dir, '').replace('.fec', ''))

    return reports


def consume_rss():
    """
    Returns a list of electronically filed reports included in an FEC
    RSS feed listing all reports submitted within the past seven days.
    """
    regex = re.compile('<link>http://docquery.fec.gov/dcdev/posted/' \
                       '([0-9]*)\.fec</link>')
    url = urllib.urlopen(RSSURL)
    rss = url.read()
    matches = []
    for match in re.findall(regex, rss):
        matches.append(match)

    return matches


def download_archive(archive):
    """
    Downloads a single archive file and saves it in the directory
    specified by the ARCSVDIR variable.  After downloading an archive,
    this subroutine compares the length of the downloaded file with the
    length of the source file and will try to download a file up to
    five times when the lengths don't match.
    """
    src = ARCFTP + archive
    dest = ARCSVDIR + archive
    y = 0
    # I have added a header to my request
    try:
        # Add a header to the request
        request = urllib2.Request(src, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'})
        srclen = float(urllib2.urlopen(request).info().get('Content-Length'))
    except:
        y = 5

    while y < 5:
        try:
            # Add a header to the request
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
        zipinfo['try_again_later'].append(archive)
        print(src + ' could not be downloaded.')


def download_report(download):
    """
    Downloads a single electronic report and saves it in the directory
    specified by the RPTSVDIR variable.  After downloading a report,
    this subroutine compares the length of the downloaded file with the
    length of the source file and will try to download a file up to
    five times when the lengths don't match.
    """
    # Construct file url and get length of file
    url = RPTURL + download + '.fec'
    y = 0

    try:
        # Add a header to the request
        request = urllib2.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'})
        srclen = float(urllib2.urlopen(request).info().get('Content-Length'))
    except:
        y = 5

    filename = RPTSVDIR + download + '.fec'

    while y < 5:
        try:
            url_headers = {'ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'ACCEPT_ENCODING': 'gzip, deflate, br',
                           'ACCEPT_LANGUAGE': 'en-US,en;q=0.5',
                           'USER-AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
            request = urllib2.Request(url, headers=url_headers)
            response = urllib2.urlopen(request)
            with open(filename, 'wb') as f:
                f.write(response.read())

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
        sys.exit()


def pickle_archives(zipinfo, archives):
    """
    Rebuilds the zipinfo.p pickle and saves it in the same directory as
    this module.

    archives is a list of archive files available for download on the
    FEC website. The list is generated by the
    build_archive_download_list function.
    """

    # To calculate most recent download, omit files in try_again_later
    downloads = [fec_file for fec_file in archives if fec_file not in zipinfo['try_again_later']]
    if len(downloads) > 0:
        zipinfo['mostrecent'] = max(downloads)

    pickle.dump(zipinfo, open('zipinfo.p', 'wb'))


def unzip_archive(archive, overwrite=0):
    """
    Extracts any files housed in a specific archive that have not been
    downloaded previously.

    Set the overwrite parameter to 1 if existing files should be
    overwritten.  The default value is 0.
    """
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
    """
    Returns a list of individual reports to be downloaded.

    Specifically, this function compares a list of available reports
    that have been submitted to the FEC during the past seven days
    (rpts) with a list of previously downloaded reports (downloaded).

    For reports that already have been downloaded, the function verifies
    the length of the downloaded file matches the length of the file
    posted on the FEC website.  When the lengths do not match, the saved
    file is deleted and retained in the download list.
    """
    downloads = []
    for rpt in rpts:
        childdirs = [RPTSVDIR, RPTPROCDIR, RPTHOLDDIR]
        if rpt not in downloaded:
            downloads.append(rpt)
        else:
            try:
                # Add a header to the request
                request = urllib2.Request(RPTURL + rpt + '.fec', headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'})
                srclen = float(urllib2.urlopen(request).info().get('Content-Length'))
            except urllib2.HTTPError:
                print(RPTURL + rpt + '.fec could not be downloaded.')
                continue

            for child in childdirs:
                try:
                    destlen = os.path.getsize(child + rpt + '.fec')
                    if srclen != destlen:
                        downloads.append(rpt)
                        os.remove(child + rpt + '.fec')
                except:
                    pass

    return downloads


if __name__ == '__main__':
    # Attempt to fetch data specifying missing .zip files and most
    # recent .zip file downloaded
    print('Attempting to retrieve information for previously '
          'downloaded archives...')
    try:
        zipinfo = pickle.load(open("zipinfo.p", "rb"))
        # Make sure new try_again_later key exists
        if 'try_again_later' not in zipinfo.keys():
            zipinfo['try_again_later'] = []
        print('Information retrieved successfully.\n')
    except:
        zipinfo = {'mostrecent': '20000101.zip', 'badfiles': [], 'try_again_later': []}
        print('zipinfo.p not found. Starting from scratch...\n')

    # IF YOU DON'T WANT TO DOWNLOAD ALL ARCHIVES BACK TO 2001 OR
    # OTHERWISE WANT TO MANUALLY CONTROL WHAT IS DOWNLOADED, YOU CAN
    # UNCOMMENT THE TWO LINES OF CODE BELOW AND EXPLICITLY SET THE
    # VALUES.
    # Set mostrecent to the last date you DON'T want, so if you want
    # everything since Jan. 1, 2013, set mostrecent to: '20121231.zip'
    # zipinfo['mostrecent'] = '20121231.zip' # YYYYMMDD.zip
    # zipinfo['badfiles'] = [] # You probably want to leave this blank

    # Go to FEC site and fetch a list of .zip files available
    print('Compiling a list of archives available for download...')
    archives = build_archive_download_list(zipinfo)
    if len(archives) == 0:
        print('No new archives found.\n')
    # If any files returned, download them using multiprocessing
    else:
        print('Done!\n')
        print('Downloading ' + str(len(archives))
              + ' new archive(s)...')
        pool = multiprocessing.Pool(processes=NUMPROC)
        for archive in archives:
            pool.apply_async(download_archive(archive))
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

        # Rebuild zipinfo and save with pickle
        print('Repickling the archives. Adding salt and vinegar...')
        pickle_archives(zipinfo, archives)
        print('Done!\n')

    # Build list of previously downloaded reports
    print('Building a list of previously downloaded reports...')
    downloaded = build_prior_report_list()
    print('Done!\n')

    # Consume FEC's RSS feed to get list of files posted in the past
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
        # download_report(rpt)
        pool.apply_async(download_report(rpt))
    pool.close()
    pool.join()
    print('Done!\n')
    print('Process completed.')
