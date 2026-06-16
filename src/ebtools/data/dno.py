# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 14:09:47 2018

@author: Eamonn_Bell
This file contains the set of lists and dictionaries which may be useful.

"""



"""
******************************************************************************
******************************************************************************

# ---- DNO data
                
                 Region Names & GSP Group look-up codes

******************************************************************************
******************************************************************************
"""


# Sources for the names and MPAS Operator IDs for each Licenced Distribution
# Network Owner (LDNO) come from:
#     -- https://en.wikipedia.org/wiki/Distribution_network_operator
#     -- https://www.elexonportal.co.uk/svallf
dno_codes = {
    10 : 'EELC',
    11 : 'EMEB',
    12 : 'LOND',
    13 : 'MANW',
    14 : 'MIDE',
    15 : 'NEEB',
    16 : 'NORW',
    17 : 'HYDE',
    18 : 'SPOW',
    19 : 'SEEB',
    20 : 'SOUT',
    21 : 'SWAE',
    22 : 'SWEB',
    23 : 'YELG',
    24 : 'IPNL',
    25 : 'LENG',
    26 : 'GUCL',
    27 : 'ETCL',
    28 : 'EDFI',
    29 : 'HARL',
    30 : 'PENL',
    31 : 'UKPD',
    32 : 'UDNL',
    33 : 'GGEN',
    34 : 'MPDL',
    35 : 'FEAL',
    36 : 'VATT',
    37 : 'FORB',
    38 : 'INDI'
    }

dno_names = {
    10 : 'Eastern England',
    11 : 'East Midlands',
    12 : 'London',
    13 : 'Merseyside and Northern Wales',
    14 : 'West Midlands',
    15 : 'North Eastern England',
    16 : 'North Western_England',
    17 : 'Northern Scotland',
    18 : 'Southern Scotland',
    19 : 'South Eastern England',
    20 : 'Southern England',
    21 : 'Southern_Wales',
    22 : 'South Western England',
    23 : 'Yorkshire'
    }

dno_to_gsp_group = {
    10 : '_A',
    11 : '_B',
    12 : '_C',
    13 : '_D',
    14 : '_E',
    15 : '_F',
    16 : '_G',
    17 : '_P',
    18 : '_N',
    19 : '_J',
    20 : '_H',
    21 : '_K',
    22 : '_L',
    23 : '_M'
    }










