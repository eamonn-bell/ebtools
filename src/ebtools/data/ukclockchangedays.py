# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 17:36:46 2023

@author: Eamonn.Bell
"""


# =============================================================================
# ---- Clock Change days - DAYLIGHT SAVINGS
# =============================================================================

# Maintain a list of clock change days here.
# The official place to look for clock change days is here:
# https://www.gov.uk/when-do-the-clocks-change
#
# The Daylight Savings Clock Change dates and times can be found as part of 
# the Market Domain Data (MDD) on the Elexon portal page here (may have to be
# logged in):
# www.elexonportal.co.uk/mddviewer
#  
# An alternative source can be found here:
# https://www.timeanddate.com/time/change/uk/london
#
# Clock change dates should be checked against the gov.uk site on a regular
# basis and then set moved to the 'Confirmed' section.


# LAST SUNDAY IN MARCH - These days will have 46 SPs
uk_clock_change_forward  = [
    
    # Confirmed
    '1998-03-29',
    '1999-03-28',
    '2000-03-26',
    '2001-03-25',
    '2002-03-31',
    '2003-03-30',
    '2004-03-28',
    '2005-03-27',
    '2006-03-26',
    '2007-03-25',
    '2008-03-30',
    '2009-03-29',
    '2010-03-28',
    '2011-03-27',
    '2012-03-25',
    '2013-03-31',
    '2014-03-30',
    '2015-03-29',
    '2016-03-27',
    '2017-03-26',
    '2018-03-25',
    '2019-03-31',
    '2020-03-29',
    '2021-03-28',
    '2022-03-27',
    '2023-03-26',
    '2024-03-31',
    '2025-03-30',
    '2026-03-29',
    
    # Unconfirmed
    '2027-03-28',
    '2028-03-26',
    '2029-03-25',    
    '2030-03-31'
    ]

# LAST SUNDAY IN OCTOBER - These days will have 50 SPs
uk_clock_change_backward = [

    # Confirmed
    '1998-10-25',
    '1999-10-31',
    '2000-10-29',
    '2001-10-28',
    '2002-10-27',
    '2003-10-26',
    '2004-10-31',
    '2005-10-30',
    '2006-10-29',
    '2007-10-28',
    '2008-10-26',
    '2009-10-25',
    '2010-10-31',
    '2011-10-30',
    '2012-10-28',
    '2013-10-27',
    '2014-10-26',
    '2015-10-25',
    '2016-10-30',
    '2017-10-29',
    '2018-10-28',
    '2019-10-27',
    '2020-10-25',
    '2021-10-31',
    '2022-10-30',
    '2023-10-29',
    '2024-10-27',
    '2025-10-26',
    '2026-10-25',
    
    # Unconfirmed
    '2027-10-31',
    '2028-10-29',
    '2029-10-28',
    '2030-10-27' 
    ]

