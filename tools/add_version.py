"""Prepends a build to a Feather source (apps.json).

Same layout as https://repository.apptesters.org/: every build is its own flat entry in `apps`,
newest first, with no AltStore `versions` array.
"""
import argparse
import json

ICON = "https://raw.githubusercontent.com/LeoTurlock/EeveeSpotify-Jam-IPAs/main/icon.png"

parser = argparse.ArgumentParser()
parser.add_argument("source")
parser.add_argument("--name", required=True)
parser.add_argument("--bundle-id", required=True)
parser.add_argument("--version", required=True)
parser.add_argument("--full-date", required=True, help="yyyymmddHHMMSS")
parser.add_argument("--size", type=int, required=True)
parser.add_argument("--url", required=True)
parser.add_argument("--notes", required=True)
args = parser.parse_args()

with open(args.source) as f:
    source = json.load(f)

entry = {
    "name": args.name,
    "type": 1,
    "bundleID": args.bundle_id,
    "bundleIdentifier": args.bundle_id,
    "version": args.version,
    "versionDate": f"{args.full_date[0:4]}-{args.full_date[4:6]}-{args.full_date[6:8]}",
    "fullDate": args.full_date,
    "size": args.size,
    "down": args.url,
    "downloadURL": args.url,
    "developerName": "Leo Turlock",
    "localizedDescription": args.notes,
    "icon": ICON,
    "iconURL": ICON,
}
source["apps"] = [a for a in source["apps"] if a["downloadURL"] != args.url]
source["apps"].insert(0, entry)

with open(args.source, "w") as f:
    json.dump(source, f, indent=4, ensure_ascii=False)
    f.write("\n")
