Release Guide

Usage with helper script (Windows):

- release.bat patch — bumps vX.Y.Z to next patch, pushes tag, triggers CI.
- release.bat minor — bumps minor (X.Y+1.0).
- release.bat major — bumps major (X+1.0.0).

Manual alternative:

- git tag -a vX.Y.Z -m "Release vX.Y.Z"
- git push origin vX.Y.Z

CI pipeline (GitHub Actions) builds a Windows .exe, downloads ffmpeg.exe and yt-dlp.exe, packages a portable .zip, and attaches both as release assets. It triggers on:

- Tag push matching v*
- Manual dispatch with tag input
- Published GitHub Release

Direct links:

- Latest .exe: https://github.com/Nikitzima/YT-DLP-GUI/releases/latest/download/YT-DLP_GUI.exe
- Latest release page: https://github.com/Nikitzima/YT-DLP-GUI/releases/latest

