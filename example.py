import datetime
import json
import pytz
import sys
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
    t = []
    i = 0
    while i < len(answer):
        the_tithi = answer[i]
        end = _panchanga_endtime_to_datetime(answer[i+1], time)
        t += [[the_tithi, end]]
        i += 2
    return t 


def nakshatra(time, place):
    jd = panchanga.gregorian_to_jd(time)
    answer = panchanga.nakshatra(jd, place)
    n = []
    i = 0
    while i < len(answer):
        the_nakshatra = answer[i]
        end = _panchanga_endtime_to_datetime(answer[i+1], time)
        n += [[the_nakshatra, end]]
        i += 2

    return n


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


def solar_month(time, place):
    jd = panchanga.gregorian_to_jd(time)
    ti = panchanga.tithi(jd, place)[0]
    critical = panchanga.sunrise(jd, place)[0]  # - tz/24 ?
    last_new_moon = panchanga.new_moon(critical, ti, -1)
    this_solar_month = panchanga.raasi(last_new_moon)
    return this_solar_month


if __name__ == "__main__":
    city_name = sys.argv[1]
    ymd = datetime.datetime.strptime(sys.argv[2], '%Y%m%d')
    # Use mid-day.
    ymd = ymd.replace(hour=12)

    f = open("sanskrit_names.json")
    names = json.load(f)

    c = open('cities.json')
    cities = json.load(c)

    the_city = cities[city_name]
    timezone = pytz.timezone(the_city['timezone'])
    ymd_tz = timezone.localize(ymd)

    now = ymd_tz
    print(city_name, "at", ymd_tz)
    tz_offset = timezone.utcoffset(datetime.datetime.utcnow()).seconds / 60 / 60
    place = panchanga.Place(the_city['latitude'], the_city['longitude'], tz_offset)

    print("Samvatsara", names["samvats"][str(samvatsara(now, place))])
    print("Ritu", names["ritus"][str(ritu(now, place))])
    m = maasa(now, place)
    print("Maasa", names["masas"][str(m[0])], "adhika" if m[1] else "")
    print("Solar month", names["raasis"][str(solar_month(now, place))])
    print("Raasi", names["raasis"][str(raasi(now))])
    tithis = tithi(now, place)
    for t in tithis:
        print("Tithi", names["tithis"][str(t[0])], "ends", t[1])
    print("Vaara", names["varas"][str(vaara(now))])
    nakshatras = nakshatra(now, place)
    for n in nakshatras:
        print("Nakshatra", names["nakshatras"][str(n[0])], "ends", n[1])

    print("Sunrise", sunrise(now, place))
    print("Sunset", sunset(now, place))
    # print("Moonrise", moonrise(now, place))
    # print("Moonset", moonset(now, place))
