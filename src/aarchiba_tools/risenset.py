import argparse

import astropy.time
import astropy.units as u

import aarchiba_tools


def main():
    parser = argparse.ArgumentParser(
        description="Compute rise and set times for a source"
    )
    parser.add_argument("source", help="SIMBAD name of the source")
    parser.add_argument(
        "observatory", help="Name of the observatory, tempo2 or astropy"
    )
    parser.add_argument(
        "--mjd", type=float, help="MJD when the rise and set are wanted (default now)"
    )
    parser.add_argument(
        "--elevation_limit",
        type=float,
        default=5.5,
        help="Elevation at which the source sets",
    )
    parser.add_argument("--lst", action="store_true", help="Give results in LST form")
    args = parser.parse_args()

    if args.mjd is None:
        mjd = None
    else:
        mjd = astropy.time.Time(mjd, format="mjd")
    rs = aarchiba_tools.rise_set(
        source=args.source,
        observatory=args.observatory,
        when=mjd,
        elevation_limit=args.elevation_limit * u.deg,
        lst=args.lst,
    )
    if args.lst:
        print("Rise:\t{}".format(rs.rise))
        print("Set:\t{}".format(rs.set))
    else:
        print("Rise:\t{}".format(rs.rise.iso))
        print("Set:\t{}".format(rs.set.iso))
