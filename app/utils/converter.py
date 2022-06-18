import os
import subprocess
import tempfile


def run_process(cmd: str): return subprocess.run(cmd.split(' '))


def convert_to(file, target_format='pdf'):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(file.read())
    temp_file.close()
    file.seek(0)
    new_filename = None

    convert_cmd = {
        'pdf': "soffice --headless --convert-to pdf --outdir /tmp {}".format(temp_file.name),
        'docx': "soffice --headless --convert-to docx --outdir /tmp {}".format(temp_file.name)
    }[target_format]

    if run_process(convert_cmd).returncode == 0:
        # success conversion
        new_filename = "{}.{}".format(temp_file.name, target_format)
    os.remove(temp_file.name)

    return new_filename


def open_file(filepath, remove=True):
    file = open(filepath, 'rb')
    if remove: os.remove(filepath)
    return file
