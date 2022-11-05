# Zotero to reMarkable Cloud
# Note: Since this project is relatively dependent on the [rmapi](https://github.com/juruen/rmapi) app, it's highly recommended to visit the said repository first.
This script can be used with the `Send to Tablet` function from [ZotFile](http://zotfile.com/).
It synchronizes the ZotFile basis folder with a folder in the reMarkable cloud.

The following changes are synchronized:
- A new file in the ZotFile folder is send to the reMarkable cloud.
- Any updated to a file on the reMarkable cloud is downloaded into the ZotFile folder.
- With the command line option `--delete`, any file that was removed from the ZotFile folder is also removed from the reMarkable cloud.

## Configuration

- After installation of ZotFile, the only necessary option in Zotero is to define an base folder in the ZotFile preferences.
- The script uses [rmapi](https://github.com/juruen/rmapi), which requires setting up the connection to the cloud.

## Help

```
usage: sync.py [-h] [--delete] [--download] [--rmapi RMAPI] Zotero reMarkable

Synchronize reMarkable and Zotero tablet export.

positional arguments:
  Zotero         Basefolder defined in ZotFile tablet settings.
  reMarkable     Mirrored folder on reMarkable.

optional arguments:
  -h, --help     show this help message and exit
  --delete       Delete all files on reMarkable that don't exists in the Zotero folder.
  --download     Download all files from reMarkable, even if they are not in the Zotero folder. (Overwrites --delete)
  --rmapi RMAPI  rmapi executable. This can be a path or the name of the rmapi executable that is in PATH. Default is rmapi
```
