import sys
import shutil
from pathlib import Path
import zipfile
import gzip
import tarfile
import clean_folder_asm.file_parser as parser
from clean_folder_asm.normalize import normalize

def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_archive(filename: Path, target_folder: Path) -> None:
    archives_folder = target_folder / 'archives'
    archives_folder.mkdir(exist_ok=True)  # перевірка та створення папки archives, якщо вона не існує
    target_folder.mkdir(exist_ok=True, parents=True)  # робимо папку для архіва
    folder_for_file = archives_folder / normalize(filename.stem)  # створення папки без розширення
    folder_for_file.mkdir(exist_ok=True, parents=True)

    if filename.suffix == '.gz':
        try:
            with gzip.open(filename, 'rb') as f_in:
                with open(folder_for_file / filename.stem, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        except OSError:
            print(f"Can't extract archive: {filename}")
            folder_for_file.rmdir()
    elif filename.suffix == '.tar':
        try:
            with tarfile.open(filename, 'r') as tar:
                tar.extractall(folder_for_file)
        except tarfile.TarError:
            print(f"Can't extract archive: {filename}")
            folder_for_file.rmdir()
    elif filename.suffix == '.zip':
        try:
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(folder_for_file)
        except zipfile.BadZipFile:
            print(f"Can't extract archive: {filename}")
            folder_for_file.rmdir()
    else:
        print(f"Unsupported archive format: {filename}")

    filename.unlink()

def handle_folder(folder: Path): #видаляємо пусті папки з яких було переміщено об'єкти
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")

def main(folder: Path):
    parser.scan(folder)
    for file in parser.JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    for file in parser.AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in parser.MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in parser.MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')
    for file in parser.DOC_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in parser.DOCX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in parser.TXT_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in parser.PDF_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in parser.XLSX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in parser.PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PPTX')
    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in parser.AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')
    for file in parser.AUTOCAD_DRAWINGS:
        handle_media(file, folder / 'drawings' / 'DWG')

    for file in parser.MY_OTHER:
        handle_media(file, folder / 'other')
    for file in parser.ARCHIVES:
        handle_archive(file, folder)

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)

def start():
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())


if __name__ == '__main__':
    if len (sys.argv) == 1: #Перевіряємо, чи є у нас аргумент командного рядка, щоб уникнути IndexError, якщо аргумент відсутній
        print("Please provide a folder path as an argument.")
    else:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())