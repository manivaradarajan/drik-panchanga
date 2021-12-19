import datetime
import json
import pytz
import swisseph as swe
import tzlocal

import panchanga

def _panchanga_date_to_datetime(date, base_datetime):
    # The input date and time elements in the tuple are expressed as floats.
    # Convert the float hour into integer hours, minutes and seconds.
    hour, second = divmod(date[3] * 60, 3600)
    minute, second = divmod(second, 60)
    return base_datetime.replace(hour=int(hour), minute=int(minute), second=int(second))


def _panchanga_endtime_to_datetime(endtime, base_datetime):
    hour, minute, second = endtime
    d = base_datetime
    if hour > 23:
        d = d + datetime.timedelta(days=1)
        hour -= 24
    return d.replace(hour=hour, minute=minute, second=minute)


def sunrise(time, place):
    jd = panchanga.gregorian_to_jd(time)
    sunrise_jd, _ = panchanga.sunrise(jd, place)
    d = panchanga.jd_to_gregorian(sunrise_jd)
    return _panchanga_date_to_datetime(d, time)


def sunset(time, place):
    jd = panchanga.gregorian_to_jd(time)
    sunset_jd, _ = panchanga.sunset(jd, place)
    d = panchanga.jd_to_gregorian(sunset_jd)
    return _panchanga_date_to_datetime(d, time)


def moonrise(time, place):
    jd = panchanga.gregorian_to_jd(time)
    moonrise_jd, _ = panchanga.moonrise(jd, place)
    d = panchanga.jd_to_gregorian(moonrise_jd)
    return _panchanga_date_to_datetime(d, time)


def moonset(time, place):
    jd = panchanga.gregorian_to_jd(time)
    moonset_jd, _ = panchanga.moonset(jd, place)
    d = panchanga.jd_to_gregorian(moonset_jd)
    return _panchanga_date_to_datetime(d, time)



def tithi(time, place):
    jd = panchanga.gregorian_to_jd(time)
    answer = panchanga.tithi(jd, place)
    t = answer[0]
    end = answer[1]
    # TODO: handle leap tithis
    return t, _panchanga_endtime_to_datetime(end, time)


def nakshatra(time, place):
    jd = panchanga.gregorian_to_jd(time)
    n, end = panchanga.nakshatra(jd, place)
    return n, _panchanga_endtime_to_datetime(end, time)


def vaara(time):
    jd = panchanga.gregorian_to_jd(time)
    return panchanga.vaara(jd)


def maasa(time, place):
    jd = panchanga.gregorian_to_jd(time)
    return panchanga.masa(jd, place)


def samvatsara(time, place):
    jd = panchanga.gregorian_to_jd(time)
    m = panchanga.masa(jd, place)
    return panchanga.samvatsara(jd, m[0])


def ritu(time, place):
    jd = panchanga.gregorian_to_jd(time)
    m = panchanga.masa(jd, place)
    return panchanga.ritu(m[0])


def raasi(time):
    jd = panchanga.gregorian_to_jd(time)
    # For some reason, raasi is 1-based and not 0-based.
    return panchanga.raasi(jd) - 1


if __name__ == "__main__":
    f = open('sanskrit_names.json')
    names = json.load(f)

    local_tz = tzlocal.get_localzone()
    #print(local_tz)
    now = datetime.datetime.now(local_tz) #- datetime.timedelta(days=30*8)
    print("Calculating for", now)
    tz_offset = local_tz.utcoffset(now).total_seconds()/60/60
    palo_alto = panchanga.Place(37.468319, -122.143936, tz_offset)

    print("Samvatsara", names['samvats'][str(samvatsara(now, palo_alto))])
    m = maasa(now, palo_alto)
    print("Maasa", names['masas'][str(m[0])], 'adhika' if m[1] else '')
    print("Ritu", names['ritus'][str(ritu(now, palo_alto))])
    t = tithi(now, palo_alto)
    print("Tithi", names['tithis'][str(t[0])], 'ends', t[1])
    print("Vaara", names['varas'][str(vaara(now))])
    n = nakshatra(now, palo_alto)
    print("Nakshatra", names['nakshatras'][str(n[0])], 'ends', n[1])
    r = raasi(now)
    print("Raasi", names['raasis'][str(r)])

    print("Sunrise", sunrise(now, palo_alto))
    print("Sunset", sunset(now, palo_alto))
    #print("Moonrise", moonrise(now, palo_alto))
    #print("Moonset", moonset(now, palo_alto))





