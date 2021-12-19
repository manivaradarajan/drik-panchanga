import datetime
import pytz
import swisseph as swe
import tzlocal

import panchanga

def sunrise(time, place):
    jd = panchanga.gregorian_to_jd(time)
    sunrise_jd, _ = panchanga.sunrise(jd, place)
    d = panchanga.jd_to_gregorian(sunrise_jd)

    # TODO: convert to utility function
    # Time is expressed as a float. Split into hours, minutes and seconds and
    # convert to integer.
    time = d[3]
    hours, seconds = divmod(time * 60, 3600)
    minutes, seconds = divmod(seconds, 60)
    sd = [int(_) for _ in d]
    sd[3] = int(hours)
    sd += [int(minutes), int(seconds)]
    # TODO: Extract timezone from input time and attach to datetime object.
    return datetime.datetime(*sd)


def tithi(time, place):
    jd = panchanga.gregorian_to_jd(time)
    t, end = panchanga.tithi(jd, place)
    hour = end[0]
    # The tithi may end on the next day. In this case the return tuple expresses
    # the hour as a value greater than 23 which is disallowed by Python's datetime.
    # Do the math to adjust.
    if hour > 23:
        d = datetime.timedelta(days=1)
        hour -= 24
    d = time.replace(hour=hour, minute=end[1], second=end[2])
    return t, d


if __name__ == "__main__":
    local_tz = tzlocal.get_localzone()
    #print(local_tz)
    now = datetime.datetime.now(local_tz) + datetime.timedelta(days=2)
    #print(now)
    tz_offset = local_tz.utcoffset(now).total_seconds()/60/60
    #print(tz_offset)
    palo_alto = panchanga.Place(37.468319, -122.143936, tz_offset)

    print("Sunrise", sunrise(now, palo_alto))
    print("Tithi", tithi(now, palo_alto))





