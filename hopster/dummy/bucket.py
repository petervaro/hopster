from pathlib import Path
from shutil import copy

from hopster.constants import BUCKET_DIRECTORY


#------------------------------------------------------------------------------#
class BucketError(Exception): pass
#------------------------------------------------------------------------------#
class FileDoesNotExist(BucketError): pass


#------------------------------------------------------------------------------#
class Bucket:
    """
    `Bucket` is a dummy implementation of a remote file-storage service, such as
    AWS's S3 via `boto`.  To keep the dependencies down and make the assignment
    as portable as possible, `Bucket` uses the file-system to simulate the
    uploads and downloads
    """

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self):
        Path(BUCKET_DIRECTORY).mkdir(exist_ok=True)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def upload(self, file_path):
        file_path = Path(file_path)
        file_path.rename(f'{BUCKET_DIRECTORY}/{file_path.name}')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def download(self, source_file_name, target_directory):
        source_path = self._path_to(source_file_name)
        if not source_path.exists():
            raise FileDoesNotExist(source_file_name)

        target_path = Path(f'{target_directory}/{source_file_name}')
        copy(source_path, target_path)

        return target_path

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __contains__(self, file_name):
        return self._path_to(file_name).exists()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @staticmethod
    def _path_to(file_name):
        return Path(f'{BUCKET_DIRECTORY}/{file_name}')
