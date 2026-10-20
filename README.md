# EeveeSpotify Jam IPAs

Feather / AltStore source for EeveeSpotify Jam builds.

Add this URL as a source in Feather:

```
https://raw.githubusercontent.com/LeoTurlock/EeveeSpotify-Jam-IPAs/main/apps.json
```

The IPAs are attached to [Releases](https://github.com/LeoTurlock/EeveeSpotify-Jam-IPAs/releases) because they're too large for git.

## Publishing a build

```bash
./publish.sh ~/Downloads/EeveeSpotify-7.0.0-9.1.88-Jam-Something-unsigned.ipa [label] [notes]
```

This uploads the IPA as a release and adds it as the newest version in `apps.json`.
