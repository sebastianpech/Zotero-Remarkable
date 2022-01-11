#!/user/bin/env python3

import os
import subprocess
import argparse
import pathlib

parser = argparse.ArgumentParser(description='Synchronize reMarkable and Zotero tablet export.')
parser.add_argument('Zotero', help="Basefolder defined in ZotFile tablet settings.")
parser.add_argument('reMarkable', help="Mirrored folder on reMarkable.")
parser.add_argument('--delete', action='store_true', help="Delete all files on reMarkable that don't exists in the Zotero folder.")
parser.add_argument('--download', action='store_true', help="Download all files from reMarkable, even if they are not in the Zotero folder. (Overwrites --delete)")
parser.add_argument('--rmapi', default="rmapi", help="rmapi executable. This can be a path or the name of the rmapi executable that is in PATH. Default is rmapi")

args = parser.parse_args()

ZOTERO_FOLDER = args.Zotero
RM_FOLDER =  args.reMarkable

RMAPI_BIN = args.rmapi

def rmapi(cmd):
    return subprocess.check_output(f"{RMAPI_BIN} {cmd}", shell=True, stderr=subprocess.STDOUT).decode("utf-8").split('\n')[0:-1]

def upload_file(file):
    path = os.path.join(ZOTERO_FOLDER, f"{file}.pdf")
    rmapi(f'put "{path}" "{RM_FOLDER}"')

def download_file(file):
    path = '/'.join([RM_FOLDER,file])
    zip_file = f"{file}.zip"
    try:
        rmapi(f'geta -a "{path}"')
        f_annotations = f"{file}-annotations.pdf"
        os.replace(f_annotations,os.path.join(ZOTERO_FOLDER,f"{file}.pdf"))
    except Exception as inst:
        if not ("document has no pages" in inst.output.decode("utf-8")):
            print(inst.output.decode("utf-8"))
    finally:
        if (os.path.isfile(zip_file)):
            os.remove(zip_file)

def delete_file(file):
    path = '/'.join([RM_FOLDER,file])
    rmapi(f'rm "{path}"')

def get_files():
    files_on_remarkable = set([f.split('\t')[-1] for f in rmapi(f"ls {RM_FOLDER}")])
    files_on_local = set([os.path.splitext(os.path.basename(f))[0] for f in os.listdir(ZOTERO_FOLDER) if f.endswith(".pdf")])
    return files_on_remarkable, files_on_local

def process_files(delete=False, download=False):
    files_on_remarkable, files_on_local = get_files()
    files_to_download = files_on_remarkable.copy()

    if not download:
        files_to_download &= files_on_local

    files_to_upload = files_on_local - files_on_remarkable
    files_to_delete = files_on_remarkable - files_on_local

    for file in files_to_upload:
        print(f"[Uploading  ] '{file}'")
        upload_file(file)

    for file in files_to_download:
        print(f"[Downloading] '{file}'")
        download_file(file)

    if delete and not download:
        for file in files_to_delete:
            print(f"[Deleting   ] '{file}'")
            delete_file(file)

process_files(delete=args.delete, download=args.download)
