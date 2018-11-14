# Parse campaign finance reports
# By Christopher Schnaars, USA TODAY
# Developed with Python 2.7.4
# See README.md for complete documentation

# Import needed libraries
import csv
import datetime
import glob
import linecache
import os
import pyodbc
import shutil
import time

"""
  Currently supported forms and versions:
 * Header: all versions through 8.1 (v1 and v2 hardcoded)
 * F1: all versions through 8.3
 * F1S: all versions through 8.3 (first used in v3)
 * F3: all versions through 8.3
 * F3L: all versions through 8.3 (first used in v6.4)
 * F3P: all versions through 8.3
 * F3X: all versions through 8.3
 * SA: all versions through 8.3
 * SB: all versions through 8.3
 * SC: all versions through 8.3
 * SC1: all versions through 8.3
 * SC2: all versions through 8.3 (does not exist in v1)
 * SD: all versions through 8.3
 * SE: all versions through 8.3
 * SF: all versions through 8.3
 * H1: all versions through 8.3
 * H2: all versions through 8.3
 * H3: all versions through 8.3 (temporarily removed v1 and v2)
 * H4: all versions through 8.3
 * H5: all versions through 8.3 (first used in 5.0)
 * H6: all versions through 8.3 (first used in 5.0)
 * SI: all versions through 7.0 (FEC discontinued as of 8.0)
 * SL: all versions through 8.3 (first used in 5.0)
 * TEXT: all versions through 8.3 (does not exist in v1 or v2)
"""

# Try to import user settings or set them explicitly.
try:
    import usersettings

    DBCONNSTR = usersettings.DBCONNSTR
    RPTERRDIR = usersettings.RPTERRDIR
    RPTHOLDDIR = usersettings.RPTHOLDDIR
    RPTOUTDIR = usersettings.RPTOUTDIR
    RPTPROCDIR = usersettings.RPTPROCDIR
    RPTRVWDIR = usersettings.RPTRVWDIR
    RPTSVDIR = usersettings.RPTSVDIR
except:
    DBCONNSTR = ''
    RPTERRDIR = 'C:\\data\\FEC\\Reports\\ErrorLogs\\'
    RPTHOLDDIR = 'C:\\data\\FEC\\Reports\\Hold\\'
    RPTOUTDIR = 'C:\\data\\FEC\\Reports\\Output\\'
    RPTPROCDIR = 'C:\\data\\FEC\\Reports\\Processed\\'
    RPTRVWDIR = 'C:\\data\\FEC\\Reports\\Review\\'
    RPTSVDIR = 'C:\\data\\FEC\\Reports\\Import\\'

# Other user variables
# --------------------
# Explicitly exclude reports that can't be parsed.
# They will be moved to the directory specified with RPTHOLDDIR.
BADREPORTS = [17247, 304004]

# Use this variable to limit the number of reports to process.
FILELIMIT = 100000

# Set default delimiter used in electronic reports to ASCII-28
# Note that this is the delimiter used in the source data files.
# It is NOT used in the output data files, which use a tab delimiter.
SRCDELIMITER = chr(28)

# Set the delimiter to be used for output data files
OUTPUTDELIMITER = '\t'

# Create counter variable to stop file iteration when reaches filelimit
filectr = 0

# Build header variables
# Note that H3 header versions 1 and 2 have been disabled. I have found
# lots of cases where version 2.02 uses version 3 headers. These rows
# are moved to a timestamped OtherData file in the directory specified
# by RPTOUTDIR until I can more closely examine the data.
filehdrs = [['F1', [[['1', '2'],
                     ['FormTp', 'CommID', 'CommNm', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'SubmDt', 'flgChgCommNm',
                      'flgAddrChg', 'CommTp', 'CandID', 'CandFullName', 'CandOff', 'CandStAbbr', 'CandDist', 'PtyCd',
                      'PtyTp', 'AffCommID', 'AffCommNm', 'AffAddr1', 'AffAddr2', 'AffCity', 'AffStAbbr', 'AffZip',
                      'AffRelCd', 'AffOrgTp', 'CustFullName', 'CustAddr1', 'CustAddr2', 'CustCity', 'CustStAbbr',
                      'CustZip', 'CustTitle', 'CustPhone', 'TrsFullName', 'TrsAddr1', 'TrsAddr2', 'TrsCity',
                      'TrsStAbbr', 'TrsZip', 'TrsTitle', 'TrsPhone', 'AgtFullName', 'AgtAddr1', 'AgtAddr2', 'AgtCity',
                      'AgtStAbbr', 'AgtZip', 'AgtTitle', 'AgtPhone', 'Bank1Nm', 'Bank1Addr1', 'Bank1Addr2', 'Bank1City',
                      'Bank1StAbbr', 'Bank1Zip', 'SignFullName', 'SignDt']],
                    [['3'],
                     ['FormTp', 'CommID', 'CommNm', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'SubmDt', 'flgChgCommNm',
                      'flgAddrChg', 'CommTp', 'CandID', 'CandFullName', 'CandOff', 'CandStAbbr', 'CandDist', 'PtyCd',
                      'PtyTp', 'AffCommID', 'AffCommNm', 'AffAddr1', 'AffAddr2', 'AffCity', 'AffStAbbr', 'AffZip',
                      'AffRelCd', 'AffOrgTp', 'CustFullName', 'CustAddr1', 'CustAddr2', 'CustCity', 'CustStAbbr',
                      'CustZip', 'CustTitle', 'CustPhone', 'TrsFullName', 'TrsAddr1', 'TrsAddr2', 'TrsCity',
                      'TrsStAbbr', 'TrsZip', 'TrsTitle', 'TrsPhone', 'AgtFullName', 'AgtAddr1', 'AgtAddr2', 'AgtCity',
                      'AgtStAbbr', 'AgtZip', 'AgtTitle', 'AgtPhone', 'Bank1Nm', 'Bank1Addr1', 'Bank1Addr2', 'Bank1City',
                      'Bank1StAbbr', 'Bank1Zip', 'SignFullName', 'SignDt', 'CommEmail', 'CommUrl']],
                    [['5.0', '5.1', '5.2', '5.3'],
                     ['FormTp', 'CommID', 'CommNm', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'SubmDt', 'flgChgCommNm',
                      'flgAddrChg', 'CommTp', 'CandID', 'CandFullName', 'CandOff', 'CandStAbbr', 'CandDist', 'PtyCd',
                      'PtyTp', 'AffCommID', 'AffCommNm', 'AffAddr1', 'AffAddr2', 'AffCity', 'AffStAbbr', 'AffZip',
                      'AffRelCd', 'AffOrgTp', 'CustFullName', 'CustAddr1', 'CustAddr2', 'CustCity', 'CustStAbbr',
                      'CustZip', 'CustTitle', 'CustPhone', 'TrsFullName', 'TrsAddr1', 'TrsAddr2', 'TrsCity',
                      'TrsStAbbr', 'TrsZip', 'TrsTitle', 'TrsPhone', 'AgtFullName', 'AgtAddr1', 'AgtAddr2', 'AgtCity',
                      'AgtStAbbr', 'AgtZip', 'AgtTitle', 'AgtPhone', 'Bank1Nm', 'Bank1Addr1', 'Bank1Addr2', 'Bank1City',
                      'Bank1StAbbr', 'Bank1Zip', 'SignFullName', 'SignDt', 'CommEmail', 'CommUrl', 'CommFax']],
                    [['6.1'],
                     ['FormTp', 'CommID', 'flgChgCommNm', 'CommNm', 'flgAddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr',
                      'Zip', 'CommEmail', 'CommUrl', 'CommFax', 'SubmDt', 'SignLName', 'SignFName', 'SignMName',
                      'SignPfx', 'SignSfx', 'SignDt', 'CommTp', 'CandID', 'CandLName', 'CandFName', 'CandMName',
                      'CandPfx', 'CandSfx', 'CandOff', 'CandStAbbr', 'CandDist', 'PtyCd', 'PtyTp', 'CustLName',
                      'CustFName', 'CustMName', 'CustPfx', 'CustSfx', 'CustAddr1', 'CustAddr2', 'CustCity',
                      'CustStAbbr', 'CustZip', 'CustTitle', 'CustPhone', 'TrsLName', 'TrsFName', 'TrsMName', 'TrsPfx',
                      'TrsSfx', 'TrsAddr1', 'TrsAddr2', 'TrsCity', 'TrsStAbbr', 'TrsZip', 'TrsTitle', 'TrsPhone',
                      'AffCommID', 'AffCommNm', 'AffAddr1', 'AffAddr2', 'AffCity', 'AffStAbbr', 'AffZip',
                      'AffRelationship', 'AffOrgTp', 'AgtLName', 'AgtFName', 'AgtMName', 'AgtPfx', 'AgtSfx', 'AgtAddr1',
                      'AgtAddr2', 'AgtCity', 'AgtStAbbr', 'AgtZip', 'AgtTitle', 'AgtPhone', 'Bank1Nm', 'Bank1Addr1',
                      'Bank1Addr2', 'Bank1City', 'Bank1StAbbr', 'Bank1Zip', 'Bank2Nm', 'Bank2Addr1', 'Bank2Addr2',
                      'Bank2City', 'Bank2StAbbr', 'Bank2Zip']],
                    [['6.2'],
                     ['FormTp', 'CommID', 'flgChgCommNm', 'CommNm', 'flgAddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr',
                      'Zip', 'CommEmail', 'CommUrl', 'CommFax', 'SubmDt', 'SignLName', 'SignFName', 'SignMName',
                      'SignPfx', 'SignSfx', 'SignDt', 'CommTp', 'CandID', 'CandLName', 'CandFName', 'CandMName',
                      'CandPfx', 'CandSfx', 'CandOff', 'CandStAbbr', 'CandDist', 'PtyCd', 'PtyTp', 'PACTp',
                      'flgLdspPAC_5f', 'AffCommID', 'AffCommNm', 'AffAddr1', 'AffAddr2', 'AffCity', 'AffStAbbr',
                      'AffZip', 'AffRelCd', 'CustLName', 'CustFName', 'CustMName', 'CustPfx', 'CustSfx', 'CustAddr1',
                      'CustAddr2', 'CustCity', 'CustStAbbr', 'CustZip', 'CustTitle', 'CustPhone', 'TrsLName',
                      'TrsFName', 'TrsMName', 'TrsPfx', 'TrsSfx', 'TrsAddr1', 'TrsAddr2', 'TrsCity', 'TrsStAbbr',
                      'TrsZip', 'TrsTitle', 'TrsPhone', 'AgtLName', 'AgtFName', 'AgtMName', 'AgtPfx', 'AgtSfx',
                      'AgtAddr1', 'AgtAddr2', 'AgtCity', 'AgtStAbbr', 'AgtZip', 'AgtTitle', 'AgtPhone', 'Bank1Nm',
                      'Bank1Addr1', 'Bank1Addr2', 'Bank1City', 'Bank1StAbbr', 'Bank1Zip', 'Bank2Nm', 'Bank2Addr1',
                      'Bank2Addr2', 'Bank2City', 'Bank2StAbbr', 'Bank2Zip']],
                    [['6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                     ['FormTp', 'CommID', 'flgChgCommNm', 'CommNm', 'flgAddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr',
                      'Zip', 'flgChgCommEmail', 'CommEmail', 'flgChgCommUrl', 'CommUrl', 'SubmDt', 'SignLName',
                      'SignFName', 'SignMName', 'SignPfx', 'SignSfx', 'SignDt', 'CommTp', 'CandID', 'CandLName',
                      'CandFName', 'CandMName', 'CandPfx', 'CandSfx', 'CandOff', 'CandStAbbr', 'CandDist', 'PtyCd',
                      'PtyTp', 'PACTp', 'flgLobRegPAC_ConnOrg_5e', 'flgLobRegPAC_MultCands_5f', 'flgLdspPAC_5f',
                      'AffCommID', 'AffCommNm', 'AffCandID', 'AffCandLName', 'AffCandFName', 'AffCandMName',
                      'AffCandPfx', 'AffCandSfx', 'AffAddr1', 'AffAddr2', 'AffCity', 'AffStAbbr', 'AffZip', 'AffRelCd',
                      'CustLName', 'CustFName', 'CustMName', 'CustPfx', 'CustSfx', 'CustAddr1', 'CustAddr2', 'CustCity',
                      'CustStAbbr', 'CustZip', 'CustTitle', 'CustPhone', 'TrsLName', 'TrsFName', 'TrsMName', 'TrsPfx',
                      'TrsSfx', 'TrsAddr1', 'TrsAddr2', 'TrsCity', 'TrsStAbbr', 'TrsZip', 'TrsTitle', 'TrsPhone',
                      'AgtLName', 'AgtFName', 'AgtMName', 'AgtPfx', 'AgtSfx', 'AgtAddr1', 'AgtAddr2', 'AgtCity',
                      'AgtStAbbr', 'AgtZip', 'AgtTitle', 'AgtPhone', 'Bank1Nm', 'Bank1Addr1', 'Bank1Addr2', 'Bank1City',
                      'Bank1StAbbr', 'Bank1Zip', 'Bank2Nm', 'Bank2Addr1', 'Bank2Addr2', 'Bank2City', 'Bank2StAbbr',
                      'Bank2Zip']]]],
            ['F1S', [[['3'],
                      ['FormTp', 'CommID', 'NotUsed1', 'NotUsed2', 'NotUsed3', 'NotUsed4', 'NotUsed5', 'NotUsed6',
                       'NotUsed7', 'NotUsed8', 'NotUsed9', 'NotUsed10', 'NotUsed11', 'NotUsed12', 'NotUsed13',
                       'NotUsed14', 'NotUsed15', 'NotUsed16', 'NotUsed17', 'AffCommID', 'AffCommNm', 'AffAddr1',
                       'AffAddr2', 'AffCity', 'AffStAbbr', 'AffZip', 'AffRel', 'OrgTp', 'CustFullNm', 'CustAddr1',
                       'CustAddr2', 'CustCity', 'CustStAbbr', 'CustZip', 'CustTitle', 'CustPhone', 'TrsFullNm',
                       'TrsAddr1', 'TrsAddr2', 'TrsCity', 'TrsStAbbr', 'TrsZip', 'TrsTitle', 'TrsPhone', 'AgtFullName',
                       'AgtAddr1', 'AgtAddr2', 'AgtCity', 'AgtStAbbr', 'AgtZip', 'AgtTitle', 'AgtPhone', 'BankNm',
                       'BankAddr1', 'BankAddr2', 'BankCity', 'BankStAbbr', 'BankZip', 'TrsFullNm', 'SignDt',
                       'CommEmail', 'CommUrl']],
                     [['5.0', '5.1', '5.2', '5.3'],
                      ['FormTp', 'CommID', 'NotUsed1', 'NotUsed2', 'NotUsed3', 'NotUsed4', 'NotUsed5', 'NotUsed6',
                       'NotUsed7', 'NotUsed8', 'NotUsed9', 'NotUsed10', 'NotUsed11', 'NotUsed12', 'NotUsed13',
                       'NotUsed14', 'NotUsed15', 'NotUsed16', 'NotUsed17', 'AffCommID', 'AffCommNm', 'AffAddr1',
                       'AffAddr2', 'AffCity', 'AffStAbbr', 'AffZip', 'AffRel', 'OrgTp', 'CustFullNm', 'CustAddr1',
                       'CustAddr2', 'CustCity', 'CustStAbbr', 'CustZip', 'CustTitle', 'CustPhone', 'TrsFullNm',
                       'TrsAddr1', 'TrsAddr2', 'TrsCity', 'TrsStAbbr', 'TrsZip', 'TrsTitle', 'TrsPhone', 'AgtFullName',
                       'AgtAddr1', 'AgtAddr2', 'AgtCity', 'AgtStAbbr', 'AgtZip', 'AgtTitle', 'AgtPhone', 'BankNm',
                       'BankAddr1', 'BankAddr2', 'BankCity', 'BankStAbbr', 'BankZip', 'TrsFullNm', 'SignDt',
                       'CommEmail', 'CommUrl', 'CommFax']],
                     [['6.1'],
                      ['FormTp', 'CommID', 'AffCommID', 'AffCommNm', 'AffAddr1', 'AffAddr2', 'AffCity', 'AffStAbbr',
                       'AffZip', 'AffRel', 'OrgTp', 'AgtLName', 'AgtFName', 'AgtMName', 'AgtPfx', 'AgtSfx', 'AgtAddr1',
                       'AgtAddr2', 'AgtCity', 'AgtStAbbr', 'AgtZip', 'AgtTitle', 'AgtPhone', 'BankNm', 'BankAddr1',
                       'BankAddr2', 'BankCity', 'BankStAbbr', 'BankZip']],
                     [['6.2'], ['FormTp', 'CommID', 'JtFndCommNm', 'JtFundCommID', 'AffCommID', 'AffCommNm', 'AffAddr1',
                                'AffAddr2', 'AffCity', 'AffStAbbr', 'AffZip', 'AffRelCd', 'AgtLName', 'AgtFName',
                                'AgtMName', 'AgtPfx', 'AgtSfx', 'AgtAddr1', 'AgtAddr2', 'AgtCity', 'AgtStAbbr',
                                'AgtZip', 'AgtTitle', 'AgtPhone', 'BankNm', 'BankAddr1', 'BankAddr2', 'BankCity',
                                'BankStAbbr', 'BankZip']],
                     [['6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                      ['FormTp', 'CommID', 'JtFndCommNm', 'JtFundCommID', 'AffCommID', 'AffCommNm', 'AffCandID',
                       'AffLName', 'AffFName', 'AffMName', 'AffPfx', 'AffSfx', 'AffAddr1', 'AffAddr2', 'AffCity',
                       'AffStAbbr', 'AffZip', 'AffRelCd', 'AgtLName', 'AgtFName', 'AgtMName', 'AgtPfx', 'AgtSfx',
                       'AgtAddr1', 'AgtAddr2', 'AgtCity', 'AgtStAbbr', 'AgtZip', 'AgtTitle', 'AgtPhone', 'BankNm',
                       'BankAddr1', 'BankAddr2', 'BankCity', 'BankStAbbr', 'BankZip']]]],
            ['F3', [[['1', '2', '3'],
                     ['FormTp', 'CommID', 'CommNm', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'AddrChg', 'ElecSt',
                      'ElecDist', 'RptCd', 'ElecCd', 'ElecDt', 'StateOfElec', 'PrimElec', 'GenElec', 'SpecElec',
                      'RunoffElec', 'CovgFmDt', 'CovgToDt', 'TotConts_P_6a', 'TotContRfds_P_6b', 'NetConts_P_6c',
                      'TotOpExps_P_7a', 'TotOffsetOpExps_P_7b', 'NetOpExps_P_7c', 'CashClose_P_8', 'DebtsTo_P_9',
                      'DebtsBy_P_10', 'IndContsItem_P_11a1', 'IndContsUnitem_P_11a2', 'IndContsTot_P_11a3',
                      'PolPtyCommConts_P_11b', 'OthPolCommConts_P_11c', 'CandConts_P_11d', 'TotConts_P_11e',
                      'TranFmOthAuthComms_P_12', 'CandLoans_P_13a', 'OthLoans_P_13b', 'TotLoans_P_13c',
                      'OffsetOpExps_P_14', 'OthRcpts_P_15', 'TotRcpts_P_16', 'OpExps_P_17', 'TranToOthAuthComms_P_18',
                      'CandLoansRepaid_P_19a', 'OthLoansRepaid_P_19b', 'TotLoansRepaid_P_19c', 'RefundsInd_P_20a',
                      'RefundsPolPtyComms_P_20b', 'RefundsOthPolComms_P_20c', 'TotRefunds_P_20d', 'OthDisb_P_21',
                      'TotDisb_P_22', 'CashBegin_P_23', 'TotRcpts_P_24', 'Subtotal_P_25', 'TotDisb_P_26',
                      'CashClose_P_27', 'TotConts_T_6a', 'TotContRfds_T_6b', 'NetConts_T_6c', 'TotOpExps_T_7a',
                      'TotOffsetOpExps_T_7b', 'NetOpExps_T_7c', 'IndContsItem_T_11a1', 'IndContsUnitem_T_11a2',
                      'IndContsTot_T_11a3', 'PolPtyCommConts_T_11b', 'OthPolCommConts_T_11c', 'CandConts_T_11d',
                      'TotConts_T_11e', 'TranFmOthAuthComms_T_12', 'CandLoans_T_13a', 'OthLoans_T_13b',
                      'TotLoans_T_13c', 'OffsetOpExps_T_14', 'OthRcpts_T_15', 'TotRcpts_T_16', 'OpExps_T_17',
                      'TranToOthAuthComms_T_18', 'CandLoansRepaid_T_19a', 'OthLoansRepaid_T_19b',
                      'TotLoansRepaid_T_19c', 'RefundsInd_T_20a', 'RefundsPolPtyComms_T_20b',
                      'RefundsOthPolComms_T_20c', 'TotRefunds_T_20d', 'OthDisb_T_21', 'TotDisb_T_22', 'TrsFullName',
                      'SignDt']],
                    [['5.0', '5.1', '5.2', '5.3'],
                     ['FormTp', 'CommID', 'CommNm', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'AddrChg', 'ElecSt',
                      'ElecDist', 'RptCd', 'ElecCd', 'ElecDt', 'StateOfElec', 'PrimElec', 'GenElec', 'SpecElec',
                      'RunoffElec', 'CovgFmDt', 'CovgToDt', 'TotConts_P_6a', 'TotContRfds_P_6b', 'NetConts_P_6c',
                      'TotOpExps_P_7a', 'TotOffsetOpExps_P_7b', 'NetOpExps_P_7c', 'CashClose_P_8', 'DebtsTo_P_9',
                      'DebtsBy_P_10', 'IndContsItem_P_11a1', 'IndContsUnitem_P_11a2', 'IndContsTot_P_11a3',
                      'PolPtyCommConts_P_11b', 'OthPolCommConts_P_11c', 'CandConts_P_11d', 'TotConts_P_11e',
                      'TranFmOthAuthComms_P_12', 'CandLoans_P_13a', 'OthLoans_P_13b', 'TotLoans_P_13c',
                      'OffsetOpExps_P_14', 'OthRcpts_P_15', 'TotRcpts_P_16', 'OpExps_P_17', 'TranToOthAuthComms_P_18',
                      'CandLoansRepaid_P_19a', 'OthLoansRepaid_P_19b', 'TotLoansRepaid_P_19c', 'RefundsInd_P_20a',
                      'RefundsPolPtyComms_P_20b', 'RefundsOthPolComms_P_20c', 'TotRefunds_P_20d', 'OthDisb_P_21',
                      'TotDisb_P_22', 'CashBegin_P_23', 'TotRcpts_P_24', 'Subtotal_P_25', 'TotDisb_P_26',
                      'CashClose_P_27', 'TotConts_T_6a', 'TotContRfds_T_6b', 'NetConts_T_6c', 'TotOpExps_T_7a',
                      'TotOffsetOpExps_T_7b', 'NetOpExps_T_7c', 'IndContsItem_T_11a1', 'IndContsUnitem_T_11a2',
                      'IndContsTot_T_11a3', 'PolPtyCommConts_T_11b', 'OthPolCommConts_T_11c', 'CandConts_T_11d',
                      'TotConts_T_11e', 'TranFmOthAuthComms_T_12', 'CandLoans_T_13a', 'OthLoans_T_13b',
                      'TotLoans_T_13c', 'OffsetOpExps_T_14', 'OthRcpts_T_15', 'TotRcpts_T_16', 'OpExps_T_17',
                      'TranToOthAuthComms_T_18', 'CandLoansRepaid_T_19a', 'OthLoansRepaid_T_19b',
                      'TotLoansRepaid_T_19c', 'RefundsInd_T_20a', 'RefundsPolPtyComms_T_20b',
                      'RefundsOthPolComms_T_20c', 'TotRefunds_T_20d', 'OthDisb_T_21', 'TotDisb_T_22', 'TrsFullName',
                      'SignDt', 'CandID', 'CandFullName', 'RptType', 'GrossRctsAuthCommsPrim', 'AggAmtPersFundsPrim',
                      'GrossRctsMinusPersFmCandPrim', 'GrossRctsAuthCommsGen', 'AggAmtPersFundsGen',
                      'GrossRctsMinusPersFmCandGen']],
                    [['6.1', '6.2', '6.3'],
                     ['FormTp', 'CommID', 'CommNm', 'AddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'ElecSt',
                      'ElecDist', 'RptCd', 'ElecCd', 'ElecDt', 'StateOfElec', 'CovgFmDt', 'CovgToDt', 'TrsLName',
                      'TrsFName', 'TrsMName', 'TrsPfx', 'TrsSfx', 'SignDt', 'CandID', 'CandLName', 'CandFName',
                      'CandMName', 'CandPfx', 'CandSfx', 'RptType', 'TotConts_P_6a', 'TotContRfds_P_6b',
                      'NetConts_P_6c', 'TotOpExps_P_7a', 'TotOffsetOpExps_P_7b', 'NetOpExps_P_7c', 'CashClose_P_8',
                      'DebtsTo_P_9', 'DebtsBy_P_10', 'IndContsItem_P_11a1', 'IndContsUnitem_P_11a2',
                      'IndContsTot_P_11a3', 'PolPtyCommConts_P_11b', 'OthPolCommConts_P_11c', 'CandConts_P_11d',
                      'TotConts_P_11e', 'TranFmOthAuthComms_P_12', 'CandLoans_P_13a', 'OthLoans_P_13b',
                      'TotLoans_P_13c', 'OffsetOpExps_P_14', 'OthRcpts_P_15', 'TotRcpts_P_16', 'OpExps_P_17',
                      'TranToOthAuthComms_P_18', 'CandLoansRepaid_P_19a', 'OthLoansRepaid_P_19b',
                      'TotLoansRepaid_P_19c', 'RefundsInd_P_20a', 'RefundsPolPtyComms_P_20b',
                      'RefundsOthPolComms_P_20c', 'TotRefunds_P_20d', 'OthDisb_P_21', 'TotDisb_P_22', 'CashBegin_P_23',
                      'TotRcpts_P_24', 'Subtotal_P_25', 'TotDisb_P_26', 'CashClose_P_27', 'TotConts_T_6a',
                      'TotContRfds_T_6b', 'NetConts_T_6c', 'TotOpExps_T_7a', 'TotOffsetOpExps_T_7b', 'NetOpExps_T_7c',
                      'IndContsItem_T_11a1', 'IndContsUnitem_T_11a2', 'IndContsTot_T_11a3', 'PolPtyCommConts_T_11b',
                      'OthPolCommConts_T_11c', 'CandConts_T_11d', 'TotConts_T_11e', 'TranFmOthAuthComms_T_12',
                      'CandLoans_T_13a', 'OthLoans_T_13b', 'TotLoans_T_13c', 'OffsetOpExps_T_14', 'OthRcpts_T_15',
                      'TotRcpts_T_16', 'OpExps_T_17', 'TranToOthAuthComms_T_18', 'CandLoansRepaid_T_19a',
                      'OthLoansRepaid_T_19b', 'TotLoansRepaid_T_19c', 'RefundsInd_T_20a', 'RefundsPolPtyComms_T_20b',
                      'RefundsOthPolComms_T_20c', 'TotRefunds_T_20d', 'OthDisb_T_21', 'TotDisb_T_22',
                      'GrossRctsAuthCommsPrim', 'AggAmtPersFundsPrim', 'GrossRctsMinusPersFmCandPrim',
                      'GrossRctsAuthCommsGen', 'AggAmtPersFundsGen', 'GrossRctsMinusPersFmCandGen']],
                    [['6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                     ['FormTp', 'CommID', 'CommNm', 'AddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'ElecSt',
                      'ElecDist', 'RptCd', 'ElecCd', 'ElecDt', 'StateOfElec', 'CovgFmDt', 'CovgToDt', 'TrsLName',
                      'TrsFName', 'TrsMName', 'TrsPfx', 'TrsSfx', 'SignDt', 'TotConts_P_6a', 'TotContRfds_P_6b',
                      'NetConts_P_6c', 'TotOpExps_P_7a', 'TotOffsetOpExps_P_7b', 'NetOpExps_P_7c', 'CashClose_P_8',
                      'DebtsTo_P_9', 'DebtsBy_P_10', 'IndContsItem_P_11a1', 'IndContsUnitem_P_11a2',
                      'IndContsTot_P_11a3', 'PolPtyCommConts_P_11b', 'OthPolCommConts_P_11c', 'CandConts_P_11d',
                      'TotConts_P_11e', 'TranFmOthAuthComms_P_12', 'CandLoans_P_13a', 'OthLoans_P_13b',
                      'TotLoans_P_13c', 'OffsetOpExps_P_14', 'OthRcpts_P_15', 'TotRcpts_P_16', 'OpExps_P_17',
                      'TranToOthAuthComms_P_18', 'CandLoansRepaid_P_19a', 'OthLoansRepaid_P_19b',
                      'TotLoansRepaid_P_19c', 'RefundsInd_P_20a', 'RefundsPolPtyComms_P_20b',
                      'RefundsOthPolComms_P_20c', 'TotRefunds_P_20d', 'OthDisb_P_21', 'TotDisb_P_22', 'CashBegin_P_23',
                      'TotRcpts_P_24', 'Subtotal_P_25', 'TotDisb_P_26', 'CashClose_P_27', 'TotConts_T_6a',
                      'TotContRfds_T_6b', 'NetConts_T_6c', 'TotOpExps_T_7a', 'TotOffsetOpExps_T_7b', 'NetOpExps_T_7c',
                      'IndContsItem_T_11a1', 'IndContsUnitem_T_11a2', 'IndContsTot_T_11a3', 'PolPtyCommConts_T_11b',
                      'OthPolCommConts_T_11c', 'CandConts_T_11d', 'TotConts_T_11e', 'TranFmOthAuthComms_T_12',
                      'CandLoans_T_13a', 'OthLoans_T_13b', 'TotLoans_T_13c', 'OffsetOpExps_T_14', 'OthRcpts_T_15',
                      'TotRcpts_T_16', 'OpExps_T_17', 'TranToOthAuthComms_T_18', 'CandLoansRepaid_T_19a',
                      'OthLoansRepaid_T_19b', 'TotLoansRepaid_T_19c', 'RefundsInd_T_20a', 'RefundsPolPtyComms_T_20b',
                      'RefundsOthPolComms_T_20c', 'TotRefunds_T_20d', 'OthDisb_T_21', 'TotDisb_T_22']]]],
            ['F3L', [[['6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                      ['FormTp', 'CommID', 'CommNm', 'AddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'ElecSt',
                       'ElecDist', 'RptCd', 'ElecDt', 'StateOfElec', 'flgInclSemiAnnPrd', 'CovgFmDt', 'CovgToDt',
                       'flgInclSemiAnnJanJun', 'flgInclSemiAnnJulDec', 'TotRptBundContribs', 'SemiAnnBundContribs',
                       'TrsLName', 'TrsFName', 'TrsMName', 'TrsPfx', 'TrsSfx', 'SignDt']]]],
            ['F3P', [[['1', '2', '3', '5.0', '5.1', '5.2', '5.3'],
                      ['FormTp', 'CommID', 'CommNm', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'AddrChg', 'PrimElec',
                       'GenElec', 'RptCd', 'ElecCd', 'ElecDt', 'ElecSt', 'CovgFmDt', 'CovgToDt', 'CashBegin_P_6',
                       'TotRcpts_P_7', 'Subtotal_P_8', 'TotDisb_P_9', 'CashClose_P_10', 'DebtsTo_P_11', 'DebtsBy_P_12',
                       'LmtdExps_P_13', 'NetConts_P_14', 'NetOpExps_P_15', 'FedFnds_P_16', 'IndContsTot_P_17a3',
                       'PolPtyCommConts_P_17b', 'OthPolCommConts_P_17c', 'CandConts_P_17d', 'TotConts_P_17e',
                       'TranFmPtyComms_P_18', 'CandLoans_P_19a', 'OthLoans_P_19b', 'TotLoans_P_19c',
                       'OptgOffsets_P_20a', 'FndrsgOffsets_P_20b', 'LegalAcctgOffsets_P_20c', 'TotOffsets_P_20d',
                       'OthRcpts_P_21', 'TotRcpts_P_22', 'OpExps_P_23', 'TranToOthAuthComms_P_24', 'FndrsgDisb_P_25',
                       'LegalAcctgDisb_P_26', 'CandLoansRepaid_P_27a', 'OthLoansRepaid_P_27b', 'TotLoansRepaid_P_27c',
                       'RefundsInd_P_28a', 'RefundsPolPtyComms_P_28b', 'RefundsOthPolComms_P_28c', 'TotRefunds_P_28d',
                       'OthDisb_P_29', 'TotDisb_P_30', 'ItmsToBeLiq_P_31', 'Alabama_P', 'Alaska_P', 'Arizona_P',
                       'Arkansas_P', 'California_P', 'Colorado_P', 'Connecticut_P', 'Delaware_P', 'DistCol_P',
                       'Florida_P', 'Georgia_P', 'Hawaii_P', 'Idaho_P', 'Illinois_P', 'Indiana_P', 'Iowa_P', 'Kansas_P',
                       'Kentucky_P', 'Louisiana_P', 'Maine_P', 'Maryland_P', 'Massachusetts_P', 'Michigan_P',
                       'Minnesota_P', 'Mississippi_P', 'Missouri_P', 'Montana_P', 'Nebraska_P', 'Nevada_P',
                       'NewHampshire_P', 'NewJersey_P', 'NewMexico_P', 'NewYork_P', 'NorthCarolina_P', 'NorthDakota_P',
                       'Ohio_P', 'Oklahoma_P', 'Oregon_P', 'Pennsylvania_P', 'RhodeIsland_P', 'SouthCarolina_P',
                       'SouthDakota_P', 'Tennessee_P', 'Texas_P', 'Utah_P', 'Vermont_P', 'Virginia_P', 'Washington_P',
                       'WestVirginia_P', 'Wisconsin_P', 'Wyoming_P', 'PuertoRico_P', 'Guam_P', 'VirginIslands_P',
                       'TotAllocs_P', 'FedFnds_T_16', 'IndContsTot_T_17a3', 'PolPtyCommConts_T_17b',
                       'OthPolCommConts_T_17c', 'CandConts_T_17d', 'TotConts_T_17e', 'TranFmPtyComms_T_18',
                       'CandLoans_T_19a', 'OthLoans_T_19b', 'TotLoans_T_19c', 'OptgOffsets_T_20a',
                       'FndrsgOffsets_T_20b', 'LegalAcctgOffsets_T_20c', 'TotOffsets_T_20d', 'OthRcpts_T_21',
                       'TotRcpts_T_22', 'OpExps_T_23', 'TranToOthAuthComms_T_24', 'FndrsgDisb_T_25',
                       'LegalAcctgDisb_T_26', 'CandLoansRepaid_T_27a', 'OthLoansRepaid_T_27b', 'TotLoansRepaid_T_27c',
                       'RefundsInd_T_28a', 'RefundsPolPtyComms_T_28b', 'RefundsOthPolComms_T_28c', 'TotRefunds_T_28d',
                       'OthDisb_T_29', 'TotDisb_T_30', 'Alabama_T', 'Alaska_T', 'Arizona_T', 'Arkansas_T',
                       'California_T', 'Colorado_T', 'Connecticut_T', 'Delaware_T', 'DistCol_T', 'Florida_T',
                       'Georgia_T', 'Hawaii_T', 'Idaho_T', 'Illinois_T', 'Indiana_T', 'Iowa_T', 'Kansas_T',
                       'Kentucky_T', 'Louisiana_T', 'Maine_T', 'Maryland_T', 'Massachusetts_T', 'Michigan_T',
                       'Minnesota_T', 'Mississippi_T', 'Missouri_T', 'Montana_T', 'Nebraska_T', 'Nevada_T',
                       'NewHampshire_T', 'NewJersey_T', 'NewMexico_T', 'NewYork_T', 'NorthCarolina_T', 'NorthDakota_T',
                       'Ohio_T', 'Oklahoma_T', 'Oregon_T', 'Pennsylvania_T', 'RhodeIsland_T', 'SouthCarolina_T',
                       'SouthDakota_T', 'Tennessee_T', 'Texas_T', 'Utah_T', 'Vermont_T', 'Virginia_T', 'Washington_T',
                       'WestVirginia_T', 'Wisconsin_T', 'Wyoming_T', 'PuertoRico_T', 'Guam_T', 'VirginIslands_T',
                       'TotAllocs_T', 'TrsFullName', 'SignDt']],
                     [['6.1', '6.2', '6.3', '6.4'],
                      ['FormTp', 'CommID', 'CommNm', 'AddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'PrimElec',
                       'GenElec', 'RptCd', 'ElecCd', 'ElecDt', 'ElecSt', 'CovgFmDt', 'CovgToDt', 'TrsLName', 'TrsFName',
                       'TrsMName', 'TrsPfx', 'TrsSfx', 'SignDt', 'CashBegin_P_6', 'TotRcpts_P_7', 'Subtotal_P_8',
                       'TotDisb_P_9', 'CashClose_P_10', 'DebtsTo_P_11', 'DebtsBy_P_12', 'LmtdExps_P_13',
                       'NetConts_P_14', 'NetOpExps_P_15', 'FedFnds_P_16', 'IndContsTot_P_17a3', 'PolPtyCommConts_P_17b',
                       'OthPolCommConts_P_17c', 'CandConts_P_17d', 'TotConts_P_17e', 'TranFmPtyComms_P_18',
                       'CandLoans_P_19a', 'OthLoans_P_19b', 'TotLoans_P_19c', 'OptgOffsets_P_20a',
                       'FndrsgOffsets_P_20b', 'LegalAcctgOffsets_P_20c', 'TotOffsets_P_20d', 'OthRcpts_P_21',
                       'TotRcpts_P_22', 'OpExps_P_23', 'TranToOthAuthComms_P_24', 'FndrsgDisb_P_25',
                       'LegalAcctgDisb_P_26', 'CandLoansRepaid_P_27a', 'OthLoansRepaid_P_27b', 'TotLoansRepaid_P_27c',
                       'RefundsInd_P_28a', 'RefundsPolPtyComms_P_28b', 'RefundsOthPolComms_P_28c', 'TotRefunds_P_28d',
                       'OthDisb_P_29', 'TotDisb_P_30', 'ItmsToBeLiq_P_31', 'Alabama_P', 'Alaska_P', 'Arizona_P',
                       'Arkansas_P', 'California_P', 'Colorado_P', 'Connecticut_P', 'Delaware_P', 'DistCol_P',
                       'Florida_P', 'Georgia_P', 'Hawaii_P', 'Idaho_P', 'Illinois_P', 'Indiana_P', 'Iowa_P', 'Kansas_P',
                       'Kentucky_P', 'Louisiana_P', 'Maine_P', 'Maryland_P', 'Massachusetts_P', 'Michigan_P',
                       'Minnesota_P', 'Mississippi_P', 'Missouri_P', 'Montana_P', 'Nebraska_P', 'Nevada_P',
                       'NewHampshire_P', 'NewJersey_P', 'NewMexico_P', 'NewYork_P', 'NorthCarolina_P', 'NorthDakota_P',
                       'Ohio_P', 'Oklahoma_P', 'Oregon_P', 'Pennsylvania_P', 'RhodeIsland_P', 'SouthCarolina_P',
                       'SouthDakota_P', 'Tennessee_P', 'Texas_P', 'Utah_P', 'Vermont_P', 'Virginia_P', 'Washington_P',
                       'WestVirginia_P', 'Wisconsin_P', 'Wyoming_P', 'PuertoRico_P', 'Guam_P', 'VirginIslands_P',
                       'TotAllocs_P', 'FedFnds_T_16', 'IndContsTot_T_17a3', 'PolPtyCommConts_T_17b',
                       'OthPolCommConts_T_17c', 'CandConts_T_17d', 'TotConts_T_17e', 'TranFmPtyComms_T_18',
                       'CandLoans_T_19a', 'OthLoans_T_19b', 'TotLoans_T_19c', 'OptgOffsets_T_20a',
                       'FndrsgOffsets_T_20b', 'LegalAcctgOffsets_T_20c', 'TotOffsets_T_20d', 'OthRcpts_T_21',
                       'TotRcpts_T_22', 'OpExps_T_23', 'TranToOthAuthComms_T_24', 'FndrsgDisb_T_25',
                       'LegalAcctgDisb_T_26', 'CandLoansRepaid_T_27a', 'OthLoansRepaid_T_27b', 'TotLoansRepaid_T_27c',
                       'RefundsInd_T_28a', 'RefundsPolPtyComms_T_28b', 'RefundsOthPolComms_T_28c', 'TotRefunds_T_28d',
                       'OthDisb_T_29', 'TotDisb_T_30', 'Alabama_T', 'Alaska_T', 'Arizona_T', 'Arkansas_T',
                       'California_T', 'Colorado_T', 'Connecticut_T', 'Delaware_T', 'DistCol_T', 'Florida_T',
                       'Georgia_T', 'Hawaii_T', 'Idaho_T', 'Illinois_T', 'Indiana_T', 'Iowa_T', 'Kansas_T',
                       'Kentucky_T', 'Louisiana_T', 'Maine_T', 'Maryland_T', 'Massachusetts_T', 'Michigan_T',
                       'Minnesota_T', 'Mississippi_T', 'Missouri_T', 'Montana_T', 'Nebraska_T', 'Nevada_T',
                       'NewHampshire_T', 'NewJersey_T', 'NewMexico_T', 'NewYork_T', 'NorthCarolina_T', 'NorthDakota_T',
                       'Ohio_T', 'Oklahoma_T', 'Oregon_T', 'Pennsylvania_T', 'RhodeIsland_T', 'SouthCarolina_T',
                       'SouthDakota_T', 'Tennessee_T', 'Texas_T', 'Utah_T', 'Vermont_T', 'Virginia_T', 'Washington_T',
                       'WestVirginia_T', 'Wisconsin_T', 'Wyoming_T', 'PuertoRico_T', 'Guam_T', 'VirginIslands_T',
                       'TotAllocs_T']],
                     [['7.0', '8.0', '8.1', '8.2', '8.3'],
                      ['FormTp', 'CommID', 'CommNm', 'AddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'PrimElec',
                       'GenElec', 'RptCd', 'ElecCd', 'ElecDt', 'ElecSt', 'CovgFmDt', 'CovgToDt', 'TrsLName', 'TrsFName',
                       'TrsMName', 'TrsPfx', 'TrsSfx', 'SignDt', 'CashBegin_P_6', 'TotRcpts_P_7', 'Subtotal_P_8',
                       'TotDisb_P_9', 'CashClose_P_10', 'DebtsTo_P_11', 'DebtsBy_P_12', 'LmtdExps_P_13',
                       'NetConts_P_14', 'NetOpExps_P_15', 'FedFnds_P_16', 'IndContsItem_P_17a1',
                       'IndContsUnitem_P_17a2', 'IndContsTot_P_17a3', 'PolPtyCommConts_P_17b', 'OthPolCommConts_P_17c',
                       'CandConts_P_17d', 'TotConts_P_17e', 'TranFmPtyComms_P_18', 'CandLoans_P_19a', 'OthLoans_P_19b',
                       'TotLoans_P_19c', 'OptgOffsets_P_20a', 'FndrsgOffsets_P_20b', 'LegalAcctgOffsets_P_20c',
                       'TotOffsets_P_20d', 'OthRcpts_P_21', 'TotRcpts_P_22', 'OpExps_P_23', 'TranToOthAuthComms_P_24',
                       'FndrsgDisb_P_25', 'LegalAcctgDisb_P_26', 'CandLoansRepaid_P_27a', 'OthLoansRepaid_P_27b',
                       'TotLoansRepaid_P_27c', 'RefundsInd_P_28a', 'RefundsPolPtyComms_P_28b',
                       'RefundsOthPolComms_P_28c', 'TotRefunds_P_28d', 'OthDisb_P_29', 'TotDisb_P_30',
                       'ItmsToBeLiq_P_31', 'Alabama_P', 'Alaska_P', 'Arizona_P', 'Arkansas_P', 'California_P',
                       'Colorado_P', 'Connecticut_P', 'Delaware_P', 'DistCol_P', 'Florida_P', 'Georgia_P', 'Hawaii_P',
                       'Idaho_P', 'Illinois_P', 'Indiana_P', 'Iowa_P', 'Kansas_P', 'Kentucky_P', 'Louisiana_P',
                       'Maine_P', 'Maryland_P', 'Massachusetts_P', 'Michigan_P', 'Minnesota_P', 'Mississippi_P',
                       'Missouri_P', 'Montana_P', 'Nebraska_P', 'Nevada_P', 'NewHampshire_P', 'NewJersey_P',
                       'NewMexico_P', 'NewYork_P', 'NorthCarolina_P', 'NorthDakota_P', 'Ohio_P', 'Oklahoma_P',
                       'Oregon_P', 'Pennsylvania_P', 'RhodeIsland_P', 'SouthCarolina_P', 'SouthDakota_P', 'Tennessee_P',
                       'Texas_P', 'Utah_P', 'Vermont_P', 'Virginia_P', 'Washington_P', 'WestVirginia_P', 'Wisconsin_P',
                       'Wyoming_P', 'PuertoRico_P', 'Guam_P', 'VirginIslands_P', 'TotAllocs_P', 'FedFnds_T_16',
                       'IndContsItem_T_17a1', 'IndContsUnitem_T_17a2', 'IndContsTot_T_17a3', 'PolPtyCommConts_T_17b',
                       'OthPolCommConts_T_17c', 'CandConts_T_17d', 'TotConts_T_17e', 'TranFmPtyComms_T_18',
                       'CandLoans_T_19a', 'OthLoans_T_19b', 'TotLoans_T_19c', 'OptgOffsets_T_20a',
                       'FndrsgOffsets_T_20b', 'LegalAcctgOffsets_T_20c', 'TotOffsets_T_20d', 'OthRcpts_T_21',
                       'TotRcpts_T_22', 'OpExps_T_23', 'TranToOthAuthComms_T_24', 'FndrsgDisb_T_25',
                       'LegalAcctgDisb_T_26', 'CandLoansRepaid_T_27a', 'OthLoansRepaid_T_27b', 'TotLoansRepaid_T_27c',
                       'RefundsInd_T_28a', 'RefundsPolPtyComms_T_28b', 'RefundsOthPolComms_T_28c', 'TotRefunds_T_28d',
                       'OthDisb_T_29', 'TotDisb_T_30', 'Alabama_T', 'Alaska_T', 'Arizona_T', 'Arkansas_T',
                       'California_T', 'Colorado_T', 'Connecticut_T', 'Delaware_T', 'DistCol_T', 'Florida_T',
                       'Georgia_T', 'Hawaii_T', 'Idaho_T', 'Illinois_T', 'Indiana_T', 'Iowa_T', 'Kansas_T',
                       'Kentucky_T', 'Louisiana_T', 'Maine_T', 'Maryland_T', 'Massachusetts_T', 'Michigan_T',
                       'Minnesota_T', 'Mississippi_T', 'Missouri_T', 'Montana_T', 'Nebraska_T', 'Nevada_T',
                       'NewHampshire_T', 'NewJersey_T', 'NewMexico_T', 'NewYork_T', 'NorthCarolina_T', 'NorthDakota_T',
                       'Ohio_T', 'Oklahoma_T', 'Oregon_T', 'Pennsylvania_T', 'RhodeIsland_T', 'SouthCarolina_T',
                       'SouthDakota_T', 'Tennessee_T', 'Texas_T', 'Utah_T', 'Vermont_T', 'Virginia_T', 'Washington_T',
                       'WestVirginia_T', 'Wisconsin_T', 'Wyoming_T', 'PuertoRico_T', 'Guam_T', 'VirginIslands_T',
                       'TotAllocs_T']]]],
            ['F3X', [[['1', '2', '3'],
                      ['FormTp', 'CommID', 'CommNm', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'AddrChg',
                       'flgQualComm', 'RptCd', 'ElecCd', 'ElecDt', 'ElecSt', 'CovgFmDt', 'CovgToDt', 'CashBegin_P_6b',
                       'TotRcpts_P_6c', 'Subtotal_P_6d', 'TotDisb_P_7', 'CashClose_P_8', 'DebtsTo_P_9', 'DebtsBy_P_10',
                       'IndContsItem_P_11a1', 'IndContsUnitem_P_11a2', 'IndContsTot_P_11a3', 'PolPtyCommConts_P_11b',
                       'OthPolCommConts_P_11c', 'TotConts_P_11d', 'TranFmPtyComms_P_12', 'AllLoansRcvd_P_13',
                       'LoanPymtsRcvd_P_14', 'RefundOffsets_P_15', 'RefundsFedConts_P_16', 'OthFedRcptsDvds_P_17',
                       'TotNonFedTrans_P_18c', 'TotRcpts_P_19', 'TotFedRcpts_P_20', 'OpExpsFedShr_P_21a1',
                       'OpExpsNonFedShr_P_21a2', 'OpExpsOthFed_P_21b', 'TotOpExps_P_21c', 'TranToPtyComms_P_22',
                       'ContsToFedCandsComms_P_23', 'IndtExps_P_24', 'CoordExpsByPtyComms_P_25', 'LoansRepaid_P_26',
                       'LoansMade_P_27', 'RefundsInd_P_28a', 'RefundsPolPtyComms_P_28b', 'RefundsOthPolComms_P_28c',
                       'TotContRefunds_P_28d', 'OthDisb_P_29', 'TotDisb_P_31', 'TotFedDisb_P_32', 'TotConts_P_33',
                       'TotContRefunds_P_34', 'NetConts_P_35', 'TotFedOpExps_P_36', 'TotOffsetsOpExp_P_37',
                       'NetOpExps_P_38', 'CashBegin_T_6a', 'CashBeginYr', 'TotRcpts_T_6c', 'Subtotal_T_6d',
                       'TotDisb_T_7', 'CashClose_T_8', 'IndContsItem_T_11a1', 'IndContsUnitem_T_11a2',
                       'IndContsTot_T_11a3', 'PolPtyCommConts_T_11b', 'OthPolCommConts_T_11c', 'TotConts_T_11d',
                       'TranFmPtyComms_T_12', 'AllLoansRcvd_T_13', 'LoanPymtsRcvd_T_14', 'RefundOffsets_T_15',
                       'RefundsFedConts_T_16', 'OthFedRcptsDvds_T_17', 'TotNonFedTrans_T_18c', 'TotRcpts_T_19',
                       'TotFedRcpts_T_20', 'OpExpsFedShr_T_21a1', 'OpExpsNonFedShr_T_21a2', 'OpExpsOthFed_T_21b',
                       'TotOpExps_T_21c', 'TranToPtyComms_T_22', 'ContsToFedCandsComms_T_23', 'IndtExps_T_24',
                       'CoordExpsByPtyComms_T_25', 'LoansRepaid_T_26', 'LoansMade_T_27', 'RefundsInd_T_28a',
                       'RefundsPolPtyComms_T_28b', 'RefundsOthPolComms_T_28c', 'TotContRefunds_T_28d', 'OthDisb_T_29',
                       'TotDisb_T_31', 'TotFedDisb_T_32', 'TotConts_T_33', 'TotContRefunds_T_34', 'NetConts_T_35',
                       'TotFedOpExps_T_36', 'TotOffsetsOpExp_T_37', 'NetOpExps_T_38', 'TrsFullName', 'SignDt']],
                     [['5.0', '5.1', '5.2', '5.3'],
                      ['FormTp', 'CommID', 'CommNm', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'AddrChg',
                       'flgQualComm', 'RptCd', 'ElecCd', 'ElecDt', 'ElecSt', 'CovgFmDt', 'CovgToDt', 'CashBegin_P_6b',
                       'TotRcpts_P_6c', 'Subtotal_P_6d', 'TotDisb_P_7', 'CashClose_P_8', 'DebtsTo_P_9', 'DebtsBy_P_10',
                       'IndContsItem_P_11a1', 'IndContsUnitem_P_11a2', 'IndContsTot_P_11a3', 'PolPtyCommConts_P_11b',
                       'OthPolCommConts_P_11c', 'TotConts_P_11d', 'TranFmPtyComms_P_12', 'AllLoansRcvd_P_13',
                       'LoanPymtsRcvd_P_14', 'RefundOffsets_P_15', 'RefundsFedConts_P_16', 'OthFedRcptsDvds_P_17',
                       'TranFmNonFedAcctH3_P_18a', 'TotRcpts_P_19', 'TotFedRcpts_P_20', 'OpExpsFedShr_P_21a1',
                       'OpExpsNonFedShr_P_21a2', 'OpExpsOthFed_P_21b', 'TotOpExps_P_21c', 'TranToPtyComms_P_22',
                       'ContsToFedCandsComms_P_23', 'IndtExps_P_24', 'CoordExpsByPtyComms_P_25', 'LoansRepaid_P_26',
                       'LoansMade_P_27', 'RefundsInd_P_28a', 'RefundsPolPtyComms_P_28b', 'RefundsOthPolComms_P_28c',
                       'TotContRefunds_P_28d', 'OthDisb_P_29', 'TotDisb_P_31', 'TotFedDisb_P_32', 'TotConts_P_33',
                       'TotContRefunds_P_34', 'NetConts_P_35', 'TotFedOpExps_P_36', 'TotOffsetsOpExp_P_37',
                       'NetOpExps_P_38', 'CashBegin_T_6a', 'CashBeginYr', 'TotRcpts_T_6c', 'Subtotal_T_6d',
                       'TotDisb_T_7', 'CashClose_T_8', 'IndContsItem_T_11a1', 'IndContsUnitem_T_11a2',
                       'IndContsTot_T_11a3', 'PolPtyCommConts_T_11b', 'OthPolCommConts_T_11c', 'TotConts_T_11d',
                       'TranFmPtyComms_T_12', 'AllLoansRcvd_T_13', 'LoanPymtsRcvd_T_14', 'RefundOffsets_T_15',
                       'RefundsFedConts_T_16', 'OthFedRcptsDvds_T_17', 'TranFmNonFedAcctH3_T_18a', 'TotRcpts_T_19',
                       'TotFedRcpts_T_20', 'OpExpsFedShr_T_21a1', 'OpExpsNonFedShr_T_21a2', 'OpExpsOthFed_T_21b',
                       'TotOpExps_T_21c', 'TranToPtyComms_T_22', 'ContsToFedCandsComms_T_23', 'IndtExps_T_24',
                       'CoordExpsByPtyComms_T_25', 'LoansRepaid_T_26', 'LoansMade_T_27', 'RefundsInd_T_28a',
                       'RefundsPolPtyComms_T_28b', 'RefundsOthPolComms_T_28c', 'TotContRefunds_T_28d', 'OthDisb_T_29',
                       'TotDisb_T_31', 'TotFedDisb_T_32', 'TotConts_T_33', 'TotContRefunds_T_34', 'NetConts_T_35',
                       'TotFedOpExps_T_36', 'TotOffsetsOpExp_T_37', 'NetOpExps_T_38', 'TrsFullName', 'SignDt',
                       'TranFmNonFedAcctH5_P_18b', 'TotNonFedTrans_P_18c', 'ShrdElecActivityFedShr_P_30a1',
                       'ShrdElecActivityNonFedShr_P_30a2', 'NonAllocFedElecActivity_P_30b', 'TotFedElecActivity_P_30c',
                       'TranFmNonFedAcctH5_T_18b', 'TotNonFedTrans_T_18c', 'ShrdElecActivityFedShr_T_30a1',
                       'ShrdElecActivityNonFedShr_T_30a2', 'NonAllocFedElecActivity_T_30b',
                       'TotFedElecActivity_T_30c']],
                     [['6.1', '6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                      ['FormTp', 'CommID', 'CommNm', 'AddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'RptCd',
                       'ElecCd', 'ElecDt', 'ElecSt', 'CovgFmDt', 'CovgToDt', 'flgQualComm', 'TrsLName', 'TrsFName',
                       'TrsMName', 'TrsPfx', 'TrsSfx', 'SignDt', 'CashBegin_P_6b', 'TotRcpts_P_6c', 'Subtotal_P_6d',
                       'TotDisb_P_7', 'CashClose_P_8', 'DebtsTo_P_9', 'DebtsBy_P_10', 'IndContsItem_P_11a1',
                       'IndContsUnitem_P_11a2', 'IndContsTot_P_11a3', 'PolPtyCommConts_P_11b', 'OthPolCommConts_P_11c',
                       'TotConts_P_11d', 'TranFmPtyComms_P_12', 'AllLoansRcvd_P_13', 'LoanPymtsRcvd_P_14',
                       'RefundOffsets_P_15', 'RefundsFedConts_P_16', 'OthFedRcptsDvds_P_17', 'TranFmNonFedAcctH3_P_18a',
                       'TranFmNonFedAcctH5_P_18b', 'TotNonFedTrans_P_18c', 'TotRcpts_P_19', 'TotFedRcpts_P_20',
                       'OpExpsFedShr_P_21a1', 'OpExpsNonFedShr_P_21a2', 'OpExpsOthFed_P_21b', 'TotOpExps_P_21c',
                       'TranToPtyComms_P_22', 'ContsToFedCandsComms_P_23', 'IndtExps_P_24', 'CoordExpsByPtyComms_P_25',
                       'LoansRepaid_P_26', 'LoansMade_P_27', 'RefundsInd_P_28a', 'RefundsPolPtyComms_P_28b',
                       'RefundsOthPolComms_P_28c', 'TotContRefunds_P_28d', 'OthDisb_P_29',
                       'ShrdElecActivityFedShr_P_30a1', 'ShrdElecActivityNonFedShr_P_30a2',
                       'NonAllocFedElecActivity_P_30b', 'TotFedElecActivity_P_30c', 'TotDisb_P_31', 'TotFedDisb_P_32',
                       'TotConts_P_33', 'TotContRefunds_P_34', 'NetConts_P_35', 'TotFedOpExps_P_36',
                       'TotOffsetsOpExp_P_37', 'NetOpExps_P_38', 'CashBegin_T_6a', 'CashBeginYr', 'TotRcpts_T_6c',
                       'Subtotal_T_6d', 'TotDisb_T_7', 'CashClose_T_8', 'IndContsItem_T_11a1', 'IndContsUnitem_T_11a2',
                       'IndContsTot_T_11a3', 'PolPtyCommConts_T_11b', 'OthPolCommConts_T_11c', 'TotConts_T_11d',
                       'TranFmPtyComms_T_12', 'AllLoansRcvd_T_13', 'LoanPymtsRcvd_T_14', 'RefundOffsets_T_15',
                       'RefundsFedConts_T_16', 'OthFedRcptsDvds_T_17', 'TranFmNonFedAcctH3_T_18a',
                       'TranFmNonFedAcctH5_T_18b', 'TotNonFedTrans_T_18c', 'TotRcpts_T_19', 'TotFedRcpts_T_20',
                       'OpExpsFedShr_T_21a1', 'OpExpsNonFedShr_T_21a2', 'OpExpsOthFed_T_21b', 'TotOpExps_T_21c',
                       'TranToPtyComms_T_22', 'ContsToFedCandsComms_T_23', 'IndtExps_T_24', 'CoordExpsByPtyComms_T_25',
                       'LoansRepaid_T_26', 'LoansMade_T_27', 'RefundsInd_T_28a', 'RefundsPolPtyComms_T_28b',
                       'RefundsOthPolComms_T_28c', 'TotContRefunds_T_28d', 'OthDisb_T_29',
                       'ShrdElecActivityFedShr_T_30a1', 'ShrdElecActivityNonFedShr_T_30a2',
                       'NonAllocFedElecActivity_T_30b', 'TotFedElecActivity_T_30c', 'TotDisb_T_31', 'TotFedDisb_T_32',
                       'TotConts_T_33', 'TotContRefunds_T_34', 'NetConts_T_35', 'TotFedOpExps_T_36',
                       'TotOffsetsOpExp_T_37', 'NetOpExps_T_38']]]],
            ['Hdr', [[['3', '5.0', '5.1', '5.2', '5.3'],
                      ['RecType', 'EFType', 'Ver', 'SftNm', 'SftVer', 'NmDelim', 'RptID', 'RptNbr', 'HdrCmnt']],
                     [['6.1', '6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                      ['RecType', 'EFType', 'Ver', 'SftNm', 'SftVer', 'RptID', 'RptNbr', 'HdrCmnt']]]],
            ['SA', [[['8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'ContOrgNm', 'ContLName',
                      'ContFName', 'ContMName', 'ContPfx', 'ContSfx', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip',
                      'ElecCd', 'ElecDesc', 'ContDt', 'ContAmt', 'ContAgg', 'ContPurpDesc', 'Emp', 'Occ', 'DonorCommID',
                      'DonorCommNm', 'DonorCandID', 'DonorCandLName', 'DonorCandFName', 'DonorCandMName',
                      'DonorCandPfx', 'DonorCandSfx', 'DonorCandOfc', 'DonorCandSt', 'DonorCandDist', 'ConduitNm',
                      'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip', 'MemoCd', 'MemoTxt',
                      'SIorSLRef']],
                    [['6.4', '7.0'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'ContOrgNm', 'ContLName',
                      'ContFName', 'ContMName', 'ContPfx', 'ContSfx', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip',
                      'ElecCd', 'ElecDesc', 'ContDt', 'ContAmt', 'ContAgg', 'ContPurpCd', 'ContPurpDesc', 'Emp', 'Occ',
                      'DonorCommID', 'DonorCommNm', 'DonorCandID', 'DonorCandLName', 'DonorCandFName', 'DonorCandMName',
                      'DonorCandPfx', 'DonorCandSfx', 'DonorCandOfc', 'DonorCandSt', 'DonorCandDist', 'ConduitNm',
                      'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip', 'MemoCd', 'MemoTxt',
                      'SIorSLRef']],
                    [['6.2', '6.3'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'ContOrgNm', 'ContLName',
                      'ContFName', 'ContMName', 'ContPfx', 'ContSfx', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip',
                      'ElecCd', 'ElecDesc', 'ContDt', 'ContAmt', 'ContAgg', 'ContPurpCd', 'ContPurpDesc', 'IncLmtCd',
                      'Emp', 'Occ', 'DonorCommID', 'DonorCommNm', 'DonorCandID', 'DonorCandLName', 'DonorCandFName',
                      'DonorCandMName', 'DonorCandPfx', 'DonorCandSfx', 'DonorCandOfc', 'DonorCandSt', 'DonorCandDist',
                      'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip',
                      'MemoCd', 'MemoTxt', 'SIorSLRef']],
                    [['6.1'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'ContOrgNm', 'ContLName',
                      'ContFName', 'ContMName', 'ContPfx', 'ContSfx', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip',
                      'ElecCd', 'ElecDesc', 'ContDt', 'ContAmt', 'ContAgg', 'ContPurpCd', 'ContPurpDesc', 'IncLmtCd',
                      'Emp', 'Occ', 'DonorCommID', 'DonorCandID', 'DonorCandLName', 'DonorCandFName', 'DonorCandMName',
                      'DonorCandPfx', 'DonorCandSfx', 'DonorCandOfc', 'DonorCandSt', 'DonorCandDist', 'ConduitNm',
                      'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip', 'MemoCd', 'MemoTxt',
                      'SIorSLRef']],
                    [['5.1', '5.2', '5.3'],
                     ['LineNbr', 'CommID', 'EntTp', 'ContFullName', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'ElecCd',
                      'ElecDesc', 'Emp', 'Occ', 'ContAgg', 'ContDt', 'ContAmt', 'ContPurpCd', 'ContPurpDesc',
                      'DonorCommID', 'DonorCandID', 'DonorCandFullName', 'DonorCandOfc', 'DonorCandSt', 'DonorCandDist',
                      'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip',
                      'MemoCd', 'MemoTxt', 'AmendCd', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'SIorSLRef', 'IncLmtCd',
                      'ContOrgName', 'ContLName', 'ContFName', 'ContMName', 'ContPfx', 'ContSfx']],
                    [['5.0'],
                     ['LineNbr', 'CommID', 'EntTp', 'ContFullName', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'ElecCd',
                      'ElecDesc', 'Emp', 'Occ', 'ContAgg', 'ContDt', 'ContAmt', 'ContPurpCd', 'ContPurpDesc',
                      'DonorCommID', 'DonorCandID', 'DonorCandFullName', 'DonorCandOfc', 'DonorCandSt', 'DonorCandDist',
                      'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip',
                      'MemoCd', 'MemoTxt', 'AmendCd', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'SIorSLRef',
                      'IncLmtCd']],
                    [['3'],
                     ['LineNbr', 'CommID', 'EntTp', 'ContFullName', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'ElecCd',
                      'ElecDesc', 'Emp', 'Occ', 'ContAgg', 'ContDt', 'ContAmt', 'ContPurpCd', 'ContPurpDesc',
                      'DonorCommID', 'DonorCandID', 'DonorCandFullName', 'DonorCandOfc', 'DonorCandSt', 'DonorCandDist',
                      'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip',
                      'MemoCd', 'MemoTxt', 'AmendCd', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'NatlCommNonFedAcct']],
                    [['2'],
                     ['LineNbr', 'CommID', 'EntTp', 'ContFullName', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'ElecCd',
                      'ElecDesc', 'Emp', 'Occ', 'ContAgg', 'ContDt', 'ContAmt', 'ContPurpCd', 'ContPurpDesc',
                      'DonorCommID', 'DonorCandID', 'DonorCandFullName', 'DonorCandOfc', 'DonorCandSt', 'DonorCandDist',
                      'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip',
                      'MemoCd', 'MemoTxt', 'AmendCd', 'TransID', 'BkRefTransID', 'BkRefSchdNm']],
                    [['1'], ['LineNbr', 'CommID', 'ContFullName', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'ElecCd',
                             'ElecDesc', 'Emp', 'Occ', 'ContAgg', 'ContDt', 'ContAmt', 'ContPurpCd', 'ContPurpDesc',
                             'DonorCommID', 'DonorCommNm', 'DonorCommAddr1', 'DonorCommAddr1', 'DonorCommCity',
                             'DonorCommState', 'DonorCommZip', 'DonorCandID', 'DonorCandFullName', 'DonorCandOfc',
                             'DonorCandState', 'DonorCandDist', 'MemoCd', 'MemoTxt', 'AmendCd']]]],
            ['SB', [[['8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm',
                      'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2',
                      'PayeeCity', 'PayeeState', 'PayeeZip', 'ElecCd', 'ElecDesc', 'ExpDt', 'ExpAmt',
                      'SemiAnnRefBundAmt', 'ExpPurpDesc', 'ExpCatCd', 'BenCommID', 'BenCommNm', 'BenCandID',
                      'BenCandLName', 'BenCandFName', 'BenCandMName', 'BenCandPfx', 'BenCandSfx', 'BenCandOfc',
                      'BenCandState', 'BenCandDist', 'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity',
                      'ConduitState', 'ConduitZip', 'MemoCd', 'MemoTxt', 'SIorSLRef']],
                    [['6.4', '7.0'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm',
                      'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2',
                      'PayeeCity', 'PayeeState', 'PayeeZip', 'ElecCd', 'ElecDesc', 'ExpDt', 'ExpAmt',
                      'SemiAnnRefBundAmt', 'ExpPurpCd', 'ExpPurpDesc', 'ExpCatCd', 'BenCommID', 'BenCommNm',
                      'BenCandID', 'BenCandLName', 'BenCandFName', 'BenCandMName', 'BenCandPfx', 'BenCandSfx',
                      'BenCandOfc', 'BenCandState', 'BenCandDist', 'ConduitNm', 'ConduitAddr1', 'ConduitAddr2',
                      'ConduitCity', 'ConduitState', 'ConduitZip', 'MemoCd', 'MemoTxt', 'SIorSLRef']],
                    [['6.2', '6.3'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm',
                      'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2',
                      'PayeeCity', 'PayeeState', 'PayeeZip', 'ElecCd', 'ElecDesc', 'ExpDt', 'ExpAmt', 'ExpPurpCd',
                      'ExpPurpDesc', 'ExpCatCd', 'RfdOrDispExcess', 'CommunDt', 'BenCommID', 'BenCommNm', 'BenCandID',
                      'BenCandLName', 'BenCandFName', 'BenCandMName', 'BenCandPfx', 'BenCandSfx', 'BenCandOfc',
                      'BenCandState', 'BenCandDist', 'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity',
                      'ConduitState', 'ConduitZip', 'MemoCd', 'MemoTxt', 'SIorSLRef']],
                    [['6.1'], ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm',
                               'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1',
                               'PayeeAddr2', 'PayeeCity', 'PayeeState', 'PayeeZip', 'ElecCd', 'ElecDesc', 'ExpDt',
                               'ExpAmt', 'ExpPurpCd', 'ExpPurpDesc', 'ExpCatCd', 'RfdOrDispExcess', 'CommunDt',
                               'BenCommID', 'BenCandID', 'BenCandLName', 'BenCandFName', 'BenCandMName', 'BenCandPfx',
                               'BenCandSfx', 'BenCandOfc', 'BenCandState', 'BenCandDist', 'ConduitNm', 'ConduitAddr1',
                               'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip', 'MemoCd', 'MemoTxt',
                               'SIorSLRef']],
                    [['5.1', '5.2', '5.3'],
                     ['LineNbr', 'CommID', 'EntTp', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity',
                      'PayeeState', 'PayeeZip', 'ExpPurpCd', 'ExpPurpDesc', 'ElecCd', 'ElecDesc', 'ExpDt', 'ExpAmt',
                      'BenCommID', 'BenCandID', 'BenCandFullName', 'BenCandOfc', 'BenCandState', 'BenCandDist',
                      'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip',
                      'MemoCd', 'MemoTxt', 'AmendCd', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'SIorSLRef',
                      'RfdOrDispExcess']],
                    [['5.0'], ['LineNbr', 'CommID', 'EntTp', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity',
                               'PayeeState', 'PayeeZip', 'ExpPurpCd', 'ExpPurpDesc', 'ElecCd', 'ElecDesc', 'ExpDt',
                               'ExpAmt', 'BenCommID', 'BenCandID', 'BenCandFullName', 'BenCandOfc', 'BenCandState',
                               'BenCandDist', 'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity',
                               'ConduitState', 'ConduitZip', 'MemoCd', 'MemoTxt', 'AmendCd', 'TransID', 'BkRefTransID',
                               'BkRefSchdNm', 'SIorSLRef', 'RfdOrDispExcess', 'ExpCatCd', 'CommunDt']],
                    [['3'], ['LineNbr', 'CommID', 'EntTp', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity',
                             'PayeeState', 'PayeeZip', 'ExpPurpCd', 'ExpPurpDesc', 'ElecCd', 'ElecDesc', 'ExpDt',
                             'ExpAmt', 'BenCommID', 'BenCandID', 'BenCandFullName', 'BenCandOfc', 'BenCandState',
                             'BenCandDist', 'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState',
                             'ConduitZip', 'MemoCd', 'MemoTxt', 'AmendCd', 'TransID', 'BkRefTransID', 'BkRefSchdNm',
                             'NatCommNonFedAcct']],
                    [['2'], ['LineNbr', 'CommID', 'EntTp', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity',
                             'PayeeState', 'PayeeZip', 'ExpPurpCd', 'ExpPurpDesc', 'ElecCd', 'ElecDesc', 'ExpDt',
                             'ExpAmt', 'BenCommID', 'BenCandID', 'BenCandFullName', 'BenCandOfc', 'BenCandState',
                             'BenCandDist', 'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState',
                             'ConduitZip', 'MemoCd', 'MemoTxt', 'AmendCd', 'TransID', 'BkRefTransID', 'BkRefSchdNm']],
                    [['1'],
                     ['LineNbr', 'CommID', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeState',
                      'PayeeZip', 'ExpPurpCd', 'ExpPurpDesc', 'ElecCd', 'ElecDesc', 'ExpDt', 'ExpAmt', 'BenCommID',
                      'BenCommNm', 'BenCommAddr1', 'BenCommAddr2', 'BenCommCity', 'BenCommState', 'BenCommZip',
                      'BenCandID', 'BenCandFullName', 'BenCandOfc', 'BenCandState', 'BenCandDist', 'MemoCd', 'MemoTxt',
                      'AmendCd']]]],
            ['SC', [[['6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'RctLnNbr', 'EntTp', 'LenderOrgName', 'LenderLName',
                      'LenderFName', 'LenderMName', 'LenderPfx', 'LenderSfx', 'LenderAddr1', 'LenderAddr2',
                      'LenderCity', 'LenderState', 'LenderZip', 'ElecCd', 'ElecDesc', 'LoanAmt', 'PymtToDt', 'LoanBlnc',
                      'IncurredDt', 'DueDt', 'IntRt', 'flgSecured', 'flgPersFunds', 'LenderCommID', 'LenderCandID',
                      'LenderCandLName', 'LenderCandFName', 'LenderCandMName', 'LenderCandPfx', 'LenderCandSfx',
                      'LenderCandOfc', 'LenderCandState', 'LenderCandDist', 'MemoCd', 'MemoTxt']],
                    [['6.1'], ['LineNbr', 'CommID', 'TransID', 'RctLnNbr', 'EntTp', 'LenderOrgName', 'LenderLName',
                               'LenderFName', 'LenderMName', 'LenderPfx', 'LenderSfx', 'LenderAddr1', 'LenderAddr2',
                               'LenderCity', 'LenderState', 'LenderZip', 'ElecCd', 'ElecDesc', 'LoanAmt', 'PymtToDt',
                               'LoanBlnc', 'IncurredDt', 'DueDt', 'IntRt', 'flgSecured', 'LenderCommID', 'LenderCandID',
                               'LenderCandLName', 'LenderCandFName', 'LenderCandMName', 'LenderCandPfx',
                               'LenderCandSfx', 'LenderCandOfc', 'LenderCandState', 'LenderCandDist']],
                    [['5.1', '5.2', '5.3'],
                     ['LineNbr', 'CommID', 'EntTp', 'LenderFullName', 'LenderAddr1', 'LenderAddr2', 'LenderCity',
                      'LenderState', 'LenderZip', 'ElecCd', 'ElecDesc', 'LoanAmt', 'PymtToDt', 'LoanBlnc', 'IncurredDt',
                      'DueDt', 'IntRt', 'flgSecured', 'LenderCommID', 'LenderCandID', 'LenderCandFullName',
                      'LenderCandOfc', 'LenderCandState', 'LenderCandDist', 'AmendCd', 'TransID', 'RctLnNbr']],
                    [['3', '5.0'],
                     ['LineNbr', 'CommID', 'EntTp', 'LenderFullName', 'LenderAddr1', 'LenderAddr2', 'LenderCity',
                      'LenderState', 'LenderZip', 'ElecCd', 'ElecDesc', 'LoanAmt', 'PymtToDt', 'LoanBlnc', 'IncurredDt',
                      'DueDt', 'IntRt', 'flgSecured', 'LenderCommID', 'LenderCandID', 'LenderCandFullName',
                      'LenderCandOfc', 'LenderCandState', 'LenderCandDist', 'AmendCd', 'TransID']],
                    [['2'], ['LineNbr', 'CommID', 'EntTp', 'LenderFullName', 'LenderAddr1', 'LenderAddr2', 'LenderCity',
                             'LenderState', 'LenderZip', 'ElecCd', 'ElecDesc', 'LoanAmt', 'PymtToDt', 'LoanBlnc',
                             'IncurredDt', 'DueDt', 'IntRt', 'flgSecured', 'LenderCommID', 'LenderCandID',
                             'LenderCandFullName', 'LenderCandOfc', 'LenderCandState', 'LenderCandDist', 'AmendCd',
                             'TransID', 'BkRefTransID', 'BkRefSchdNm']],
                    [['1'],
                     ['LineNbr', 'CommID', 'TransID', 'LenderFullName', 'LenderAddr1', 'LenderAddr2', 'LenderCity',
                      'LenderState', 'LenderZip', 'ElecCd', 'ElecDesc', 'LoanAmt', 'PymtToDt', 'LoanBlnc', 'IncurredDt',
                      'DueDt', 'IntRt', 'flgSecured', 'Guar1FullName', 'Guar1Addr1', 'Guar1Addr2', 'Guar1City',
                      'Guar1State', 'Guar1Zip', 'Guar1Emp', 'Guar1Occ', 'Guar1Blnc', 'Guar2FullName', 'Guar2Addr1',
                      'Guar2Addr2', 'Guar2City', 'Guar2State', 'Guar2Zip', 'Guar2Emp', 'Guar2Occ', 'Guar2Blnc',
                      'Guar3FullName', 'Guar3Addr1', 'Guar3Addr2', 'Guar3City', 'Guar3State', 'Guar3Zip', 'Guar3Emp',
                      'Guar3Occ', 'Guar3Blnc', 'AmendCd']]]],
            ['SC1', [[['6.1', '6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                      ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'Lender', 'LenderAddr1', 'LenderAddr2',
                       'LenderCity', 'LenderState', 'LenderZip', 'LoanAmt', 'IntRt', 'IncurredDt', 'DueDt',
                       'flgLoanRestructured', 'OrigLoanDt', 'CrdtAmtThisDraw', 'TotBlnc', 'flgOthersLiable',
                       'flgCollateral', 'CollateralDesc', 'CollateralVal', 'flgPerfectedInt', 'flgFutIncPledged',
                       'FutIncDesc', 'FutIncEstVal', 'DepAcctEstDt', 'AcctLocName', 'AcctLocAddr1', 'AcctLocAddr2',
                       'AcctLocCity', 'AcctLocState', 'AcctLocZip', 'DepAcctAuthDt', 'LoanBasisDesc', 'TrsLName',
                       'TrsFName', 'TrsMName', 'TrsPfx', 'TrsSfx', 'TrsSignDt', 'LendRepLName', 'LendRepFName',
                       'LendRepMName', 'LendRepPfx', 'LendRepSfx', 'LendRepTitle', 'LendRepSignDt']],
                     [['5.0', '5.1', '5.2', '5.3'],
                      ['LineNbr', 'CommID', 'BkRefTransID', 'EntTp', 'Lender', 'LenderAddr1', 'LenderAddr2',
                       'LenderCity', 'LenderState', 'LenderZip', 'LoanAmt', 'IntRt', 'IncurredDt', 'DueDt',
                       'flgLoanRestructured', 'OrigLoanDt', 'CrdtAmtThisDraw', 'TotBlnc', 'flgOthersLiable',
                       'flgCollateral', 'CollateralDesc', 'CollateralVal', 'flgPerfectedInt', 'flgFutIncPledged',
                       'FutIncDesc', 'FutIncEstVal', 'DepAcctEstDt', 'AcctLocName', 'AcctLocAddr1', 'AcctLocAddr2',
                       'AcctLocCity', 'AcctLocState', 'AcctLocZip', 'DepAcctAuthDt', 'LoanBasisDesc', 'TrsFullName',
                       'TrsSignDt', 'LendRepFullName', 'LendRepTitle', 'LendRepSignDt', 'AmendCd']],
                     [['3'], ['LineNbr', 'CommID', 'BkRefTransID', 'EntTp', 'Lender', 'LenderAddr1', 'LenderAddr2',
                              'LenderCity', 'LenderState', 'LenderZip', 'LoanAmt', 'IntRt', 'IncurredDt', 'DueDt',
                              'flgLoanRestructured', 'OrigLoanDt', 'CrdtAmtThisDraw', 'TotBlnc', 'flgOthersLiable',
                              'flgCollateral', 'CollateralDesc', 'CollateralVal', 'flgPerfectedInt', 'flgFutIncPledged',
                              'FutIncDesc', 'FutIncEstVal', 'DepAcctEstDt', 'AcctLocName', 'AcctLocAddr1',
                              'AcctLocAddr2', 'AcctLocCity', 'AcctLocState', 'AcctLocZip', 'DepAcctAuthDt',
                              'LoanBasisDesc', 'TrsFullName', 'TrsSignDt', 'LendRepFullName', 'LendRepTitle',
                              'LendRepSignDt']],
                     [['2'], ['LineNbr', 'CommID', 'BkRefTransID', 'EntTp', 'Lender', 'LenderAddr1', 'LenderAddr2',
                              'LenderCity', 'LenderState', 'LenderZip', 'LoanAmt', 'IntRt', 'IncurredDt', 'DueDt',
                              'flgLoanRestructured', 'OrigLoanDt', 'CrdtAmtThisDraw', 'TotBlnc', 'flgOthersLiable',
                              'flgCollateral', 'CollateralDesc', 'CollateralVal', 'flgPerfectedInt', 'flgFutIncPledged',
                              'FutIncDesc', 'FutIncEstVal', 'DepAcctEstDt', 'AcctLocName', 'AcctLocAddr1',
                              'AcctLocAddr2', 'AcctLocCity', 'AcctLocState', 'AcctLocZip', 'DepAcctAuthDt',
                              'LoanBasisDesc', 'TrsFullName', 'TrsSignDt', 'LendRepFullName', 'LendRepTitle']],
                     [['1'], ['LineNbr', 'CommID', 'TransID', 'Lender', 'LenderAddr1', 'LenderAddr2', 'LenderCity',
                              'LenderState', 'LenderZip', 'LoanAmt', 'IntRt', 'IncurredDt', 'DueDt',
                              'flgLoanRestructured', 'OrigLoanDt', 'CrdtAmtThisDraw', 'TotBlnc', 'flgOthersLiable',
                              'flgCollateral', 'CollateralDesc', 'CollateralVal', 'flgPerfectedInt', 'flgFutIncPledged',
                              'FutIncDesc', 'FutIncEstVal', 'DepAcctEstDt', 'AcctLocName', 'AcctLocAddr1',
                              'AcctLocAddr2', 'AcctLocCity', 'AcctLocState', 'AcctLocZip', 'DepAcctAuthDt',
                              'LoanBasisDesc', 'TrsFullName', 'TrsSignDt', 'LendRepFullName', 'LendRepTitle',
                              'LendRepSignDt', 'AmendCd']]]],
            ['SC2', [[['6.1', '6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                      ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'GuarLName', 'GuarFName', 'GuarMName', 'GuarPfx',
                       'GuarSfx', 'GuarAddr1', 'GuarAddr2', 'GuarCity', 'GuarState', 'GuarZip', 'GuarEmp', 'GuarOcc',
                       'GuarAmt']],
                     [['5.0', '5.1', '5.2', '5.3'],
                      ['LineNbr', 'CommID', 'BkRefTransID', 'GuarFullName', 'GuarAddr1', 'GuarAddr2', 'GuarCity',
                       'GuarState', 'GuarZip', 'GuarEmp', 'GuarOcc', 'GuarAmt', 'AmendCd']],
                     [['2', '3'],
                      ['LineNbr', 'CommID', 'BkRefTransID', 'GuarFullName', 'GuarAddr1', 'GuarAddr2', 'GuarCity',
                       'GuarState', 'GuarZip', 'GuarEmp', 'GuarOcc', 'GuarAmt']]]],
            ['SD', [[['6.1', '6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'EntTp', 'CreditorOrgName', 'CreditorLName', 'CreditorFName',
                      'CreditorMName', 'CreditorPfx', 'CreditorSfx', 'CreditorAddr1', 'CreditorAddr2', 'CreditorCity',
                      'CreditorState', 'CreditorZip', 'DebtPurp', 'BegBlnc_P', 'IncurAmt_P', 'PymtAmt_P',
                      'BalClose_P']],
                    [['3', '5.0', '5.1', '5.2', '5.3'],
                     ['LineNbr', 'CommID', 'EntTp', 'CreditorOrgName', 'CreditorAddr1', 'CreditorAddr2', 'CreditorCity',
                      'CreditorState', 'CreditorZip', 'DebtPurp', 'BegBlnc_P', 'IncurAmt_P', 'PymtAmt_P', 'BalClose_P',
                      'CreditorCommID', 'CreditorCandID', 'CreditorCandFullName', 'CreditorCandOfc',
                      'CreditorCandState', 'CreditorCandDist', 'ConduitName', 'ConduitAddr1', 'ConduitAddr2',
                      'ConduitCity', 'ConduitState', 'ConduitZip', 'AmendCd', 'TransID']],
                    [['2'],
                     ['LineNbr', 'CommID', 'EntTp', 'CreditorOrgName', 'CreditorAddr1', 'CreditorAddr2', 'CreditorCity',
                      'CreditorState', 'CreditorZip', 'DebtPurp', 'BegBlnc_P', 'IncurAmt_P', 'PymtAmt_P', 'BalClose_P',
                      'CreditorCommID', 'CreditorCandID', 'CreditorCandFullName', 'CreditorCandOfc',
                      'CreditorCandState', 'CreditorCandDist', 'ConduitName', 'ConduitAddr1', 'ConduitAddr2',
                      'ConduitCity', 'ConduitState', 'ConduitZip', 'AmendCd', 'TransID', 'BkRefTransID',
                      'BkRefSchdNm']],
                    [['1'], ['LineNbr', 'CommID', 'CreditorOrgName', 'CreditorAddr1', 'CreditorAddr2', 'CreditorCity',
                             'CreditorState', 'CreditorZip', 'DebtPurp', 'BegBlnc_P', 'IncurAmt_P', 'PymtAmt_P',
                             'BalClose_P']]]],
            ['SE', [[['8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm',
                      'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2',
                      'PayeeCity', 'PayeeStAbbr', 'PayeeZip', 'ElecCd', 'ElecDesc', 'DissmntnDt', 'ExpAmt', 'ExpDt',
                      'ExpAgg', 'ExpPurpDesc', 'ExpCatCd', 'PayeeCommID', 'SupOppCd', 'SupOppCandID', 'SupOppCandLName',
                      'SupOppCandFName', 'SupOppCandMName', 'SupOppCandPfx', 'SupOppCandSfx', 'SupOppCandOfc',
                      'SupOppCandDist', 'SupOppCandStAbbr', 'CompLName', 'CompFName', 'CompMName', 'CompPfx', 'CompSfx',
                      'SignDt', 'MemoCd', 'MemoTxt']],
                    [['8.0'], ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm',
                               'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1',
                               'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr', 'PayeeZip', 'ElecCd', 'ElecDesc', 'ExpDt',
                               'ExpAmt', 'ExpAgg', 'ExpPurpDesc', 'ExpCatCd', 'PayeeCommID', 'SupOppCd', 'SupOppCandID',
                               'SupOppCandLName', 'SupOppCandFName', 'SupOppCandMName', 'SupOppCandPfx',
                               'SupOppCandSfx', 'SupOppCandOfc', 'SupOppCandStAbbr', 'SupOppCandDist', 'CompLName',
                               'CompFName', 'CompMName', 'CompPfx', 'CompSfx', 'SignDt', 'MemoCd', 'MemoTxt']],
                    [['6.1', '6.2', '6.3', '6.4', '7.0'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm',
                      'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2',
                      'PayeeCity', 'PayeeStAbbr', 'PayeeZip', 'ElecCd', 'ElecDesc', 'ExpDt', 'ExpAmt', 'ExpAgg',
                      'ExpPurpCd', 'ExpPurpDesc', 'ExpCatCd', 'PayeeCommID', 'SupOppCd', 'SupOppCandID',
                      'SupOppCandLName', 'SupOppCandFName', 'SupOppCandMName', 'SupOppCandPfx', 'SupOppCandSfx',
                      'SupOppCandOfc', 'SupOppCandStAbbr', 'SupOppCandDist', 'CompLName', 'CompFName', 'CompMName',
                      'CompPfx', 'CompSfx', 'SignDt', 'MemoCd', 'MemoTxt']],
                    [['3', '5.0', '5.1', '5.2', '5.3'],
                     ['LineNbr', 'CommID', 'EntTp', 'PayeeFullNm', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity',
                      'PayeeStAbbr', 'PayeeZip', 'ExpPurpDesc', 'ExpDt', 'ExpAmt', 'SupOppCd', 'SupOppCandID',
                      'SupOppCandFullName', 'SupOppCandOfc', 'SupOppCandStAbbr', 'SupOppCandDist', 'SupOppCommID',
                      'Unused1', 'Unused2', 'Unused3', 'Unused4', 'Unused5', 'ConduitNm', 'ConduitAddr1',
                      'ConduitAddr2', 'ConduitCity', 'ConduitStAbbr', 'ConduitZip', 'CompFullName', 'SignDt',
                      'NotaryDt', 'NotaryExpDt', 'NotaryFullNm', 'AmendCd', 'TransID', 'MemoCd', 'MemoTxt',
                      'BkRefTransID', 'BkRefSchdNm', 'ElecCd', 'ElecDesc', 'ExpCatCd', 'TransCd', 'ExpAgg']],
                    [['2'], ['LineNbr', 'CommID', 'EntTp', 'PayeeFullNm', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity',
                             'PayeeStAbbr', 'PayeeZip', 'ExpPurpDesc', 'ExpDt', 'ExpAmt', 'SupOppCd', 'SupOppCandID',
                             'SupOppCandFullName', 'SupOppCandOfc', 'SupOppCandStAbbr', 'SupOppCandDist',
                             'SupOppCommID', 'OthCandID', 'OthCandFullNm', 'OthCandOfc', 'OthCandStAbbr', 'OthCandDist',
                             'ConduitNm', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitStAbbr', 'ConduitZip',
                             'CompFullName', 'SignDt', 'NotaryDt', 'NotaryExpDt', 'NotaryFullNm', 'AmendCd', 'TransID',
                             'BkRefTransID', 'MemoTxt']],
                    [['1'], ['LineNbr', 'CommID', 'PayeeFullNm', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr',
                             'PayeeZip', 'ExpPurpDesc', 'ExpDt', 'ExpAmt', 'SupOppCandID', 'SupOppCandFullName',
                             'SupOppCandOfc', 'SupOppCandStAbbr', 'SupOppCandDist', 'SupOppCd', 'CompFullName',
                             'SignDt', 'NotaryDt', 'NotaryExpDt', 'NotaryFullNm', 'AmendCd']]]],
            ['SF', [[['8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'flgDesigCoordExp', 'DesigCommID',
                      'DesigCommNm', 'SubordCommID', 'SubordCommNm', 'SubordAddr1', 'SubordAddr2', 'SubordCity',
                      'SubordStAbbr', 'SubordZip', 'EntTp', 'PayeeOrgNm', 'PayeeLName', 'PayeeFName', 'PayeeMName',
                      'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr', 'PayeeZip',
                      'ExpDt', 'ExpAmt', 'ExpAgg', 'ExpPurpDesc', 'ExpCatCd', 'PayeeCommID', 'PayeeCandID',
                      'PayeeCandLName', 'PayeeCandFName', 'PayeeCandMName', 'PayeeCandPfx', 'PayeeCandSfx',
                      'PayeeCandOfc', 'PayeeCandStAbbr', 'PayeeCandDist', 'MemoCd', 'MemoTxt']],
                    [['6.4', '7.0'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'flgDesigCoordExp', 'DesigCommID',
                      'DesigCommNm', 'SubordCommID', 'SubordCommNm', 'SubordAddr1', 'SubordAddr2', 'SubordCity',
                      'SubordStAbbr', 'SubordZip', 'EntTp', 'PayeeOrgNm', 'PayeeLName', 'PayeeFName', 'PayeeMName',
                      'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr', 'PayeeZip',
                      'ExpDt', 'ExpAmt', 'ExpAgg', 'ExpPurpCd', 'ExpPurpDesc', 'ExpCatCd', 'PayeeCommID', 'PayeeCandID',
                      'PayeeCandLName', 'PayeeCandFName', 'PayeeCandMName', 'PayeeCandPfx', 'PayeeCandSfx',
                      'PayeeCandOfc', 'PayeeCandStAbbr', 'PayeeCandDist', 'MemoCd', 'MemoTxt']],
                    [['6.1', '6.2', '6.3'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'flgDesigCoordExp', 'DesigCommID',
                      'DesigCommNm', 'SubordCommID', 'SubordCommNm', 'SubordAddr1', 'SubordAddr2', 'SubordCity',
                      'SubordStAbbr', 'SubordZip', 'EntTp', 'PayeeOrgNm', 'PayeeLName', 'PayeeFName', 'PayeeMName',
                      'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr', 'PayeeZip',
                      'ExpDt', 'ExpAmt', 'ExpAgg', 'ExpPurpCd', 'ExpPurpDesc', 'ExpCatCd', 'IncLimit', 'PayeeCommID',
                      'PayeeCandID', 'PayeeCandLName', 'PayeeCandFName', 'PayeeCandMName', 'PayeeCandPfx',
                      'PayeeCandSfx', 'PayeeCandOfc', 'PayeeCandStAbbr', 'PayeeCandDist', 'MemoCd', 'MemoTxt']],
                    [['5.0', '5.1', '5.2', '5.3'],
                     ['LineNbr', 'CommID', 'flgDesigCoordExp', 'DesigCommID', 'DesigCommNm', 'SubordCommID',
                      'SubordCommNm', 'SubordAddr1', 'SubordAddr2', 'SubordCity', 'SubordStAbbr', 'SubordZip', 'EntTp',
                      'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr', 'PayeeZip', 'ExpAgg',
                      'ExpPurpDesc', 'ExpDt', 'ExpAmt', 'PayeeCommID', 'PayeeCandID', 'PayeeCandFullName',
                      'PayeeCandOfc', 'PayeeCandStAbbr', 'PayeeCandDist', 'ConduitNm', 'ConduitAddr1', 'ConduitAddr2',
                      'ConduitCity', 'ConduitStAbbr', 'ConduitZip', 'AmendCd', 'TransID', 'MemoCd', 'MemoTxt',
                      'BkRefTransID', 'BkRefSchdNm', 'UnlmtdSpndg', 'ExpCatCd', 'ExpPurpCd']],
                    [['3'], ['LineNbr', 'CommID', 'flgDesigCoordExp', 'DesigCommID', 'DesigCommNm', 'SubordCommID',
                             'SubordCommNm', 'SubordAddr1', 'SubordAddr2', 'SubordCity', 'SubordStAbbr', 'SubordZip',
                             'EntTp', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr',
                             'PayeeZip', 'ExpAgg', 'ExpPurpDesc', 'ExpDt', 'ExpAmt', 'PayeeCommID', 'PayeeCandID',
                             'PayeeCandFullName', 'PayeeCandOfc', 'PayeeCandStAbbr', 'PayeeCandDist', 'ConduitNm',
                             'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitStAbbr', 'ConduitZip', 'AmendCd',
                             'TransID', 'MemoCd', 'MemoTxt', 'BkRefTransID', 'BkRefSchdNm']],
                    [['2'], ['LineNbr', 'CommID', 'flgDesigCoordExp', 'DesigCommID', 'DesigCommNm', 'SubordCommID',
                             'SubordCommNm', 'SubordAddr1', 'SubordAddr2', 'SubordCity', 'SubordStAbbr', 'SubordZip',
                             'EntTp', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr',
                             'PayeeZip', 'ExpAgg', 'ExpPurpDesc', 'ExpDt', 'ExpAmt', 'PayeeCommID', 'PayeeCandID',
                             'PayeeCandFullName', 'PayeeCandOfc', 'PayeeCandStAbbr', 'PayeeCandDist', 'ConduitNm',
                             'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitStAbbr', 'ConduitZip', 'AmendCd',
                             'TransID', 'BkRefTransID', 'BkRefSchdNm']],
                    [['1'], ['LineNbr', 'CommID', 'flgDesigCoordExp', 'DesigCommID', 'SubordCommNm', 'SubordAddr1',
                             'SubordAddr2', 'SubordCity', 'SubordStAbbr', 'SubordZip', 'PayeeFullName', 'PayeeAddr1',
                             'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr', 'PayeeZip', 'PayeeCandID', 'PayeeCandFullName',
                             'PayeeCandOfc', 'PayeeCandStAbbr', 'PayeeCandDist', 'ExpAgg', 'ExpPurpDesc', 'ExpDt',
                             'ExpAmt', 'AmendCd']]]],
            ['H1', [[['6.1', '6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'flgStLocFxPctPresOnly', 'flgStLocFxPctPresAndSen',
                      'flgStLocFxPctSenOnly', 'flgStLocFxPctNonPresNonSen', 'flgFlatMin50PctFed', 'FedPct', 'NonFedPct',
                      'flgAdmRatio', 'flgGenericVoterDrvRatio', 'flgPubCommunRefPrtyRatio']],
                    [['5.2', '5.3'],
                     ['LineNbr', 'CommID', 'Unused1', 'Unused2', 'Unused3', 'Unused4', 'Unused5', 'Unused6', 'Unused7',
                      'Unused8', 'Unused9', 'Unused10', 'Unused11', 'Unused12', 'Unused13', 'Unused14', 'Unused15',
                      'Unused16', 'Unused17', 'Unused18', 'Unused19', 'Unused20', 'Unused21', 'Unused22', 'Unused23',
                      'Unused24', 'Unused25', 'InternalUse', 'TransID', 'flgStLocFxPctPresOnly',
                      'flgStLocFxPctPresAndSen', 'flgStLocFxPctSenOnly', 'flgStLocFxPctNonPresNonSen',
                      'flgFlatMin50PctFed', 'FedPct', 'NonFedPct', 'flgAdmRatio', 'flgGenericVoterDrvRatio',
                      'flgPubCommunRefPrtyRatio']],
                    [['5.0', '5.1'],
                     ['LineNbr', 'CommID', 'NatPtyCommsPct', 'HseSenPtyCommsPct', 'HseSenPtyCmtesEstFedCandSup',
                      'HseSenPtyCmtesEstNonFedCandSup', 'HseSenPtyCmtesActFedCandSup', 'HseSenPtyCmtesActNonFedCandSup',
                      'HseSenPtyCmtesActFedPct', 'EstDirCandSupFedPct', 'EstDirCandSupNonFedPct', 'ActDirCandSupFedAmt',
                      'ActDirCandSupNonFedAmt', 'ActDirCandSupFedPct', 'BallotCompPres', 'BallotCompSen',
                      'BallotCompHse', 'FedSub', 'BallotCompGov', 'OthStatewide', 'StSen', 'StRep', 'LocCands',
                      'ExtraNonFed', 'Subtotal', 'TotPts', 'FedAllocPct', 'AmendCd', 'TransID', 'flgStLocFxPctPresOnly',
                      'flgStLocFxPctPresAndSen', 'flgStLocFxPctSenOnly', 'flgStLocFxPctNonPresNonSen']],
                    [['3'], ['LineNbr', 'CommID', 'NatPtyCommsPct', 'HseSenPtyCommsPct', 'HseSenPtyCmtesEstFedCandSup',
                             'HseSenPtyCmtesEstNonFedCandSup', 'HseSenPtyCmtesActFedCandSup',
                             'HseSenPtyCmtesActNonFedCandSup', 'HseSenPtyCmtesActFedPct',
                             'SepSegFundsAndPctNonConnCmtesEstFedCandSup',
                             'SepSegFundsAndPctNonConnCmtesEstNonFedCandSup', 'SepSegFundsAndNonConnCmtesActFedCandSup',
                             'SepSegFundsAndNonConnCmtesActNonFedCandSup',
                             'SepSegFundsAndPctNonConnCmtesActNonFedCandSup', 'BallotCompPres', 'BallotCompSen',
                             'BallotCompHse', 'FedSub', 'BallotCompGov', 'OthStatewide', 'StSen', 'StRep', 'LocCands',
                             'ExtraNonFed', 'Subtotal', 'TotPts', 'FedAllocPct', 'AmendCd', 'TransID']],
                    [['2'], ['LineNbr', 'CommID', 'NatPtyCommsPct', 'HseSenPtyCommsPct', 'HseSenPtyCmtesEstFedCandSup',
                             'HseSenPtyCmtesEstNonFedCandSup', 'HseSenPtyCmtesActFedCandSup',
                             'HseSenPtyCmtesActNonFedCandSup', 'HseSenPtyCmtesActFedPct',
                             'SepSegFundsAndPctNonConnCmtesEstFedCandSup',
                             'SepSegFundsAndPctNonConnCmtesEstNonFedCandSup', 'SepSegFundsAndNonConnCmtesActFedCandSup',
                             'SepSegFundsAndNonConnCmtesActNonFedCandSup',
                             'SepSegFundsAndPctNonConnCmtesActNonFedCandSup', 'BallotCompPres', 'BallotCompSen',
                             'BallotCompHse', 'FedSub', 'BallotCompGov', 'OthStatewide', 'StSen', 'StRep', 'LocCands',
                             'ExtraNonFed', 'Subtotal', 'TotPts', 'FedAllocPct', 'AmendCd', 'TransID', 'BkRefTransID',
                             'BkRefSchdNm']],
                    [['1'], ['LineNbr', 'CommID', 'NatPtyCommsPct', 'HseSenPtyCommsPct', 'HseSenPtyCmtesEstFedCandSup',
                             'HseSenPtyCmtesEstNonFedCandSup', 'HseSenPtyCmtesActFedCandSup',
                             'HseSenPtyCmtesActNonFedCandSup', 'HseSenPtyCmtesActFedPct',
                             'SepSegFundsAndPctNonConnCmtesEstFedCandSup',
                             'SepSegFundsAndPctNonConnCmtesEstNonFedCandSup', 'SepSegFundsAndNonConnCmtesActFedCandSup',
                             'SepSegFundsAndNonConnCmtesActNonFedCandSup',
                             'SepSegFundsAndPctNonConnCmtesActNonFedCandSup', 'BallotCompPres', 'BallotCompSen',
                             'BallotCompHse', 'FedSub', 'BallotCompGov', 'OthStatewide', 'StSen', 'StRep', 'LocCands',
                             'ExtraNonFed', 'Subtotal', 'TotPts', 'FedAllocPct', 'AmendCd']]]],
            ['H2', [[['6.1', '6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'EventNm', 'flgDirFndrsg', 'flgDirCandSup', 'RatioCd', 'FedPct',
                      'NonFedPct']],
                    [['5.2', '5.3'],
                     ['LineNbr', 'CommID', 'EventNm', 'flgDirFndrsg', 'Unused', 'flgDirCandSup', 'RatioCd', 'FedPct',
                      'NonFedPct', 'InternalUse', 'TransID']],
                    [['3', '5.0', '5.1'],
                     ['LineNbr', 'CommID', 'EventNm', 'flgDirFndrsg', 'flgExemptAct', 'flgDirCandSup', 'RatioCd',
                      'FedPct', 'NonFedPct', 'AmendCd', 'TransID']],
                    [['2'], ['LineNbr', 'CommID', 'EventNm', 'flgDirFndrsg', 'flgExemptAct', 'flgDirCandSup', 'RatioCd',
                             'FedPct', 'NonFedPct', 'AmendCd', 'TransID', 'BkRefTransID', 'BkRefSchdNm']],
                    [['1'],
                     ['LineNbr', 'CommID', 'EventNm', 'EventNbr', 'flgDirFndrsg', 'flgExemptAct', 'flgDirCandSup',
                      'RatioCd', 'FedPct', 'NonFedPct', 'AmendCd']]]],
            ['H3', [[['6.1', '6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'AcctNm', 'EventTp', 'EventNm', 'RcptDt',
                      'TotAmtTrans', 'TransAmt']],
                    [['5.2', '5.3'],
                     ['LineNbr', 'CommID', 'BkRefTransID', 'AcctNm', 'EventNm', 'EventTp', 'RcptDt', 'TransAmt',
                      'TotAmtTrans', 'InternalUse', 'TransID']],
                    [['3', '5.0', '5.1'],
                     ['LineNbr', 'CommID', 'BkRefTransID', 'AcctNm', 'EventNm', 'EventTp', 'RcptDt', 'TransAmt',
                      'TotAmtTrans', 'AmendCd', 'TransID']]
                    #    ,
                    #    [['2'], ['LineNbr', 'CommID', 'AcctNm', 'RcptDt', 'TotAmtTrans', 'AdmVtrDrv', 'TotDirFundrsgAmt', 'TotExemptActDirCandSup', 'AmendCd', 'TransID', 'BkRefTransID', 'BkRefSchdNm']],
                    #    [['1'], ['LineNbr', 'CommID', 'AcctNm', 'RcptDt', 'TotAmtTrans', 'AdmVtrDrv', 'EventNm', 'EventNbr', 'TransAmt', 'EventNm2', 'EventNbr2', 'TransAmt2', 'EventNm3', 'EventNbr3', 'TransAmt3', 'EventNm4', 'EventNbr4', 'TransAmt4', 'TotDirFndrsgAmt', 'EventNm5', 'EventNbr5', 'TransAmt5', 'EventNm6', 'EventNbr6', 'TransAmt6', 'EventNm7', 'EventNbr7', 'TransAmt7', 'EventNm8', 'EventNbr8', 'TransAmt8', 'TotExemptActDirCandSup', 'AmendCd']]
                    ]],
            ['H4', [[['8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm',
                      'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2',
                      'PayeeCity', 'PayeeStAbbr', 'PayeeZip', 'EventNm', 'ExpDt', 'ExpAmt', 'FedAmt', 'NonFedAmt',
                      'EventAgg', 'ExpPurpDesc', 'ExpCatCd', 'flgAdminActivity', 'flgDirectFndrsg', 'flgExempt',
                      'flgGenVtrDrv', 'flgDirCandSup', 'flgPubCommun', 'MemoCd', 'MemoTxt']],
                    [['6.1', '6.2', '6.3', '6.4', '7.0'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm',
                      'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2',
                      'PayeeCity', 'PayeeStAbbr', 'PayeeZip', 'EventNm', 'ExpDt', 'ExpAmt', 'FedAmt', 'NonFedAmt',
                      'EventAgg', 'ExpPurpCd', 'ExpPurpDesc', 'ExpCatCd', 'flgAdminActivity', 'flgDirectFndrsg',
                      'flgExempt', 'flgGenVtrDrv', 'flgDirCandSup', 'flgPubCommun', 'MemoCd', 'MemoTxt']],
                    [['5.2', '5.3'],
                     ['LineNbr', 'CommID', 'EntTp', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity',
                      'PayeeStAbbr', 'PayeeZip', 'ExpPurpDesc', 'ExpDt', 'ExpAmt', 'FedAmt', 'NonFedAmt', 'Unused',
                      'flgDirectFndrsg', 'flgExempt', 'flgDirCandSup', 'ExpAgg', 'ExpPurpDesc', 'CandCommID', 'CandID',
                      'CandFullName', 'CandOfc', 'CandStAbbr', 'CandDist', 'ConduitNm', 'ConduitAddr1', 'ConduitAddr2',
                      'ConduitCity', 'ConduitStAbbr', 'ConduitZip', 'InternalUse', 'TransID', 'MemoCd', 'MemoTxt',
                      'BkRefTransID', 'BkRefSchdNm', 'flgAdminActivity', 'flgGenVtrDrv', 'ExpCatCd', 'ExpPurpCd',
                      'flgPubCommun']],
                    [['5.0', '5.1'],
                     ['LineNbr', 'CommID', 'EntTp', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity',
                      'PayeeStAbbr', 'PayeeZip', 'ExpPurpDesc', 'ExpDt', 'ExpAmt', 'FedAmt', 'NonFedAmt',
                      'flgAdminVtrDrv', 'flgDirectFndrsg', 'flgExempt', 'flgDirCandSup', 'ExpAgg', 'ExpPurpDesc',
                      'CandCommID', 'CandID', 'CandFullName', 'CandOfc', 'CandStAbbr', 'CandDist', 'ConduitNm',
                      'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitStAbbr', 'ConduitZip', 'AmendCd',
                      'TransID', 'MemoCd', 'MemoTxt', 'BkRefTransID', 'BkRefSchdNm', 'flgAdminActivity', 'flgGenVtrDrv',
                      'ExpCatCd', 'ExpPurpCd']],
                    [['3'], ['LineNbr', 'CommID', 'EntTp', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity',
                             'PayeeStAbbr', 'PayeeZip', 'EventNm', 'ExpDt', 'ExpAmt', 'FedAmt', 'NonFedAmt',
                             'flgAdminVtrDrv', 'flgDirectFndrsg', 'flgExempt', 'flgDirCandSup', 'ExpAgg', 'ExpPurpDesc',
                             'CandCommID', 'CandID', 'CandFullName', 'CandOfc', 'CandStAbbr', 'CandDist', 'ConduitNm',
                             'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitStAbbr', 'ConduitZip', 'AmendCd',
                             'TransID', 'MemoCd', 'MemoTxt', 'BkRefTransID', 'BkRefSchdNm']],
                    [['2'], ['LineNbr', 'CommID', 'EntTp', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity',
                             'PayeeStAbbr', 'PayeeZip', 'EventNm', 'ExpDt', 'ExpAmt', 'FedAmt', 'NonFedAmt',
                             'flgAdminVtrDrv', 'flgDirectFndrsg', 'flgExempt', 'flgDirCandSup', 'ExpAgg', 'ExpPurpDesc',
                             'CandCommID', 'CandID', 'CandFullName', 'CandOfc', 'CandStAbbr', 'CandDist', 'ConduitNm',
                             'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitStAbbr', 'ConduitZip', 'AmendCd',
                             'TransID', 'BkRefTransID', 'BkRefSchdNm']],
                    [['1'],
                     ['LineNbr', 'CommID', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr',
                      'PayeeZip', 'EventNm', 'EventNbr', 'ExpDt', 'ExpAmt', 'FedAmt', 'NonFedAmt', 'flgAdminVtrDrv',
                      'flgDirectFndrsg', 'flgExempt', 'flgDirCandSup', 'ExpAgg', 'ExpPurpDesc', 'AmendCd']]]],
            ['H5', [[['6.1', '6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'AcctNm', 'RcptDt', 'TotAmt', 'VotRegnAmt', 'VotIDAmt', 'GOTVAmt',
                      'GenCampAmt']],
                    [['5.0', '5.1', '5.2', '5.3'],
                     ['LineNbr', 'CommID', 'AcctNm', 'RcptDt', 'VotRegnAmt', 'VotIDAmt', 'GOTVAmt', 'GenCampAmt',
                      'TotAmt', 'AmendCd', 'TransID']]]],
            ['H6', [[['8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm',
                      'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2',
                      'PayeeCity', 'PayeeStAbbr', 'PayeeZip', 'EventNm', 'ExpDt', 'TotExpAmt', 'FedAmt', 'LevinAmt',
                      'ExpAgg', 'ExpPurpDesc', 'ExpCatCd', 'flgActVotRegn', 'flgActGOTV', 'flgActVotID',
                      'flgActGenCamp', 'MemoCd', 'MemoTxt']],
                    [['6.1', '6.2', '6.3', '6.4', '7.0'],
                     ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm',
                      'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2',
                      'PayeeCity', 'PayeeStAbbr', 'PayeeZip', 'EventNm', 'ExpDt', 'TotExpAmt', 'FedAmt', 'LevinAmt',
                      'ExpAgg', 'ExpPurpCd', 'ExpPurpDesc', 'ExpCatCd', 'flgActVotRegn', 'flgActGOTV', 'flgActVotID',
                      'flgActGenCamp', 'MemoCd', 'MemoTxt']],
                    [['5.0', '5.1', '5.2', '5.3'],
                     ['LineNbr', 'CommID', 'EntTp', 'PayeeFullName', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity',
                      'PayeeStAbbr', 'PayeeZip', 'ExpCatCd', 'ExpCd', 'ExpDesc', 'ExpDt', 'TotExpAmt', 'FedAmt',
                      'LevinAmt', 'flgActVotRegn', 'flgActVotID', 'flgActGOTV', 'flgActGenCamp', 'ExpAgg', 'AddlDesc',
                      'CandCommID', 'CandID', 'CandName', 'CandOfc', 'CandStAbbr', 'CandDist', 'ConduitCommID',
                      'ConduitName', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitStAbbr', 'ConduitZip',
                      'MemoCd', 'MemoTxt', 'AmendCd', 'TransID', 'BkRefTransID', 'BkRefSchdNm']]]],
            ['SI', [[['6.1', '6.2', '6.3', '6.4', '7.0'],
                     ['LineNbr', 'CommID', 'TransID', 'RecIDNbr', 'AcctNm', 'BankAcctID', 'CovgFmDt', 'CovgToDt',
                      'TotRcpts', 'TransToFed', 'TransToStAndLoc', 'DirStLocCandSup', 'OthDisb', 'TotDisb', 'BegCOH',
                      'Rcpts', 'Subtotal', 'Disb', 'EndCOH', 'TotRcpts2', 'TransToFed2', 'TransToStAndLoc2',
                      'DirStLocCandSup2', 'OthDisb2', 'TotDisb2', 'BegCOH2', 'Rcpts2', 'Subtotal2', 'Disb2',
                      'EndCOH2']],
                    [['5.0', '5.1', '5.2', '5.3'],
                     ['LineNbr', 'CommID', 'BankAcctID', 'AcctNm', 'CovgFmDt', 'CovgToDt', 'TotRcpts', 'TransToFed',
                      'TransToStAndLoc', 'DirStLocCandSup', 'OthDisb', 'TotDisb', 'BegCOH', 'Rcpts', 'Subtotal', 'Disb',
                      'EndCOH', 'TotRcpts2', 'TransToFed2', 'TransToStAndLoc2', 'DirStLocCandSup2', 'OthDisb2',
                      'TotDisb2', 'BegCOH2', 'Rcpts2', 'Subtotal2', 'Disb2', 'EndCOH2', 'AmendCd', 'TransID', 'SysCd']],
                    [['3'],
                     ['LineNbr', 'CommID', 'BankAcctID', 'AcctNm', 'CovgFmDt', 'CovgToDt', 'TotRcpts', 'TransToFed',
                      'TransToStAndLoc', 'DirStLocCandSup', 'OthDisb', 'TotDisb', 'BegCOH', 'Rcpts', 'Subtotal', 'Disb',
                      'EndCOH', 'TotRcpts2', 'TransToFed2', 'TransToStAndLoc2', 'DirStLocCandSup2', 'OthDisb2',
                      'TotDisb2', 'BegCOH2', 'Rcpts2', 'Subtotal2', 'Disb2', 'EndCOH2', 'AmendCd', 'TransID',
                      'AcctNbr']],
                    [['2'],
                     ['LineNbr', 'CommID', 'BankAcctID', 'AcctNm', 'CovgFmDt', 'CovgToDt', 'TotRcpts', 'TransToFed',
                      'TransToStAndLoc', 'DirStLocCandSup', 'OthDisb', 'TotDisb', 'BegCOH', 'Rcpts', 'Subtotal', 'Disb',
                      'EndCOH', 'TotRcpts2', 'TransToFed2', 'TransToStAndLoc2', 'DirStLocCandSup2', 'OthDisb2',
                      'TotDisb2', 'BegCOH2', 'Rcpts2', 'Subtotal2', 'Disb2', 'EndCOH2', 'AmendCd', 'TransID',
                      'BkRefTransID', 'BkRefSchdNm']],
                    [['1'],
                     ['LineNbr', 'CommID', 'BankAcctID', 'AcctNm', 'CovgFmDt', 'CovgToDt', 'TotRcpts', 'TransToFed',
                      'TransToStAndLoc', 'DirStLocCandSup', 'OthDisb', 'TotDisb', 'BegCOH', 'Rcpts', 'Subtotal', 'Disb',
                      'EndCOH', 'TotRcpts2', 'TransToFed2', 'TransToStAndLoc2', 'DirStLocCandSup2', 'OthDisb2',
                      'TotDisb2', 'BegCOH2', 'Rcpts2', 'Subtotal2', 'Disb2', 'EndCOH2', 'AmendCd']]]],
            ['SL', [[['6.1', '6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                     ['LineNbr', 'CommID', 'TransID', 'RecordID', 'AcctNm', 'CovgFmDt', 'CovgToDt', 'IndRcptsItem_P',
                      'IndRcptsUnitem_P', 'IndRcptsTot_P', 'OthRcpts_P', 'TotRcpts_P', 'TransVotReg_P', 'TransVotID_P',
                      'TransGOTV_P', 'TransGenCamp_P', 'TransTot_P', 'OthDisb_P', 'TotDisb_P', 'BegCOH_P', 'Rcpts_P',
                      'Subtotal_P', 'Disb_P', 'EndCOH_P', 'IndRcptsItem_T', 'IndRcptsUnitem_T', 'IndRcptsTot_T',
                      'OthRcpts_T', 'TotRcpts_T', 'TransVotReg_T', 'TransVotID_T', 'TransGOTV_T', 'TransGenCamp_T',
                      'TransTot_T', 'OthDisb_T', 'TotDisb_T', 'BegCOH_T', 'Rcpts_T', 'Subtotal_T', 'Disb_T',
                      'EndCOH_T']],
                    [['5.0', '5.1', '5.2', '5.3'],
                     ['LineNbr', 'CommID', 'AcctNm', 'SysCd', 'CovgFmDt', 'CovgToDt', 'IndRcptsItem_P',
                      'IndRcptsUnitem_P', 'IndRcptsTot_P', 'OthRcpts_P', 'TotRcpts_P', 'TransVotReg_P', 'TransVotID_P',
                      'TransGOTV_P', 'TransGenCamp_P', 'TransTot_P', 'OthDisb_P', 'TotDisb_P', 'BegCOH_P', 'Rcpts_P',
                      'Subtotal_P', 'Disb_P', 'IndRcptsItem_T', 'IndRcptsUnitem_T', 'IndRcptsTot_T', 'OthRcpts_T',
                      'TotRcpts_T', 'TransVotReg_T', 'TransVotID_T', 'TransGOTV_T', 'TransGenCamp_T', 'TransTot_T',
                      'OthDisb_T', 'TotDisb_T', 'BegCOH_T', 'Rcpts_T', 'Subtotal_T', 'Disb_T', 'EndCOH_T', 'AmendCd',
                      'TransID']]]],
            ['TEXT', [[['6.1', '6.2', '6.3', '6.4', '7.0', '8.0', '8.1', '8.2', '8.3'],
                       ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'FullText']],
                      [['5.0', '5.1', '5.2', '5.3'], ['LineNbr', 'ParentTp', 'BkRefTransID', 'FullText', 'AmendCd']],
                      [['3'], ['LineNbr', 'ParentTp', 'BkRefTransID', 'FullText']]]]]

outputhdrs = {
    'F1': ['FormTp', 'CommID', 'flgChgCommNm', 'CommNm', 'flgAddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip',
           'flgChgCommEmail', 'CommEmail', 'flgChgCommUrl', 'CommUrl', 'SubmDt', 'SignFullName', 'SignLName',
           'SignFName', 'SignMName', 'SignPfx', 'SignSfx', 'SignDt', 'CommTp', 'CandID', 'CandFullName', 'CandLName',
           'CandFName', 'CandMName', 'CandPfx', 'CandSfx', 'CandOff', 'CandStAbbr', 'CandDist', 'PtyCd', 'PtyTp',
           'PACTp', 'flgLobRegPAC_ConnOrg_5e', 'flgLobRegPAC_MultCands_5f', 'flgLdspPAC_5f', 'AffCommID', 'AffCommNm',
           'AffCandID', 'AffCandLName', 'AffCandFName', 'AffCandMName', 'AffCandPfx', 'AffCandSfx', 'AffAddr1',
           'AffAddr2', 'AffCity', 'AffStAbbr', 'AffZip', 'AffRelCd', 'CustFullName', 'CustLName', 'CustFName',
           'CustMName', 'CustPfx', 'CustSfx', 'CustAddr1', 'CustAddr2', 'CustCity', 'CustStAbbr', 'CustZip',
           'CustTitle', 'CustPhone', 'TrsFullName', 'TrsLName', 'TrsFName', 'TrsMName', 'TrsPfx', 'TrsSfx', 'TrsAddr1',
           'TrsAddr2', 'TrsCity', 'TrsStAbbr', 'TrsZip', 'TrsTitle', 'TrsPhone', 'AgtFullName', 'AgtLName', 'AgtFName',
           'AgtMName', 'AgtPfx', 'AgtSfx', 'AgtAddr1', 'AgtAddr2', 'AgtCity', 'AgtStAbbr', 'AgtZip', 'AgtTitle',
           'AgtPhone', 'Bank1Nm', 'Bank1Addr1', 'Bank1Addr2', 'Bank1City', 'Bank1StAbbr', 'Bank1Zip', 'Bank2Nm',
           'Bank2Addr1', 'Bank2Addr2', 'Bank2City', 'Bank2StAbbr', 'Bank2Zip'],
    'F1S': ['FormTp', 'CommID', 'JtFndCommNm', 'JtFundCommID', 'AffCommID', 'AffCommNm', 'AffCandID', 'AffLName',
            'AffFName', 'AffMName', 'AffPfx', 'AffSfx', 'AffAddr1', 'AffAddr2', 'AffCity', 'AffStAbbr', 'AffZip',
            'AffRelCd', 'AgtLName', 'AgtFName', 'AgtMName', 'AgtPfx', 'AgtSfx', 'AgtAddr1', 'AgtAddr2', 'AgtCity',
            'AgtStAbbr', 'AgtZip', 'AgtTitle', 'AgtPhone', 'BankNm', 'BankAddr1', 'BankAddr2', 'BankCity', 'BankStAbbr',
            'BankZip'],
    'F3': ['FormTp', 'CommID', 'CommNm', 'AddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'ElecSt', 'ElecDist',
           'RptCd', 'ElecCd', 'ElecDt', 'StateOfElec', 'CovgFmDt', 'CovgToDt', 'TrsFullName', 'TrsLName', 'TrsFName',
           'TrsMName', 'TrsPfx', 'TrsSfx', 'SignDt', 'TotConts_P_6a', 'TotContRfds_P_6b', 'NetConts_P_6c',
           'TotOpExps_P_7a', 'TotOffsetOpExps_P_7b', 'NetOpExps_P_7c', 'CashClose_P_8', 'DebtsTo_P_9', 'DebtsBy_P_10',
           'IndContsItem_P_11a1', 'IndContsUnitem_P_11a2', 'IndContsTot_P_11a3', 'PolPtyCommConts_P_11b',
           'OthPolCommConts_P_11c', 'CandConts_P_11d', 'TotConts_P_11e', 'TranFmOthAuthComms_P_12', 'CandLoans_P_13a',
           'OthLoans_P_13b', 'TotLoans_P_13c', 'OffsetOpExps_P_14', 'OthRcpts_P_15', 'TotRcpts_P_16', 'OpExps_P_17',
           'TranToOthAuthComms_P_18', 'CandLoansRepaid_P_19a', 'OthLoansRepaid_P_19b', 'TotLoansRepaid_P_19c',
           'RefundsInd_P_20a', 'RefundsPolPtyComms_P_20b', 'RefundsOthPolComms_P_20c', 'TotRefunds_P_20d',
           'OthDisb_P_21', 'TotDisb_P_22', 'CashBegin_P_23', 'TotRcpts_P_24', 'Subtotal_P_25', 'TotDisb_P_26',
           'CashClose_P_27', 'TotConts_T_6a', 'TotContRfds_T_6b', 'NetConts_T_6c', 'TotOpExps_T_7a',
           'TotOffsetOpExps_T_7b', 'NetOpExps_T_7c', 'IndContsItem_T_11a1', 'IndContsUnitem_T_11a2',
           'IndContsTot_T_11a3', 'PolPtyCommConts_T_11b', 'OthPolCommConts_T_11c', 'CandConts_T_11d', 'TotConts_T_11e',
           'TranFmOthAuthComms_T_12', 'CandLoans_T_13a', 'OthLoans_T_13b', 'TotLoans_T_13c', 'OffsetOpExps_T_14',
           'OthRcpts_T_15', 'TotRcpts_T_16', 'OpExps_T_17', 'TranToOthAuthComms_T_18', 'CandLoansRepaid_T_19a',
           'OthLoansRepaid_T_19b', 'TotLoansRepaid_T_19c', 'RefundsInd_T_20a', 'RefundsPolPtyComms_T_20b',
           'RefundsOthPolComms_T_20c', 'TotRefunds_T_20d', 'OthDisb_T_21', 'TotDisb_T_22'],
    'F3L': ['FormTp', 'CommID', 'CommNm', 'AddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'ElecSt', 'ElecDist',
            'RptCd', 'ElecDt', 'StateOfElec', 'flgInclSemiAnnPrd', 'CovgFmDt', 'CovgToDt', 'flgInclSemiAnnJanJun',
            'flgInclSemiAnnJulDec', 'TotRptBundContribs', 'SemiAnnBundContribs', 'TrsFullName', 'TrsLName', 'TrsFName',
            'TrsMName', 'TrsPfx', 'TrsSfx', 'SignDt'],
    'F3P': ['FormTp', 'CommID', 'CommNm', 'AddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'PrimElec', 'GenElec',
            'RptCd', 'ElecCd', 'ElecDt', 'ElecSt', 'CovgFmDt', 'CovgToDt', 'TrsFullName', 'TrsLName', 'TrsFName',
            'TrsMName', 'TrsPfx', 'TrsSfx', 'SignDt', 'CashBegin_P_6', 'TotRcpts_P_7', 'Subtotal_P_8', 'TotDisb_P_9',
            'CashClose_P_10', 'DebtsTo_P_11', 'DebtsBy_P_12', 'LmtdExps_P_13', 'NetConts_P_14', 'NetOpExps_P_15',
            'FedFnds_P_16', 'IndContsItem_P_17a1', 'IndContsUnitem_P_17a2', 'IndContsTot_P_17a3',
            'PolPtyCommConts_P_17b', 'OthPolCommConts_P_17c', 'CandConts_P_17d', 'TotConts_P_17e',
            'TranFmPtyComms_P_18', 'CandLoans_P_19a', 'OthLoans_P_19b', 'TotLoans_P_19c', 'OptgOffsets_P_20a',
            'FndrsgOffsets_P_20b', 'LegalAcctgOffsets_P_20c', 'TotOffsets_P_20d', 'OthRcpts_P_21', 'TotRcpts_P_22',
            'OpExps_P_23', 'TranToOthAuthComms_P_24', 'FndrsgDisb_P_25', 'LegalAcctgDisb_P_26', 'CandLoansRepaid_P_27a',
            'OthLoansRepaid_P_27b', 'TotLoansRepaid_P_27c', 'RefundsInd_P_28a', 'RefundsPolPtyComms_P_28b',
            'RefundsOthPolComms_P_28c', 'TotRefunds_P_28d', 'OthDisb_P_29', 'TotDisb_P_30', 'ItmsToBeLiq_P_31',
            'Alabama_P', 'Alaska_P', 'Arizona_P', 'Arkansas_P', 'California_P', 'Colorado_P', 'Connecticut_P',
            'Delaware_P', 'DistCol_P', 'Florida_P', 'Georgia_P', 'Hawaii_P', 'Idaho_P', 'Illinois_P', 'Indiana_P',
            'Iowa_P', 'Kansas_P', 'Kentucky_P', 'Louisiana_P', 'Maine_P', 'Maryland_P', 'Massachusetts_P', 'Michigan_P',
            'Minnesota_P', 'Mississippi_P', 'Missouri_P', 'Montana_P', 'Nebraska_P', 'Nevada_P', 'NewHampshire_P',
            'NewJersey_P', 'NewMexico_P', 'NewYork_P', 'NorthCarolina_P', 'NorthDakota_P', 'Ohio_P', 'Oklahoma_P',
            'Oregon_P', 'Pennsylvania_P', 'RhodeIsland_P', 'SouthCarolina_P', 'SouthDakota_P', 'Tennessee_P', 'Texas_P',
            'Utah_P', 'Vermont_P', 'Virginia_P', 'Washington_P', 'WestVirginia_P', 'Wisconsin_P', 'Wyoming_P',
            'PuertoRico_P', 'Guam_P', 'VirginIslands_P', 'TotAllocs_P', 'FedFnds_T_16', 'IndContsItem_T_17a1',
            'IndContsUnitem_T_17a2', 'IndContsTot_T_17a3', 'PolPtyCommConts_T_17b', 'OthPolCommConts_T_17c',
            'CandConts_T_17d', 'TotConts_T_17e', 'TranFmPtyComms_T_18', 'CandLoans_T_19a', 'OthLoans_T_19b',
            'TotLoans_T_19c', 'OptgOffsets_T_20a', 'FndrsgOffsets_T_20b', 'LegalAcctgOffsets_T_20c', 'TotOffsets_T_20d',
            'OthRcpts_T_21', 'TotRcpts_T_22', 'OpExps_T_23', 'TranToOthAuthComms_T_24', 'FndrsgDisb_T_25',
            'LegalAcctgDisb_T_26', 'CandLoansRepaid_T_27a', 'OthLoansRepaid_T_27b', 'TotLoansRepaid_T_27c',
            'RefundsInd_T_28a', 'RefundsPolPtyComms_T_28b', 'RefundsOthPolComms_T_28c', 'TotRefunds_T_28d',
            'OthDisb_T_29', 'TotDisb_T_30', 'Alabama_T', 'Alaska_T', 'Arizona_T', 'Arkansas_T', 'California_T',
            'Colorado_T', 'Connecticut_T', 'Delaware_T', 'DistCol_T', 'Florida_T', 'Georgia_T', 'Hawaii_T', 'Idaho_T',
            'Illinois_T', 'Indiana_T', 'Iowa_T', 'Kansas_T', 'Kentucky_T', 'Louisiana_T', 'Maine_T', 'Maryland_T',
            'Massachusetts_T', 'Michigan_T', 'Minnesota_T', 'Mississippi_T', 'Missouri_T', 'Montana_T', 'Nebraska_T',
            'Nevada_T', 'NewHampshire_T', 'NewJersey_T', 'NewMexico_T', 'NewYork_T', 'NorthCarolina_T', 'NorthDakota_T',
            'Ohio_T', 'Oklahoma_T', 'Oregon_T', 'Pennsylvania_T', 'RhodeIsland_T', 'SouthCarolina_T', 'SouthDakota_T',
            'Tennessee_T', 'Texas_T', 'Utah_T', 'Vermont_T', 'Virginia_T', 'Washington_T', 'WestVirginia_T',
            'Wisconsin_T', 'Wyoming_T', 'PuertoRico_T', 'Guam_T', 'VirginIslands_T', 'TotAllocs_T'],
    'F3X': ['FormTp', 'CommID', 'CommNm', 'AddrChg', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'RptCd', 'ElecCd',
            'ElecDt', 'ElecSt', 'CovgFmDt', 'CovgToDt', 'flgQualComm', 'TrsFullName', 'TrsLName', 'TrsFName',
            'TrsMName', 'TrsPfx', 'TrsSfx', 'SignDt', 'CashBegin_P_6b', 'TotRcpts_P_6c', 'Subtotal_P_6d', 'TotDisb_P_7',
            'CashClose_P_8', 'DebtsTo_P_9', 'DebtsBy_P_10', 'IndContsItem_P_11a1', 'IndContsUnitem_P_11a2',
            'IndContsTot_P_11a3', 'PolPtyCommConts_P_11b', 'OthPolCommConts_P_11c', 'TotConts_P_11d',
            'TranFmPtyComms_P_12', 'AllLoansRcvd_P_13', 'LoanPymtsRcvd_P_14', 'RefundOffsets_P_15',
            'RefundsFedConts_P_16', 'OthFedRcptsDvds_P_17', 'TranFmNonFedAcctH3_P_18a', 'TranFmNonFedAcctH5_P_18b',
            'TotNonFedTrans_P_18c', 'TotRcpts_P_19', 'TotFedRcpts_P_20', 'OpExpsFedShr_P_21a1',
            'OpExpsNonFedShr_P_21a2', 'OpExpsOthFed_P_21b', 'TotOpExps_P_21c', 'TranToPtyComms_P_22',
            'ContsToFedCandsComms_P_23', 'IndtExps_P_24', 'CoordExpsByPtyComms_P_25', 'LoansRepaid_P_26',
            'LoansMade_P_27', 'RefundsInd_P_28a', 'RefundsPolPtyComms_P_28b', 'RefundsOthPolComms_P_28c',
            'TotContRefunds_P_28d', 'OthDisb_P_29', 'ShrdElecActivityFedShr_P_30a1', 'ShrdElecActivityNonFedShr_P_30a2',
            'NonAllocFedElecActivity_P_30b', 'TotFedElecActivity_P_30c', 'TotDisb_P_31', 'TotFedDisb_P_32',
            'TotConts_P_33', 'TotContRefunds_P_34', 'NetConts_P_35', 'TotFedOpExps_P_36', 'TotOffsetsOpExp_P_37',
            'NetOpExps_P_38', 'CashBegin_T_6a', 'CashBeginYr', 'TotRcpts_T_6c', 'Subtotal_T_6d', 'TotDisb_T_7',
            'CashClose_T_8', 'IndContsItem_T_11a1', 'IndContsUnitem_T_11a2', 'IndContsTot_T_11a3',
            'PolPtyCommConts_T_11b', 'OthPolCommConts_T_11c', 'TotConts_T_11d', 'TranFmPtyComms_T_12',
            'AllLoansRcvd_T_13', 'LoanPymtsRcvd_T_14', 'RefundOffsets_T_15', 'RefundsFedConts_T_16',
            'OthFedRcptsDvds_T_17', 'TranFmNonFedAcctH3_T_18a', 'TranFmNonFedAcctH5_T_18b', 'TotNonFedTrans_T_18c',
            'TotRcpts_T_19', 'TotFedRcpts_T_20', 'OpExpsFedShr_T_21a1', 'OpExpsNonFedShr_T_21a2', 'OpExpsOthFed_T_21b',
            'TotOpExps_T_21c', 'TranToPtyComms_T_22', 'ContsToFedCandsComms_T_23', 'IndtExps_T_24',
            'CoordExpsByPtyComms_T_25', 'LoansRepaid_T_26', 'LoansMade_T_27', 'RefundsInd_T_28a',
            'RefundsPolPtyComms_T_28b', 'RefundsOthPolComms_T_28c', 'TotContRefunds_T_28d', 'OthDisb_T_29',
            'ShrdElecActivityFedShr_T_30a1', 'ShrdElecActivityNonFedShr_T_30a2', 'NonAllocFedElecActivity_T_30b',
            'TotFedElecActivity_T_30c', 'TotDisb_T_31', 'TotFedDisb_T_32', 'TotConts_T_33', 'TotContRefunds_T_34',
            'NetConts_T_35', 'TotFedOpExps_T_36', 'TotOffsetsOpExp_T_37', 'NetOpExps_T_38'],
    'SA': ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'ContOrgNm', 'ContLName',
           'ContFName', 'ContMName', 'ContPfx', 'ContSfx', 'Addr1', 'Addr2', 'City', 'StAbbr', 'Zip', 'ElecCd',
           'ElecDesc', 'ContDt', 'ContAmt', 'ContAgg', 'ContPurpCd', 'ContPurpDesc', 'Emp', 'Occ', 'DonorCommID',
           'DonorCommNm', 'DonorCandID', 'DonorCandLName', 'DonorCandFName', 'DonorCandMName', 'DonorCandPfx',
           'DonorCandSfx', 'DonorCandOfc', 'DonorCandSt', 'DonorCandDist', 'ConduitNm', 'ConduitAddr1', 'ConduitAddr2',
           'ConduitCity', 'ConduitState', 'ConduitZip', 'MemoCd', 'MemoTxt', 'SIorSLRef'],
    'SB': ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm', 'PayeeLName',
           'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeState',
           'PayeeZip', 'ElecCd', 'ElecDesc', 'ExpDt', 'ExpAmt', 'SemiAnnRefBundAmt', 'ExpPurpCd', 'ExpPurpDesc',
           'ExpCatCd', 'BenCommID', 'BenCommNm', 'BenCandID', 'BenCandLName', 'BenCandFName', 'BenCandMName',
           'BenCandPfx', 'BenCandSfx', 'BenCandOfc', 'BenCandState', 'BenCandDist', 'ConduitNm', 'ConduitAddr1',
           'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip', 'MemoCd', 'MemoTxt', 'SIorSLRef'],
    'SC': ['LineNbr', 'CommID', 'TransID', 'RctLnNbr', 'EntTp', 'LenderOrgName', 'LenderLName', 'LenderFName',
           'LenderMName', 'LenderPfx', 'LenderSfx', 'LenderAddr1', 'LenderAddr2', 'LenderCity', 'LenderState',
           'LenderZip', 'ElecCd', 'ElecDesc', 'LoanAmt', 'PymtToDt', 'LoanBlnc', 'IncurredDt', 'DueDt', 'IntRt',
           'flgSecured', 'flgPersFunds', 'LenderCommID', 'LenderCandID', 'LenderCandLName', 'LenderCandFName',
           'LenderCandMName', 'LenderCandPfx', 'LenderCandSfx', 'LenderCandOfc', 'LenderCandState', 'LenderCandDist',
           'MemoCd', 'MemoTxt'],
    'SC1': ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'Lender', 'LenderAddr1', 'LenderAddr2', 'LenderCity',
            'LenderState', 'LenderZip', 'LoanAmt', 'IntRt', 'IncurredDt', 'DueDt', 'flgLoanRestructured', 'OrigLoanDt',
            'CrdtAmtThisDraw', 'TotBlnc', 'flgOthersLiable', 'flgCollateral', 'CollateralDesc', 'CollateralVal',
            'flgPerfectedInt', 'flgFutIncPledged', 'FutIncDesc', 'FutIncEstVal', 'DepAcctEstDt', 'AcctLocName',
            'AcctLocAddr1', 'AcctLocAddr2', 'AcctLocCity', 'AcctLocState', 'AcctLocZip', 'DepAcctAuthDt',
            'LoanBasisDesc', 'TrsLName', 'TrsFName', 'TrsMName', 'TrsPfx', 'TrsSfx', 'TrsSignDt', 'LendRepLName',
            'LendRepFName', 'LendRepMName', 'LendRepPfx', 'LendRepSfx', 'LendRepTitle', 'LendRepSignDt'],
    'SC2': ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'GuarLName', 'GuarFName', 'GuarMName', 'GuarPfx', 'GuarSfx',
            'GuarAddr1', 'GuarAddr2', 'GuarCity', 'GuarState', 'GuarZip', 'GuarEmp', 'GuarOcc', 'GuarAmt'],
    'SD': ['LineNbr', 'CommID', 'EntTp', 'CreditorOrgName', 'CreditorLName', 'CreditorFName', 'CreditorMName',
           'CreditorPfx', 'CreditorSfx', 'CreditorAddr1', 'CreditorAddr2', 'CreditorCity', 'CreditorState',
           'CreditorZip', 'DebtPurp', 'BegBlnc_P', 'IncurAmt_P', 'PymtAmt_P', 'BalClose_P', 'CreditorCommID',
           'CreditorCandID', 'CreditorCandFullName', 'CreditorCandOfc', 'CreditorCandState', 'CreditorCandDist',
           'ConduitName', 'ConduitAddr1', 'ConduitAddr2', 'ConduitCity', 'ConduitState', 'ConduitZip', 'TransID'],
    'SE': ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm', 'PayeeLName',
           'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr',
           'PayeeZip', 'ElecCd', 'ElecDesc', 'DissmntnDt', 'ExpDt', 'ExpAmt', 'ExpAgg', 'ExpPurpDesc', 'ExpCatCd',
           'PayeeCommID', 'SupOppCd', 'SupOppCandID', 'SupOppCandLName', 'SupOppCandFName', 'SupOppCandMName',
           'SupOppCandPfx', 'SupOppCandSfx', 'SupOppCandOfc', 'SupOppCandStAbbr', 'SupOppCandDist', 'CompLName',
           'CompFName', 'CompMName', 'CompPfx', 'CompSfx', 'SignDt', 'MemoCd', 'MemoTxt'],
    'SF': ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'flgDesigCoordExp', 'DesigCommID',
           'DesigCommNm', 'SubordCommID', 'SubordCommNm', 'SubordAddr1', 'SubordAddr2', 'SubordCity', 'SubordStAbbr',
           'SubordZip', 'EntTp', 'PayeeOrgNm', 'PayeeLName', 'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx',
           'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr', 'PayeeZip', 'ExpDt', 'ExpAmt', 'ExpAgg', 'ExpPurpCd',
           'ExpPurpDesc', 'ExpCatCd', 'PayeeCommID', 'PayeeCandID', 'PayeeCandLName', 'PayeeCandFName',
           'PayeeCandMName', 'PayeeCandPfx', 'PayeeCandSfx', 'PayeeCandOfc', 'PayeeCandStAbbr', 'PayeeCandDist',
           'MemoCd', 'MemoTxt'],
    'H1': ['LineNbr', 'CommID', 'TransID', 'flgStLocFxPctPresOnly', 'flgStLocFxPctPresAndSen', 'flgStLocFxPctSenOnly',
           'flgStLocFxPctNonPresNonSen', 'flgFlatMin50PctFed', 'FedPct', 'NonFedPct', 'flgAdmRatio',
           'flgGenericVoterDrvRatio', 'flgPubCommunRefPrtyRatio'],
    'H2': ['LineNbr', 'CommID', 'TransID', 'EventNm', 'flgDirFndrsg', 'flgDirCandSup', 'RatioCd', 'FedPct',
           'NonFedPct'],
    'H3': ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'AcctNm', 'EventTp', 'EventNm', 'RcptDt', 'TotAmtTrans',
           'TransAmt'],
    'H4': ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm', 'PayeeLName',
           'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr',
           'PayeeZip', 'EventNm', 'ExpDt', 'ExpAmt', 'FedAmt', 'NonFedAmt', 'EventAgg', 'ExpPurpCd', 'ExpPurpDesc',
           'ExpCatCd', 'flgAdminActivity', 'flgDirectFndrsg', 'flgExempt', 'flgGenVtrDrv', 'flgDirCandSup',
           'flgPubCommun', 'MemoCd', 'MemoTxt'],
    'H5': ['LineNbr', 'CommID', 'TransID', 'AcctNm', 'RcptDt', 'TotAmt', 'VotRegnAmt', 'VotIDAmt', 'GOTVAmt',
           'GenCampAmt'],
    'H6': ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'EntTp', 'PayeeOrgNm', 'PayeeLName',
           'PayeeFName', 'PayeeMName', 'PayeePfx', 'PayeeSfx', 'PayeeAddr1', 'PayeeAddr2', 'PayeeCity', 'PayeeStAbbr',
           'PayeeZip', 'EventNm', 'ExpDt', 'TotExpAmt', 'FedAmt', 'LevinAmt', 'ExpAgg', 'ExpPurpCd', 'ExpPurpDesc',
           'ExpCatCd', 'flgActVotRegn', 'flgActGOTV', 'flgActVotID', 'flgActGenCamp', 'MemoCd', 'MemoTxt'],
    'SI': ['LineNbr', 'CommID', 'TransID', 'RecIDNbr', 'AcctNm', 'BankAcctID', 'CovgFmDt', 'CovgToDt', 'TotRcpts',
           'TransToFed', 'TransToStAndLoc', 'DirStLocCandSup', 'OthDisb', 'TotDisb', 'BegCOH', 'Rcpts', 'Subtotal',
           'Disb', 'EndCOH', 'TotRcpts2', 'TransToFed2', 'TransToStAndLoc2', 'DirStLocCandSup2', 'OthDisb2', 'TotDisb2',
           'BegCOH2', 'Rcpts2', 'Subtotal2', 'Disb2', 'EndCOH2'],
    'SL': ['LineNbr', 'CommID', 'TransID', 'RecordID', 'AcctNm', 'CovgFmDt', 'CovgToDt', 'IndRcptsItem_P',
           'IndRcptsUnitem_P', 'IndRcptsTot_P', 'OthRcpts_P', 'TotRcpts_P', 'TransVotReg_P', 'TransVotID_P',
           'TransGOTV_P', 'TransGenCamp_P', 'TransTot_P', 'OthDisb_P', 'TotDisb_P', 'BegCOH_P', 'Rcpts_P', 'Subtotal_P',
           'Disb_P', 'EndCOH_P', 'IndRcptsItem_T', 'IndRcptsUnitem_T', 'IndRcptsTot_T', 'OthRcpts_T', 'TotRcpts_T',
           'TransVotReg_T', 'TransVotID_T', 'TransGOTV_T', 'TransGenCamp_T', 'TransTot_T', 'OthDisb_T', 'TotDisb_T',
           'BegCOH_T', 'Rcpts_T', 'Subtotal_T', 'Disb_T', 'EndCOH_T'],
    'TEXT': ['LineNbr', 'CommID', 'TransID', 'BkRefTransID', 'BkRefSchdNm', 'FullText']}


def add_entry_to_error_log(logfile, logtext):
    with open(logfile, 'a+b') as output:
        output.write(logtext.strip() + '\n')


def build_data_row(data, headers, imageid, rpttype):
    output = [str(imageid)]
    if rpttype != None:
        output.append(rpttype)
    for header in headers:
        if data[header] == None:
            output.append('')
        elif data[header] == '':
            output.append('')
        else:
            output.append(data[header])
    return output


def build_list_of_supported_report_types():
    types = []
    for hdr in filehdrs:
        types.append(hdr[0])
    return types


def ck_curr_val(val, image, fieldname, formtype, rownbr):
    errfile = RPTERRDIR + 'BadDates.log'
    try:
        if val == None:
            return ''
        val = val.replace('$', '').replace(',', '').strip(' "')
        if val == '':
            return ''
        else:
            float(val)
            return val
    except:
        add_entry_to_error_log(errfile,
                               'Unable to convert ' + fieldname + ' field (value: "' + val + '") to number for row ' + str(
                                   rownbr) + ' (form type: ' + formtype + ') of ' + str(image) + '.')
        return ''


def clean_sql_text(val, nullstring='', outputtextdelim=''):
    # This function removes leading and trailing quotation marks and whitespace
    # and converts any instances of an apostrope to two apostrophes so the
    # text can be imported into SQL Server.
    # nullstring value returned when None or empty string found.
    val = val.strip(' "')
    if val == None:
        return nullstring
    elif val == '':
        return nullstring
    else:
        while val.find("''") != -1:
            val = val.replace("''", "'")
        while val.find('""') != -1:
            val = val.replace('""', '"')
        if outputtextdelim == "'":
            val = val.replace("'", "''")
        return outputtextdelim + val + outputtextdelim


def convert_to_bit(val):
    val = val.strip()
    if val == '':
        val = '0'
    elif val == 'N':
        val = '0'
    elif val == '0':
        val = '0'
    else:
        val = '1'
    return val


def convert_to_date(val, dateformat, image, fieldname, formtype, rownbr, sched, trans=''):
    errfile = RPTERRDIR + 'BadDates.log'
    if val == None:
        return ''
    val = val.strip(' "')
    if val == '':
        return ''
    else:
        try:
            year = ''
            month = ''
            day = ''
            currtime = datetime.datetime.now()
            curryear = int(currtime.strftime('%Y'))
            # First see if date string is M/D/(CC)YY or M-D-(CC)YY
            if val.find('/') != -1:
                if val[val.find('/') + 1:].find('/') != -1:
                    x1 = val.find('/')
                    x2 = x1 + val[x1 + 1:].find('/') + 1
                    month = val[:x1].lstrip('0')
                    day = val[x1 + 1:x2].lstrip('0')
                    year = val[x2 + 1:]
                    if int(year) < 10:
                        year = '0' + year
                    if int(year) < 100:
                        year = '20' + year
                    if int(year) > curryear:
                        year = '19' + year[-2:]
            elif val.find('-') != -1:
                if val[val.find('-') + 1:].find('-') != -1:
                    x1 = val.find('-')
                    x2 = x1 + val[x1 + 1:].find('-') + 1
                    month = val[:x1].lstrip('0')
                    day = val[x1 + 1:x2].lstrip('0')
                    year = val[x2 + 1:]
                    if int(year) < 10:
                        year = '0' + year
                    if int(year) < 100:
                        year = '20' + year
                    if int(year) > curryear:
                        year = '19' + year[-2:]
            else:
                month = dateformat.find('MM')
                month = val[month:month + 2]  # .lstrip('0')
                day = dateformat.find('DD')
                day = val[day:day + 2]  # .lstrip('0')
                if dateformat.find('CCYY') != -1:
                    year = val[dateformat.find('CCYY'):dateformat.find('CCYY') + 4]
                elif dateformat.find('YYYY') != -1:
                    year = val[dateformat.find('YYYY'):dateformat.find('YYYY') + 4]
                elif dateformat.find('YY') != -1:
                    year = '20' + val[dateformat.find('YY'):dateformat.find('YY') + 2]
                    if int(year) > curryear:
                        year = '19' + val[-2:]
                else:
                    add_entry_to_error_log(errfile, str(image) + '\t' + sched + '\t' + trans + '\t' + str(
                        rownbr) + '\t' + formtype + '\t' + fieldname + '\t' + val + '\t' + dateformat)
                    with open(errfile, 'a+b') as output:
                        output.write(errtxt + '\n')
                    return ''
            datestring = month + '/' + day + '/' + year
            datadate = time.strptime(datestring, '%m/%d/%Y')
            return datestring

        except:
            add_entry_to_error_log(errfile, str(image) + '\t' + sched + '\t' + trans + '\t' + str(
                rownbr) + '\t' + formtype + '\t' + fieldname + '\t' + val + '\t' + dateformat)
            return ''


def convert_to_tinyint(val, image, fieldname, formtype, rownbr, sched, trans=''):
    errfile = RPTERRDIR + 'BadIntegers.log'
    if val == None:
        return ''
    val = val.strip().strip(' "')
    if val == '':
        return ''
    else:
        try:
            x = int(val)
            if x < 0 or x > 255:
                add_entry_to_error_log(errfile, str(image) + '\t' + sched + '\t' + trans + '\t' + str(
                    rownbr) + '\t' + formtype + '\t' + fieldname + '\t' + val)
                return ''
            else:
                return str(x)
        except:
            add_entry_to_error_log(errfile, str(image) + '\t' + sched + '\t' + trans + '\t' + str(
                rownbr) + '\t' + formtype + '\t' + fieldname + '\t' + val)
            return ''


def create_file_timestamp():
    filetime = datetime.datetime.now()
    return filetime.strftime('%Y%m%d%H%M')


def get_row_headers(header, version):
    rowhdrs = []
    for hdr in filehdrs:
        if hdr[0] == header:
            for subhdr in hdr[1]:
                if str(version) in subhdr[0]:
                    rowhdrs = subhdr[1]
    return rowhdrs


def load_rpt_hdrs(rpttype, imageid, rowdata, filehdr, outputhdrs, DBCONNSTR):
    errfile = RPTERRDIR + 'ErrorMessages.log'
    # Create stored procedure call to load header data into database
    sql = 'EXEC dbo.usp_AddRptHdr_' + rpttype + ' ' + str(imageid) + ', '

    # Add report header data values
    # Ignore full names
    for hdr in outputhdrs:
        if hdr == 'TrsFullName' or hdr == 'SignFullName' or hdr == 'AgtFullName' or hdr == 'CustFullName' or hdr == 'CandFullName':
            continue
        data = rowdata[hdr]
        if data == None or data == '':
            data = 'NULL'
        elif data == 'nullstring':
            data = "''"
        sql += data + ', '

    # Add file header data values
    sql += str(filehdr['Ver']) + ', '
    sql += clean_sql_text(filehdr['SftNm'], '', "'") + ', '
    sql += clean_sql_text(filehdr['SftVer'], '', "'") + ', '
    sql += clean_sql_text(filehdr['RptID'], '', "'") + ', '
    sql += clean_sql_text(filehdr['RptNbr'], '', "'") + ', '
    sql += clean_sql_text(filehdr['HdrCmnt'], '', "'")

    # Replace empty strings with NULL
    while sql.find(', ,') != -1:
        sql = sql.replace(', ,', ', NULL,')
    if sql.endswith(', '):
        sql += 'NULL'

    # Create SQL Server connection
    conn = pyodbc.connect(DBCONNSTR)
    cursor = conn.cursor()

    # Excecute stored procedure
    cursor.execute(sql)
    sqlresult = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    # Display error messages
    if sqlresult == -1:
        add_entry_to_error_log(errfile, str(imageid) + '.fec already ' \
                                                       'exists in the FEC database. Data ' \
                                                       'from this file will not be imported, ' \
                                                       'and the file has been moved to the ' \
                                                       'Review directory.')
    elif sqlresult == -2:
        add_entry_to_error_log(errfile, 'The stored procedure ' \
                                        'returned an error when this Python ' \
                                        'script attempted to load the header ' \
                                        'for ' + str(imageid) + '. The data ' \
                                                                'was not loaded into the database, ' \
                                                                'and the file has been moved to the ' \
                                                                'Review directory. The stored ' \
                                                                'procedure call which failed was: ' + sql
                               )
    return sqlresult


def parse_data_row(data, delim):
    # There are many cases where a field begins with " but is cut off or
    # otherwise ends with no closing ". This causes multiple fields to
    # be joined together and the parsing to fail. For that reason, I'm
    # using csv module only for comma delimiters.
    if delim == ',':
        for x in csv.reader([data], SRCDELIMITER=',', quotechar='"'):
            data = x
    else:
        data = data.split(delim)
        data[:] = (datum.strip('" ') for datum in data)

    return data


def parse_full_name(data, delimiter):
    fullname = data.split(delimiter)
    for name in fullname:
        name = name.strip(' "')
    if len(fullname) == 1:
        fullname[0] = clean_sql_text(fullname[0])
        fullname.append('')
        fullname.append('')
        fullname.append('')
        fullname.append('')
    elif len(fullname) == 2:
        fullname[0] = clean_sql_text(fullname[0])
        fullname[1] = clean_sql_text(fullname[1])
        fullname.append('')
        fullname.append('')
        fullname.append('')
    elif len(fullname) == 3:
        fullname[0] = clean_sql_text(fullname[0])
        fullname[1] = clean_sql_text(fullname[1])
        fullname.insert(2, '')
        fullname[3] = clean_sql_text(fullname[3])
        fullname.append('')
    elif len(fullname) == 4:
        fullname[0] = clean_sql_text(fullname[0])
        fullname[1] = clean_sql_text(fullname[1])
        fullname.insert(2, '')
        fullname[3] = clean_sql_text(fullname[3])
        fullname[4] = clean_sql_text(fullname[4])
    elif len(fullname) == 5:
        fullname[0] = clean_sql_text(fullname[0])
        fullname[1] = clean_sql_text(fullname[1])
        fullname[2] = clean_sql_text(fullname[2])
        fullname[3] = clean_sql_text(fullname[3])
        fullname[4] = clean_sql_text(fullname[4])
    else:
        while len(fullname) < 5:
            fullname.append('')
        fullname = fullname[:5]
        fullname[0] = clean_sql_text(data.replace(delimiter, ', '))
        fullname[1] = ''
        fullname[2] = ''
        fullname[3] = ''
        fullname[4] = ''

    # Copy entire name to last name field if any other field is too long
    if len(fullname[1]) > 35 or len(fullname[2]) > 20 or len(fullname[3]) > 20 or len(fullname[4]) > 15:
        fullname[0] = clean_sql_text(data.replace(delimiter, ', '))
        fullname[1] = ''
        fullname[2] = ''
        fullname[3] = ''
        fullname[4] = ''

    return fullname


def populate_data_row_dict(data, headers, output):
    for x in range(len(headers)):
        if headers[x] in output.keys() and x < len(
                data):  # 100235 (F3X, v5.0) missing last 12 cols after treas sign date
            output[headers[x]] = data[x].strip().replace('\t', ' ').strip(' "\n')
    return output


def check_rpt_hdrs_f3(image, data, namedelim='', dateformat='CCYYMMDD'):
    # FormTp
    data['FormTp'] = clean_sql_text(data['FormTp'], 'nullstring', "'")

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'], 'nullstring', "'")

    # CommNm
    data['CommNm'] = clean_sql_text(data['CommNm'], 'nullstring', "'")

    # AddrChg
    data['AddrChg'] = convert_to_bit(clean_sql_text(data['AddrChg']))

    # Addr1
    data['Addr1'] = clean_sql_text(data['Addr1'], 'nullstring', "'")

    # Addr2
    data['Addr2'] = clean_sql_text(data['Addr2'], '', "'")

    # City
    data['City'] = clean_sql_text(data['City'], 'nullstring', "'")

    # StAbbr
    data['StAbbr'] = clean_sql_text(data['StAbbr'], 'nullstring', "'")

    # Zip
    data['Zip'] = clean_sql_text(data['Zip'], 'nullstring', "'")

    # ElecSt
    data['ElecSt'] = clean_sql_text(data['ElecSt'], 'nullstring', "'")

    # ElecDist
    data['ElecDist'] = convert_to_tinyint(data['ElecDist'], image, 'ElecDist', 'Header', 0, 'F3', '')

    # RptCd
    data['RptCd'] = clean_sql_text(data['RptCd'], 'nullstring', "'")

    # ElecCd
    data['ElecCd'] = clean_sql_text(data['ElecCd'], '', "'")

    # ElecDt
    data['ElecDt'] = "'" + convert_to_date(data['ElecDt'], dateformat, image, 'ElecDt', 'Header', 0, 'F3', '') + "'"
    if data['ElecDt'] == "''":
        data['ElecDt'] = 'NULL'

    # StateOfElec
    data['StateOfElec'] = clean_sql_text(data['StateOfElec'], 'nullstring', "'")

    # CovgFmDt
    data['CovgFmDt'] = "'" + convert_to_date(data['CovgFmDt'], dateformat, image, 'CovgFmDt', 'Header', 0, 'F3',
                                             '') + "'"
    if data['CovgFmDt'] == "''":
        data['CovgFmDt'] = 'NULL'

    # CovgToDt
    data['CovgToDt'] = "'" + convert_to_date(data['CovgToDt'], dateformat, image, 'CovgToDt', 'Header', 0, 'F3',
                                             '') + "'"
    if data['CovgToDt'] == "''":
        data['CovgToDt'] = 'NULL'

    # TrsFullName
    if data['TrsFullName'] != '':
        if data['TrsLName'] != '' or data['TrsFName'] != '' or data['TrsMName'] != '' or data['TrsPfx'] != '' or data[
            'TrsSfx'] != '':
            add_entry_to_error_log(RPTERRDIR + 'ErrorMessages.log', 'Treasurer full name (' + data[
                'TrsFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            treas = parse_full_name(data['TrsFullName'], namedelim)
            data['TrsLName'] = treas[0]
            data['TrsFName'] = treas[1]
            data['TrsMName'] = treas[2]
            data['TrsPfx'] = treas[3]
            data['TrsSfx'] = treas[4]
        else:
            data['TrsLName'] = data['TrsFullName']

    # TrsLName
    data['TrsLName'] = clean_sql_text(data['TrsLName'], 'nullstring', "'")

    # TrsFName
    data['TrsFName'] = clean_sql_text(data['TrsFName'], '', "'")

    # TrsMName
    data['TrsMName'] = clean_sql_text(data['TrsMName'], '', "'")

    # TrsPfx
    data['TrsPfx'] = clean_sql_text(data['TrsPfx'], '', "'")

    # TrsSfx
    data['TrsSfx'] = clean_sql_text(data['TrsSfx'], '', "'")

    # SignDt
    data['SignDt'] = "'" + convert_to_date(data['SignDt'], dateformat, image, 'SignDt', 'Header', 0, 'F3', '') + "'"
    if data['SignDt'] == "''":
        data['SignDt'] = 'NULL'

    # TotConts_P_6a
    data['TotConts_P_6a'] = ck_curr_val(data['TotConts_P_6a'], image, 'TotConts_P_6a', 'Header', 0)

    # TotContRfds_P_6b
    data['TotContRfds_P_6b'] = ck_curr_val(data['TotContRfds_P_6b'], image, 'TotContRfds_P_6b', 'Header', 0)

    # NetConts_P_6c
    data['NetConts_P_6c'] = ck_curr_val(data['NetConts_P_6c'], image, 'NetConts_P_6c', 'Header', 0)

    # TotOpExps_P_7a
    data['TotOpExps_P_7a'] = ck_curr_val(data['TotOpExps_P_7a'], image, 'TotOpExps_P_7a', 'Header', 0)

    # TotOffsetOpExps_P_7b
    data['TotOffsetOpExps_P_7b'] = ck_curr_val(data['TotOffsetOpExps_P_7b'], image, 'TotOffsetOpExps_P_7b', 'Header', 0)

    # NetOpExps_P_7c
    data['NetOpExps_P_7c'] = ck_curr_val(data['NetOpExps_P_7c'], image, 'NetOpExps_P_7c', 'Header', 0)

    # CashClose_P_8
    data['CashClose_P_8'] = ck_curr_val(data['CashClose_P_8'], image, 'CashClose_P_8', 'Header', 0)

    # DebtsTo_P_9
    data['DebtsTo_P_9'] = ck_curr_val(data['DebtsTo_P_9'], image, 'DebtsTo_P_9', 'Header', 0)

    # DebtsBy_P_10
    data['DebtsBy_P_10'] = ck_curr_val(data['DebtsBy_P_10'], image, 'DebtsBy_P_10', 'Header', 0)

    # IndContsItem_P_11a1
    data['IndContsItem_P_11a1'] = ck_curr_val(data['IndContsItem_P_11a1'], image, 'IndContsItem_P_11a1', 'Header', 0)

    # IndContsUnitem_P_11a2
    data['IndContsUnitem_P_11a2'] = ck_curr_val(data['IndContsUnitem_P_11a2'], image, 'IndContsUnitem_P_11a2', 'Header',
                                                0)

    # IndContsTot_P_11a3
    data['IndContsTot_P_11a3'] = ck_curr_val(data['IndContsTot_P_11a3'], image, 'IndContsTot_P_11a3', 'Header', 0)

    # PolPtyCommConts_P_11b
    data['PolPtyCommConts_P_11b'] = ck_curr_val(data['PolPtyCommConts_P_11b'], image, 'PolPtyCommConts_P_11b', 'Header',
                                                0)

    # OthPolCommConts_P_11c
    data['OthPolCommConts_P_11c'] = ck_curr_val(data['OthPolCommConts_P_11c'], image, 'OthPolCommConts_P_11c', 'Header',
                                                0)

    # CandConts_P_11d
    data['CandConts_P_11d'] = ck_curr_val(data['CandConts_P_11d'], image, 'CandConts_P_11d', 'Header', 0)

    # TotConts_P_11e
    data['TotConts_P_11e'] = ck_curr_val(data['TotConts_P_11e'], image, 'TotConts_P_11e', 'Header', 0)

    # TranFmOthAuthComms_P_12
    data['TranFmOthAuthComms_P_12'] = ck_curr_val(data['TranFmOthAuthComms_P_12'], image, 'TranFmOthAuthComms_P_12',
                                                  'Header', 0)

    # CandLoans_P_13a
    data['CandLoans_P_13a'] = ck_curr_val(data['CandLoans_P_13a'], image, 'CandLoans_P_13a', 'Header', 0)

    # OthLoans_P_13b
    data['OthLoans_P_13b'] = ck_curr_val(data['OthLoans_P_13b'], image, 'OthLoans_P_13b', 'Header', 0)

    # TotLoans_P_13c
    data['TotLoans_P_13c'] = ck_curr_val(data['TotLoans_P_13c'], image, 'TotLoans_P_13c', 'Header', 0)

    # OffsetOpExps_P_14
    data['OffsetOpExps_P_14'] = ck_curr_val(data['OffsetOpExps_P_14'], image, 'OffsetOpExps_P_14', 'Header', 0)

    # OthRcpts_P_15
    data['OthRcpts_P_15'] = ck_curr_val(data['OthRcpts_P_15'], image, 'OthRcpts_P_15', 'Header', 0)

    # TotRcpts_P_16
    data['TotRcpts_P_16'] = ck_curr_val(data['TotRcpts_P_16'], image, 'TotRcpts_P_16', 'Header', 0)

    # OpExps_P_17
    data['OpExps_P_17'] = ck_curr_val(data['OpExps_P_17'], image, 'OpExps_P_17', 'Header', 0)

    # TranToOthAuthComms_P_18
    data['TranToOthAuthComms_P_18'] = ck_curr_val(data['TranToOthAuthComms_P_18'], image, 'TranToOthAuthComms_P_18',
                                                  'Header', 0)

    # CandLoansRepaid_P_19a
    data['CandLoansRepaid_P_19a'] = ck_curr_val(data['CandLoansRepaid_P_19a'], image, 'CandLoansRepaid_P_19a', 'Header',
                                                0)

    # OthLoansRepaid_P_19b
    data['OthLoansRepaid_P_19b'] = ck_curr_val(data['OthLoansRepaid_P_19b'], image, 'OthLoansRepaid_P_19b', 'Header', 0)

    # TotLoansRepaid_P_19c
    data['TotLoansRepaid_P_19c'] = ck_curr_val(data['TotLoansRepaid_P_19c'], image, 'TotLoansRepaid_P_19c', 'Header', 0)

    # RefundsInd_P_20a
    data['RefundsInd_P_20a'] = ck_curr_val(data['RefundsInd_P_20a'], image, 'RefundsInd_P_20a', 'Header', 0)

    # RefundsPolPtyComms_P_20b
    data['RefundsPolPtyComms_P_20b'] = ck_curr_val(data['RefundsPolPtyComms_P_20b'], image, 'RefundsPolPtyComms_P_20b',
                                                   'Header', 0)

    # RefundsOthPolComms_P_20c
    data['RefundsOthPolComms_P_20c'] = ck_curr_val(data['RefundsOthPolComms_P_20c'], image, 'RefundsOthPolComms_P_20c',
                                                   'Header', 0)

    # TotRefunds_P_20d
    data['TotRefunds_P_20d'] = ck_curr_val(data['TotRefunds_P_20d'], image, 'TotRefunds_P_20d', 'Header', 0)

    # OthDisb_P_21
    data['OthDisb_P_21'] = ck_curr_val(data['OthDisb_P_21'], image, 'OthDisb_P_21', 'Header', 0)

    # TotDisb_P_22
    data['TotDisb_P_22'] = ck_curr_val(data['TotDisb_P_22'], image, 'TotDisb_P_22', 'Header', 0)

    # CashBegin_P_23
    data['CashBegin_P_23'] = ck_curr_val(data['CashBegin_P_23'], image, 'CashBegin_P_23', 'Header', 0)

    # TotRcpts_P_24
    data['TotRcpts_P_24'] = ck_curr_val(data['TotRcpts_P_24'], image, 'TotRcpts_P_24', 'Header', 0)

    # Subtotal_P_25
    data['Subtotal_P_25'] = ck_curr_val(data['Subtotal_P_25'], image, 'Subtotal_P_25', 'Header', 0)

    # TotDisb_P_26
    data['TotDisb_P_26'] = ck_curr_val(data['TotDisb_P_26'], image, 'TotDisb_P_26', 'Header', 0)

    # CashClose_P_27
    data['CashClose_P_27'] = ck_curr_val(data['CashClose_P_27'], image, 'CashClose_P_27', 'Header', 0)

    # TotConts_T_6a
    data['TotConts_T_6a'] = ck_curr_val(data['TotConts_T_6a'], image, 'TotConts_T_6a', 'Header', 0)

    # TotContRfds_T_6b
    data['TotContRfds_T_6b'] = ck_curr_val(data['TotContRfds_T_6b'], image, 'TotContRfds_T_6b', 'Header', 0)

    # NetConts_T_6c
    data['NetConts_T_6c'] = ck_curr_val(data['NetConts_T_6c'], image, 'NetConts_T_6c', 'Header', 0)

    # TotOpExps_T_7a
    data['TotOpExps_T_7a'] = ck_curr_val(data['TotOpExps_T_7a'], image, 'TotOpExps_T_7a', 'Header', 0)

    # TotOffsetOpExps_T_7b
    data['TotOffsetOpExps_T_7b'] = ck_curr_val(data['TotOffsetOpExps_T_7b'], image, 'TotOffsetOpExps_T_7b', 'Header', 0)

    # NetOpExps_T_7c
    data['NetOpExps_T_7c'] = ck_curr_val(data['NetOpExps_T_7c'], image, 'NetOpExps_T_7c', 'Header', 0)

    # IndContsItem_T_11a1
    data['IndContsItem_T_11a1'] = ck_curr_val(data['IndContsItem_T_11a1'], image, 'IndContsItem_T_11a1', 'Header', 0)

    # IndContsUnitem_T_11a2
    data['IndContsUnitem_T_11a2'] = ck_curr_val(data['IndContsUnitem_T_11a2'], image, 'IndContsUnitem_T_11a2', 'Header',
                                                0)

    # IndContsTot_T_11a3
    data['IndContsTot_T_11a3'] = ck_curr_val(data['IndContsTot_T_11a3'], image, 'IndContsTot_T_11a3', 'Header', 0)

    # PolPtyCommConts_T_11b
    data['PolPtyCommConts_T_11b'] = ck_curr_val(data['PolPtyCommConts_T_11b'], image, 'PolPtyCommConts_T_11b', 'Header',
                                                0)

    # OthPolCommConts_T_11c
    data['OthPolCommConts_T_11c'] = ck_curr_val(data['OthPolCommConts_T_11c'], image, 'OthPolCommConts_T_11c', 'Header',
                                                0)

    # CandConts_T_11d
    data['CandConts_T_11d'] = ck_curr_val(data['CandConts_T_11d'], image, 'CandConts_T_11d', 'Header', 0)

    # TotConts_T_11e
    data['TotConts_T_11e'] = ck_curr_val(data['TotConts_T_11e'], image, 'TotConts_T_11e', 'Header', 0)

    # TranFmOthAuthComms_T_12
    data['TranFmOthAuthComms_T_12'] = ck_curr_val(data['TranFmOthAuthComms_T_12'], image, 'TranFmOthAuthComms_T_12',
                                                  'Header', 0)

    # CandLoans_T_13a
    data['CandLoans_T_13a'] = ck_curr_val(data['CandLoans_T_13a'], image, 'CandLoans_T_13a', 'Header', 0)

    # OthLoans_T_13b
    data['OthLoans_T_13b'] = ck_curr_val(data['OthLoans_T_13b'], image, 'OthLoans_T_13b', 'Header', 0)

    # TotLoans_T_13c
    data['TotLoans_T_13c'] = ck_curr_val(data['TotLoans_T_13c'], image, 'TotLoans_T_13c', 'Header', 0)

    # OffsetOpExps_T_14
    data['OffsetOpExps_T_14'] = ck_curr_val(data['OffsetOpExps_T_14'], image, 'OffsetOpExps_T_14', 'Header', 0)

    # OthRcpts_T_15
    data['OthRcpts_T_15'] = ck_curr_val(data['OthRcpts_T_15'], image, 'OthRcpts_T_15', 'Header', 0)

    # TotRcpts_T_16
    data['TotRcpts_T_16'] = ck_curr_val(data['TotRcpts_T_16'], image, 'TotRcpts_T_16', 'Header', 0)

    # OpExps_T_17
    data['OpExps_T_17'] = ck_curr_val(data['OpExps_T_17'], image, 'OpExps_T_17', 'Header', 0)

    # TranToOthAuthComms_T_18
    data['TranToOthAuthComms_T_18'] = ck_curr_val(data['TranToOthAuthComms_T_18'], image, 'TranToOthAuthComms_T_18',
                                                  'Header', 0)

    # CandLoansRepaid_T_19a
    data['CandLoansRepaid_T_19a'] = ck_curr_val(data['CandLoansRepaid_T_19a'], image, 'CandLoansRepaid_T_19a', 'Header',
                                                0)

    # OthLoansRepaid_T_19b
    data['OthLoansRepaid_T_19b'] = ck_curr_val(data['OthLoansRepaid_T_19b'], image, 'OthLoansRepaid_T_19b', 'Header', 0)

    # TotLoansRepaid_T_19c
    data['TotLoansRepaid_T_19c'] = ck_curr_val(data['TotLoansRepaid_T_19c'], image, 'TotLoansRepaid_T_19c', 'Header', 0)

    # RefundsInd_T_20a
    data['RefundsInd_T_20a'] = ck_curr_val(data['RefundsInd_T_20a'], image, 'RefundsInd_T_20a', 'Header', 0)

    # RefundsPolPtyComms_T_20b
    data['RefundsPolPtyComms_T_20b'] = ck_curr_val(data['RefundsPolPtyComms_T_20b'], image, 'RefundsPolPtyComms_T_20b',
                                                   'Header', 0)

    # RefundsOthPolComms_T_20c
    data['RefundsOthPolComms_T_20c'] = ck_curr_val(data['RefundsOthPolComms_T_20c'], image, 'RefundsOthPolComms_T_20c',
                                                   'Header', 0)

    # TotRefunds_T_20d
    data['TotRefunds_T_20d'] = ck_curr_val(data['TotRefunds_T_20d'], image, 'TotRefunds_T_20d', 'Header', 0)

    # OthDisb_T_21
    data['OthDisb_T_21'] = ck_curr_val(data['OthDisb_T_21'], image, 'OthDisb_T_21', 'Header', 0)

    # TotDisb_T_22
    data['TotDisb_T_22'] = ck_curr_val(data['TotDisb_T_22'], image, 'TotDisb_T_22', 'Header', 0)

    return data


def check_rpt_hdrs_f3l(image, data, namedelim='', dateformat='CCYYMMDD'):
    # FormTp
    data['FormTp'] = clean_sql_text(data['FormTp'], 'nullstring', "'")

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'], 'nullstring', "'")

    # CommNm
    data['CommNm'] = clean_sql_text(data['CommNm'], 'nullstring', "'")

    # AddrChg
    data['AddrChg'] = convert_to_bit(clean_sql_text(data['AddrChg']))

    # Addr1
    data['Addr1'] = clean_sql_text(data['Addr1'], 'nullstring', "'")

    # Addr2
    data['Addr2'] = clean_sql_text(data['Addr2'], '', "'")

    # City
    data['City'] = clean_sql_text(data['City'], 'nullstring', "'")

    # StAbbr
    data['StAbbr'] = clean_sql_text(data['StAbbr'], 'nullstring', "'")

    # Zip
    data['Zip'] = clean_sql_text(data['Zip'], 'nullstring', "'")

    # ElecSt
    data['ElecSt'] = clean_sql_text(data['ElecSt'], 'nullstring', "'")

    # ElecDist
    data['ElecDist'] = convert_to_tinyint(data['ElecDist'], image, 'ElecDist', 'Header', 0, 'F3', '')

    # RptCd
    data['RptCd'] = clean_sql_text(data['RptCd'], 'nullstring', "'")

    # ElecDt
    data['ElecDt'] = "'" + convert_to_date(data['ElecDt'], dateformat, image, 'ElecDt', 'Header', 0, 'F3', '') + "'"
    if data['ElecDt'] == "''":
        data['ElecDt'] = 'NULL'

    # StateOfElec
    data['StateOfElec'] = clean_sql_text(data['StateOfElec'], 'nullstring', "'")

    # flgInclSemiAnnPrd
    data['flgInclSemiAnnPrd'] = convert_to_bit(clean_sql_text(data['flgInclSemiAnnPrd']))

    # CovgFmDt
    data['CovgFmDt'] = "'" + convert_to_date(data['CovgFmDt'], dateformat, image, 'CovgFmDt', 'Header', 0, 'F3',
                                             '') + "'"
    if data['CovgFmDt'] == "''":
        data['CovgFmDt'] = 'NULL'

    # CovgToDt
    data['CovgToDt'] = "'" + convert_to_date(data['CovgToDt'], dateformat, image, 'CovgToDt', 'Header', 0, 'F3',
                                             '') + "'"
    if data['CovgToDt'] == "''":
        data['CovgToDt'] = 'NULL'

    # flgInclSemiAnnJanJun
    data['flgInclSemiAnnJanJun'] = convert_to_bit(clean_sql_text(data['flgInclSemiAnnJanJun']))

    # flgInclSemiAnnJulDec
    data['flgInclSemiAnnJulDec'] = convert_to_bit(clean_sql_text(data['flgInclSemiAnnJulDec']))

    # TotRptBundContribs
    data['TotRptBundContribs'] = ck_curr_val(data['TotRptBundContribs'], image, 'TotRptBundContribs', 'Header', 0)

    # SemiAnnBundContribs
    data['SemiAnnBundContribs'] = ck_curr_val(data['SemiAnnBundContribs'], image, 'SemiAnnBundContribs', 'Header', 0)

    # TrsLName
    data['TrsLName'] = clean_sql_text(data['TrsLName'], 'nullstring', "'")

    # TrsFName
    data['TrsFName'] = clean_sql_text(data['TrsFName'], '', "'")

    # TrsMName
    data['TrsMName'] = clean_sql_text(data['TrsMName'], '', "'")

    # TrsPfx
    data['TrsPfx'] = clean_sql_text(data['TrsPfx'], '', "'")

    # TrsSfx
    data['TrsSfx'] = clean_sql_text(data['TrsSfx'], '', "'")

    # SignDt
    data['SignDt'] = "'" + convert_to_date(data['SignDt'], dateformat, image, 'SignDt', 'Header', 0, 'F3', '') + "'"
    if data['SignDt'] == "''":
        data['SignDt'] = 'NULL'

    return data


def check_rpt_hdrs_f3p(image, data, namedelim='', dateformat='CCYYMMDD'):
    # FormTp
    data['FormTp'] = clean_sql_text(data['FormTp'], 'nullstring', "'")

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'], 'nullstring', "'")

    # CommNm
    data['CommNm'] = clean_sql_text(data['CommNm'], 'nullstring', "'")

    # AddrChg
    data['AddrChg'] = convert_to_bit(clean_sql_text(data['AddrChg']))

    # Addr1
    data['Addr1'] = clean_sql_text(data['Addr1'], 'nullstring', "'")

    # Addr2
    data['Addr2'] = clean_sql_text(data['Addr2'], '', "'")

    # City
    data['City'] = clean_sql_text(data['City'], 'nullstring', "'")

    # StAbbr
    data['StAbbr'] = clean_sql_text(data['StAbbr'], 'nullstring', "'")

    # Zip
    data['Zip'] = clean_sql_text(data['Zip'], 'nullstring', "'")

    # PrimElec
    data['PrimElec'] = convert_to_bit(clean_sql_text(data['PrimElec']))

    # GenElec
    data['GenElec'] = convert_to_bit(clean_sql_text(data['GenElec']))

    # RptCd
    data['RptCd'] = clean_sql_text(data['RptCd'], 'nullstring', "'")

    # ElecCd
    data['ElecCd'] = clean_sql_text(data['ElecCd'], '', "'")

    # ElecDt
    data['ElecDt'] = "'" + convert_to_date(data['ElecDt'], dateformat, image, 'ElecDt', 'Header', 0, 'F3P', '') + "'"
    if data['ElecDt'] == "''":
        data['ElecDt'] = 'NULL'

    # ElecSt
    data['ElecSt'] = clean_sql_text(data['ElecSt'], 'nullstring', "'")

    # CovgFmDt
    data['CovgFmDt'] = "'" + convert_to_date(data['CovgFmDt'], dateformat, image, 'CovgFmDt', 'Header', 0, 'F3P',
                                             '') + "'"
    if data['CovgFmDt'] == "''":
        data['CovgFmDt'] = 'NULL'

    # CovgToDt
    data['CovgToDt'] = "'" + convert_to_date(data['CovgToDt'], dateformat, image, 'CovgToDt', 'Header', 0, 'F3P',
                                             '') + "'"
    if data['CovgToDt'] == "''":
        data['CovgToDt'] = 'NULL'

    # TrsFullName
    if data['TrsFullName'] != '':
        if data['TrsLName'] != '' or data['TrsFName'] != '' or data['TrsMName'] != '' or data['TrsPfx'] != '' or data[
            'TrsSfx'] != '':
            AddEntryToErrorLog('Treasurer full name (' + data[
                'TrsFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            treas = parse_full_name(data['TrsFullName'], namedelim)
            data['TrsLName'] = treas[0]
            data['TrsFName'] = treas[1]
            data['TrsMName'] = treas[2]
            data['TrsPfx'] = treas[3]
            data['TrsSfx'] = treas[4]
        else:
            data['TrsLName'] = data['TrsFullName']

    # TrsLName
    data['TrsLName'] = clean_sql_text(data['TrsLName'], 'nullstring', "'")

    # TrsFName
    data['TrsFName'] = clean_sql_text(data['TrsFName'], '', "'")

    # TrsMName
    data['TrsMName'] = clean_sql_text(data['TrsMName'], '', "'")

    # TrsPfx
    data['TrsPfx'] = clean_sql_text(data['TrsPfx'], '', "'")

    # TrsSfx
    data['TrsSfx'] = clean_sql_text(data['TrsSfx'], '', "'")

    # SignDt
    data['SignDt'] = "'" + convert_to_date(data['SignDt'], dateformat, image, 'SignDt', 'Header', 0, 'F3P', '') + "'"
    if data['SignDt'] == "''":
        data['SignDt'] = 'NULL'

    # CashBegin_P_6
    data['CashBegin_P_6'] = ck_curr_val(data['CashBegin_P_6'], image, 'CashBegin_P_6', 'Header', 0)

    # TotRcpts_P_7
    data['TotRcpts_P_7'] = ck_curr_val(data['TotRcpts_P_7'], image, 'TotRcpts_P_7', 'Header', 0)

    # Subtotal_P_8
    data['Subtotal_P_8'] = ck_curr_val(data['Subtotal_P_8'], image, 'Subtotal_P_8', 'Header', 0)

    # TotDisb_P_9
    data['TotDisb_P_9'] = ck_curr_val(data['TotDisb_P_9'], image, 'TotDisb_P_9', 'Header', 0)

    # CashClose_P_10
    data['CashClose_P_10'] = ck_curr_val(data['CashClose_P_10'], image, 'CashClose_P_10', 'Header', 0)

    # DebtsTo_P_11
    data['DebtsTo_P_11'] = ck_curr_val(data['DebtsTo_P_11'], image, 'DebtsTo_P_11', 'Header', 0)

    # DebtsBy_P_12
    data['DebtsBy_P_12'] = ck_curr_val(data['DebtsBy_P_12'], image, 'DebtsBy_P_12', 'Header', 0)

    # LmtdExps_P_13
    data['LmtdExps_P_13'] = ck_curr_val(data['LmtdExps_P_13'], image, 'LmtdExps_P_13', 'Header', 0)

    # NetConts_P_14
    data['NetConts_P_14'] = ck_curr_val(data['NetConts_P_14'], image, 'NetConts_P_14', 'Header', 0)

    # NetOpExps_P_15
    data['NetOpExps_P_15'] = ck_curr_val(data['NetOpExps_P_15'], image, 'NetOpExps_P_15', 'Header', 0)

    # FedFnds_P_16
    data['FedFnds_P_16'] = ck_curr_val(data['FedFnds_P_16'], image, 'FedFnds_P_16', 'Header', 0)

    # IndContsItem_P_17a1
    data['IndContsItem_P_17a1'] = ck_curr_val(data['IndContsItem_P_17a1'], image, 'IndContsItem_P_17a1', 'Header', 0)

    # IndContsUnitem_P_17a2
    data['IndContsUnitem_P_17a2'] = ck_curr_val(data['IndContsUnitem_P_17a2'], image, 'IndContsUnitem_P_17a2', 'Header',
                                                0)

    # IndContsTot_P_17a3
    data['IndContsTot_P_17a3'] = ck_curr_val(data['IndContsTot_P_17a3'], image, 'IndContsTot_P_17a3', 'Header', 0)

    # PolPtyCommConts_P_17b
    data['PolPtyCommConts_P_17b'] = ck_curr_val(data['PolPtyCommConts_P_17b'], image, 'PolPtyCommConts_P_17b', 'Header',
                                                0)

    # OthPolCommConts_P_17c
    data['OthPolCommConts_P_17c'] = ck_curr_val(data['OthPolCommConts_P_17c'], image, 'OthPolCommConts_P_17c', 'Header',
                                                0)

    # CandConts_P_17d
    data['CandConts_P_17d'] = ck_curr_val(data['CandConts_P_17d'], image, 'CandConts_P_17d', 'Header', 0)

    # TotConts_P_17e
    data['TotConts_P_17e'] = ck_curr_val(data['TotConts_P_17e'], image, 'TotConts_P_17e', 'Header', 0)

    # TranFmPtyComms_P_18
    data['TranFmPtyComms_P_18'] = ck_curr_val(data['TranFmPtyComms_P_18'], image, 'TranFmPtyComms_P_18', 'Header', 0)

    # CandLoans_P_19a
    data['CandLoans_P_19a'] = ck_curr_val(data['CandLoans_P_19a'], image, 'CandLoans_P_19a', 'Header', 0)

    # OthLoans_P_19b
    data['OthLoans_P_19b'] = ck_curr_val(data['OthLoans_P_19b'], image, 'OthLoans_P_19b', 'Header', 0)

    # TotLoans_P_19c
    data['TotLoans_P_19c'] = ck_curr_val(data['TotLoans_P_19c'], image, 'TotLoans_P_19c', 'Header', 0)

    # OptgOffsets_P_20a
    data['OptgOffsets_P_20a'] = ck_curr_val(data['OptgOffsets_P_20a'], image, 'OptgOffsets_P_20a', 'Header', 0)

    # FndrsgOffsets_P_20b
    data['FndrsgOffsets_P_20b'] = ck_curr_val(data['FndrsgOffsets_P_20b'], image, 'FndrsgOffsets_P_20b', 'Header', 0)

    # LegalAcctgOffsets_P_20c
    data['LegalAcctgOffsets_P_20c'] = ck_curr_val(data['LegalAcctgOffsets_P_20c'], image, 'LegalAcctgOffsets_P_20c',
                                                  'Header', 0)

    # TotOffsets_P_20d
    data['TotOffsets_P_20d'] = ck_curr_val(data['TotOffsets_P_20d'], image, 'TotOffsets_P_20d', 'Header', 0)

    # OthRcpts_P_21
    data['OthRcpts_P_21'] = ck_curr_val(data['OthRcpts_P_21'], image, 'OthRcpts_P_21', 'Header', 0)

    # TotRcpts_P_22
    data['TotRcpts_P_22'] = ck_curr_val(data['TotRcpts_P_22'], image, 'TotRcpts_P_22', 'Header', 0)

    # OpExps_P_23
    data['OpExps_P_23'] = ck_curr_val(data['OpExps_P_23'], image, 'OpExps_P_23', 'Header', 0)

    # TranToOthAuthComms_P_24
    data['TranToOthAuthComms_P_24'] = ck_curr_val(data['TranToOthAuthComms_P_24'], image, 'TranToOthAuthComms_P_24',
                                                  'Header', 0)

    # FndrsgDisb_P_25
    data['FndrsgDisb_P_25'] = ck_curr_val(data['FndrsgDisb_P_25'], image, 'FndrsgDisb_P_25', 'Header', 0)

    # LegalAcctgDisb_P_26
    data['LegalAcctgDisb_P_26'] = ck_curr_val(data['LegalAcctgDisb_P_26'], image, 'LegalAcctgDisb_P_26', 'Header', 0)

    # CandLoansRepaid_P_27a
    data['CandLoansRepaid_P_27a'] = ck_curr_val(data['CandLoansRepaid_P_27a'], image, 'CandLoansRepaid_P_27a', 'Header',
                                                0)

    # OthLoansRepaid_P_27b
    data['OthLoansRepaid_P_27b'] = ck_curr_val(data['OthLoansRepaid_P_27b'], image, 'OthLoansRepaid_P_27b', 'Header', 0)

    # TotLoansRepaid_P_27c
    data['TotLoansRepaid_P_27c'] = ck_curr_val(data['TotLoansRepaid_P_27c'], image, 'TotLoansRepaid_P_27c', 'Header', 0)

    # RefundsInd_P_28a
    data['RefundsInd_P_28a'] = ck_curr_val(data['RefundsInd_P_28a'], image, 'RefundsInd_P_28a', 'Header', 0)

    # RefundsPolPtyComms_P_28b
    data['RefundsPolPtyComms_P_28b'] = ck_curr_val(data['RefundsPolPtyComms_P_28b'], image, 'RefundsPolPtyComms_P_28b',
                                                   'Header', 0)

    # RefundsOthPolComms_P_28c
    data['RefundsOthPolComms_P_28c'] = ck_curr_val(data['RefundsOthPolComms_P_28c'], image, 'RefundsOthPolComms_P_28c',
                                                   'Header', 0)

    # TotRefunds_P_28d
    data['TotRefunds_P_28d'] = ck_curr_val(data['TotRefunds_P_28d'], image, 'TotRefunds_P_28d', 'Header', 0)

    # OthDisb_P_29
    data['OthDisb_P_29'] = ck_curr_val(data['OthDisb_P_29'], image, 'OthDisb_P_29', 'Header', 0)

    # TotDisb_P_30
    data['TotDisb_P_30'] = ck_curr_val(data['TotDisb_P_30'], image, 'TotDisb_P_30', 'Header', 0)

    # ItmsToBeLiq_P_31
    data['ItmsToBeLiq_P_31'] = ck_curr_val(data['ItmsToBeLiq_P_31'], image, 'ItmsToBeLiq_P_31', 'Header', 0)

    # Alabama_P
    data['Alabama_P'] = ck_curr_val(data['Alabama_P'], image, 'Alabama_P', 'Header', 0)

    # Alaska_P
    data['Alaska_P'] = ck_curr_val(data['Alaska_P'], image, 'Alaska_P', 'Header', 0)

    # Arizona_P
    data['Arizona_P'] = ck_curr_val(data['Arizona_P'], image, 'Arizona_P', 'Header', 0)

    # Arkansas_P
    data['Arkansas_P'] = ck_curr_val(data['Arkansas_P'], image, 'Arkansas_P', 'Header', 0)

    # California_P
    data['California_P'] = ck_curr_val(data['California_P'], image, 'California_P', 'Header', 0)

    # Colorado_P
    data['Colorado_P'] = ck_curr_val(data['Colorado_P'], image, 'Colorado_P', 'Header', 0)

    # Connecticut_P
    data['Connecticut_P'] = ck_curr_val(data['Connecticut_P'], image, 'Connecticut_P', 'Header', 0)

    # Delaware_P
    data['Delaware_P'] = ck_curr_val(data['Delaware_P'], image, 'Delaware_P', 'Header', 0)

    # DistCol_P
    data['DistCol_P'] = ck_curr_val(data['DistCol_P'], image, 'DistCol_P', 'Header', 0)

    # Florida_P
    data['Florida_P'] = ck_curr_val(data['Florida_P'], image, 'Florida_P', 'Header', 0)

    # Georgia_P
    data['Georgia_P'] = ck_curr_val(data['Georgia_P'], image, 'Georgia_P', 'Header', 0)

    # Hawaii_P
    data['Hawaii_P'] = ck_curr_val(data['Hawaii_P'], image, 'Hawaii_P', 'Header', 0)

    # Idaho_P
    data['Idaho_P'] = ck_curr_val(data['Idaho_P'], image, 'Idaho_P', 'Header', 0)

    # Illinois_P
    data['Illinois_P'] = ck_curr_val(data['Illinois_P'], image, 'Illinois_P', 'Header', 0)

    # Indiana_P
    data['Indiana_P'] = ck_curr_val(data['Indiana_P'], image, 'Indiana_P', 'Header', 0)

    # Iowa_P
    data['Iowa_P'] = ck_curr_val(data['Iowa_P'], image, 'Iowa_P', 'Header', 0)

    # Kansas_P
    data['Kansas_P'] = ck_curr_val(data['Kansas_P'], image, 'Kansas_P', 'Header', 0)

    # Kentucky_P
    data['Kentucky_P'] = ck_curr_val(data['Kentucky_P'], image, 'Kentucky_P', 'Header', 0)

    # Louisiana_P
    data['Louisiana_P'] = ck_curr_val(data['Louisiana_P'], image, 'Louisiana_P', 'Header', 0)

    # Maine_P
    data['Maine_P'] = ck_curr_val(data['Maine_P'], image, 'Maine_P', 'Header', 0)

    # Maryland_P
    data['Maryland_P'] = ck_curr_val(data['Maryland_P'], image, 'Maryland_P', 'Header', 0)

    # Massachusetts_P
    data['Massachusetts_P'] = ck_curr_val(data['Massachusetts_P'], image, 'Massachusetts_P', 'Header', 0)

    # Michigan_P
    data['Michigan_P'] = ck_curr_val(data['Michigan_P'], image, 'Michigan_P', 'Header', 0)

    # Minnesota_P
    data['Minnesota_P'] = ck_curr_val(data['Minnesota_P'], image, 'Minnesota_P', 'Header', 0)

    # Mississippi_P
    data['Mississippi_P'] = ck_curr_val(data['Mississippi_P'], image, 'Mississippi_P', 'Header', 0)

    # Missouri_P
    data['Missouri_P'] = ck_curr_val(data['Missouri_P'], image, 'Missouri_P', 'Header', 0)

    # Montana_P
    data['Montana_P'] = ck_curr_val(data['Montana_P'], image, 'Montana_P', 'Header', 0)

    # Nebraska_P
    data['Nebraska_P'] = ck_curr_val(data['Nebraska_P'], image, 'Nebraska_P', 'Header', 0)

    # Nevada_P
    data['Nevada_P'] = ck_curr_val(data['Nevada_P'], image, 'Nevada_P', 'Header', 0)

    # NewHampshire_P
    data['NewHampshire_P'] = ck_curr_val(data['NewHampshire_P'], image, 'NewHampshire_P', 'Header', 0)

    # NewJersey_P
    data['NewJersey_P'] = ck_curr_val(data['NewJersey_P'], image, 'NewJersey_P', 'Header', 0)

    # NewMexico_P
    data['NewMexico_P'] = ck_curr_val(data['NewMexico_P'], image, 'NewMexico_P', 'Header', 0)

    # NewYork_P
    data['NewYork_P'] = ck_curr_val(data['NewYork_P'], image, 'NewYork_P', 'Header', 0)

    # NorthCarolina_P
    data['NorthCarolina_P'] = ck_curr_val(data['NorthCarolina_P'], image, 'NorthCarolina_P', 'Header', 0)

    # NorthDakota_P
    data['NorthDakota_P'] = ck_curr_val(data['NorthDakota_P'], image, 'NorthDakota_P', 'Header', 0)

    # Ohio_P
    data['Ohio_P'] = ck_curr_val(data['Ohio_P'], image, 'Ohio_P', 'Header', 0)

    # Oklahoma_P
    data['Oklahoma_P'] = ck_curr_val(data['Oklahoma_P'], image, 'Oklahoma_P', 'Header', 0)

    # Oregon_P
    data['Oregon_P'] = ck_curr_val(data['Oregon_P'], image, 'Oregon_P', 'Header', 0)

    # Pennsylvania_P
    data['Pennsylvania_P'] = ck_curr_val(data['Pennsylvania_P'], image, 'Pennsylvania_P', 'Header', 0)

    # RhodeIsland_P
    data['RhodeIsland_P'] = ck_curr_val(data['RhodeIsland_P'], image, 'RhodeIsland_P', 'Header', 0)

    # SouthCarolina_P
    data['SouthCarolina_P'] = ck_curr_val(data['SouthCarolina_P'], image, 'SouthCarolina_P', 'Header', 0)

    # SouthDakota_P
    data['SouthDakota_P'] = ck_curr_val(data['SouthDakota_P'], image, 'SouthDakota_P', 'Header', 0)

    # Tennessee_P
    data['Tennessee_P'] = ck_curr_val(data['Tennessee_P'], image, 'Tennessee_P', 'Header', 0)

    # Texas_P
    data['Texas_P'] = ck_curr_val(data['Texas_P'], image, 'Texas_P', 'Header', 0)

    # Utah_P
    data['Utah_P'] = ck_curr_val(data['Utah_P'], image, 'Utah_P', 'Header', 0)

    # Vermont_P
    data['Vermont_P'] = ck_curr_val(data['Vermont_P'], image, 'Vermont_P', 'Header', 0)

    # Virginia_P
    data['Virginia_P'] = ck_curr_val(data['Virginia_P'], image, 'Virginia_P', 'Header', 0)

    # Washington_P
    data['Washington_P'] = ck_curr_val(data['Washington_P'], image, 'Washington_P', 'Header', 0)

    # WestVirginia_P
    data['WestVirginia_P'] = ck_curr_val(data['WestVirginia_P'], image, 'WestVirginia_P', 'Header', 0)

    # Wisconsin_P
    data['Wisconsin_P'] = ck_curr_val(data['Wisconsin_P'], image, 'Wisconsin_P', 'Header', 0)

    # Wyoming_P
    data['Wyoming_P'] = ck_curr_val(data['Wyoming_P'], image, 'Wyoming_P', 'Header', 0)

    # PuertoRico_P
    data['PuertoRico_P'] = ck_curr_val(data['PuertoRico_P'], image, 'PuertoRico_P', 'Header', 0)

    # Guam_P
    data['Guam_P'] = ck_curr_val(data['Guam_P'], image, 'Guam_P', 'Header', 0)

    # VirginIslands_P
    data['VirginIslands_P'] = ck_curr_val(data['VirginIslands_P'], image, 'VirginIslands_P', 'Header', 0)

    # TotAllocs_P
    data['TotAllocs_P'] = ck_curr_val(data['TotAllocs_P'], image, 'TotAllocs_P', 'Header', 0)

    # FedFnds_T_16
    data['FedFnds_T_16'] = ck_curr_val(data['FedFnds_T_16'], image, 'FedFnds_T_16', 'Header', 0)

    # IndContsItem_T_17a1
    data['IndContsItem_T_17a1'] = ck_curr_val(data['IndContsItem_T_17a1'], image, 'IndContsItem_T_17a1', 'Header', 0)

    # IndContsUnitem_T_17a2
    data['IndContsUnitem_T_17a2'] = ck_curr_val(data['IndContsUnitem_T_17a2'], image, 'IndContsUnitem_T_17a2', 'Header',
                                                0)

    # IndContsTot_T_17a3
    data['IndContsTot_T_17a3'] = ck_curr_val(data['IndContsTot_T_17a3'], image, 'IndContsTot_T_17a3', 'Header', 0)

    # PolPtyCommConts_T_17b
    data['PolPtyCommConts_T_17b'] = ck_curr_val(data['PolPtyCommConts_T_17b'], image, 'PolPtyCommConts_T_17b', 'Header',
                                                0)

    # OthPolCommConts_T_17c
    data['OthPolCommConts_T_17c'] = ck_curr_val(data['OthPolCommConts_T_17c'], image, 'OthPolCommConts_T_17c', 'Header',
                                                0)

    # CandConts_T_17d
    data['CandConts_T_17d'] = ck_curr_val(data['CandConts_T_17d'], image, 'CandConts_T_17d', 'Header', 0)

    # TotConts_T_17e
    data['TotConts_T_17e'] = ck_curr_val(data['TotConts_T_17e'], image, 'TotConts_T_17e', 'Header', 0)

    # TranFmPtyComms_T_18
    data['TranFmPtyComms_T_18'] = ck_curr_val(data['TranFmPtyComms_T_18'], image, 'TranFmPtyComms_T_18', 'Header', 0)

    # CandLoans_T_19a
    data['CandLoans_T_19a'] = ck_curr_val(data['CandLoans_T_19a'], image, 'CandLoans_T_19a', 'Header', 0)

    # OthLoans_T_19b
    data['OthLoans_T_19b'] = ck_curr_val(data['OthLoans_T_19b'], image, 'OthLoans_T_19b', 'Header', 0)

    # TotLoans_T_19c
    data['TotLoans_T_19c'] = ck_curr_val(data['TotLoans_T_19c'], image, 'TotLoans_T_19c', 'Header', 0)

    # OptgOffsets_T_20a
    data['OptgOffsets_T_20a'] = ck_curr_val(data['OptgOffsets_T_20a'], image, 'OptgOffsets_T_20a', 'Header', 0)

    # FndrsgOffsets_T_20b
    data['FndrsgOffsets_T_20b'] = ck_curr_val(data['FndrsgOffsets_T_20b'], image, 'FndrsgOffsets_T_20b', 'Header', 0)

    # LegalAcctgOffsets_T_20c
    data['LegalAcctgOffsets_T_20c'] = ck_curr_val(data['LegalAcctgOffsets_T_20c'], image, 'LegalAcctgOffsets_T_20c',
                                                  'Header', 0)

    # TotOffsets_T_20d
    data['TotOffsets_T_20d'] = ck_curr_val(data['TotOffsets_T_20d'], image, 'TotOffsets_T_20d', 'Header', 0)

    # OthRcpts_T_21
    data['OthRcpts_T_21'] = ck_curr_val(data['OthRcpts_T_21'], image, 'OthRcpts_T_21', 'Header', 0)

    # TotRcpts_T_22
    data['TotRcpts_T_22'] = ck_curr_val(data['TotRcpts_T_22'], image, 'TotRcpts_T_22', 'Header', 0)

    # OpExps_T_23
    data['OpExps_T_23'] = ck_curr_val(data['OpExps_T_23'], image, 'OpExps_T_23', 'Header', 0)

    # TranToOthAuthComms_T_24
    data['TranToOthAuthComms_T_24'] = ck_curr_val(data['TranToOthAuthComms_T_24'], image, 'TranToOthAuthComms_T_24',
                                                  'Header', 0)

    # FndrsgDisb_T_25
    data['FndrsgDisb_T_25'] = ck_curr_val(data['FndrsgDisb_T_25'], image, 'FndrsgDisb_T_25', 'Header', 0)

    # LegalAcctgDisb_T_26
    data['LegalAcctgDisb_T_26'] = ck_curr_val(data['LegalAcctgDisb_T_26'], image, 'LegalAcctgDisb_T_26', 'Header', 0)

    # CandLoansRepaid_T_27a
    data['CandLoansRepaid_T_27a'] = ck_curr_val(data['CandLoansRepaid_T_27a'], image, 'CandLoansRepaid_T_27a', 'Header',
                                                0)

    # OthLoansRepaid_T_27b
    data['OthLoansRepaid_T_27b'] = ck_curr_val(data['OthLoansRepaid_T_27b'], image, 'OthLoansRepaid_T_27b', 'Header', 0)

    # TotLoansRepaid_T_27c
    data['TotLoansRepaid_T_27c'] = ck_curr_val(data['TotLoansRepaid_T_27c'], image, 'TotLoansRepaid_T_27c', 'Header', 0)

    # RefundsInd_T_28a
    data['RefundsInd_T_28a'] = ck_curr_val(data['RefundsInd_T_28a'], image, 'RefundsInd_T_28a', 'Header', 0)

    # RefundsPolPtyComms_T_28b
    data['RefundsPolPtyComms_T_28b'] = ck_curr_val(data['RefundsPolPtyComms_T_28b'], image, 'RefundsPolPtyComms_T_28b',
                                                   'Header', 0)

    # RefundsOthPolComms_T_28c
    data['RefundsOthPolComms_T_28c'] = ck_curr_val(data['RefundsOthPolComms_T_28c'], image, 'RefundsOthPolComms_T_28c',
                                                   'Header', 0)

    # TotRefunds_T_28d
    data['TotRefunds_T_28d'] = ck_curr_val(data['TotRefunds_T_28d'], image, 'TotRefunds_T_28d', 'Header', 0)

    # OthDisb_T_29
    data['OthDisb_T_29'] = ck_curr_val(data['OthDisb_T_29'], image, 'OthDisb_T_29', 'Header', 0)

    # TotDisb_T_30
    data['TotDisb_T_30'] = ck_curr_val(data['TotDisb_T_30'], image, 'TotDisb_T_30', 'Header', 0)

    # Alabama_T
    data['Alabama_T'] = ck_curr_val(data['Alabama_T'], image, 'Alabama_T', 'Header', 0)

    # Alaska_T
    data['Alaska_T'] = ck_curr_val(data['Alaska_T'], image, 'Alaska_T', 'Header', 0)

    # Arizona_T
    data['Arizona_T'] = ck_curr_val(data['Arizona_T'], image, 'Arizona_T', 'Header', 0)

    # Arkansas_T
    data['Arkansas_T'] = ck_curr_val(data['Arkansas_T'], image, 'Arkansas_T', 'Header', 0)

    # California_T
    data['California_T'] = ck_curr_val(data['California_T'], image, 'California_T', 'Header', 0)

    # Colorado_T
    data['Colorado_T'] = ck_curr_val(data['Colorado_T'], image, 'Colorado_T', 'Header', 0)

    # Connecticut_T
    data['Connecticut_T'] = ck_curr_val(data['Connecticut_T'], image, 'Connecticut_T', 'Header', 0)

    # Delaware_T
    data['Delaware_T'] = ck_curr_val(data['Delaware_T'], image, 'Delaware_T', 'Header', 0)

    # DistCol_T
    data['DistCol_T'] = ck_curr_val(data['DistCol_T'], image, 'DistCol_T', 'Header', 0)

    # Florida_T
    data['Florida_T'] = ck_curr_val(data['Florida_T'], image, 'Florida_T', 'Header', 0)

    # Georgia_T
    data['Georgia_T'] = ck_curr_val(data['Georgia_T'], image, 'Georgia_T', 'Header', 0)

    # Hawaii_T
    data['Hawaii_T'] = ck_curr_val(data['Hawaii_T'], image, 'Hawaii_T', 'Header', 0)

    # Idaho_T
    data['Idaho_T'] = ck_curr_val(data['Idaho_T'], image, 'Idaho_T', 'Header', 0)

    # Illinois_T
    data['Illinois_T'] = ck_curr_val(data['Illinois_T'], image, 'Illinois_T', 'Header', 0)

    # Indiana_T
    data['Indiana_T'] = ck_curr_val(data['Indiana_T'], image, 'Indiana_T', 'Header', 0)

    # Iowa_T
    data['Iowa_T'] = ck_curr_val(data['Iowa_T'], image, 'Iowa_T', 'Header', 0)

    # Kansas_T
    data['Kansas_T'] = ck_curr_val(data['Kansas_T'], image, 'Kansas_T', 'Header', 0)

    # Kentucky_T
    data['Kentucky_T'] = ck_curr_val(data['Kentucky_T'], image, 'Kentucky_T', 'Header', 0)

    # Louisiana_T
    data['Louisiana_T'] = ck_curr_val(data['Louisiana_T'], image, 'Louisiana_T', 'Header', 0)

    # Maine_T
    data['Maine_T'] = ck_curr_val(data['Maine_T'], image, 'Maine_T', 'Header', 0)

    # Maryland_T
    data['Maryland_T'] = ck_curr_val(data['Maryland_T'], image, 'Maryland_T', 'Header', 0)

    # Massachusetts_T
    data['Massachusetts_T'] = ck_curr_val(data['Massachusetts_T'], image, 'Massachusetts_T', 'Header', 0)

    # Michigan_T
    data['Michigan_T'] = ck_curr_val(data['Michigan_T'], image, 'Michigan_T', 'Header', 0)

    # Minnesota_T
    data['Minnesota_T'] = ck_curr_val(data['Minnesota_T'], image, 'Minnesota_T', 'Header', 0)

    # Mississippi_T
    data['Mississippi_T'] = ck_curr_val(data['Mississippi_T'], image, 'Mississippi_T', 'Header', 0)

    # Missouri_T
    data['Missouri_T'] = ck_curr_val(data['Missouri_T'], image, 'Missouri_T', 'Header', 0)

    # Montana_T
    data['Montana_T'] = ck_curr_val(data['Montana_T'], image, 'Montana_T', 'Header', 0)

    # Nebraska_T
    data['Nebraska_T'] = ck_curr_val(data['Nebraska_T'], image, 'Nebraska_T', 'Header', 0)

    # Nevada_T
    data['Nevada_T'] = ck_curr_val(data['Nevada_T'], image, 'Nevada_T', 'Header', 0)

    # NewHampshire_T
    data['NewHampshire_T'] = ck_curr_val(data['NewHampshire_T'], image, 'NewHampshire_T', 'Header', 0)

    # NewJersey_T
    data['NewJersey_T'] = ck_curr_val(data['NewJersey_T'], image, 'NewJersey_T', 'Header', 0)

    # NewMexico_T
    data['NewMexico_T'] = ck_curr_val(data['NewMexico_T'], image, 'NewMexico_T', 'Header', 0)

    # NewYork_T
    data['NewYork_T'] = ck_curr_val(data['NewYork_T'], image, 'NewYork_T', 'Header', 0)

    # NorthCarolina_T
    data['NorthCarolina_T'] = ck_curr_val(data['NorthCarolina_T'], image, 'NorthCarolina_T', 'Header', 0)

    # NorthDakota_T
    data['NorthDakota_T'] = ck_curr_val(data['NorthDakota_T'], image, 'NorthDakota_T', 'Header', 0)

    # Ohio_T
    data['Ohio_T'] = ck_curr_val(data['Ohio_T'], image, 'Ohio_T', 'Header', 0)

    # Oklahoma_T
    data['Oklahoma_T'] = ck_curr_val(data['Oklahoma_T'], image, 'Oklahoma_T', 'Header', 0)

    # Oregon_T
    data['Oregon_T'] = ck_curr_val(data['Oregon_T'], image, 'Oregon_T', 'Header', 0)

    # Pennsylvania_T
    data['Pennsylvania_T'] = ck_curr_val(data['Pennsylvania_T'], image, 'Pennsylvania_T', 'Header', 0)

    # RhodeIsland_T
    data['RhodeIsland_T'] = ck_curr_val(data['RhodeIsland_T'], image, 'RhodeIsland_T', 'Header', 0)

    # SouthCarolina_T
    data['SouthCarolina_T'] = ck_curr_val(data['SouthCarolina_T'], image, 'SouthCarolina_T', 'Header', 0)

    # SouthDakota_T
    data['SouthDakota_T'] = ck_curr_val(data['SouthDakota_T'], image, 'SouthDakota_T', 'Header', 0)

    # Tennessee_T
    data['Tennessee_T'] = ck_curr_val(data['Tennessee_T'], image, 'Tennessee_T', 'Header', 0)

    # Texas_T
    data['Texas_T'] = ck_curr_val(data['Texas_T'], image, 'Texas_T', 'Header', 0)

    # Utah_T
    data['Utah_T'] = ck_curr_val(data['Utah_T'], image, 'Utah_T', 'Header', 0)

    # Vermont_T
    data['Vermont_T'] = ck_curr_val(data['Vermont_T'], image, 'Vermont_T', 'Header', 0)

    # Virginia_T
    data['Virginia_T'] = ck_curr_val(data['Virginia_T'], image, 'Virginia_T', 'Header', 0)

    # Washington_T
    data['Washington_T'] = ck_curr_val(data['Washington_T'], image, 'Washington_T', 'Header', 0)

    # WestVirginia_T
    data['WestVirginia_T'] = ck_curr_val(data['WestVirginia_T'], image, 'WestVirginia_T', 'Header', 0)

    # Wisconsin_T
    data['Wisconsin_T'] = ck_curr_val(data['Wisconsin_T'], image, 'Wisconsin_T', 'Header', 0)

    # Wyoming_T
    data['Wyoming_T'] = ck_curr_val(data['Wyoming_T'], image, 'Wyoming_T', 'Header', 0)

    # PuertoRico_T
    data['PuertoRico_T'] = ck_curr_val(data['PuertoRico_T'], image, 'PuertoRico_T', 'Header', 0)

    # Guam_T
    data['Guam_T'] = ck_curr_val(data['Guam_T'], image, 'Guam_T', 'Header', 0)

    # VirginIslands_T
    data['VirginIslands_T'] = ck_curr_val(data['VirginIslands_T'], image, 'VirginIslands_T', 'Header', 0)

    # TotAllocs_T
    data['TotAllocs_T'] = ck_curr_val(data['TotAllocs_T'], image, 'TotAllocs_T', 'Header', 0)

    return data


def check_rpt_hdrs_f3x(image, data, namedelim='', dateformat='CCYYMMDD'):
    # FormTp
    data['FormTp'] = clean_sql_text(data['FormTp'], 'nullstring', "'")

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'], 'nullstring', "'")

    # CommNm
    data['CommNm'] = clean_sql_text(data['CommNm'], 'nullstring', "'")

    # AddrChg
    data['AddrChg'] = convert_to_bit(clean_sql_text(data['AddrChg']))

    # Addr1
    data['Addr1'] = clean_sql_text(data['Addr1'], 'nullstring', "'")

    # Addr2
    data['Addr2'] = clean_sql_text(data['Addr2'], '', "'")

    # City
    data['City'] = clean_sql_text(data['City'], 'nullstring', "'")

    # StAbbr
    data['StAbbr'] = clean_sql_text(data['StAbbr'], 'nullstring', "'")

    # Zip
    data['Zip'] = clean_sql_text(data['Zip'], 'nullstring', "'")

    # RptCd
    data['RptCd'] = clean_sql_text(data['RptCd'], 'nullstring', "'")

    # ElecCd
    data['ElecCd'] = clean_sql_text(data['ElecCd'], '', "'")

    # ElecDt
    data['ElecDt'] = "'" + convert_to_date(data['ElecDt'], dateformat, image, 'ElecDt', 'Header', 0, 'F3X', '') + "'"
    if data['ElecDt'] == "''":
        data['ElecDt'] = 'NULL'

    # ElecSt
    data['ElecSt'] = clean_sql_text(data['ElecSt'], 'nullstring', "'")

    # CovgFmDt
    data['CovgFmDt'] = "'" + convert_to_date(data['CovgFmDt'], dateformat, image, 'CovgFmDt', 'Header', 0, 'F3X',
                                             '') + "'"
    if data['CovgFmDt'] == "''":
        data['CovgFmDt'] = 'NULL'

    # CovgToDt
    data['CovgToDt'] = "'" + convert_to_date(data['CovgToDt'], dateformat, image, 'CovgToDt', 'Header', 0, 'F3X',
                                             '') + "'"
    if data['CovgToDt'] == "''":
        data['CovgToDt'] = 'NULL'

    # flgQualComm
    data['flgQualComm'] = convert_to_bit(clean_sql_text(data['flgQualComm'], '', "'"))

    # TrsFullName
    if data['TrsFullName'] != '':
        if data['TrsLName'] != '' or data['TrsFName'] != '' or data['TrsMName'] != '' or data['TrsPfx'] != '' or data[
            'TrsSfx'] != '':
            AddEntryToErrorLog('Treasurer full name (' + data[
                'TrsFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            treas = parse_full_name(data['TrsFullName'], namedelim)
            data['TrsLName'] = treas[0]
            data['TrsFName'] = treas[1]
            data['TrsMName'] = treas[2]
            data['TrsPfx'] = treas[3]
            data['TrsSfx'] = treas[4]
        else:
            data['TrsLName'] = data['TrsFullName']

    # TrsLName
    data['TrsLName'] = clean_sql_text(data['TrsLName'], 'nullstring', "'")

    # TrsFName
    data['TrsFName'] = clean_sql_text(data['TrsFName'], '', "'")

    # TrsMName
    data['TrsMName'] = clean_sql_text(data['TrsMName'], '', "'")

    # TrsPfx
    data['TrsPfx'] = clean_sql_text(data['TrsPfx'], '', "'")

    # TrsSfx
    data['TrsSfx'] = clean_sql_text(data['TrsSfx'], '', "'")

    # SignDt
    data['SignDt'] = "'" + convert_to_date(data['SignDt'], dateformat, image, 'SignDt', 'Header', 0, 'F3X', '') + "'"
    if data['SignDt'] == "''":
        data['SignDt'] = 'NULL'

    # CashBegin_P_6b
    data['CashBegin_P_6b'] = ck_curr_val(data['CashBegin_P_6b'], image, 'CashBegin_P_6b', 'Header', 0)

    # TotRcpts_P_6c
    data['TotRcpts_P_6c'] = ck_curr_val(data['TotRcpts_P_6c'], image, 'TotRcpts_P_6c', 'Header', 0)

    # Subtotal_P_6d
    data['Subtotal_P_6d'] = ck_curr_val(data['Subtotal_P_6d'], image, 'Subtotal_P_6d', 'Header', 0)

    # TotDisb_P_7
    data['TotDisb_P_7'] = ck_curr_val(data['TotDisb_P_7'], image, 'TotDisb_P_7', 'Header', 0)

    # CashClose_P_8
    data['CashClose_P_8'] = ck_curr_val(data['CashClose_P_8'], image, 'CashClose_P_8', 'Header', 0)

    # DebtsTo_P_9
    data['DebtsTo_P_9'] = ck_curr_val(data['DebtsTo_P_9'], image, 'DebtsTo_P_9', 'Header', 0)

    # DebtsBy_P_10
    data['DebtsBy_P_10'] = ck_curr_val(data['DebtsBy_P_10'], image, 'DebtsBy_P_10', 'Header', 0)

    # IndContsItem_P_11a1
    data['IndContsItem_P_11a1'] = ck_curr_val(data['IndContsItem_P_11a1'], image, 'IndContsItem_P_11a1', 'Header', 0)

    # IndContsUnitem_P_11a2
    data['IndContsUnitem_P_11a2'] = ck_curr_val(data['IndContsUnitem_P_11a2'], image, 'IndContsUnitem_P_11a2', 'Header',
                                                0)

    # IndContsTot_P_11a3
    data['IndContsTot_P_11a3'] = ck_curr_val(data['IndContsTot_P_11a3'], image, 'IndContsTot_P_11a3', 'Header', 0)

    # PolPtyCommConts_P_11b
    data['PolPtyCommConts_P_11b'] = ck_curr_val(data['PolPtyCommConts_P_11b'], image, 'PolPtyCommConts_P_11b', 'Header',
                                                0)

    # OthPolCommConts_P_11c
    data['OthPolCommConts_P_11c'] = ck_curr_val(data['OthPolCommConts_P_11c'], image, 'OthPolCommConts_P_11c', 'Header',
                                                0)

    # TotConts_P_11d
    data['TotConts_P_11d'] = ck_curr_val(data['TotConts_P_11d'], image, 'TotConts_P_11d', 'Header', 0)

    # TranFmPtyComms_P_12
    data['TranFmPtyComms_P_12'] = ck_curr_val(data['TranFmPtyComms_P_12'], image, 'TranFmPtyComms_P_12', 'Header', 0)

    # AllLoansRcvd_P_13
    data['AllLoansRcvd_P_13'] = ck_curr_val(data['AllLoansRcvd_P_13'], image, 'AllLoansRcvd_P_13', 'Header', 0)

    # LoanPymtsRcvd_P_14
    data['LoanPymtsRcvd_P_14'] = ck_curr_val(data['LoanPymtsRcvd_P_14'], image, 'LoanPymtsRcvd_P_14', 'Header', 0)

    # RefundOffsets_P_15
    data['RefundOffsets_P_15'] = ck_curr_val(data['RefundOffsets_P_15'], image, 'RefundOffsets_P_15', 'Header', 0)

    # RefundsFedConts_P_16
    data['RefundsFedConts_P_16'] = ck_curr_val(data['RefundsFedConts_P_16'], image, 'RefundsFedConts_P_16', 'Header', 0)

    # OthFedRcptsDvds_P_17
    data['OthFedRcptsDvds_P_17'] = ck_curr_val(data['OthFedRcptsDvds_P_17'], image, 'OthFedRcptsDvds_P_17', 'Header', 0)

    # TranFmNonFedAcctH3_P_18a
    data['TranFmNonFedAcctH3_P_18a'] = ck_curr_val(data['TranFmNonFedAcctH3_P_18a'], image, 'TranFmNonFedAcctH3_P_18a',
                                                   'Header', 0)

    # TranFmNonFedAcctH5_P_18b
    data['TranFmNonFedAcctH5_P_18b'] = ck_curr_val(data['TranFmNonFedAcctH5_P_18b'], image, 'TranFmNonFedAcctH5_P_18b',
                                                   'Header', 0)

    # TotNonFedTrans_P_18c
    data['TotNonFedTrans_P_18c'] = ck_curr_val(data['TotNonFedTrans_P_18c'], image, 'TotNonFedTrans_P_18c', 'Header', 0)

    # TotRcpts_P_19
    data['TotRcpts_P_19'] = ck_curr_val(data['TotRcpts_P_19'], image, 'TotRcpts_P_19', 'Header', 0)

    # TotFedRcpts_P_20
    data['TotFedRcpts_P_20'] = ck_curr_val(data['TotFedRcpts_P_20'], image, 'TotFedRcpts_P_20', 'Header', 0)

    # OpExpsFedShr_P_21a1
    data['OpExpsFedShr_P_21a1'] = ck_curr_val(data['OpExpsFedShr_P_21a1'], image, 'OpExpsFedShr_P_21a1', 'Header', 0)

    # OpExpsNonFedShr_P_21a2
    data['OpExpsNonFedShr_P_21a2'] = ck_curr_val(data['OpExpsNonFedShr_P_21a2'], image, 'OpExpsNonFedShr_P_21a2',
                                                 'Header', 0)

    # OpExpsOthFed_P_21b
    data['OpExpsOthFed_P_21b'] = ck_curr_val(data['OpExpsOthFed_P_21b'], image, 'OpExpsOthFed_P_21b', 'Header', 0)

    # TotOpExps_P_21c
    data['TotOpExps_P_21c'] = ck_curr_val(data['TotOpExps_P_21c'], image, 'TotOpExps_P_21c', 'Header', 0)

    # TranToPtyComms_P_22
    data['TranToPtyComms_P_22'] = ck_curr_val(data['TranToPtyComms_P_22'], image, 'TranToPtyComms_P_22', 'Header', 0)

    # ContsToFedCandsComms_P_23
    data['ContsToFedCandsComms_P_23'] = ck_curr_val(data['ContsToFedCandsComms_P_23'], image,
                                                    'ContsToFedCandsComms_P_23', 'Header', 0)

    # IndtExps_P_24
    data['IndtExps_P_24'] = ck_curr_val(data['IndtExps_P_24'], image, 'IndtExps_P_24', 'Header', 0)

    # CoordExpsByPtyComms_P_25
    data['CoordExpsByPtyComms_P_25'] = ck_curr_val(data['CoordExpsByPtyComms_P_25'], image, 'CoordExpsByPtyComms_P_25',
                                                   'Header', 0)

    # LoansRepaid_P_26
    data['LoansRepaid_P_26'] = ck_curr_val(data['LoansRepaid_P_26'], image, 'LoansRepaid_P_26', 'Header', 0)

    # LoansMade_P_27
    data['LoansMade_P_27'] = ck_curr_val(data['LoansMade_P_27'], image, 'LoansMade_P_27', 'Header', 0)

    # RefundsInd_P_28a
    data['RefundsInd_P_28a'] = ck_curr_val(data['RefundsInd_P_28a'], image, 'RefundsInd_P_28a', 'Header', 0)

    # RefundsPolPtyComms_P_28b
    data['RefundsPolPtyComms_P_28b'] = ck_curr_val(data['RefundsPolPtyComms_P_28b'], image, 'RefundsPolPtyComms_P_28b',
                                                   'Header', 0)

    # RefundsOthPolComms_P_28c
    data['RefundsOthPolComms_P_28c'] = ck_curr_val(data['RefundsOthPolComms_P_28c'], image, 'RefundsOthPolComms_P_28c',
                                                   'Header', 0)

    # TotContRefunds_P_28d
    data['TotContRefunds_P_28d'] = ck_curr_val(data['TotContRefunds_P_28d'], image, 'TotContRefunds_P_28d', 'Header', 0)

    # OthDisb_P_29
    data['OthDisb_P_29'] = ck_curr_val(data['OthDisb_P_29'], image, 'OthDisb_P_29', 'Header', 0)

    # ShrdElecActivityFedShr_P_30a1
    data['ShrdElecActivityFedShr_P_30a1'] = ck_curr_val(data['ShrdElecActivityFedShr_P_30a1'], image,
                                                        'ShrdElecActivityFedShr_P_30a1', 'Header', 0)

    # ShrdElecActivityNonFedShr_P_30a2
    data['ShrdElecActivityNonFedShr_P_30a2'] = ck_curr_val(data['ShrdElecActivityNonFedShr_P_30a2'], image,
                                                           'ShrdElecActivityNonFedShr_P_30a2', 'Header', 0)

    # NonAllocFedElecActivity_P_30b
    data['NonAllocFedElecActivity_P_30b'] = ck_curr_val(data['NonAllocFedElecActivity_P_30b'], image,
                                                        'NonAllocFedElecActivity_P_30b', 'Header', 0)

    # TotFedElecActivity_P_30c
    data['TotFedElecActivity_P_30c'] = ck_curr_val(data['TotFedElecActivity_P_30c'], image, 'TotFedElecActivity_P_30c',
                                                   'Header', 0)

    # TotDisb_P_31
    data['TotDisb_P_31'] = ck_curr_val(data['TotDisb_P_31'], image, 'TotDisb_P_31', 'Header', 0)

    # TotFedDisb_P_32
    data['TotFedDisb_P_32'] = ck_curr_val(data['TotFedDisb_P_32'], image, 'TotFedDisb_P_32', 'Header', 0)

    # TotConts_P_33
    data['TotConts_P_33'] = ck_curr_val(data['TotConts_P_33'], image, 'TotConts_P_33', 'Header', 0)

    # TotContRefunds_P_34
    data['TotContRefunds_P_34'] = ck_curr_val(data['TotContRefunds_P_34'], image, 'TotContRefunds_P_34', 'Header', 0)

    # NetConts_P_35
    data['NetConts_P_35'] = ck_curr_val(data['NetConts_P_35'], image, 'NetConts_P_35', 'Header', 0)

    # TotFedOpExps_P_36
    data['TotFedOpExps_P_36'] = ck_curr_val(data['TotFedOpExps_P_36'], image, 'TotFedOpExps_P_36', 'Header', 0)

    # TotOffsetsOpExp_P_37
    data['TotOffsetsOpExp_P_37'] = ck_curr_val(data['TotOffsetsOpExp_P_37'], image, 'TotOffsetsOpExp_P_37', 'Header', 0)

    # NetOpExps_P_38
    data['NetOpExps_P_38'] = ck_curr_val(data['NetOpExps_P_38'], image, 'NetOpExps_P_38', 'Header', 0)

    # CashBegin_T_6a
    data['CashBegin_T_6a'] = ck_curr_val(data['CashBegin_T_6a'], image, 'CashBegin_T_6a', 'Header', 0)

    # CashBeginYr
    data['CashBeginYr'] = ck_curr_val(data['CashBeginYr'], image, 'CashBeginYr', 'Header', 0)

    # TotRcpts_T_6c
    data['TotRcpts_T_6c'] = ck_curr_val(data['TotRcpts_T_6c'], image, 'TotRcpts_T_6c', 'Header', 0)

    # Subtotal_T_6d
    data['Subtotal_T_6d'] = ck_curr_val(data['Subtotal_T_6d'], image, 'Subtotal_T_6d', 'Header', 0)

    # TotDisb_T_7
    data['TotDisb_T_7'] = ck_curr_val(data['TotDisb_T_7'], image, 'TotDisb_T_7', 'Header', 0)

    # CashClose_T_8
    data['CashClose_T_8'] = ck_curr_val(data['CashClose_T_8'], image, 'CashClose_T_8', 'Header', 0)

    # IndContsItem_T_11a1
    data['IndContsItem_T_11a1'] = ck_curr_val(data['IndContsItem_T_11a1'], image, 'IndContsItem_T_11a1', 'Header', 0)

    # IndContsUnitem_T_11a2
    data['IndContsUnitem_T_11a2'] = ck_curr_val(data['IndContsUnitem_T_11a2'], image, 'IndContsUnitem_T_11a2', 'Header',
                                                0)

    # IndContsTot_T_11a3
    data['IndContsTot_T_11a3'] = ck_curr_val(data['IndContsTot_T_11a3'], image, 'IndContsTot_T_11a3', 'Header', 0)

    # PolPtyCommConts_T_11b
    data['PolPtyCommConts_T_11b'] = ck_curr_val(data['PolPtyCommConts_T_11b'], image, 'PolPtyCommConts_T_11b', 'Header',
                                                0)

    # OthPolCommConts_T_11c
    data['OthPolCommConts_T_11c'] = ck_curr_val(data['OthPolCommConts_T_11c'], image, 'OthPolCommConts_T_11c', 'Header',
                                                0)

    # TotConts_T_11d
    data['TotConts_T_11d'] = ck_curr_val(data['TotConts_T_11d'], image, 'TotConts_T_11d', 'Header', 0)

    # TranFmPtyComms_T_12
    data['TranFmPtyComms_T_12'] = ck_curr_val(data['TranFmPtyComms_T_12'], image, 'TranFmPtyComms_T_12', 'Header', 0)

    # AllLoansRcvd_T_13
    data['AllLoansRcvd_T_13'] = ck_curr_val(data['AllLoansRcvd_T_13'], image, 'AllLoansRcvd_T_13', 'Header', 0)

    # LoanPymtsRcvd_T_14
    data['LoanPymtsRcvd_T_14'] = ck_curr_val(data['LoanPymtsRcvd_T_14'], image, 'LoanPymtsRcvd_T_14', 'Header', 0)

    # RefundOffsets_T_15
    data['RefundOffsets_T_15'] = ck_curr_val(data['RefundOffsets_T_15'], image, 'RefundOffsets_T_15', 'Header', 0)

    # RefundsFedConts_T_16
    data['RefundsFedConts_T_16'] = ck_curr_val(data['RefundsFedConts_T_16'], image, 'RefundsFedConts_T_16', 'Header', 0)

    # OthFedRcptsDvds_T_17
    data['OthFedRcptsDvds_T_17'] = ck_curr_val(data['OthFedRcptsDvds_T_17'], image, 'OthFedRcptsDvds_T_17', 'Header', 0)

    # TranFmNonFedAcctH3_T_18a
    data['TranFmNonFedAcctH3_T_18a'] = ck_curr_val(data['TranFmNonFedAcctH3_T_18a'], image, 'TranFmNonFedAcctH3_T_18a',
                                                   'Header', 0)

    # TranFmNonFedAcctH5_T_18b
    data['TranFmNonFedAcctH5_T_18b'] = ck_curr_val(data['TranFmNonFedAcctH5_T_18b'], image, 'TranFmNonFedAcctH5_T_18b',
                                                   'Header', 0)

    # TotNonFedTrans_T_18c
    data['TotNonFedTrans_T_18c'] = ck_curr_val(data['TotNonFedTrans_T_18c'], image, 'TotNonFedTrans_T_18c', 'Header', 0)

    # TotRcpts_T_19
    data['TotRcpts_T_19'] = ck_curr_val(data['TotRcpts_T_19'], image, 'TotRcpts_T_19', 'Header', 0)

    # TotFedRcpts_T_20
    data['TotFedRcpts_T_20'] = ck_curr_val(data['TotFedRcpts_T_20'], image, 'TotFedRcpts_T_20', 'Header', 0)

    # OpExpsFedShr_T_21a1
    data['OpExpsFedShr_T_21a1'] = ck_curr_val(data['OpExpsFedShr_T_21a1'], image, 'OpExpsFedShr_T_21a1', 'Header', 0)

    # OpExpsNonFedShr_T_21a2
    data['OpExpsNonFedShr_T_21a2'] = ck_curr_val(data['OpExpsNonFedShr_T_21a2'], image, 'OpExpsNonFedShr_T_21a2',
                                                 'Header', 0)

    # OpExpsOthFed_T_21b
    data['OpExpsOthFed_T_21b'] = ck_curr_val(data['OpExpsOthFed_T_21b'], image, 'OpExpsOthFed_T_21b', 'Header', 0)

    # TotOpExps_T_21c
    data['TotOpExps_T_21c'] = ck_curr_val(data['TotOpExps_T_21c'], image, 'TotOpExps_T_21c', 'Header', 0)

    # TranToPtyComms_T_22
    data['TranToPtyComms_T_22'] = ck_curr_val(data['TranToPtyComms_T_22'], image, 'TranToPtyComms_T_22', 'Header', 0)

    # ContsToFedCandsComms_T_23
    data['ContsToFedCandsComms_T_23'] = ck_curr_val(data['ContsToFedCandsComms_T_23'], image,
                                                    'ContsToFedCandsComms_T_23', 'Header', 0)

    # IndtExps_T_24
    data['IndtExps_T_24'] = ck_curr_val(data['IndtExps_T_24'], image, 'IndtExps_T_24', 'Header', 0)

    # CoordExpsByPtyComms_T_25
    data['CoordExpsByPtyComms_T_25'] = ck_curr_val(data['CoordExpsByPtyComms_T_25'], image, 'CoordExpsByPtyComms_T_25',
                                                   'Header', 0)

    # LoansRepaid_T_26
    data['LoansRepaid_T_26'] = ck_curr_val(data['LoansRepaid_T_26'], image, 'LoansRepaid_T_26', 'Header', 0)

    # LoansMade_T_27
    data['LoansMade_T_27'] = ck_curr_val(data['LoansMade_T_27'], image, 'LoansMade_T_27', 'Header', 0)

    # RefundsInd_T_28a
    data['RefundsInd_T_28a'] = ck_curr_val(data['RefundsInd_T_28a'], image, 'RefundsInd_T_28a', 'Header', 0)

    # RefundsPolPtyComms_T_28b
    data['RefundsPolPtyComms_T_28b'] = ck_curr_val(data['RefundsPolPtyComms_T_28b'], image, 'RefundsPolPtyComms_T_28b',
                                                   'Header', 0)

    # RefundsOthPolComms_T_28c
    data['RefundsOthPolComms_T_28c'] = ck_curr_val(data['RefundsOthPolComms_T_28c'], image, 'RefundsOthPolComms_T_28c',
                                                   'Header', 0)

    # TotContRefunds_T_28d
    data['TotContRefunds_T_28d'] = ck_curr_val(data['TotContRefunds_T_28d'], image, 'TotContRefunds_T_28d', 'Header', 0)

    # OthDisb_T_29
    data['OthDisb_T_29'] = ck_curr_val(data['OthDisb_T_29'], image, 'OthDisb_T_29', 'Header', 0)

    # ShrdElecActivityFedShr_T_30a1
    data['ShrdElecActivityFedShr_T_30a1'] = ck_curr_val(data['ShrdElecActivityFedShr_T_30a1'], image,
                                                        'ShrdElecActivityFedShr_T_30a1', 'Header', 0)

    # ShrdElecActivityNonFedShr_T_30a2
    data['ShrdElecActivityNonFedShr_T_30a2'] = ck_curr_val(data['ShrdElecActivityNonFedShr_T_30a2'], image,
                                                           'ShrdElecActivityNonFedShr_T_30a2', 'Header', 0)

    # NonAllocFedElecActivity_T_30b
    data['NonAllocFedElecActivity_T_30b'] = ck_curr_val(data['NonAllocFedElecActivity_T_30b'], image,
                                                        'NonAllocFedElecActivity_T_30b', 'Header', 0)

    # TotFedElecActivity_T_30c
    data['TotFedElecActivity_T_30c'] = ck_curr_val(data['TotFedElecActivity_T_30c'], image, 'TotFedElecActivity_T_30c',
                                                   'Header', 0)

    # TotDisb_T_31
    data['TotDisb_T_31'] = ck_curr_val(data['TotDisb_T_31'], image, 'TotDisb_T_31', 'Header', 0)

    # TotFedDisb_T_32
    data['TotFedDisb_T_32'] = ck_curr_val(data['TotFedDisb_T_32'], image, 'TotFedDisb_T_32', 'Header', 0)

    # TotConts_T_33
    data['TotConts_T_33'] = ck_curr_val(data['TotConts_T_33'], image, 'TotConts_T_33', 'Header', 0)

    # TotContRefunds_T_34
    data['TotContRefunds_T_34'] = ck_curr_val(data['TotContRefunds_T_34'], image, 'TotContRefunds_T_34', 'Header', 0)

    # NetConts_T_35
    data['NetConts_T_35'] = ck_curr_val(data['NetConts_T_35'], image, 'NetConts_T_35', 'Header', 0)

    # TotFedOpExps_T_36
    data['TotFedOpExps_T_36'] = ck_curr_val(data['TotFedOpExps_T_36'], image, 'TotFedOpExps_T_36', 'Header', 0)

    # TotOffsetsOpExp_T_37
    data['TotOffsetsOpExp_T_37'] = ck_curr_val(data['TotOffsetsOpExp_T_37'], image, 'TotOffsetsOpExp_T_37', 'Header', 0)

    # NetOpExps_T_38
    data['NetOpExps_T_38'] = ck_curr_val(data['NetOpExps_T_38'], image, 'NetOpExps_T_38', 'Header', 0)

    return data


def check_rpt_hdrs_f1(image, data, namedelim='', dateformat='CCYYMMDD'):
    # FormTp
    data['FormTp'] = clean_sql_text(data['FormTp'], 'nullstring', "'")

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'], 'nullstring', "'")

    # flgChgCommNm
    data['flgChgCommNm'] = convert_to_bit(clean_sql_text(data['flgChgCommNm']))

    # CommNm
    data['CommNm'] = clean_sql_text(data['CommNm'], 'nullstring', "'")

    # flgAddrChg
    data['flgAddrChg'] = convert_to_bit(clean_sql_text(data['flgAddrChg']))

    # Addr1
    data['Addr1'] = clean_sql_text(data['Addr1'], 'nullstring', "'")

    # Addr2
    data['Addr2'] = clean_sql_text(data['Addr2'], '', "'")

    # City
    data['City'] = clean_sql_text(data['City'], 'nullstring', "'")

    # StAbbr
    data['StAbbr'] = clean_sql_text(data['StAbbr'], 'nullstring', "'")

    # Zip
    data['Zip'] = clean_sql_text(data['Zip'], 'nullstring', "'")

    # flgChgCommEmail
    data['flgChgCommEmail'] = convert_to_bit(clean_sql_text(data['flgChgCommEmail']))

    # CommEmail
    data['CommEmail'] = clean_sql_text(data['CommEmail'], '', "'")

    # flgChgCommUrl
    data['flgChgCommUrl'] = convert_to_bit(clean_sql_text(data['flgChgCommUrl']))

    # CommUrl
    data['CommUrl'] = clean_sql_text(data['CommUrl'], 'nullstring', "'")

    # SubmDt
    data['SubmDt'] = "'" + convert_to_date(data['SubmDt'], dateformat, image, 'SubmDt', 'Header', 0, 'F1', '') + "'"
    if data['SubmDt'] == "''":
        data['SubmDt'] = 'NULL'

    # SignFullName
    if data['SignFullName'] != '':
        if data['SignLName'] != '' or data['SignFName'] != '' or data['SignMName'] != '' or data['SignPfx'] != '' or \
                        data['SignSfx'] != '':
            AddEntryToErrorLog('Signer full name (' + data[
                'SignFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            treas = parse_full_name(data['SignFullName'], namedelim)
            data['SignLName'] = treas[0]
            data['SignFName'] = treas[1]
            data['SignMName'] = treas[2]
            data['SignPfx'] = treas[3]
            data['SignSfx'] = treas[4]
        else:
            data['SignLName'] = data['SignFullName']

    # SignLName
    data['SignLName'] = clean_sql_text(data['SignLName'], 'nullstring', "'")

    # SignFName
    data['SignFName'] = clean_sql_text(data['SignFName'], '', "'")

    # SignMName
    data['SignMName'] = clean_sql_text(data['SignMName'], '', "'")

    # SignPfx
    data['SignPfx'] = clean_sql_text(data['SignPfx'], '', "'")

    # SignSfx
    data['SignSfx'] = clean_sql_text(data['SignSfx'], '', "'")

    # SignDt
    data['SignDt'] = "'" + convert_to_date(data['SignDt'], dateformat, image, 'SignDt', 'Header', 0, 'F1', '') + "'"
    if data['SignDt'] == "''":
        data['SignDt'] = 'NULL'

    # CommTp
    data['CommTp'] = clean_sql_text(data['CommTp'], 'nullstring', "'")

    # CandID
    data['CandID'] = clean_sql_text(data['CandID'], 'nullstring', "'")

    # CandFullName
    if data['CandFullName'] != '':
        if data['CandLName'] != '' or data['CandFName'] != '' or data['CandMName'] != '' or data['CandPfx'] != '' or \
                        data['CandSfx'] != '':
            AddEntryToErrorLog('Candidate full name (' + data[
                'CandFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            treas = parse_full_name(data['CandFullName'], namedelim)
            data['CandLName'] = treas[0]
            data['CandFName'] = treas[1]
            data['CandMName'] = treas[2]
            data['CandPfx'] = treas[3]
            data['CandSfx'] = treas[4]
        else:
            data['CandLName'] = data['CandFullName']

    # CandLName
    data['CandLName'] = clean_sql_text(data['CandLName'], '', "'")

    # CandFName
    data['CandFName'] = clean_sql_text(data['CandFName'], '', "'")

    # CandMName
    data['CandMName'] = clean_sql_text(data['CandMName'], '', "'")

    # CandPfx
    data['CandPfx'] = clean_sql_text(data['CandPfx'], '', "'")

    # CandSfx
    data['CandSfx'] = clean_sql_text(data['CandSfx'], '', "'")

    # CandOff
    data['CandOff'] = clean_sql_text(data['CandOff'], 'nullstring', "'")

    # CandStAbbr
    data['CandStAbbr'] = clean_sql_text(data['CandStAbbr'], 'nullstring', "'")

    # CandDist
    data['CandDist'] = convert_to_tinyint(data['CandDist'], image, 'CandDist', 'N/A', 0, 'F1', 'N/A')

    # PtyCd
    data['PtyCd'] = clean_sql_text(data['PtyCd'], 'nullstring', "'")

    # PtyTp
    data['PtyTp'] = clean_sql_text(data['PtyTp'], 'nullstring', "'")

    # PACTp
    data['PACTp'] = clean_sql_text(data['PACTp'], 'nullstring', "'")

    # flgLobRegPAC_ConnOrg_5e
    data['flgLobRegPAC_ConnOrg_5e'] = convert_to_bit(clean_sql_text(data['flgLobRegPAC_ConnOrg_5e']))

    # flgLobRegPAC_MultCands_5f
    data['flgLobRegPAC_MultCands_5f'] = convert_to_bit(clean_sql_text(data['flgLobRegPAC_MultCands_5f']))

    # flgLdspPAC_5f
    data['flgLdspPAC_5f'] = convert_to_bit(clean_sql_text(data['flgLdspPAC_5f']))

    # AffCommID
    data['AffCommID'] = clean_sql_text(data['AffCommID'], 'nullstring', "'")

    # AffCommNm
    data['AffCommNm'] = clean_sql_text(data['AffCommNm'], '', "'")

    # AffCandID
    data['AffCandID'] = clean_sql_text(data['AffCandID'], 'nullstring', "'")

    # AffCandLName
    data['AffCandLName'] = clean_sql_text(data['AffCandLName'], '', "'")

    # AffCandFName
    data['AffCandFName'] = clean_sql_text(data['AffCandFName'], '', "'")

    # AffCandMName
    data['AffCandMName'] = clean_sql_text(data['AffCandMName'], '', "'")

    # AffCandPfx
    data['AffCandPfx'] = clean_sql_text(data['AffCandPfx'], '', "'")

    # AffCandSfx
    data['AffCandSfx'] = clean_sql_text(data['AffCandSfx'], '', "'")

    # AffAddr1
    data['AffAddr1'] = clean_sql_text(data['AffAddr1'], '', "'")

    # AffAddr2
    data['AffAddr2'] = clean_sql_text(data['AffAddr2'], '', "'")

    # AffCity
    data['AffCity'] = clean_sql_text(data['AffCity'], '', "'")

    # AffStAbbr
    data['AffStAbbr'] = clean_sql_text(data['AffStAbbr'], 'nullstring', "'")

    # AffZip
    data['AffZip'] = clean_sql_text(data['AffZip'], '', "'")

    # AffRelCd
    data['AffRelCd'] = clean_sql_text(data['AffRelCd'], 'nullstring', "'").upper()

    # CustFullName
    if data['CustFullName'] != '':
        if data['CustLName'] != '' or data['CustFName'] != '' or data['CustMName'] != '' or data['CustPfx'] != '' or \
                        data['CustSfx'] != '':
            AddEntryToErrorLog('Custodian full name (' + data[
                'CustFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            treas = parse_full_name(data['CustFullName'], namedelim)
            data['CustLName'] = treas[0]
            data['CustFName'] = treas[1]
            data['CustMName'] = treas[2]
            data['CustPfx'] = treas[3]
            data['CustSfx'] = treas[4]
        else:
            data['CustLName'] = data['CustFullName']

    # CustLName
    data['CustLName'] = clean_sql_text(data['CustLName'], '', "'")

    # CustFName
    data['CustFName'] = clean_sql_text(data['CustFName'], '', "'")

    # CustMName
    data['CustMName'] = clean_sql_text(data['CustMName'], '', "'")

    # CustPfx
    data['CustPfx'] = clean_sql_text(data['CustPfx'], '', "'")

    # CustSfx
    data['CustSfx'] = clean_sql_text(data['CustSfx'], '', "'")

    # CustAddr1
    data['CustAddr1'] = clean_sql_text(data['CustAddr1'], '', "'")

    # CustAddr2
    data['CustAddr2'] = clean_sql_text(data['CustAddr2'], '', "'")

    # CustCity
    data['CustCity'] = clean_sql_text(data['CustCity'], '', "'")

    # CustStAbbr
    data['CustStAbbr'] = clean_sql_text(data['CustStAbbr'], 'nullstring', "'")

    # CustZip
    data['CustZip'] = clean_sql_text(data['CustZip'], '', "'")

    # CustTitle
    data['CustTitle'] = clean_sql_text(data['CustTitle'], '', "'")

    # CustPhone
    data['CustPhone'] = clean_sql_text(data['CustPhone'], '', "'")

    # TrsFullName
    if data['TrsFullName'] != '':
        if data['TrsLName'] != '' or data['TrsFName'] != '' or data['TrsMName'] != '' or data['TrsPfx'] != '' or data[
            'TrsSfx'] != '':
            AddEntryToErrorLog('Treasurer full name (' + data[
                'TrsFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            treas = parse_full_name(data['TrsFullName'], namedelim)
            data['TrsLName'] = treas[0]
            data['TrsFName'] = treas[1]
            data['TrsMName'] = treas[2]
            data['TrsPfx'] = treas[3]
            data['TrsSfx'] = treas[4]
        else:
            data['TrsLName'] = data['TrsFullName']

    # TrsLName
    data['TrsLName'] = clean_sql_text(data['TrsLName'], '', "'")

    # TrsFName
    data['TrsFName'] = clean_sql_text(data['TrsFName'], '', "'")

    # TrsMName
    data['TrsMName'] = clean_sql_text(data['TrsMName'], '', "'")

    # TrsPfx
    data['TrsPfx'] = clean_sql_text(data['TrsPfx'], '', "'")

    # TrsSfx
    data['TrsSfx'] = clean_sql_text(data['TrsSfx'], '', "'")

    # TrsAddr1
    data['TrsAddr1'] = clean_sql_text(data['TrsAddr1'], '', "'")

    # TrsAddr2
    data['TrsAddr2'] = clean_sql_text(data['TrsAddr2'], '', "'")

    # TrsCity
    data['TrsCity'] = clean_sql_text(data['TrsCity'], '', "'")

    # TrsStAbbr
    data['TrsStAbbr'] = clean_sql_text(data['TrsStAbbr'], 'nullstring', "'")

    # TrsZip
    data['TrsZip'] = clean_sql_text(data['TrsZip'], '', "'")

    # TrsTitle
    data['TrsTitle'] = clean_sql_text(data['TrsTitle'], '', "'")

    # TrsPhone
    data['TrsPhone'] = clean_sql_text(data['TrsPhone'], '', "'")

    # AgtFullName
    if data['AgtFullName'] != '':
        if data['AgtLName'] != '' or data['AgtFName'] != '' or data['AgtMName'] != '' or data['AgtPfx'] != '' or data[
            'AgtSfx'] != '':
            AddEntryToErrorLog('Agent full name (' + data[
                'AgtFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            treas = parse_full_name(data['AgtFullName'], namedelim)
            data['AgtLName'] = treas[0]
            data['AgtFName'] = treas[1]
            data['AgtMName'] = treas[2]
            data['AgtPfx'] = treas[3]
            data['AgtSfx'] = treas[4]
        else:
            data['AgtLName'] = data['AgtFullName']

    # AgtLName
    data['AgtLName'] = clean_sql_text(data['AgtLName'], '', "'")

    # AgtFName
    data['AgtFName'] = clean_sql_text(data['AgtFName'], '', "'")

    # AgtMName
    data['AgtMName'] = clean_sql_text(data['AgtMName'], '', "'")

    # AgtPfx
    data['AgtPfx'] = clean_sql_text(data['AgtPfx'], '', "'")

    # AgtSfx
    data['AgtSfx'] = clean_sql_text(data['AgtSfx'], '', "'")

    # AgtAddr1
    data['AgtAddr1'] = clean_sql_text(data['AgtAddr1'], '', "'")

    # AgtAddr2
    data['AgtAddr2'] = clean_sql_text(data['AgtAddr2'], '', "'")

    # AgtCity
    data['AgtCity'] = clean_sql_text(data['AgtCity'], '', "'")

    # AgtStAbbr
    data['AgtStAbbr'] = clean_sql_text(data['AgtStAbbr'], 'nullstring', "'")

    # AgtZip
    data['AgtZip'] = clean_sql_text(data['AgtZip'], '', "'")

    # AgtTitle
    data['AgtTitle'] = clean_sql_text(data['AgtTitle'], '', "'")

    # AgtPhone
    data['AgtPhone'] = clean_sql_text(data['AgtPhone'], '', "'")

    # Bank1Nm
    data['Bank1Nm'] = clean_sql_text(data['Bank1Nm'], '', "'")

    # Bank1Addr1
    data['Bank1Addr1'] = clean_sql_text(data['Bank1Addr1'], '', "'")

    # Bank1Addr2
    data['Bank1Addr2'] = clean_sql_text(data['Bank1Addr2'], '', "'")

    # Bank1City
    data['Bank1City'] = clean_sql_text(data['Bank1City'], '', "'")

    # Bank1StAbbr
    data['Bank1StAbbr'] = clean_sql_text(data['Bank1StAbbr'], 'nullstring', "'")

    # Bank1Zip
    data['Bank1Zip'] = clean_sql_text(data['Bank1Zip'], '', "'")

    # Bank2Nm
    data['Bank2Nm'] = clean_sql_text(data['Bank2Nm'], '', "'")

    # Bank2Addr1
    data['Bank2Addr1'] = clean_sql_text(data['Bank2Addr1'], '', "'")

    # Bank2Addr2
    data['Bank2Addr2'] = clean_sql_text(data['Bank2Addr2'], '', "'")

    # Bank2City
    data['Bank2City'] = clean_sql_text(data['Bank2City'], '', "'")

    # Bank2StAbbr
    data['Bank2StAbbr'] = clean_sql_text(data['Bank2StAbbr'], 'nullstring', "'")

    # Bank2Zip
    data['Bank2Zip'] = clean_sql_text(data['Bank2Zip'], '', "'")

    return data


def check_row_data_f1s(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # FormTp
    data['FormTp'] = clean_sql_text(data['FormTp'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # JtFndCommNm
    data['JtFndCommNm'] = clean_sql_text(data['JtFndCommNm'])

    # JtFundCommID
    data['JtFundCommID'] = clean_sql_text(data['JtFundCommID'])

    # AffCommID
    data['AffCommID'] = clean_sql_text(data['AffCommID'])

    # AffCommNm
    data['AffCommNm'] = clean_sql_text(data['AffCommNm'])

    # AffCandID
    data['AffCandID'] = clean_sql_text(data['AffCandID'])

    # AffLName
    data['AffLName'] = clean_sql_text(data['AffLName'])

    # AffFName
    data['AffFName'] = clean_sql_text(data['AffFName'])

    # AffMName
    data['AffMName'] = clean_sql_text(data['AffMName'])

    # AffPfx
    data['AffPfx'] = clean_sql_text(data['AffPfx'])

    # AffSfx
    data['AffSfx'] = clean_sql_text(data['AffSfx'])

    # AffAddr1
    data['AffAddr1'] = clean_sql_text(data['AffAddr1'])

    # AffAddr2
    data['AffAddr2'] = clean_sql_text(data['AffAddr2'])

    # AffCity
    data['AffCity'] = clean_sql_text(data['AffCity'])

    # AffStAbbr
    data['AffStAbbr'] = clean_sql_text(data['AffStAbbr'])

    # AffZip
    data['AffZip'] = clean_sql_text(data['AffZip'])

    # AffRelCd
    data['AffRelCd'] = clean_sql_text(data['AffRelCd'])

    # AgtLName
    data['AgtLName'] = clean_sql_text(data['AgtLName'])

    # AgtFName
    data['AgtFName'] = clean_sql_text(data['AgtFName'])

    # AgtMName
    data['AgtMName'] = clean_sql_text(data['AgtMName'])

    # AgtPfx
    data['AgtPfx'] = clean_sql_text(data['AgtPfx'])

    # AgtSfx
    data['AgtSfx'] = clean_sql_text(data['AgtSfx'])

    # AgtAddr1
    data['AgtAddr1'] = clean_sql_text(data['AgtAddr1'])

    # AgtAddr2
    data['AgtAddr2'] = clean_sql_text(data['AgtAddr2'])

    # AgtCity
    data['AgtCity'] = clean_sql_text(data['AgtCity'])

    # AgtStAbbr
    data['AgtStAbbr'] = clean_sql_text(data['AgtStAbbr'])

    # AgtZip
    data['AgtZip'] = clean_sql_text(data['AgtZip'])

    # AgtTitle
    data['AgtTitle'] = clean_sql_text(data['AgtTitle'])

    # AgtPhone
    data['AgtPhone'] = clean_sql_text(data['AgtPhone'])

    # BankNm
    data['BankNm'] = clean_sql_text(data['BankNm'])

    # BankAddr1
    data['BankAddr1'] = clean_sql_text(data['BankAddr1'])

    # BankAddr2
    data['BankAddr2'] = clean_sql_text(data['BankAddr2'])

    # BankCity
    data['BankCity'] = clean_sql_text(data['BankCity'])

    # BankStAbbr
    data['BankStAbbr'] = clean_sql_text(data['BankStAbbr'])

    # BankZip
    data['BankZip'] = clean_sql_text(data['BankZip'])

    return data


def check_row_data_sch_a(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])
    if len(data['TransID']) > 20:
        print(("TransID field too long.", image, rownbr, data))
        sys.exit(("TransID field too long.", image, rownbr, data))

    # BkRefTransID
    data['BkRefTransID'] = clean_sql_text(data['BkRefTransID'])

    # BkRefSchdNm
    data['BkRefSchdNm'] = clean_sql_text(data['BkRefSchdNm'])

    # EntTp
    data['EntTp'] = clean_sql_text(data['EntTp'])

    # ContOrgNm
    data['ContOrgNm'] = clean_sql_text(data['ContOrgNm'])

    # ContFullName
    if data['ContFullName'] != '':
        if data['ContLName'] != '' or data['ContFName'] != '' or data['ContMName'] != '' or data['ContPfx'] != '' or \
                        data['ContSfx'] != '':
            AddEntryToErrorLog('Contributor full name (' + data[
                'ContFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            name = parse_full_name(data['ContFullName'], namedelim)
            data['ContLName'] = name[0]
            data['ContFName'] = name[1]
            data['ContMName'] = name[2]
            data['ContPfx'] = name[3]
            data['ContSfx'] = name[4]
        else:
            data['ContLName'] = data['ContFullName']

    # ContLName
    data['ContLName'] = clean_sql_text(data['ContLName'])

    # ContFName
    data['ContFName'] = clean_sql_text(data['ContFName'])

    # ContMName
    data['ContMName'] = clean_sql_text(data['ContMName'])

    # ContPfx
    data['ContPfx'] = clean_sql_text(data['ContPfx'])

    # ContSfx
    data['ContSfx'] = clean_sql_text(data['ContSfx'])

    # Addr1
    data['Addr1'] = clean_sql_text(data['Addr1'])

    # Addr2
    data['Addr2'] = clean_sql_text(data['Addr2'])

    # City
    data['City'] = clean_sql_text(data['City'])

    # StAbbr
    data['StAbbr'] = clean_sql_text(data['StAbbr'])
    if len(data['StAbbr']) > 2:
        print(("StAbbr field too long.", image, rownbr, data))
        sys.exit(("StAbbr field too long.", image, rownbr, data))

    # Zip
    data['Zip'] = clean_sql_text(data['Zip'])

    # ElecCd
    data['ElecCd'] = clean_sql_text(data['ElecCd'])

    # ElecDesc
    data['ElecDesc'] = clean_sql_text(data['ElecDesc'])

    # ContDt
    data['ContDt'] = convert_to_date(data['ContDt'], dateformat, image, 'ContDt', data['LineNbr'], rownbr, 'SA',
                                     data['TransID'])

    # ContAmt
    data['ContAmt'] = ck_curr_val(data['ContAmt'], image, 'ContAmt', data['LineNbr'], rownbr)

    # ContAgg
    data['ContAgg'] = ck_curr_val(data['ContAgg'], image, 'ContAgg', data['LineNbr'], rownbr)

    # ContPurpCd
    data['ContPurpCd'] = clean_sql_text(data['ContPurpCd'])

    # ContPurpDesc
    data['ContPurpDesc'] = clean_sql_text(data['ContPurpDesc'])

    # Emp
    data['Emp'] = clean_sql_text(data['Emp'])
    if len(data['Emp']) > 38:
        print(("Emp field too long.", image, rownbr, data))
        sys.exit(("Emp field too long.", image, rownbr, data))

    # Occ
    data['Occ'] = clean_sql_text(data['Occ'])
    if len(data['Occ']) > 38:
        print(("Occ field too long.", image, rownbr, data))
        sys.exit(("Occ field too long.", image, rownbr, data))

    # DonorCommID
    data['DonorCommID'] = clean_sql_text(data['DonorCommID'])
    if len(data['DonorCommID']) > 11:
        print(("DonorCommID field too long.", image, rownbr, data))
        sys.exit(("DonorCommID field too long.", image, rownbr, data))

    # DonorCommNm
    data['DonorCommNm'] = clean_sql_text(data['DonorCommNm'])

    # DonorCandID
    data['DonorCandID'] = clean_sql_text(data['DonorCandID'])

    # DonorCandFullName
    if data['DonorCandFullName'] != '':
        if data['DonorCandLName'] != '' or data['DonorCandFName'] != '' or data['DonorCandMName'] != '' or data[
            'DonorCandPfx'] != '' or data['DonorCandSfx'] != '':
            AddEntryToErrorLog('Donor candidater full name (' + data[
                'DonorCandFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            name = parse_full_name(data['DonorCandFullName'], namedelim)
            data['DonorCandLName'] = name[0]
            data['DonorCandFName'] = name[1]
            data['DonorCandMName'] = name[2]
            data['DonorCandPfx'] = name[3]
            data['DonorCandSfx'] = name[4]
        else:
            data['DonorCandLName'] = data['DonorCandFullName']

    # DonorCandLName
    data['DonorCandLName'] = clean_sql_text(data['DonorCandLName'])

    # DonorCandFName
    data['DonorCandFName'] = clean_sql_text(data['DonorCandFName'])

    # DonorCandMName
    data['DonorCandMName'] = clean_sql_text(data['DonorCandMName'])

    # DonorCandPfx
    data['DonorCandPfx'] = clean_sql_text(data['DonorCandPfx'])

    # DonorCandSfx
    data['DonorCandSfx'] = clean_sql_text(data['DonorCandSfx'])

    # DonorCandOfc
    data['DonorCandOfc'] = clean_sql_text(data['DonorCandOfc'])
    if len(data['DonorCandOfc']) > 3:
        print(("DonorCandOfc field too long.", image, rownbr, data))
        sys.exit(("DonorCandOfc field too long.", image, rownbr, data))

    # DonorCandSt
    data['DonorCandSt'] = clean_sql_text(data['DonorCandSt'])

    # DonorCandDist
    data['DonorCandDist'] = convert_to_tinyint(data['DonorCandDist'], image, 'DonorCandDist', data['LineNbr'], rownbr,
                                               'SA', data['TransID'])

    # ConduitNm
    data['ConduitNm'] = clean_sql_text(data['ConduitNm'])

    # ConduitAddr1
    data['ConduitAddr1'] = clean_sql_text(data['ConduitAddr1'])

    # ConduitAddr2
    data['ConduitAddr2'] = clean_sql_text(data['ConduitAddr2'])

    # ConduitCity
    data['ConduitCity'] = clean_sql_text(data['ConduitCity'])

    # ConduitState
    data['ConduitState'] = clean_sql_text(data['ConduitState'])

    # ConduitZip
    data['ConduitZip'] = clean_sql_text(data['ConduitZip'])

    # MemoCd
    data['MemoCd'] = convert_to_bit(clean_sql_text(data['MemoCd']))

    # MemoTxt
    data['MemoTxt'] = clean_sql_text(data['MemoTxt'])

    # SIorSLRef
    data['SIorSLRef'] = clean_sql_text(data['SIorSLRef'])

    return data


def check_row_data_sch_b(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # BkRefTransID
    data['BkRefTransID'] = clean_sql_text(data['BkRefTransID'])

    # BkRefSchdNm
    data['BkRefSchdNm'] = clean_sql_text(data['BkRefSchdNm'])

    # EntTp
    data['EntTp'] = clean_sql_text(data['EntTp'])

    # PayeeOrgNm
    data['PayeeOrgNm'] = clean_sql_text(data['PayeeOrgNm'])

    # PayeeFullName
    if data['PayeeFullName'] != '':
        if data['PayeeLName'] != '' or data['PayeeFName'] != '' or data['PayeeMName'] != '' or data['PayeePfx'] != '' or \
                        data['PayeeSfx'] != '':
            AddEntryToErrorLog('Payee full name (' + data[
                'PayeeFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            name = parse_full_name(data['PayeeFullName'], namedelim)
            data['PayeeLName'] = name[0]
            data['PayeeFName'] = name[1]
            data['PayeeMName'] = name[2]
            data['PayeePfx'] = name[3]
            data['PayeeSfx'] = name[4]
        else:
            data['PayeeLName'] = data['PayeeFullName']

    # PayeeLName
    data['PayeeLName'] = clean_sql_text(data['PayeeLName'])

    # PayeeFName
    data['PayeeFName'] = clean_sql_text(data['PayeeFName'])

    # PayeeMName
    data['PayeeMName'] = clean_sql_text(data['PayeeMName'])

    # PayeePfx
    data['PayeePfx'] = clean_sql_text(data['PayeePfx'])

    # PayeeSfx
    data['PayeeSfx'] = clean_sql_text(data['PayeeSfx'])

    # PayeeAddr1
    data['PayeeAddr1'] = clean_sql_text(data['PayeeAddr1'])

    # PayeeAddr2
    data['PayeeAddr2'] = clean_sql_text(data['PayeeAddr2'])

    # PayeeCity
    data['PayeeCity'] = clean_sql_text(data['PayeeCity'])

    # PayeeState
    data['PayeeState'] = clean_sql_text(data['PayeeState'])

    # PayeeZip
    data['PayeeZip'] = clean_sql_text(data['PayeeZip'])

    # ElecCd
    data['ElecCd'] = clean_sql_text(data['ElecCd'])

    # ElecDesc
    data['ElecDesc'] = clean_sql_text(data['ElecDesc'])

    # ExpDt
    data['ExpDt'] = convert_to_date(data['ExpDt'], dateformat, image, 'ExpDt', data['LineNbr'], rownbr, 'SB',
                                    data['TransID'])

    # ExpAmt
    data['ExpAmt'] = ck_curr_val(data['ExpAmt'], image, 'ExpAmt', data['LineNbr'], rownbr)

    # SemiAnnRefBundAmt
    data['SemiAnnRefBundAmt'] = ck_curr_val(data['SemiAnnRefBundAmt'], image, 'SemiAnnRefBundAmt', data['LineNbr'],
                                            rownbr)

    # ExpPurpCd
    data['ExpPurpCd'] = clean_sql_text(data['ExpPurpCd'])

    # ExpPurpDesc
    data['ExpPurpDesc'] = clean_sql_text(data['ExpPurpDesc'])

    # ExpCatCd
    data['ExpCatCd'] = clean_sql_text(data['ExpCatCd'])

    # BenCommID
    data['BenCommID'] = clean_sql_text(data['BenCommID'])

    # BenCommNm
    data['BenCommNm'] = clean_sql_text(data['BenCommNm'])

    # BenCandID
    data['BenCandID'] = clean_sql_text(data['BenCandID'])

    # BenCandFullName
    if data['BenCandFullName'] != '':
        if data['BenCandLName'] != '' or data['BenCandFName'] != '' or data['BenCandMName'] != '' or data[
            'BenCandPfx'] != '' or data['BenCandSfx'] != '':
            AddEntryToErrorLog('Beneficiary candidate full name (' + data[
                'BenCandFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            name = parse_full_name(data['BenCandFullName'], namedelim)
            data['BenCandLName'] = name[0]
            data['BenCandFName'] = name[1]
            data['BenCandMName'] = name[2]
            data['BenCandPfx'] = name[3]
            data['BenCandSfx'] = name[4]
        else:
            data['BenCandLName'] = data['BenCandFullName']

    # BenCandLName
    data['BenCandLName'] = clean_sql_text(data['BenCandLName'])

    # BenCandFName
    data['BenCandFName'] = clean_sql_text(data['BenCandFName'])

    # BenCandMName
    data['BenCandMName'] = clean_sql_text(data['BenCandMName'])

    # BenCandPfx
    data['BenCandPfx'] = clean_sql_text(data['BenCandPfx'])

    # BenCandSfx
    data['BenCandSfx'] = clean_sql_text(data['BenCandSfx'])

    # BenCandOfc
    data['BenCandOfc'] = clean_sql_text(data['BenCandOfc'])

    # BenCandState
    data['BenCandState'] = clean_sql_text(data['BenCandState'])

    # BenCandDist
    # Sometimes this column just contains a second copy of the state abbreviation
    # or NA
    if data['BenCandDist'] == data['BenCandState']:
        try:
            float(data['BenCandDist'])
        except:
            data['BenCandDist'] = None
    elif data['BenCandDist'] == 'NA' or data['BenCandDist'] == '**':
        data['BenCandDist'] = None
    data['BenCandDist'] = convert_to_tinyint(data['BenCandDist'], image, 'BenCandDist', data['LineNbr'], rownbr, 'SB',
                                             data['TransID'])

    # ConduitNm
    data['ConduitNm'] = clean_sql_text(data['ConduitNm'])

    # ConduitAddr1
    data['ConduitAddr1'] = clean_sql_text(data['ConduitAddr1'])

    # ConduitAddr2
    data['ConduitAddr2'] = clean_sql_text(data['ConduitAddr2'])

    # ConduitCity
    data['ConduitCity'] = clean_sql_text(data['ConduitCity'])

    # ConduitState
    data['ConduitState'] = clean_sql_text(data['ConduitState'])

    # ConduitZip
    data['ConduitZip'] = clean_sql_text(data['ConduitZip'])

    # MemoCd
    data['MemoCd'] = convert_to_bit(clean_sql_text(data['MemoCd']))

    # MemoTxt
    data['MemoTxt'] = clean_sql_text(data['MemoTxt'])

    # SIorSLRef
    data['SIorSLRef'] = clean_sql_text(data['SIorSLRef'])

    return data


def check_row_data_sch_c(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # RctLnNbr
    data['RctLnNbr'] = clean_sql_text(data['RctLnNbr'])

    # EntTp
    data['EntTp'] = clean_sql_text(data['EntTp'])

    # LenderOrgName
    data['LenderOrgName'] = clean_sql_text(data['LenderOrgName'])

    # LenderLName
    data['LenderLName'] = clean_sql_text(data['LenderLName'])

    # LenderFName
    data['LenderFName'] = clean_sql_text(data['LenderFName'])

    # LenderMName
    data['LenderMName'] = clean_sql_text(data['LenderMName'])

    # LenderPfx
    data['LenderPfx'] = clean_sql_text(data['LenderPfx'])

    # LenderSfx
    data['LenderSfx'] = clean_sql_text(data['LenderSfx'])

    # LenderAddr1
    data['LenderAddr1'] = clean_sql_text(data['LenderAddr1'])

    # LenderAddr2
    data['LenderAddr2'] = clean_sql_text(data['LenderAddr2'])

    # LenderCity
    data['LenderCity'] = clean_sql_text(data['LenderCity'])

    # LenderState
    data['LenderState'] = clean_sql_text(data['LenderState'])

    # LenderZip
    data['LenderZip'] = clean_sql_text(data['LenderZip'])

    # ElecCd
    data['ElecCd'] = clean_sql_text(data['ElecCd'])

    # ElecDesc
    data['ElecDesc'] = clean_sql_text(data['ElecDesc'])

    # LoanAmt
    data['LoanAmt'] = ck_curr_val(data['LoanAmt'], image, 'LoanAmt', data['LineNbr'], rownbr)

    # PymtToDt
    data['PymtToDt'] = ck_curr_val(data['PymtToDt'], image, 'PymtToDt', data['LineNbr'], rownbr)

    # LoanBlnc
    data['LoanBlnc'] = ck_curr_val(data['LoanBlnc'], image, 'LoanBlnc', data['LineNbr'], rownbr)

    # IncurredDt
    data['IncurredDt'] = convert_to_date(data['IncurredDt'], dateformat, image, 'IncurredDt', data['LineNbr'], rownbr,
                                         'SC', data['TransID'])

    # DueDt
    data['DueDt'] = convert_to_date(data['DueDt'], dateformat, image, 'IncurredDt', data['LineNbr'], rownbr, 'SC',
                                    data['TransID'])

    # IntRt
    data['IntRt'] = clean_sql_text(data['IntRt'])

    # flgSecured
    data['flgSecured'] = convert_to_bit(clean_sql_text(data['flgSecured']))

    # flgPersFunds
    data['flgPersFunds'] = convert_to_bit(clean_sql_text(data['flgPersFunds']))

    # LenderCommID
    data['LenderCommID'] = clean_sql_text(data['LenderCommID'])

    # LenderCandID
    data['LenderCandID'] = clean_sql_text(data['LenderCandID'])

    # LenderCandLName
    data['LenderCandLName'] = clean_sql_text(data['LenderCandLName'])

    # LenderCandFName
    data['LenderCandFName'] = clean_sql_text(data['LenderCandFName'])

    # LenderCandMName
    data['LenderCandMName'] = clean_sql_text(data['LenderCandMName'])

    # LenderCandPfx
    data['LenderCandPfx'] = clean_sql_text(data['LenderCandPfx'])

    # LenderCandSfx
    data['LenderCandSfx'] = clean_sql_text(data['LenderCandSfx'])

    # LenderCandOfc
    data['LenderCandOfc'] = clean_sql_text(data['LenderCandOfc'])

    # LenderCandState
    data['LenderCandState'] = clean_sql_text(data['LenderCandState'])

    # LenderCandDist
    data['LenderCandDist'] = convert_to_tinyint(data['LenderCandDist'], image, 'LenderCandDist', data['LineNbr'],
                                                rownbr, 'SC', data['TransID'])

    # MemoCd
    data['MemoCd'] = convert_to_bit(clean_sql_text(data['MemoCd']))

    # MemoTxt
    data['MemoTxt'] = clean_sql_text(data['MemoTxt'])

    return data


def check_row_data_sch_c1(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # BkRefTransID
    data['BkRefTransID'] = clean_sql_text(data['BkRefTransID'])

    # Lender
    data['Lender'] = clean_sql_text(data['Lender'])

    # LenderAddr1
    data['LenderAddr1'] = clean_sql_text(data['LenderAddr1'])

    # LenderAddr2
    data['LenderAddr2'] = clean_sql_text(data['LenderAddr2'])

    # LenderCity
    data['LenderCity'] = clean_sql_text(data['LenderCity'])

    # LenderState
    data['LenderState'] = clean_sql_text(data['LenderState'])

    # LenderZip
    data['LenderZip'] = clean_sql_text(data['LenderZip'])

    # LoanAmt
    data['LoanAmt'] = ck_curr_val(data['LoanAmt'], image, 'LoanAmt', data['LineNbr'], rownbr)

    # IntRt
    data['IntRt'] = clean_sql_text(data['IntRt'])

    # IncurredDt
    data['IncurredDt'] = convert_to_date(data['IncurredDt'], dateformat, image, 'IncurredDt', data['LineNbr'], rownbr,
                                         'SC1', data['TransID'])

    # DueDt
    data['DueDt'] = convert_to_date(data['DueDt'], dateformat, image, 'DueDt', data['LineNbr'], rownbr, 'SC1',
                                    data['TransID'])

    # flgLoanRestructured
    data['flgLoanRestructured'] = convert_to_bit(clean_sql_text(data['flgLoanRestructured']))

    # OrigLoanDt
    data['OrigLoanDt'] = convert_to_date(data['OrigLoanDt'], dateformat, image, 'OrigLoanDt', data['LineNbr'], rownbr,
                                         'SC1', data['TransID'])

    # CrdtAmtThisDraw
    data['CrdtAmtThisDraw'] = ck_curr_val(data['CrdtAmtThisDraw'], image, 'CrdtAmtThisDraw', data['LineNbr'], rownbr)

    # TotBlnc
    data['TotBlnc'] = ck_curr_val(data['TotBlnc'], image, 'TotBlnc', data['LineNbr'], rownbr)

    # flgOthersLiable
    data['flgOthersLiable'] = convert_to_bit(clean_sql_text(data['flgOthersLiable']))

    # flgCollateral
    data['flgCollateral'] = convert_to_bit(clean_sql_text(data['flgCollateral']))

    # CollateralDesc
    data['CollateralDesc'] = clean_sql_text(data['CollateralDesc'])

    # CollateralVal
    data['CollateralVal'] = ck_curr_val(data['CollateralVal'], image, 'CollateralVal', data['LineNbr'], rownbr)

    # flgPerfectedInt
    data['flgPerfectedInt'] = convert_to_bit(clean_sql_text(data['flgPerfectedInt']))

    # flgFutIncPledged
    data['flgFutIncPledged'] = convert_to_bit(clean_sql_text(data['flgFutIncPledged']))

    # FutIncDesc
    data['FutIncDesc'] = clean_sql_text(data['FutIncDesc'])

    # FutIncEstVal
    data['FutIncEstVal'] = ck_curr_val(data['FutIncEstVal'], image, 'FutIncEstVal', data['LineNbr'], rownbr)

    # DepAcctEstDt
    data['DepAcctEstDt'] = convert_to_date(data['DepAcctEstDt'], dateformat, image, 'DepAcctEstDt', data['LineNbr'],
                                           rownbr, 'SC1', data['TransID'])

    # AcctLocName
    data['AcctLocName'] = clean_sql_text(data['AcctLocName'])

    # AcctLocAddr1
    data['AcctLocAddr1'] = clean_sql_text(data['AcctLocAddr1'])

    # AcctLocAddr2
    data['AcctLocAddr2'] = clean_sql_text(data['AcctLocAddr2'])

    # AcctLocCity
    data['AcctLocCity'] = clean_sql_text(data['AcctLocCity'])

    # AcctLocState
    data['AcctLocState'] = clean_sql_text(data['AcctLocState'])

    # AcctLocZip
    data['AcctLocZip'] = clean_sql_text(data['AcctLocZip'])

    # DepAcctAuthDt
    data['DepAcctAuthDt'] = convert_to_date(data['DepAcctAuthDt'], dateformat, image, 'DepAcctAuthDt', data['LineNbr'],
                                            rownbr, 'SC1', data['TransID'])

    # LoanBasisDesc
    data['LoanBasisDesc'] = clean_sql_text(data['LoanBasisDesc'])

    # TrsFullName
    if data['TrsFullName'] != '':
        if data['TrsLName'] != '' or data['TrsFName'] != '' or data['TrsMName'] != '' or data['TrsPfx'] != '' or data[
            'TrsSfx'] != '':
            AddEntryToErrorLog('Treasurer full name (' + data[
                'TrsFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            treas = parse_full_name(data['TrsFullName'], namedelim)
            data['TrsLName'] = treas[0]
            data['TrsFName'] = treas[1]
            data['TrsMName'] = treas[2]
            data['TrsPfx'] = treas[3]
            data['TrsSfx'] = treas[4]
        else:
            data['TrsLName'] = data['TrsFullName']

    # TrsLName
    data['TrsLName'] = clean_sql_text(data['TrsLName'])

    # TrsFName
    data['TrsFName'] = clean_sql_text(data['TrsFName'])

    # TrsMName
    data['TrsMName'] = clean_sql_text(data['TrsMName'])

    # TrsPfx
    data['TrsPfx'] = clean_sql_text(data['TrsPfx'])

    # TrsSfx
    data['TrsSfx'] = clean_sql_text(data['TrsSfx'])

    # TrsSignDt
    data['TrsSignDt'] = convert_to_date(data['TrsSignDt'], dateformat, image, 'TrsSignDt', data['LineNbr'], rownbr,
                                        'SC1', data['TransID'])

    # LendRepFullName
    if data['LendRepFullName'] != '':
        if data['LendRepLName'] != '' or data['LendRepFName'] != '' or data['LendRepMName'] != '' or data[
            'LendRepPfx'] != '' or data['LendRepSfx'] != '':
            AddEntryToErrorLog('Treasurer full name (' + data[
                'LendRepFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            treas = parse_full_name(data['LendRepFullName'], namedelim)
            data['LendRepLName'] = treas[0]
            data['LendRepFName'] = treas[1]
            data['LendRepMName'] = treas[2]
            data['LendRepPfx'] = treas[3]
            data['LendRepSfx'] = treas[4]
        else:
            data['LendRepLName'] = data['LendRepFullName']

    # LendRepLName
    data['LendRepLName'] = clean_sql_text(data['LendRepLName'])

    # LendRepFName
    data['LendRepFName'] = clean_sql_text(data['LendRepFName'])

    # LendRepMName
    data['LendRepMName'] = clean_sql_text(data['LendRepMName'])

    # LendRepPfx
    data['LendRepPfx'] = clean_sql_text(data['LendRepPfx'])

    # LendRepSfx
    data['LendRepSfx'] = clean_sql_text(data['LendRepSfx'])

    # LendRepTitle
    data['LendRepTitle'] = clean_sql_text(data['LendRepTitle'])

    # LendRepSignDt
    data['LendRepSignDt'] = convert_to_date(data['LendRepSignDt'], dateformat, image, 'LendRepSignDt', data['LineNbr'],
                                            rownbr, 'SC1', data['TransID'])

    return data


def check_row_data_sch_c2(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # BkRefTransID
    data['BkRefTransID'] = clean_sql_text(data['BkRefTransID'])

    # GuarFullName
    if data['GuarFullName'] != '':
        if data['GuarLName'] != '' or data['GuarFName'] != '' or data['GuarMName'] != '' or data['GuarPfx'] != '' or \
                        data['GuarSfx'] != '':
            AddEntryToErrorLog('Treasurer full name (' + data[
                'GuarFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            guar = parse_full_name(data['GuarFullName'], namedelim)
            data['GuarLName'] = guar[0]
            data['GuarFName'] = guar[1]
            data['GuarMName'] = guar[2]
            data['GuarPfx'] = guar[3]
            data['GuarSfx'] = guar[4]
        else:
            data['GuarLName'] = data['GuarFullName']

    # GuarLName
    data['GuarLName'] = clean_sql_text(data['GuarLName'])

    # GuarFName
    data['GuarFName'] = clean_sql_text(data['GuarFName'])

    # GuarMName
    data['GuarMName'] = clean_sql_text(data['GuarMName'])

    # GuarPfx
    data['GuarPfx'] = clean_sql_text(data['GuarPfx'])

    # GuarSfx
    data['GuarSfx'] = clean_sql_text(data['GuarSfx'])

    # GuarAddr1
    data['GuarAddr1'] = clean_sql_text(data['GuarAddr1'])

    # GuarAddr2
    data['GuarAddr2'] = clean_sql_text(data['GuarAddr2'])

    # GuarCity
    data['GuarCity'] = clean_sql_text(data['GuarCity'])

    # GuarState
    data['GuarState'] = clean_sql_text(data['GuarState'])

    # GuarZip
    data['GuarZip'] = clean_sql_text(data['GuarZip'])

    # GuarEmp
    data['GuarEmp'] = clean_sql_text(data['GuarEmp'])

    # GuarOcc
    data['GuarOcc'] = clean_sql_text(data['GuarOcc'])

    # GuarAmt
    data['GuarAmt'] = ck_curr_val(data['GuarAmt'], image, 'GuarAmt', data['LineNbr'], rownbr)

    return data


def check_row_data_sch_d(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # EntTp
    data['EntTp'] = clean_sql_text(data['EntTp'])

    # CreditorOrgName
    data['CreditorOrgName'] = clean_sql_text(data['CreditorOrgName'])

    # CreditorLName
    data['CreditorLName'] = clean_sql_text(data['CreditorLName'])

    # CreditorFName
    data['CreditorFName'] = clean_sql_text(data['CreditorFName'])

    # CreditorMName
    data['CreditorMName'] = clean_sql_text(data['CreditorMName'])

    # CreditorPfx
    data['CreditorPfx'] = clean_sql_text(data['CreditorPfx'])

    # CreditorSfx
    data['CreditorSfx'] = clean_sql_text(data['CreditorSfx'])

    # CreditorAddr1
    data['CreditorAddr1'] = clean_sql_text(data['CreditorAddr1'])

    # CreditorAddr2
    data['CreditorAddr2'] = clean_sql_text(data['CreditorAddr2'])

    # CreditorCity
    data['CreditorCity'] = clean_sql_text(data['CreditorCity'])

    # CreditorState
    data['CreditorState'] = clean_sql_text(data['CreditorState'])

    # CreditorZip
    data['CreditorZip'] = clean_sql_text(data['CreditorZip'])

    # DebtPurp
    data['DebtPurp'] = clean_sql_text(data['DebtPurp'])

    # BegBlnc_P
    data['BegBlnc_P'] = ck_curr_val(data['BegBlnc_P'], image, 'BegBlnc_P', data['LineNbr'], rownbr)

    # IncurAmt_P
    data['IncurAmt_P'] = ck_curr_val(data['IncurAmt_P'], image, 'IncurAmt_P', data['LineNbr'], rownbr)

    # PymtAmt_P
    data['PymtAmt_P'] = ck_curr_val(data['PymtAmt_P'], image, 'PymtAmt_P', data['LineNbr'], rownbr)

    # BalClose_P
    data['BalClose_P'] = ck_curr_val(data['BalClose_P'], image, 'BalClose_P', data['LineNbr'], rownbr)

    # CreditorCommID
    data['CreditorCommID'] = clean_sql_text(data['CreditorCommID'])

    # CreditorCandID
    data['CreditorCandID'] = clean_sql_text(data['CreditorCandID'])

    # CreditorCandFullName
    data['CreditorCandFullName'] = clean_sql_text(data['CreditorCandFullName'])

    # CreditorCandOfc
    data['CreditorCandOfc'] = clean_sql_text(data['CreditorCandOfc'])

    # CreditorCandState
    data['CreditorCandState'] = clean_sql_text(data['CreditorCandState'])

    # CreditorCandDist
    data['CreditorCandDist'] = convert_to_tinyint(data['CreditorCandDist'], image, 'CreditorCandDist', data['LineNbr'],
                                                  rownbr, 'SD', data['TransID'])

    # ConduitName
    data['ConduitName'] = clean_sql_text(data['ConduitName'])

    # ConduitAddr1
    data['ConduitAddr1'] = clean_sql_text(data['ConduitAddr1'])

    # ConduitAddr2
    data['ConduitAddr2'] = clean_sql_text(data['ConduitAddr2'])

    # ConduitCity
    data['ConduitCity'] = clean_sql_text(data['ConduitCity'])

    # ConduitState
    data['ConduitState'] = clean_sql_text(data['ConduitState'])

    # ConduitZip
    data['ConduitZip'] = clean_sql_text(data['ConduitZip'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    return data


def check_row_data_sch_e(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # BkRefTransID
    data['BkRefTransID'] = clean_sql_text(data['BkRefTransID'])

    # BkRefSchdNm
    data['BkRefSchdNm'] = clean_sql_text(data['BkRefSchdNm'])

    # EntTp
    data['EntTp'] = clean_sql_text(data['EntTp'])

    # PayeeOrgNm
    data['PayeeOrgNm'] = clean_sql_text(data['PayeeOrgNm'])

    # PayeeFullName
    if data['PayeeFullName'] != '':
        if data['PayeeLName'] != '' or data['PayeeFName'] != '' or data['PayeeMName'] != '' or data['PayeePfx'] != '' or \
                        data['PayeeSfx'] != '':
            AddEntryToErrorLog('Payee full name (' + data[
                'PayeeFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            name = parse_full_name(data['PayeeFullName'], namedelim)
            data['PayeeLName'] = name[0]
            data['PayeeFName'] = name[1]
            data['PayeeMName'] = name[2]
            data['PayeePfx'] = name[3]
            data['PayeeSfx'] = name[4]
        else:
            data['PayeeLName'] = data['PayeeFullName']

    # PayeeLName
    data['PayeeLName'] = clean_sql_text(data['PayeeLName'])

    # PayeeFName
    data['PayeeFName'] = clean_sql_text(data['PayeeFName'])

    # PayeeMName
    data['PayeeMName'] = clean_sql_text(data['PayeeMName'])

    # PayeePfx
    data['PayeePfx'] = clean_sql_text(data['PayeePfx'])

    # PayeeSfx
    data['PayeeSfx'] = clean_sql_text(data['PayeeSfx'])

    # PayeeAddr1
    data['PayeeAddr1'] = clean_sql_text(data['PayeeAddr1'])

    # PayeeAddr2
    data['PayeeAddr2'] = clean_sql_text(data['PayeeAddr2'])

    # PayeeCity
    data['PayeeCity'] = clean_sql_text(data['PayeeCity'])

    # PayeeStAbbr
    data['PayeeStAbbr'] = clean_sql_text(data['PayeeStAbbr'])

    # PayeeZip
    data['PayeeZip'] = clean_sql_text(data['PayeeZip'])

    # ElecCd
    data['ElecCd'] = clean_sql_text(data['ElecCd'])

    # ElecDesc
    data['ElecDesc'] = clean_sql_text(data['ElecDesc'])

    # DissmntnDt
    data['DissmntnDt'] = convert_to_date(data['DissmntnDt'], dateformat, image, 'DissmntnDt', data['LineNbr'], rownbr,
                                         'SE', data['TransID'])

    # ExpDt
    data['ExpDt'] = convert_to_date(data['ExpDt'], dateformat, image, 'ExpDt', data['LineNbr'], rownbr, 'SE',
                                    data['TransID'])

    # ExpAmt
    data['ExpAmt'] = ck_curr_val(data['ExpAmt'], image, 'ExpAmt', data['LineNbr'], rownbr)

    # ExpAgg
    data['ExpAgg'] = ck_curr_val(data['ExpAgg'], image, 'ExpAgg', data['LineNbr'], rownbr)

    # ExpPurpDesc
    data['ExpPurpDesc'] = clean_sql_text(data['ExpPurpDesc'])

    # ExpCatCd
    data['ExpCatCd'] = clean_sql_text(data['ExpCatCd'])

    # PayeeCommID
    data['PayeeCommID'] = clean_sql_text(data['PayeeCommID'])

    # SupOppCd
    data['SupOppCd'] = clean_sql_text(data['SupOppCd'])

    # SupOppCandID
    data['SupOppCandID'] = clean_sql_text(data['SupOppCandID'])

    # SupOppCandFullName
    if data['SupOppCandFullName'] != '':
        if data['SupOppCandLName'] != '' or data['SupOppCandFName'] != '' or data['SupOppCandMName'] != '' or data[
            'SupOppCandPfx'] != '' or data['SupOppCandSfx'] != '':
            AddEntryToErrorLog('Sup/Opp candidate full name (' + data[
                'SupOppCandFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            name = parse_full_name(data['SupOppCandFullName'], namedelim)
            data['SupOppCandLName'] = name[0]
            data['SupOppCandFName'] = name[1]
            data['SupOppCandMName'] = name[2]
            data['SupOppCandPfx'] = name[3]
            data['SupOppCandSfx'] = name[4]
        else:
            data['SupOppCandLName'] = data['SupOppCandFullName']

    # SupOppCandLName
    data['SupOppCandLName'] = clean_sql_text(data['SupOppCandLName'])

    # SupOppCandFName
    data['SupOppCandFName'] = clean_sql_text(data['SupOppCandFName'])

    # SupOppCandMName
    data['SupOppCandMName'] = clean_sql_text(data['SupOppCandMName'])

    # SupOppCandPfx
    data['SupOppCandPfx'] = clean_sql_text(data['SupOppCandPfx'])

    # SupOppCandSfx
    data['SupOppCandSfx'] = clean_sql_text(data['SupOppCandSfx'])

    # SupOppCandOfc
    data['SupOppCandOfc'] = clean_sql_text(data['SupOppCandOfc'])

    # SupOppCandStAbbr
    data['SupOppCandStAbbr'] = clean_sql_text(data['SupOppCandStAbbr'])

    # SupOppCandDist
    data['SupOppCandDist'] = convert_to_tinyint(data['SupOppCandDist'], image, 'SupOppCandDist', data['LineNbr'],
                                                rownbr, 'SE', data['TransID'])

    # CompFullName
    if data['CompFullName'] != '':
        if data['CompLName'] != '' or data['CompFName'] != '' or data['CompMName'] != '' or data['CompPfx'] != '' or \
                        data['CompSfx'] != '':
            AddEntryToErrorLog('Form completed by full name (' + data[
                'CompFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            name = parse_full_name(data['CompFullName'], namedelim)
            data['CompLName'] = name[0]
            data['CompFName'] = name[1]
            data['CompMName'] = name[2]
            data['CompPfx'] = name[3]
            data['CompSfx'] = name[4]
        else:
            data['CompLName'] = data['CompFullName']

    # CompLName
    data['CompLName'] = clean_sql_text(data['CompLName'])

    # CompFName
    data['CompFName'] = clean_sql_text(data['CompFName'])

    # CompMName
    data['CompMName'] = clean_sql_text(data['CompMName'])

    # CompPfx
    data['CompPfx'] = clean_sql_text(data['CompPfx'])

    # CompSfx
    data['CompSfx'] = clean_sql_text(data['CompSfx'])

    # SignDt
    data['SignDt'] = convert_to_date(data['SignDt'], dateformat, image, 'SignDt', data['LineNbr'], rownbr, 'SE',
                                     data['TransID'])

    # MemoCd
    data['MemoCd'] = convert_to_bit(clean_sql_text(data['MemoCd']))

    # MemoTxt
    data['MemoTxt'] = clean_sql_text(data['MemoTxt'])

    return data


def check_row_data_sch_f(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # BkRefTransID
    data['BkRefTransID'] = clean_sql_text(data['BkRefTransID'])

    # BkRefSchdNm
    data['BkRefSchdNm'] = clean_sql_text(data['BkRefSchdNm'])

    # flgDesigCoordExp
    data['flgDesigCoordExp'] = convert_to_bit(convert_to_bit(clean_sql_text(data['flgDesigCoordExp'])))

    # DesigCommID
    data['DesigCommID'] = clean_sql_text(data['DesigCommID'])

    # DesigCommNm
    data['DesigCommNm'] = clean_sql_text(data['DesigCommNm'])

    # SubordCommID
    data['SubordCommID'] = clean_sql_text(data['SubordCommID'])

    # SubordCommNm
    data['SubordCommNm'] = clean_sql_text(data['SubordCommNm'])

    # SubordAddr1
    data['SubordAddr1'] = clean_sql_text(data['SubordAddr1'])

    # SubordAddr2
    data['SubordAddr2'] = clean_sql_text(data['SubordAddr2'])

    # SubordCity
    data['SubordCity'] = clean_sql_text(data['SubordCity'])

    # SubordStAbbr
    data['SubordStAbbr'] = clean_sql_text(data['SubordStAbbr'])

    # SubordZip
    data['SubordZip'] = clean_sql_text(data['SubordZip'])

    # EntTp
    data['EntTp'] = clean_sql_text(data['EntTp'])

    # PayeeOrgNm
    data['PayeeOrgNm'] = clean_sql_text(data['PayeeOrgNm'])

    # PayeeFullName
    if data['PayeeFullName'] != '':
        if data['PayeeLName'] != '' or data['PayeeFName'] != '' or data['PayeeMName'] != '' or data['PayeePfx'] != '' or \
                        data['PayeeSfx'] != '':
            AddEntryToErrorLog('Payee full name (' + data[
                'PayeeFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            name = parse_full_name(data['PayeeFullName'], namedelim)
            data['PayeeLName'] = name[0]
            data['PayeeFName'] = name[1]
            data['PayeeMName'] = name[2]
            data['PayeePfx'] = name[3]
            data['PayeeSfx'] = name[4]
        else:
            data['PayeeLName'] = data['PayeeFullName']

    # PayeeLName
    data['PayeeLName'] = clean_sql_text(data['PayeeLName'])

    # PayeeFName
    data['PayeeFName'] = clean_sql_text(data['PayeeFName'])

    # PayeeMName
    data['PayeeMName'] = clean_sql_text(data['PayeeMName'])

    # PayeePfx
    data['PayeePfx'] = clean_sql_text(data['PayeePfx'])

    # PayeeSfx
    data['PayeeSfx'] = clean_sql_text(data['PayeeSfx'])

    # PayeeAddr1
    data['PayeeAddr1'] = clean_sql_text(data['PayeeAddr1'])

    # PayeeAddr2
    data['PayeeAddr2'] = clean_sql_text(data['PayeeAddr2'])

    # PayeeCity
    data['PayeeCity'] = clean_sql_text(data['PayeeCity'])

    # PayeeStAbbr
    data['PayeeStAbbr'] = clean_sql_text(data['PayeeStAbbr'])

    # PayeeZip
    data['PayeeZip'] = clean_sql_text(data['PayeeZip'])

    # ExpDt
    data['ExpDt'] = convert_to_date(data['ExpDt'], dateformat, image, 'ExpDt', data['LineNbr'], rownbr, 'SF',
                                    data['TransID'])

    # ExpAmt
    data['ExpAmt'] = ck_curr_val(data['ExpAmt'], image, 'ExpAmt', data['LineNbr'], rownbr)

    # ExpAgg
    data['ExpAgg'] = ck_curr_val(data['ExpAgg'], image, 'ExpAgg', data['LineNbr'], rownbr)

    # ExpPurpCd
    data['ExpPurpCd'] = clean_sql_text(data['ExpPurpCd'])

    # ExpPurpDesc
    data['ExpPurpDesc'] = clean_sql_text(data['ExpPurpDesc'])

    # ExpCatCd
    data['ExpCatCd'] = clean_sql_text(data['ExpCatCd'])

    # PayeeCommID
    data['PayeeCommID'] = clean_sql_text(data['PayeeCommID'])

    # PayeeCandID
    data['PayeeCandID'] = clean_sql_text(data['PayeeCandID'])

    # PayeeCandFullName
    if data['PayeeCandFullName'] != '':
        if data['PayeeCandLName'] != '' or data['PayeeCandFName'] != '' or data['PayeeCandMName'] != '' or data[
            'PayeeCandPfx'] != '' or data['PayeeCandSfx'] != '':
            AddEntryToErrorLog('Payee candidate full name (' + data[
                'PayeeCandFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            name = parse_full_name(data['PayeeCandFullName'], namedelim)
            data['PayeeCandLName'] = name[0]
            data['PayeeCandFName'] = name[1]
            data['PayeeCandMName'] = name[2]
            data['PayeeCandPfx'] = name[3]
            data['PayeeCandSfx'] = name[4]
        else:
            data['PayeeCandLName'] = data['PayeeCandFullName']

    # PayeeCandLName
    data['PayeeCandLName'] = clean_sql_text(data['PayeeCandLName'])

    # PayeeCandFName
    data['PayeeCandFName'] = clean_sql_text(data['PayeeCandFName'])

    # PayeeCandMName
    data['PayeeCandMName'] = clean_sql_text(data['PayeeCandMName'])

    # PayeeCandPfx
    data['PayeeCandPfx'] = clean_sql_text(data['PayeeCandPfx'])

    # PayeeCandSfx
    data['PayeeCandSfx'] = clean_sql_text(data['PayeeCandSfx'])

    # PayeeCandOfc
    data['PayeeCandOfc'] = clean_sql_text(data['PayeeCandOfc'])

    # PayeeCandStAbbr
    data['PayeeCandStAbbr'] = clean_sql_text(data['PayeeCandStAbbr'])

    # PayeeCandDist
    data['PayeeCandDist'] = convert_to_tinyint(data['PayeeCandDist'], image, 'PayeeCandDist', data['LineNbr'], rownbr,
                                               'SF', data['TransID'])

    # MemoCd
    data['MemoCd'] = convert_to_bit(clean_sql_text(data['MemoCd']))

    # MemoTxt
    data['MemoTxt'] = clean_sql_text(data['MemoTxt'])

    return data


def check_row_data_sch_h1(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # flgStLocFxPctPresOnly
    data['flgStLocFxPctPresOnly'] = convert_to_bit(clean_sql_text(data['flgStLocFxPctPresOnly']))

    # flgStLocFxPctPresAndSen
    data['flgStLocFxPctPresAndSen'] = convert_to_bit(clean_sql_text(data['flgStLocFxPctPresAndSen']))

    # flgStLocFxPctSenOnly
    data['flgStLocFxPctSenOnly'] = convert_to_bit(clean_sql_text(data['flgStLocFxPctSenOnly']))

    # flgStLocFxPctNonPresNonSen
    data['flgStLocFxPctNonPresNonSen'] = convert_to_bit(clean_sql_text(data['flgStLocFxPctNonPresNonSen']))

    # flgFlatMin50PctFed
    data['flgFlatMin50PctFed'] = convert_to_bit(clean_sql_text(data['flgFlatMin50PctFed']))

    # FedPct
    data['FedPct'] = ck_curr_val(data['FedPct'], image, 'FedPct', data['LineNbr'], rownbr)

    # NonFedPct
    data['NonFedPct'] = ck_curr_val(data['NonFedPct'], image, 'NonFedPct', data['LineNbr'], rownbr)

    # flgAdmRatio
    data['flgAdmRatio'] = convert_to_bit(clean_sql_text(data['flgAdmRatio']))

    # flgGenericVoterDrvRatio
    data['flgGenericVoterDrvRatio'] = convert_to_bit(clean_sql_text(data['flgGenericVoterDrvRatio']))

    # flgPubCommunRefPrtyRatio
    data['flgPubCommunRefPrtyRatio'] = convert_to_bit(clean_sql_text(data['flgPubCommunRefPrtyRatio']))

    return data


def check_row_data_sch_h2(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # EventNm
    data['EventNm'] = clean_sql_text(data['EventNm'])

    # flgDirFndrsg
    data['flgDirFndrsg'] = convert_to_bit(clean_sql_text(data['flgDirFndrsg']))

    # flgDirCandSup
    data['flgDirCandSup'] = convert_to_bit(clean_sql_text(data['flgDirCandSup']))

    # RatioCd
    data['RatioCd'] = clean_sql_text(data['RatioCd'])

    # FedPct
    data['FedPct'] = ck_curr_val(data['FedPct'], image, 'FedPct', data['LineNbr'], rownbr)

    # NonFedPct
    data['NonFedPct'] = ck_curr_val(data['NonFedPct'], image, 'NonFedPct', data['LineNbr'], rownbr)

    return data


def check_row_data_sch_h3(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # BkRefTransID
    data['BkRefTransID'] = clean_sql_text(data['BkRefTransID'])

    # AcctNm
    data['AcctNm'] = clean_sql_text(data['AcctNm'])

    # EventTp
    data['EventTp'] = clean_sql_text(data['EventTp'])

    # EventNm
    data['EventNm'] = clean_sql_text(data['EventNm'])

    # RcptDt
    data['RcptDt'] = convert_to_date(data['RcptDt'], dateformat, image, 'RcptDt', data['LineNbr'], rownbr, 'H3',
                                     data['TransID'])

    # TotAmtTrans
    data['TotAmtTrans'] = ck_curr_val(data['TotAmtTrans'], image, 'TotAmtTrans', data['LineNbr'], rownbr)

    # TransAmt
    data['TransAmt'] = ck_curr_val(data['TransAmt'], image, 'TransAmt', data['LineNbr'], rownbr)

    return data


def check_row_data_sch_h4(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # BkRefTransID
    data['BkRefTransID'] = clean_sql_text(data['BkRefTransID'])

    # BkRefSchdNm
    data['BkRefSchdNm'] = clean_sql_text(data['BkRefSchdNm'])

    # EntTp
    data['EntTp'] = clean_sql_text(data['EntTp'])

    # PayeeOrgNm
    data['PayeeOrgNm'] = clean_sql_text(data['PayeeOrgNm'])

    # PayeeFullName
    if data['PayeeFullName'] != '':
        if data['PayeeLName'] != '' or data['PayeeFName'] != '' or data['PayeeMName'] != '' or data['PayeePfx'] != '' or \
                        data['PayeeSfx'] != '':
            AddEntryToErrorLog('Payee full name (' + data[
                'PayeeFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            name = parse_full_name(data['PayeeFullName'], namedelim)
            data['PayeeLName'] = name[0]
            data['PayeeFName'] = name[1]
            data['PayeeMName'] = name[2]
            data['PayeePfx'] = name[3]
            data['PayeeSfx'] = name[4]
        else:
            data['PayeeLName'] = data['PayeeFullName']

    # PayeeLName
    data['PayeeLName'] = clean_sql_text(data['PayeeLName'])

    # PayeeFName
    data['PayeeFName'] = clean_sql_text(data['PayeeFName'])

    # PayeeMName
    data['PayeeMName'] = clean_sql_text(data['PayeeMName'])

    # PayeePfx
    data['PayeePfx'] = clean_sql_text(data['PayeePfx'])

    # PayeeSfx
    data['PayeeSfx'] = clean_sql_text(data['PayeeSfx'])

    # PayeeAddr1
    data['PayeeAddr1'] = clean_sql_text(data['PayeeAddr1'])

    # PayeeAddr2
    data['PayeeAddr2'] = clean_sql_text(data['PayeeAddr2'])

    # PayeeCity
    data['PayeeCity'] = clean_sql_text(data['PayeeCity'])

    # PayeeStAbbr
    data['PayeeStAbbr'] = clean_sql_text(data['PayeeStAbbr'])

    # PayeeZip
    data['PayeeZip'] = clean_sql_text(data['PayeeZip'])

    # EventNm
    data['EventNm'] = clean_sql_text(data['EventNm'])

    # ExpDt
    data['ExpDt'] = convert_to_date(data['ExpDt'], dateformat, image, 'ExpDt', data['LineNbr'], rownbr, 'H4',
                                    data['TransID'])

    # ExpAmt
    data['ExpAmt'] = ck_curr_val(data['ExpAmt'], image, 'ExpAmt', data['LineNbr'], rownbr)

    # FedAmt
    data['FedAmt'] = ck_curr_val(data['FedAmt'], image, 'FedAmt', data['LineNbr'], rownbr)

    # NonFedAmt
    data['NonFedAmt'] = ck_curr_val(data['NonFedAmt'], image, 'NonFedAmt', data['LineNbr'], rownbr)

    # EventAgg
    data['EventAgg'] = ck_curr_val(data['EventAgg'], image, 'EventAgg', data['LineNbr'], rownbr)

    # ExpPurpCd
    data['ExpPurpCd'] = clean_sql_text(data['ExpPurpCd'])

    # ExpPurpDesc
    data['ExpPurpDesc'] = clean_sql_text(data['ExpPurpDesc'])

    # ExpCatCd
    data['ExpCatCd'] = clean_sql_text(data['ExpCatCd'])

    # flgAdminActivity
    data['flgAdminActivity'] = convert_to_bit(clean_sql_text(data['flgAdminActivity']))

    # flgDirectFndrsg
    data['flgDirectFndrsg'] = convert_to_bit(clean_sql_text(data['flgDirectFndrsg']))

    # flgExempt
    data['flgExempt'] = convert_to_bit(clean_sql_text(data['flgExempt']))

    # flgGenVtrDrv
    data['flgGenVtrDrv'] = convert_to_bit(clean_sql_text(data['flgGenVtrDrv']))

    # flgDirCandSup
    data['flgDirCandSup'] = convert_to_bit(clean_sql_text(data['flgDirCandSup']))

    # flgPubCommun
    data['flgPubCommun'] = convert_to_bit(clean_sql_text(data['flgPubCommun']))

    # MemoCd
    data['MemoCd'] = convert_to_bit(clean_sql_text(data['MemoCd']))

    # MemoTxt
    data['MemoTxt'] = clean_sql_text(data['MemoTxt'])

    return data


def check_row_data_sch_h5(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # AcctNm
    data['AcctNm'] = clean_sql_text(data['AcctNm'])

    # RcptDt
    data['RcptDt'] = convert_to_date(data['RcptDt'], dateformat, image, 'RcptDt', data['LineNbr'], rownbr, 'H5',
                                     data['TransID'])

    # TotAmt
    data['TotAmt'] = ck_curr_val(data['TotAmt'], image, 'TotAmt', data['LineNbr'], rownbr)

    # VotRegnAmt
    data['VotRegnAmt'] = ck_curr_val(data['VotRegnAmt'], image, 'VotRegnAmt', data['LineNbr'], rownbr)

    # VotIDAmt
    data['VotIDAmt'] = ck_curr_val(data['VotIDAmt'], image, 'VotIDAmt', data['LineNbr'], rownbr)

    # GOTVAmt
    data['GOTVAmt'] = ck_curr_val(data['GOTVAmt'], image, 'GOTVAmt', data['LineNbr'], rownbr)

    # GenCampAmt
    data['GenCampAmt'] = ck_curr_val(data['GenCampAmt'], image, 'GenCampAmt', data['LineNbr'], rownbr)

    return data


def check_row_data_sch_h6(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # BkRefTransID
    data['BkRefTransID'] = clean_sql_text(data['BkRefTransID'])

    # BkRefSchdNm
    data['BkRefSchdNm'] = clean_sql_text(data['BkRefSchdNm'])

    # EntTp
    data['EntTp'] = clean_sql_text(data['EntTp'])

    # PayeeOrgNm
    data['PayeeOrgNm'] = clean_sql_text(data['PayeeOrgNm'])

    # PayeeFullName
    if data['PayeeFullName'] != '':
        if data['PayeeLName'] != '' or data['PayeeFName'] != '' or data['PayeeMName'] != '' or data['PayeePfx'] != '' or \
                        data['PayeeSfx'] != '':
            AddEntryToErrorLog('Payee full name (' + data[
                'PayeeFullName'] + ') could not be parsed for ' + imageid + ' because that would overwrite existing data. This script will attempt to add this data row to the database, but the full name field will be ignored.')
        elif namedelim != '':
            name = parse_full_name(data['PayeeFullName'], namedelim)
            data['PayeeLName'] = name[0]
            data['PayeeFName'] = name[1]
            data['PayeeMName'] = name[2]
            data['PayeePfx'] = name[3]
            data['PayeeSfx'] = name[4]
        else:
            data['PayeeLName'] = data['PayeeFullName']

    # PayeeLName
    data['PayeeLName'] = clean_sql_text(data['PayeeLName'])

    # PayeeFName
    data['PayeeFName'] = clean_sql_text(data['PayeeFName'])

    # PayeeMName
    data['PayeeMName'] = clean_sql_text(data['PayeeMName'])

    # PayeePfx
    data['PayeePfx'] = clean_sql_text(data['PayeePfx'])

    # PayeeSfx
    data['PayeeSfx'] = clean_sql_text(data['PayeeSfx'])

    # PayeeAddr1
    data['PayeeAddr1'] = clean_sql_text(data['PayeeAddr1'])

    # PayeeAddr2
    data['PayeeAddr2'] = clean_sql_text(data['PayeeAddr2'])

    # PayeeCity
    data['PayeeCity'] = clean_sql_text(data['PayeeCity'])

    # PayeeStAbbr
    data['PayeeStAbbr'] = clean_sql_text(data['PayeeStAbbr'])

    # PayeeZip
    data['PayeeZip'] = clean_sql_text(data['PayeeZip'])

    # EventNm
    data['EventNm'] = clean_sql_text(data['EventNm'])

    # ExpDt
    data['ExpDt'] = convert_to_date(data['ExpDt'], dateformat, image, 'ExpDt', data['LineNbr'], rownbr, 'H6',
                                    data['TransID'])

    # TotExpAmt
    data['TotExpAmt'] = ck_curr_val(data['TotExpAmt'], image, 'TotExpAmt', data['LineNbr'], rownbr)

    # FedAmt
    data['FedAmt'] = ck_curr_val(data['FedAmt'], image, 'FedAmt', data['LineNbr'], rownbr)

    # LevinAmt
    data['LevinAmt'] = ck_curr_val(data['LevinAmt'], image, 'LevinAmt', data['LineNbr'], rownbr)

    # ExpAgg
    data['ExpAgg'] = ck_curr_val(data['ExpAgg'], image, 'ExpAgg', data['LineNbr'], rownbr)

    # ExpPurpCd
    data['ExpPurpCd'] = clean_sql_text(data['ExpPurpCd'])

    # ExpPurpDesc
    data['ExpPurpDesc'] = clean_sql_text(data['ExpPurpDesc'])

    # ExpCatCd
    data['ExpCatCd'] = clean_sql_text(data['ExpCatCd'])

    # flgActVotRegn
    data['flgActVotRegn'] = convert_to_bit(clean_sql_text(data['flgActVotRegn']))

    # flgActGOTV
    data['flgActGOTV'] = convert_to_bit(clean_sql_text(data['flgActGOTV']))

    # flgActVotID
    data['flgActVotID'] = convert_to_bit(clean_sql_text(data['flgActVotID']))

    # flgActGenCamp
    data['flgActGenCamp'] = convert_to_bit(clean_sql_text(data['flgActGenCamp']))

    # MemoCd
    data['MemoCd'] = convert_to_bit(clean_sql_text(data['MemoCd']))

    # MemoTxt
    data['MemoTxt'] = clean_sql_text(data['MemoTxt'])

    return data


def check_row_data_sch_i(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # RecIDNbr
    data['RecIDNbr'] = clean_sql_text(data['RecIDNbr'])

    # AcctNm
    data['AcctNm'] = clean_sql_text(data['AcctNm'])

    # BankAcctID
    data['BankAcctID'] = clean_sql_text(data['BankAcctID'])

    # CovgFmDt
    data['CovgFmDt'] = convert_to_date(data['CovgFmDt'], dateformat, image, 'CovgFmDt', data['LineNbr'], rownbr, 'SI',
                                       data['TransID'])

    # CovgToDt
    data['CovgToDt'] = convert_to_date(data['CovgToDt'], dateformat, image, 'CovgToDt', data['LineNbr'], rownbr, 'SI',
                                       data['TransID'])

    # TotRcpts
    data['TotRcpts'] = ck_curr_val(data['TotRcpts'], image, 'TotRcpts', data['LineNbr'], rownbr)

    # TransToFed
    data['TransToFed'] = ck_curr_val(data['TransToFed'], image, 'TransToFed', data['LineNbr'], rownbr)

    # TransToStAndLoc
    data['TransToStAndLoc'] = ck_curr_val(data['TransToStAndLoc'], image, 'TransToStAndLoc', data['LineNbr'], rownbr)

    # DirStLocCandSup
    data['DirStLocCandSup'] = ck_curr_val(data['DirStLocCandSup'], image, 'DirStLocCandSup', data['LineNbr'], rownbr)

    # OthDisb
    data['OthDisb'] = ck_curr_val(data['OthDisb'], image, 'OthDisb', data['LineNbr'], rownbr)

    # TotDisb
    data['TotDisb'] = ck_curr_val(data['TotDisb'], image, 'TotDisb', data['LineNbr'], rownbr)

    # BegCOH
    data['BegCOH'] = ck_curr_val(data['BegCOH'], image, 'BegCOH', data['LineNbr'], rownbr)

    # Rcpts
    data['Rcpts'] = ck_curr_val(data['Rcpts'], image, 'Rcpts', data['LineNbr'], rownbr)

    # Subtotal
    data['Subtotal'] = ck_curr_val(data['Subtotal'], image, 'Subtotal', data['LineNbr'], rownbr)

    # Disb
    data['Disb'] = ck_curr_val(data['Disb'], image, 'Disb', data['LineNbr'], rownbr)

    # EndCOH
    data['EndCOH'] = ck_curr_val(data['EndCOH'], image, 'EndCOH', data['LineNbr'], rownbr)

    # TotRcpts2
    data['TotRcpts2'] = ck_curr_val(data['TotRcpts2'], image, 'TotRcpts2', data['LineNbr'], rownbr)

    # TransToFed2
    data['TransToFed2'] = ck_curr_val(data['TransToFed2'], image, 'TransToFed2', data['LineNbr'], rownbr)

    # TransToStAndLoc2
    data['TransToStAndLoc2'] = ck_curr_val(data['TransToStAndLoc2'], image, 'TransToStAndLoc2', data['LineNbr'], rownbr)

    # DirStLocCandSup2
    data['DirStLocCandSup2'] = ck_curr_val(data['DirStLocCandSup2'], image, 'DirStLocCandSup2', data['LineNbr'], rownbr)

    # OthDisb2
    data['OthDisb2'] = ck_curr_val(data['OthDisb2'], image, 'OthDisb2', data['LineNbr'], rownbr)

    # TotDisb2
    data['TotDisb2'] = ck_curr_val(data['TotDisb2'], image, 'TotDisb2', data['LineNbr'], rownbr)

    # BegCOH
    data['BegCOH2'] = ck_curr_val(data['BegCOH2'], image, 'BegCOH2', data['LineNbr'], rownbr)

    # Rcpts2
    data['Rcpts2'] = ck_curr_val(data['Rcpts2'], image, 'Rcpts2', data['LineNbr'], rownbr)

    # Subtotal2
    data['Subtotal2'] = ck_curr_val(data['Subtotal2'], image, 'Subtotal2', data['LineNbr'], rownbr)

    # Disb2
    data['Disb2'] = ck_curr_val(data['Disb2'], image, 'Disb2', data['LineNbr'], rownbr)

    # EndCOH2
    data['EndCOH2'] = ck_curr_val(data['EndCOH2'], image, 'EndCOH2', data['LineNbr'], rownbr)

    return data


def check_row_data_sch_l(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # RecordID
    data['RecordID'] = clean_sql_text(data['RecordID'])

    # AcctNm
    data['AcctNm'] = clean_sql_text(data['AcctNm'])

    # CovgFmDt
    data['CovgFmDt'] = convert_to_date(data['CovgFmDt'], dateformat, image, 'CovgFmDt', data['LineNbr'], rownbr, 'SL',
                                       data['TransID'])

    # CovgToDt
    data['CovgToDt'] = convert_to_date(data['CovgToDt'], dateformat, image, 'CovgToDt', data['LineNbr'], rownbr, 'SL',
                                       data['TransID'])

    # IndRcptsItem_P
    data['IndRcptsItem_P'] = ck_curr_val(data['IndRcptsItem_P'], image, 'IndRcptsItem_P', data['LineNbr'], 0)

    # IndRcptsUnitem_P
    data['IndRcptsUnitem_P'] = ck_curr_val(data['IndRcptsUnitem_P'], image, 'IndRcptsUnitem_P', data['LineNbr'], 0)

    # IndRcptsTot_P
    data['IndRcptsTot_P'] = ck_curr_val(data['IndRcptsTot_P'], image, 'IndRcptsTot_P', data['LineNbr'], 0)

    # OthRcpts_P
    data['OthRcpts_P'] = ck_curr_val(data['OthRcpts_P'], image, 'OthRcpts_P', data['LineNbr'], 0)

    # TotRcpts_P
    data['TotRcpts_P'] = ck_curr_val(data['TotRcpts_P'], image, 'TotRcpts_P', data['LineNbr'], 0)

    # TransVotReg_P
    data['TransVotReg_P'] = ck_curr_val(data['TransVotReg_P'], image, 'TransVotReg_P', data['LineNbr'], 0)

    # TransVotID_P
    data['TransVotID_P'] = ck_curr_val(data['TransVotID_P'], image, 'TransVotID_P', data['LineNbr'], 0)

    # TransGOTV_P
    data['TransGOTV_P'] = ck_curr_val(data['TransGOTV_P'], image, 'TransGOTV_P', data['LineNbr'], 0)

    # TransGenCamp_P
    data['TransGenCamp_P'] = ck_curr_val(data['TransGenCamp_P'], image, 'TransGenCamp_P', data['LineNbr'], 0)

    # TransTot_P
    data['TransTot_P'] = ck_curr_val(data['TransTot_P'], image, 'TransTot_P', data['LineNbr'], 0)

    # OthDisb_P
    data['OthDisb_P'] = ck_curr_val(data['OthDisb_P'], image, 'OthDisb_P', data['LineNbr'], 0)

    # TotDisb_P
    data['TotDisb_P'] = ck_curr_val(data['TotDisb_P'], image, 'TotDisb_P', data['LineNbr'], 0)

    # BegCOH_P
    data['BegCOH_P'] = ck_curr_val(data['BegCOH_P'], image, 'BegCOH_P', data['LineNbr'], 0)

    # Rcpts_P
    data['Rcpts_P'] = ck_curr_val(data['Rcpts_P'], image, 'Rcpts_P', data['LineNbr'], 0)

    # Subtotal_P
    data['Subtotal_P'] = ck_curr_val(data['Subtotal_P'], image, 'Subtotal_P', data['LineNbr'], 0)

    # Disb_P
    data['Disb_P'] = ck_curr_val(data['Disb_P'], image, 'Disb_P', data['LineNbr'], 0)

    # EndCOH_P
    data['EndCOH_P'] = ck_curr_val(data['EndCOH_P'], image, 'EndCOH_P', data['LineNbr'], 0)

    # IndRcptsItem_T
    data['IndRcptsItem_T'] = ck_curr_val(data['IndRcptsItem_T'], image, 'IndRcptsItem_T', data['LineNbr'], 0)

    # IndRcptsUnitem_T
    data['IndRcptsUnitem_T'] = ck_curr_val(data['IndRcptsUnitem_T'], image, 'IndRcptsUnitem_T', data['LineNbr'], 0)

    # IndRcptsTot_T
    data['IndRcptsTot_T'] = ck_curr_val(data['IndRcptsTot_T'], image, 'IndRcptsTot_T', data['LineNbr'], 0)

    # OthRcpts_T
    data['OthRcpts_T'] = ck_curr_val(data['OthRcpts_T'], image, 'OthRcpts_T', data['LineNbr'], 0)

    # TotRcpts_T
    data['TotRcpts_T'] = ck_curr_val(data['TotRcpts_T'], image, 'TotRcpts_T', data['LineNbr'], 0)

    # TransVotReg_T
    data['TransVotReg_T'] = ck_curr_val(data['TransVotReg_T'], image, 'TransVotReg_T', data['LineNbr'], 0)

    # TransVotID_T
    data['TransVotID_T'] = ck_curr_val(data['TransVotID_T'], image, 'TransVotID_T', data['LineNbr'], 0)

    # TransGOTV_T
    data['TransGOTV_T'] = ck_curr_val(data['TransGOTV_T'], image, 'TransGOTV_T', data['LineNbr'], 0)

    # TransGenCamp_T
    data['TransGenCamp_T'] = ck_curr_val(data['TransGenCamp_T'], image, 'TransGenCamp_T', data['LineNbr'], 0)

    # TransTot_T
    data['TransTot_T'] = ck_curr_val(data['TransTot_T'], image, 'TransTot_T', data['LineNbr'], 0)

    # OthDisb_T
    data['OthDisb_T'] = ck_curr_val(data['OthDisb_T'], image, 'OthDisb_T', data['LineNbr'], 0)

    # TotDisb_T
    data['TotDisb_T'] = ck_curr_val(data['TotDisb_T'], image, 'TotDisb_T', data['LineNbr'], 0)

    # BegCOH_T
    data['BegCOH_T'] = ck_curr_val(data['BegCOH_T'], image, 'BegCOH_T', data['LineNbr'], 0)

    # Rcpts_T
    data['Rcpts_T'] = ck_curr_val(data['Rcpts_T'], image, 'Rcpts_T', data['LineNbr'], 0)

    # Subtotal_T
    data['Subtotal_T'] = ck_curr_val(data['Subtotal_T'], image, 'Subtotal_T', data['LineNbr'], 0)

    # Disb_T
    data['Disb_T'] = ck_curr_val(data['Disb_T'], image, 'Disb_T', data['LineNbr'], 0)

    # EndCOH_T'
    data['EndCOH_T'] = ck_curr_val(data['EndCOH_T'], image, 'EndCOH_T', data['LineNbr'], 0)

    return data


def check_row_data_text(data, image, rownbr, namedelim='', dateformat='CCYYMMDD'):
    # LineNbr
    data['LineNbr'] = clean_sql_text(data['LineNbr'])

    # CommID
    data['CommID'] = clean_sql_text(data['CommID'])

    # TransID
    data['TransID'] = clean_sql_text(data['TransID'])

    # BkRefTransID
    data['BkRefTransID'] = clean_sql_text(data['BkRefTransID'])

    # BkRefSchdNm
    data['BkRefSchdNm'] = clean_sql_text(data['BkRefSchdNm'])

    # FullText
    data['FullText'] = clean_sql_text(data['FullText'])

    return data


##############################################



# Built list of supported report types
rpttypes = build_list_of_supported_report_types()

# Create timestamp to append to output files
filestamp = create_file_timestamp()

# Build files to house data output
otherdatafile = RPTOUTDIR + 'OtherData_' + filestamp + '.txt'
schedafile = RPTOUTDIR + 'SchedA_' + filestamp + '.txt'
schedbfile = RPTOUTDIR + 'SchedB_' + filestamp + '.txt'
schedcfile = RPTOUTDIR + 'SchedC_' + filestamp + '.txt'
schedc1file = RPTOUTDIR + 'SchedC1_' + filestamp + '.txt'
schedc2file = RPTOUTDIR + 'SchedC2_' + filestamp + '.txt'
scheddfile = RPTOUTDIR + 'SchedD_' + filestamp + '.txt'
schedefile = RPTOUTDIR + 'SchedE_' + filestamp + '.txt'
schedffile = RPTOUTDIR + 'SchedF_' + filestamp + '.txt'
schedh1file = RPTOUTDIR + 'SchedH1_' + filestamp + '.txt'
schedh2file = RPTOUTDIR + 'SchedH2_' + filestamp + '.txt'
schedh3file = RPTOUTDIR + 'SchedH3_' + filestamp + '.txt'
schedh4file = RPTOUTDIR + 'SchedH4_' + filestamp + '.txt'
schedh5file = RPTOUTDIR + 'SchedH5_' + filestamp + '.txt'
schedh6file = RPTOUTDIR + 'SchedH6_' + filestamp + '.txt'
schedifile = RPTOUTDIR + 'SchedI_' + filestamp + '.txt'
schedlfile = RPTOUTDIR + 'SchedL_' + filestamp + '.txt'
textfile = RPTOUTDIR + 'Text_' + filestamp + '.txt'
f1sfile = RPTOUTDIR + 'F1S_' + filestamp + '.txt'

# Write headers to data output files
with open(schedafile, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['SA'])) + '\r')

with open(schedbfile, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['SB'])) + '\r')

with open(schedcfile, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['SC'])) + '\r')

with open(schedc1file, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['SC1'])) + '\r')

with open(schedc2file, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['SC2'])) + '\r')

with open(scheddfile, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['SD'])) + '\r')

with open(schedefile, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['SE'])) + '\r')

with open(schedffile, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['SF'])) + '\r')

with open(schedh1file, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['H1'])) + '\r')

with open(schedh2file, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['H2'])) + '\r')

with open(schedh3file, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['H3'])) + '\r')

with open(schedh4file, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['H4'])) + '\r')

with open(schedh5file, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['H5'])) + '\r')

with open(schedh6file, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['H6'])) + '\r')

with open(schedifile, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['SI'])) + '\r')

with open(schedlfile, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['SL'])) + '\r')

with open(textfile, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + 'PrtTp' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(
        map(str, outputhdrs['TEXT'])) + '\r')

with open(f1sfile, 'wb') as outputfile:
    outputfile.write('ImageID' + OUTPUTDELIMITER + OUTPUTDELIMITER.join(map(str, outputhdrs['F1S'])) + '\r')

# Append full name fields to output headers
outputhdrs['SA'].append('ContFullName')
outputhdrs['SA'].append('DonorCandFullName')
outputhdrs['SB'].append('PayeeFullName')
outputhdrs['SB'].append('BenCandFullName')
outputhdrs['SC'].append('LenderFullName')
outputhdrs['SC'].append('LenderCandFullName')
outputhdrs['SC1'].append('LendRepFullName')
outputhdrs['SC1'].append('TrsFullName')
outputhdrs['SC2'].append('GuarFullName')
outputhdrs['SE'].append('PayeeFullName')
outputhdrs['SE'].append('SupOppCandFullName')
outputhdrs['SE'].append('CompFullName')
outputhdrs['SF'].append('PayeeFullName')
outputhdrs['SF'].append('PayeeCandFullName')
outputhdrs['H4'].append('PayeeFullName')
outputhdrs['H6'].append('PayeeFullName')
outputhdrs['F1S'].append('AgtFullName')

# Iterate through each file
for fecfile in glob.glob(os.path.join(RPTSVDIR, '*.fec')):

    # Iterate counter and break at desired file count
    filectr += 1
    if filectr > FILELIMIT:
        break

    # Store ImageID in variable
    imageid = int(fecfile.replace(RPTSVDIR, '').replace('.fec', ''))

    # Move file to hold directory if it's a known bad file
    if imageid in BADREPORTS:
        os.rename(fecfile, fecfile.replace(RPTSVDIR, RPTHOLDDIR))
        continue

    # Extract file header
    filehdr = linecache.getline(fecfile, 1)

    # Headers in versions 1 and 2 are multiple lines
    # If first line contains /* Header, it's an old style header
    x = 2
    if filehdr.lower().find('/* header') != -1:
        filehdr = filehdr.replace('/* Header', '').replace('/* header', '').replace('/* HEADER', '').strip()
        flg = 0
        while flg == 0:
            y = linecache.getline(fecfile, x)
            if y.lower().find('/* end header') == -1:
                filehdr = filehdr + '\n' + y.strip()
            else:
                flg = 1
            x += 1

    # Extract report header
    rpthdr = linecache.getline(fecfile, x)

    # Clear linecache
    linecache.clearcache()

    # Change file delimiter to commas if ASCII-28 not found in report header
    if not SRCDELIMITER in rpthdr:
        SRCDELIMITER = ','

    # Extract report type from report header
    fullrpttype = rpthdr[:rpthdr.find(SRCDELIMITER)].lstrip(' "').rstrip(' "')
    rpttype = fullrpttype.rstrip('ANT')

    # If report type not supported, move file to Hold directory
    # and proceed to next file; otherwise retrieve header version
    if rpttype not in rpttypes:
        os.rename(fecfile, fecfile.replace(RPTSVDIR, RPTHOLDDIR))
        continue
    else:
        hdrver = ''
        if filehdr.lower().find('fec_ver_#') != -1:  # FEC_VER_#, FEC_Ver_#
            hdrver = filehdr[filehdr.lower().find('fec_ver_#') + 9:].lstrip(' =')
            hdrver = float(hdrver[:hdrver.find('\n')].strip(' "'))
        else:
            hdrver = float(filehdr.split(SRCDELIMITER)[2].strip(' "'))

    # Now that we know the form type and header version, we are going
    # to build the header data row to insert into the database.

    # First, fetch file headers. Custom code needed for versions 1 and 2.
    filehdrdata = {'ImageID': imageid,
                   'RecType': 'HDR',
                   'EFType': 'FEC',
                   'Ver': hdrver,
                   'SftNm': '',
                   'SftVer': '',
                   'RptID': '',
                   'RptNbr': '0',
                   'HdrCmnt': '',
                   'NmDelim': '',
                   'DecNoDec': 'DEC',
                   'DtFmt': 'CCYYMMDD'}

    if hdrver < 3.0:
        # Custom code for multiline headers (versions 1 and 2)
        # Set default name delimiter to ^
        filehdrdata['NmDelim'] = '^'
        filehdr = filehdr.split('\n')
        for hdr in filehdr:
            line = hdr.strip()
            if line.lower().startswith('soft_name'):
                filehdrdata['SftNm'] = line[line.find('=') + 1:].strip(' "')
            elif line.lower().startswith('soft_ver'):
                filehdrdata['SftVer'] = line[line.find('=') + 1:].strip(' "')
            elif line.lower().startswith('control'):
                filehdrdata['RptID'] = line[line.find('=') + 1:].strip(' "')
            elif line.lower().startswith('namedelim'):
                filehdrdata['NmDelim'] = line[line.find('=') + 1:].strip(' "')
            elif line.lower().startswith('dec/nodec'):
                filehdrdata['DecNoDec'] = line[line.find('=') + 1:].strip(' "')
            elif line.lower().startswith('date_fmat'):
                filehdrdata['DtFmt'] = line[line.find('=') + 1:].strip(' "')
            elif line.lower().find('comment') != -1:
                filehdrdata['HdrCmnt'] = line[line.find('=') + 1:].strip(' "')

    else:
        rowhdrs = get_row_headers('Hdr', hdrver)

        # Parse file header row
        filehdr = parse_data_row(filehdr, SRCDELIMITER)

        # Iterate through file header row and populate header dictionary
        for x in range(len(rowhdrs)):
            if rowhdrs[x] in filehdrdata.keys() and x < len(
                    filehdr):  # Checking len because sometimes header comment omitted
                filehdrdata[rowhdrs[x]] = filehdr[x].strip().replace(OUTPUTDELIMITER, ' ').strip(' "\n')

    # First, change hdrver to int when < 4
    if hdrver < 4:
        hdrver = int(hdrver)

    # Get output headers
    rpthdrdata = {}
    for hdr in outputhdrs[rpttype]:
        rpthdrdata[hdr] = ''

    # Get headers for report header row
    rowhdrs = get_row_headers(rpttype, hdrver)

    # Parse report header row
    rpthdr = parse_data_row(rpthdr, SRCDELIMITER)

    # Iterate through report header row and populate report header dictionary
    for x in range(len(rowhdrs)):
        if rowhdrs[x] in rpthdrdata.keys() and x < len(
                rpthdr):  # 100235 (F3X, v5.0) missing last 12 cols after treas sign date
            rpthdrdata[rowhdrs[x]] = rpthdr[x].strip().replace(OUTPUTDELIMITER, ' ').strip(' "\n')

    # Attempt to determine name delimiter if missing
    if filehdrdata['NmDelim'] == '':
        if 'TrsFullName' in rpthdrdata.keys():
            if rpthdrdata['TrsFullName'].find('^') != -1:
                filehdrdata['NmDelim'] = '^'
            elif rpthdrdata['TrsFullName'].find(',') != -1:
                filehdrdata['NmDelim'] = ','

    # Call function to verify data is valid, then load into database
    sqlresult = 0
    if rpttype == 'F3':
        rpthdrdata = check_rpt_hdrs_f3(imageid, rpthdrdata, filehdrdata['NmDelim'], filehdrdata['DtFmt'])
        sqlresult = load_rpt_hdrs(rpttype, imageid, rpthdrdata, filehdrdata, outputhdrs[rpttype], DBCONNSTR)
    elif rpttype == 'F3L':
        rpthdrdata = check_rpt_hdrs_f3l(imageid, rpthdrdata, filehdrdata['NmDelim'], filehdrdata['DtFmt'])
        sqlresult = load_rpt_hdrs(rpttype, imageid, rpthdrdata, filehdrdata, outputhdrs[rpttype], DBCONNSTR)
    elif rpttype == 'F3P':
        rpthdrdata = check_rpt_hdrs_f3p(imageid, rpthdrdata, filehdrdata['NmDelim'], filehdrdata['DtFmt'])
        sqlresult = load_rpt_hdrs(rpttype, imageid, rpthdrdata, filehdrdata, outputhdrs[rpttype], DBCONNSTR)
    elif rpttype == 'F3X':
        rpthdrdata = check_rpt_hdrs_f3x(imageid, rpthdrdata, filehdrdata['NmDelim'], filehdrdata['DtFmt'])
        sqlresult = load_rpt_hdrs(rpttype, imageid, rpthdrdata, filehdrdata, outputhdrs[rpttype], DBCONNSTR)
    elif rpttype == 'F1':
        rpthdrdata = check_rpt_hdrs_f1(imageid, rpthdrdata, filehdrdata['NmDelim'], filehdrdata['DtFmt'])
        sqlresult = load_rpt_hdrs(rpttype, imageid, rpthdrdata, filehdrdata, outputhdrs[rpttype], DBCONNSTR)

    # On error, move file to Review directory
    if sqlresult == -1:
        shutil.move(fecfile, fecfile.replace(RPTSVDIR, RPTRVWDIR))
        continue
    elif sqlresult == -2:
        shutil.move(fecfile, fecfile.replace(RPTSVDIR, RPTRVWDIR))
        continue

    # ITERATE OVER DATA ROWS
    # ----------------------
    # Because some headers are multiple lines, create a flag to look for
    # the report header and ignore all rows before finding a line that
    # begins with the report type.
    with open(fecfile, 'rb') as datafile:
        # Create header flag and lists to house output data
        hdrflg = 0
        otherdata = []
        scheda = []
        schedb = []
        schedc = []
        schedc1 = []
        schedc2 = []
        schedd = []
        schede = []
        schedf = []
        schedh1 = []
        schedh2 = []
        schedh3 = []
        schedh4 = []
        schedh5 = []
        schedh6 = []
        schedi = []
        schedl = []
        text = []
        f1s = []

        # Iterate through the file
        linenbr = 0
        for line in datafile:
            linenbr += 1
            # Skip blank lines
            if line.strip() == '':
                continue

            # Create list to house this line's data
            data = []

            # Do some basic whitespace cleanup
            # If OUTPUTDELIMITER is tab, change all tabs and newlines to spaces
            if OUTPUTDELIMITER == '\t':
                line = line.expandtabs(1).replace('\r', ' ').strip()

            # Remove all instances of two spaces
            while '  ' in line:
                line = line.replace('  ', ' ')

            # Convert line to list
            data = parse_data_row(line, SRCDELIMITER)

            # If hdrflag == 0, see if this is header line; if not, continue
            if hdrflg == 0:
                if data[0] == rpthdrdata['FormTp'].strip(" '"):
                    hdrflg = 1
                continue

            # This is a data row. Determine row's form type.
            # Additional coding is necessary for Text, the three types
            # of Schedule C forms and the six types of Schedule H forms.
            formtype = ''
            if data[0].startswith('SC1'):
                formtype = 'SC1'
            elif data[0].startswith('SC2'):
                formtype = 'SC2'
            elif data[0].startswith('SC'):
                formtype = 'SC'
            elif data[0].startswith('H1'):
                formtype = 'H1'
            elif data[0].startswith('H2'):
                formtype = 'H2'
            elif data[0].startswith('H3'):
                formtype = 'H3'
            elif data[0].startswith('H4'):
                formtype = 'H4'
            elif data[0].startswith('H5'):
                formtype = 'H5'
            elif data[0].startswith('H6'):
                formtype = 'H6'
            elif data[0].lower() == 'text':  # Sometimes not ALLCAPS
                formtype = 'TEXT'
            elif data[0].startswith('F1S'):
                formtype = 'F1S'
            else:
                for key in outputhdrs.keys():
                    if data[0].startswith(key):
                        formtype = key
                        continue

            # Write the row to the other data file if row's form type not found
            # and skip to next line
            if formtype == '':
                otherdata.append(str(imageid) + OUTPUTDELIMITER + str(hdrver) + OUTPUTDELIMITER + 'line: ' + str(
                    linenbr) + OUTPUTDELIMITER + line + '\r')
                continue

            # Make local copy of output headers
            linehdrs = outputhdrs[formtype][:]

            # Build output dictionary to house data
            linedata = {}
            for hdr in linehdrs:
                linedata[hdr] = ''

            # Get headers for data row
            rowhdrs = get_row_headers(formtype, hdrver)

            # Write the row to the other data file if no headers found
            if rowhdrs == []:
                otherdata.append(str(imageid) + OUTPUTDELIMITER + str(hdrver) + OUTPUTDELIMITER + 'line: ' + str(
                    linenbr) + OUTPUTDELIMITER + line + '\r')
                continue

            # Populate data row dictionary
            linedata = populate_data_row_dict(data, rowhdrs, linedata)

            # Call function to verify data is valid before loading into database
            if formtype == 'SA':
                # Validate data
                linedata = check_row_data_sch_a(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                filehdrdata['DtFmt'])
                # Remove full name fields
                linehdrs.remove('ContFullName')
                linehdrs.remove('DonorCandFullName')
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                scheda.append(data)
            elif formtype == 'SB':
                # Validate data
                linedata = check_row_data_sch_b(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                filehdrdata['DtFmt'])
                # Remove full name fields
                linehdrs.remove('PayeeFullName')
                linehdrs.remove('BenCandFullName')
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedb.append(data)
            elif formtype == 'SC':
                # Validate data
                linedata = check_row_data_sch_c(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                filehdrdata['DtFmt'])
                # Remove full name fields
                linehdrs.remove('LenderFullName')
                linehdrs.remove('LenderCandFullName')
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedc.append(data)
            elif formtype == 'SC1':
                # Validate data
                linedata = check_row_data_sch_c1(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                 filehdrdata['DtFmt'])
                # Remove full name fields
                linehdrs.remove('LendRepFullName')
                linehdrs.remove('TrsFullName')
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedc1.append(data)
            elif formtype == 'SC2':
                linedata = check_row_data_sch_c2(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                 filehdrdata['DtFmt'])
                # Remove full name fields
                linehdrs.remove('GuarFullName')
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedc2.append(data)
            elif formtype == 'SD':
                # No full name fields in data dictionary
                # Validate data
                linedata = check_row_data_sch_d(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                filehdrdata['DtFmt'])
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedd.append(data)
            elif formtype == 'SE':
                # Validate data
                linedata = check_row_data_sch_e(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                filehdrdata['DtFmt'])
                # Remove full name fields
                linehdrs.remove('PayeeFullName')
                linehdrs.remove('SupOppCandFullName')
                linehdrs.remove('CompFullName')
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schede.append(data)
            elif formtype == 'SF':
                # Validate data
                linedata = check_row_data_sch_f(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                filehdrdata['DtFmt'])
                # Remove full name fields
                linehdrs.remove('PayeeFullName')
                linehdrs.remove('PayeeCandFullName')
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedf.append(data)
            elif formtype == 'H1':
                # No full name fields in data dictionary
                # Validate data
                linedata = check_row_data_sch_h1(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                 filehdrdata['DtFmt'])
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedh1.append(data)
            elif formtype == 'H2':
                # No full name fields in data dictionary
                # Validate data
                linedata = check_row_data_sch_h2(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                 filehdrdata['DtFmt'])
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedh2.append(data)
            elif formtype == 'H3':
                # No full name fields in data dictionary
                # Validate data
                linedata = check_row_data_sch_h3(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                 filehdrdata['DtFmt'])
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedh3.append(data)
            elif formtype == 'H4':
                # Validate data
                linedata = check_row_data_sch_h4(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                 filehdrdata['DtFmt'])
                # Remove full name fields
                linehdrs.remove('PayeeFullName')
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedh4.append(data)
            elif formtype == 'H5':
                # No full name fields in data dictionary
                # Validate data
                linedata = check_row_data_sch_h5(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                 filehdrdata['DtFmt'])
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedh5.append(data)
            elif formtype == 'H6':
                # Validate data
                linedata = check_row_data_sch_h6(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                 filehdrdata['DtFmt'])
                # Remove full name fields
                linehdrs.remove('PayeeFullName')
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedh6.append(data)
            elif formtype == 'SI':
                # No full name fields in data dictionary
                # Validate data
                linedata = check_row_data_sch_i(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                filehdrdata['DtFmt'])
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedi.append(data)
            elif formtype == 'SL':
                # No full name fields in data dictionary
                # Validate data
                linedata = check_row_data_sch_l(linedata, imageid, linenbr, filehdrdata['NmDelim'],
                                                filehdrdata['DtFmt'])
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                schedl.append(data)
            elif formtype == 'TEXT':
                # No full name fields in data dictionary
                # Validate data
                linedata = check_row_data_text(linedata, imageid, linenbr, filehdrdata['NmDelim'], filehdrdata['DtFmt'])
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, fullrpttype)
                text.append(data)
            elif formtype == 'F1S':
                # Validate data
                linedata = check_row_data_f1s(linedata, imageid, linenbr, filehdrdata['NmDelim'], filehdrdata['DtFmt'])
                # Remove full name fields
                linehdrs.remove('AgtFullName')
                # Create list for the data row
                data = build_data_row(linedata, linehdrs, imageid, None)
                f1s.append(data)

        # Write data to files
        if len(otherdata) > 0:
            with open(otherdatafile, 'a+b') as outputfile:
                for row in otherdata:
                    outputfile.write(row)

        if len(scheda) > 0:
            with open(schedafile, 'a+b') as outputfile:
                for row in scheda:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedb) > 0:
            with open(schedbfile, 'a+b') as outputfile:
                for row in schedb:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedc) > 0:
            with open(schedcfile, 'a+b') as outputfile:
                for row in schedc:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedc1) > 0:
            with open(schedc1file, 'a+b') as outputfile:
                for row in schedc1:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedc2) > 0:
            with open(schedc2file, 'a+b') as outputfile:
                for row in schedc2:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedd) > 0:
            with open(scheddfile, 'a+b') as outputfile:
                for row in schedd:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schede) > 0:
            with open(schedefile, 'a+b') as outputfile:
                for row in schede:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedf) > 0:
            with open(schedffile, 'a+b') as outputfile:
                for row in schedf:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedh1) > 0:
            with open(schedh1file, 'a+b') as outputfile:
                for row in schedh1:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedh2) > 0:
            with open(schedh2file, 'a+b') as outputfile:
                for row in schedh2:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedh3) > 0:
            with open(schedh3file, 'a+b') as outputfile:
                for row in schedh3:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedh4) > 0:
            with open(schedh4file, 'a+b') as outputfile:
                for row in schedh4:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedh5) > 0:
            with open(schedh5file, 'a+b') as outputfile:
                for row in schedh5:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedh6) > 0:
            with open(schedh6file, 'a+b') as outputfile:
                for row in schedh6:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedi) > 0:
            with open(schedifile, 'a+b') as outputfile:
                for row in schedi:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(schedl) > 0:
            with open(schedlfile, 'a+b') as outputfile:
                for row in schedl:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(text) > 0:
            with open(textfile, 'a+b') as outputfile:
                for row in text:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

        if len(f1s) > 0:
            with open(f1sfile, 'a+b') as outputfile:
                for row in f1s:
                    outputfile.write(OUTPUTDELIMITER.join(map(str, row)) + '\r')

    # Move the file to the processed directory
    shutil.move(fecfile, fecfile.replace(RPTSVDIR, RPTPROCDIR))
    continue

# Run stored procedure to deactivate overlapping reports
# not covered by database triggers
try:
    sql = 'EXEC dbo.usp_DeactivateOverlappingReports'

    # Create SQL Server connection
    conn = pyodbc.connect(DBCONNSTR)
    cursor = conn.cursor()

    # Excecute stored procedure
    cursor.execute(sql)
    conn.commit()
    conn.close()
except:
    pass
