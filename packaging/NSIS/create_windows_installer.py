# Copyright (c) 2022 UltiMaker
# Cura is released under the terms of the LGPLv3 or higher.


import os
import argparse  # Command line arguments parsing and help.
import re
import subprocess

import shutil
from datetime import datetime

from pathlib import Path

from jinja2 import Template


def _application_directory(dist_loc: Path) -> Path:
    """Return the PyInstaller output directory used by this build."""
    for directory_name in ("BCN3D-Stratos", "UltiMaker-Cura"):
        candidate = dist_loc.joinpath(directory_name)
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("Could not find the BCN3D-Stratos PyInstaller output directory")


def _version_from_environment_or_filename(filename: str) -> str:
    version = os.getenv("CURA_VERSION_FULL")
    if version:
        return version

    match = re.search(r"(\d+\.\d+\.\d+(?:\.[A-Za-z0-9]+)?)", Path(filename).name)
    if match:
        return match.group(1)
    raise RuntimeError("Set CURA_VERSION_FULL or include the version in the installer filename")


def generate_nsi(source_path: str, dist_path: str, filename: str):
    dist_loc = Path(os.getcwd(), dist_path)
    source_loc = Path(os.getcwd(), source_path)
    application_dir = _application_directory(dist_loc)
    main_app = (
        "BCN3D-Stratos.exe"
        if application_dir.name == "BCN3D-Stratos"
        else "UltiMaker-Cura.exe"
    )
    version = _version_from_environment_or_filename(filename)
    numeric_version = version.split(".")[:3]
    if len(numeric_version) != 3:
        raise RuntimeError(f"Invalid Cura version: {version}")

    instdir = Path("$INSTDIR")
    dist_paths = [
        path.relative_to(application_dir)
        for path in sorted(application_dir.rglob("*"))
        if path.is_file()
    ]
    mapped_out_paths = {}
    for relative_path in dist_paths:
        if "__pycache__" not in relative_path.parts:
            out_path = instdir.joinpath(relative_path).parent
            if out_path not in mapped_out_paths:
                mapped_out_paths[out_path] = [
                    (application_dir.joinpath(relative_path), instdir.joinpath(relative_path))
                ]
            else:
                mapped_out_paths[out_path].append(
                    (application_dir.joinpath(relative_path), instdir.joinpath(relative_path))
                )

    rmdir_paths = set()
    for rmdir_f in mapped_out_paths.values():
        for _, rmdir_p in rmdir_f:
            for rmdir in rmdir_p.parents:
                rmdir_paths.add(rmdir)

    rmdir_paths = sorted(list(rmdir_paths), reverse = True)[:-2]  # Removes the `.` and `..` from the list

    jinja_template_path = Path(source_loc.joinpath("packaging", "NSIS", "Ultimaker-Cura.nsi.jinja"))
    with open(jinja_template_path, "r") as f:
        template = Template(f.read())


    nsis_content = template.render(
        app_name = f"BCN3D Stratos {version}",
        main_app = main_app,
        version = version,
        version_major = numeric_version[0],
        version_minor = numeric_version[1],
        version_patch = numeric_version[2],
        company = "BCN3D",
        web_site = "https://www.bcn3d.com",
        year = datetime.now().year,
        cura_license_file = str(source_loc.joinpath("packaging", "cura_license.txt")),
        compression_method = "LZMA",  # ZLIB, BZIP2 or LZMA
        cura_banner_img = str(source_loc.joinpath("packaging", "NSIS", "cura_banner_nsis.bmp")),
        cura_icon = str(source_loc.joinpath("packaging", "icons", "Cura.ico")),
        mapped_out_paths = mapped_out_paths,
        rmdir_paths = rmdir_paths,
        destination = filename
    )

    with open(dist_loc.joinpath("UltiMaker-Cura.nsi"), "w") as f:
        f.write(nsis_content)

    shutil.copy(source_loc.joinpath("packaging", "NSIS", "fileassoc.nsh"), dist_loc.joinpath("fileassoc.nsh"))


def build(dist_path: str):
    dist_loc = Path(os.getcwd(), dist_path)
    makensis = shutil.which("makensis")
    if not makensis:
        program_files_x86 = os.environ.get("ProgramFiles(x86)")
        if program_files_x86:
            candidate = Path(program_files_x86, "NSIS", "makensis.exe")
            if candidate.is_file():
                makensis = str(candidate)
    if not makensis:
        raise FileNotFoundError("Could not find makensis.exe")

    command = [makensis, "/V2", "/P4", str(dist_loc.joinpath("UltiMaker-Cura.nsi"))]
    subprocess.run(command, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Create Windows exe installer of Cura.")
    parser.add_argument("source_path", type=str, help="Path to Conan install Cura folder.")
    parser.add_argument("dist_path", type=str, help="Path to Pyinstaller dist folder")
    parser.add_argument("filename", type = str, help = "Filename of the exe (e.g. 'UltiMaker-Cura-5.1.0-beta-Windows-X64.exe')")
    args = parser.parse_args()
    generate_nsi(args.source_path, args.dist_path, args.filename)
    build(args.dist_path)
