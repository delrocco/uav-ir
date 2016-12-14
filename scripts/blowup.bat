@echo off
setlocal disableDelayedExpansion
set "search=%1\*.tif"
set "files="
for /r %%F in (%search%) do call set files=%%files%% "%1\%%~nxF"

@echo on
"C:\Program Files\Blow Up\Blow Up 3\Alien Skin Blow Up 3 x64.exe" %files%