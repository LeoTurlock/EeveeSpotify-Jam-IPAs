"""Prepends a version to the only app in an AltStore/Feather source (apps.json)."""
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("source")
parser.add_argument("--version", required=True)
parser.add_argument("--date", required=True)
parser.add_argument("--size", type=int, required=True)
parser.add_argument("--url", required=True)
parser.add_argument("--notes", required=True)
parser.add_argument("--min-os", required=True)
args = parser.parse_args()

with open(args.source) as f:
    source = json.load(f)

app = source["apps"][0]
entry = {
    "version": args.version,
    "date": args.date,
    "size": args.size,
    "downloadURL": args.url,
    "localizedDescription": args.notes,
    "minOSVersion": args.min_os,
}
app["versions"] = [v for v in app.get("versions", []) if v["version"] != args.version]
app["versions"].insert(0, entry)

# Older clients only read these top-level fields.
app["version"] = entry["version"]
app["versionDate"] = entry["date"]
app["versionDescription"] = entry["localizedDescription"]
app["downloadURL"] = entry["downloadURL"]
app["size"] = entry["size"]

with open(args.source, "w") as f:
    json.dump(source, f, indent=2, ensure_ascii=False)
    f.write("\n")
