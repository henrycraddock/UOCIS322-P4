"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

# Global dicts for min and max speeds
MIN_SPEEDS = {200: 15, 400: 15, 600: 15, 1000: 11.428}
MAX_SPEEDS = {200: 34, 400: 32, 600: 30, 1000: 28}


def convert_to_time(dist, speed):
    """Helper function that takes distance and speed values and returns time in hours and minutes"""
    dec = str(dist / speed)
    dec = dec.split('.')
    hour = int(dec[0])
    min = int(round(float('.' + dec[1]) * 60))
    return [hour, min]


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    # Set function variables and truncate distance
    hrs = 0
    mins = 0
    time_open = brevet_start_time
    control_dist_km = round(control_dist_km)

    # Check if control distance is suitable for the brevet
    if brevet_dist_km < control_dist_km <= brevet_dist_km * 1.2:
        control_dist_km = brevet_dist_km
    elif control_dist_km > brevet_dist_km * 1.2:
        raise ValueError
    elif control_dist_km < 0:
        raise ValueError

    # Perform checks on control distance to determine proper times
    if 600 < control_dist_km <= 1000:
        km_200 = convert_to_time(200, MAX_SPEEDS[200])
        km_400 = convert_to_time(200, MAX_SPEEDS[400])
        km_600 = convert_to_time(200, MAX_SPEEDS[600])
        km_1000 = convert_to_time(control_dist_km - 600, MAX_SPEEDS[1000])
        hrs = km_200[0] + km_400[0] + km_600[0] + km_1000[0]
        mins = km_200[1] + km_400[1] + km_600[1] + km_1000[1]
    elif 400 < control_dist_km <= 600:
        km_200 = convert_to_time(200, MAX_SPEEDS[200])
        km_400 = convert_to_time(200, MAX_SPEEDS[400])
        km_600 = convert_to_time(control_dist_km - 400, MAX_SPEEDS[600])
        hrs = km_200[0] + km_400[0] + km_600[0]
        mins = km_200[1] + km_400[1] + km_600[1]
    elif 200 < control_dist_km <= 400:
        km_200 = convert_to_time(200, MAX_SPEEDS[200])
        km_400 = convert_to_time(control_dist_km - 200, MAX_SPEEDS[400])
        hrs = km_200[0] + km_400[0]
        mins = km_200[1] + km_400[1]
    elif 0 < control_dist_km <= 200:
        km_200 = convert_to_time(control_dist_km, MAX_SPEEDS[200])
        hrs = km_200[0]
        mins = km_200[1]
    elif control_dist_km == 0:
        hrs = 0
        mins = 0

    time_open = time_open.shift(hours=hrs, minutes=mins)
    return time_open


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
        control_dist_km:  number, control distance in kilometers
        brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600,
          or 1000 (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    # Set function variables and truncate distance
    hrs = 0
    mins = 0
    time_close = brevet_start_time
    control_dist_km = round(control_dist_km)

    # Check if control distance is suitable for the brevet
    if brevet_dist_km < control_dist_km <= brevet_dist_km * 1.2:
        control_dist_km = brevet_dist_km
    elif control_dist_km > brevet_dist_km * 1.2:
        raise ValueError
    elif control_dist_km < 0:
        raise ValueError

    # Perform checks on control distance to determine proper times
    # This first check is to determine if the current control is the final control,
    # and if so, then the proper closing time is assigned, according to https://en.m.wikipedia.org/wiki/Randonneuring
    if control_dist_km == brevet_dist_km:
        if control_dist_km == 200:
            hrs = 13
            mins = 30
        elif control_dist_km == 300:
            hrs = 20
            mins = 0
        elif control_dist_km == 400:
            hrs = 27
            mins = 0
        elif control_dist_km == 600:
            hrs = 40
            mins = 0
        elif control_dist_km == 1000:
            hrs = 75
            mins = 0
    else:
        # If it is not the final control, preform normal checks
        if 600 < control_dist_km <= 1000:
            km_600 = convert_to_time(600, MIN_SPEEDS[600])
            km_1000 = convert_to_time(control_dist_km - 600, MIN_SPEEDS[1000])
            hrs = km_600[0] + km_1000[0]
            mins = km_600[1] + km_1000[1]
        # The 200, 400, and 600 km ranges can be put into one check since they have the same minimum speed
        elif 60 < control_dist_km <= 600:
            km_600 = convert_to_time(control_dist_km, MIN_SPEEDS[600])
            hrs = km_600[0]
            mins = km_600[1]
        # The following is for the French variation of controls under 60 km
        elif 0 < control_dist_km <= 60:
            km_60 = convert_to_time(control_dist_km, 20)
            hrs = km_60[0] + 1
            mins = km_60[1]
        elif control_dist_km == 0:
            hrs = 1
            mins = 0

    time_close = time_close.shift(hours=hrs, minutes=mins)
    return time_close
