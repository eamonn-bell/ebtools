# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 17:37:15 2023

@author: Eamonn.Bell
"""

# =============================================================================
# ---- UK Bank Holidays
# =============================================================================

# Maintain a list of UK Bank Holidays here.
#
# The official source for UK Bank Holidays is:
# https://www.gov.uk/bank-holidays
# At this gov.uk site the list of UK bank holidays is available from 2016
# to one year ahead of the current year. 
#
# For Bank Holidays ahead of the current and next year, dates are gathered
# from the Gottex multi-year calendar. A version is available here:
# https://vdocuments.site/gottex-calendar.html
# These dates should be indicated as being 'Unconfirmed' and should be 
# confirmed closer to realtime via the gov.uk website above.

uk_bank_hols = [
    # Confirmed
    '2016-01-01',
    '2016-03-25',
    '2016-03-28',
    '2016-05-02',
    '2016-05-30',
    '2016-08-29',
    '2016-12-26',
    '2016-12-27',
    
    # Confirmed
    '2017-01-02',
    '2017-04-14',
    '2017-04-17',
    '2017-05-01',
    '2017-05-29',
    '2017-08-28',
    '2017-12-25',
    '2017-12-26',    
    
    # Confirmed
    '2018-01-01',
    '2018-03-30',
    '2018-04-02',
    '2018-05-07',
    '2018-05-28',
    '2018-08-27',
    '2018-12-25',
    '2018-12-26',
    
    # Confirmed
    '2019-01-01',
    '2019-04-19',
    '2019-04-22',
    '2019-05-06',
    '2019-05-27',
    '2019-08-26',
    '2019-12-25',
    '2019-12-26',
    
    # Confirmed
    '2020-01-01',
    '2020-04-10',
    '2020-04-13',
    '2020-05-08',
    '2020-05-25',
    '2020-08-31',
    '2020-12-25',
    '2020-12-28',
    
    # Confirmed
    # 2021 Bank Holiday days with description to compare with 2022.
    '2021-01-01',  # New Year's Day
    '2021-04-02',  # Good Friday
    '2021-04-05',  # Easter Monday
    '2021-05-03',  # Early May Bank Holiday
    '2021-05-31',  # Spring Bank Holiday
    '2021-08-30',  # Summer Bank Holiday
    '2021-12-27',  # Christmas Day (substitute day)
    '2021-12-28',  # Boxing Day (substitute day)
    
    # Confirmed
    # 2022 will have TWO EXTRA BANK HOLIDAYS - Queen's Platinum Jubilee Year
    '2022-01-03',  # New Year's Day  
    '2022-04-15',  # Good Friday
    '2022-04-18',  # Easter Monday
    '2022-05-02',  # Early May Bank Holiday
    '2022-06-02',  # Spring Bank Holiday
    '2022-06-03',  # Platinum Jubilee Bank Holiday  <--- EXTRA BANK HOLIDAY
    '2022-08-29',  # Summer Bank Holiday
    '2022-09-19',  # Queen's State Funeral          <--- EXTRA BANK HOLIDAY
    '2022-12-26',  # Boxing Day
    '2022-12-27',  # Christmas Day (substitute day)
    
    # Confirmed
    # 2023 will have AN EXTRA BANK HOLIDAY - Conronation of Charles III
    '2023-01-02',  # New Year's Day
    '2023-04-07',  # Good Friday
    '2023-04-10',  # Easter Monday
    '2023-05-01',  # Early May Bank Holiday
    '2023-05-08',  # Bank Holiday for the coronation of King Charles III <--- EXTRA BANK HOLIDAY
    '2023-05-29',  # Spring Bank Holiday
    '2023-08-28',  # Summer Bank Holiday
    '2023-12-25',  # Christmas Day
    '2023-12-26',  # Boxing Day

    # Confirmed
    '2024-01-01',  # New Year's Day
    '2024-03-29',  # Good Friday
    '2024-04-01',  # Easter Monday
    '2024-05-06',  # Early May Bank Holiday
    '2024-05-27',  # Spring Bank Holiday
    '2024-08-26',  # Summer Bank Holiday
    '2024-12-25',  # Christmas Day
    '2024-12-26',  # Boxing Day

    # Confirmed
    '2025-01-01',  # New Year's Day
    '2025-04-18',  # Good Friday
    '2025-04-21',  # Easter Monday
    '2025-05-05',  # Early May Bank Holiday
    '2025-05-26',  # Spring Bank Holiday
    '2025-08-25',  # Summer Bank Holiday
    '2025-12-25',  # Christmas Day
    '2025-12-26',  # Boxing Day

    ## Unconfirmed
    '2026-01-01',
    '2026-04-03',
    '2026-04-06',
    '2026-05-04',
    '2026-05-25',
    '2026-08-31',
    '2026-12-25',
    '2026-12-28',

    ## Unconfirmed
    '2027-01-01',
    '2027-03-26',
    '2027-03-29',
    '2027-05-03',
    '2027-05-21',
    '2027-08-30',
    '2027-12-27',
    '2027-12-28',

    ## Unconfirmed
    '2028-01-03',
    '2028-04-14',
    '2028-04-17',
    '2028-05-01',
    '2028-05-29',
    '2028-08-28',
    '2028-12-25',
    '2028-12-26',

    ## Unconfirmed
    '2029-01-01',
    '2029-03-30',
    '2029-04-02',
    '2029-05-07',
    '2029-05-28',
    '2029-08-27',
    '2029-12-25',
    '2029-12-26',

    ## Unconfirmed
    '2030-01-01',
    '2030-04-19',
    '2030-04-22',
    '2030-05-06',
    '2030-05-27',
    '2030-08-26',
    '2030-12-25',
    '2030-12-26'
    ]