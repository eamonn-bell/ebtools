# -*- coding: utf-8 -*-
"""
Created on Wed May 26 17:24:12 2021

@author: Eamonn.Bell
"""

"""
These are standard lists of DATETIME FORMAT codes to check when importing
data from sources with possibly different datetime formats.

=============
Format Codes:
=============
The user may wish to compile their own format code list for usage in 
specific situations. In that case, the user should build a list of 
FORMAT strings based on the set of acceptable python FORMAT CODES to be 
found at the following link under the heading "strftime() and strptime()
Format Codes":
https://docs.python.org/3/library/datetime.html

"""

# Non-timezone-specific dates: the most common datetime occurance
format_list_standard = [
    
    # Year-first date formats
    '%Y-%m-%d',
    '%y-%m-%d',
    
    # Year-first with TIME formats
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M',    
    
    # Day-first formats
    '%d-%m-%y',
    '%d-%b-%y',
    '%d-%b-%Y',
    '%d-%m-%Y', 
    '%d/%m/%Y',
    '%d/%m/%y',
    
    # Datetime formats
    '%d/%m/%Y %H:%M',
    '%d/%m/%Y %H:%M:%S'
    
    ]

# Timezone-specific dates: when there is a timezone element in the datetime
format_list_tz = [
    
    # Format code strings registering ZULU time (GMT)
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%S Z',
    '%Y-%m-%d %H:%M:%SZ',
    '%Y-%m-%d %H:%M:%S Z',
    
    # Format code strings with a UTC OFFSET: +01:00 / -0600 / etc
    '%Y-%m-%dT%H:%M:%S%z',
    '%Y-%m-%dT%H:%M:%S %z',
    '%Y-%m-%d %H:%M:%S%z',
    '%Y-%m-%d %H:%M:%S %z'
    ]

