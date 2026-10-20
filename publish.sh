#!/bin/bash
# Publishes an EeveeSpotify Jam IPA to this Feather source:
#   1. uploads the IPA as a GitHub release asset (IPAs are too big for git)
#   2. adds it as the newest entry in apps.json (flat, one entry per build)
#   3. commits and pushes apps.json
#
# usage: publish.sh <file.ipa> [label] [notes]
#   label  short build name, e.g. JamQueue4 (default: taken from the IPA filename)
#   notes  text shown in Feather for this version
set -euo pipefail
cd "$(dirname "$0")"

[ $# -ge 1 ] || { sed -n 2,9p "$0"; exit 1; }
IPA=$1
[ -f "$IPA" ] || { echo "no such file: $IPA"; exit 1; }
LABEL=${2:-$(basename "$IPA" .ipa | sed -E 's/^EeveeSpotify[-_0-9.]*-?Jam-?//; s/-?unsigned$//')}
LABEL=${LABEL:-Jam}
NOTES=${3:-"EeveeSpotify Jam build: $LABEL"}

REPO=LeoTurlock/EeveeSpotify-Jam-IPAs
WORK=$(mktemp -d /tmp/jam-publish.XXXX)
trap 'rm -rf "$WORK"' EXIT

unzip -q "$IPA" 'Payload/*.app/Info.plist' -d "$WORK"
PLIST=$(find "$WORK/Payload" -maxdepth 2 -name Info.plist | head -1)
SPOTIFY_VERSION=$(/usr/libexec/PlistBuddy -c "Print :CFBundleShortVersionString" "$PLIST")

STAMP=$(date +%Y%m%d.%H%M)
VERSION="$SPOTIFY_VERSION-jam.$STAMP"
TAG="v$VERSION"
ASSET="EeveeSpotify-$SPOTIFY_VERSION-Jam-$LABEL.ipa"
cp "$IPA" "$WORK/$ASSET"

git pull -q --ff-only
gh release create "$TAG" "$WORK/$ASSET" --repo "$REPO" \
    --title "$SPOTIFY_VERSION Jam – $LABEL" --notes "$NOTES"

/usr/bin/python3 -I tools/add_version.py apps.json \
    --name "EeveeSpotify Jam ($LABEL)" \
    --bundle-id "$(/usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" "$PLIST")" \
    --version "$SPOTIFY_VERSION" \
    --full-date "$(date +%Y%m%d%H%M%S)" \
    --size "$(stat -f %z "$IPA")" \
    --url "https://github.com/$REPO/releases/download/$TAG/$ASSET" \
    --notes "$NOTES"

git add apps.json
git commit -q -m "Add $LABEL ($TAG)"
git push -q
echo "published $ASSET ($TAG)"
