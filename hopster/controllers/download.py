from pathlib import Path

from flask import after_this_request

from hopster.error import ServerError
from hopster.constants import DOWNLOAD_DIRECTORY
from hopster.dummy.bucket import (Bucket,
                                  FileDoesNotExist)


#------------------------------------------------------------------------------#
class DownloadError(ServerError): pass
#------------------------------------------------------------------------------#
class MissingArgument(DownloadError): pass
#------------------------------------------------------------------------------#
class VideoDoesNotExist(DownloadError): pass


#------------------------------------------------------------------------------#
def download(raw_download_details):

    try:
        file_name = raw_download_details['video_file']
    except KeyError as key:
        raise MissingArgument(str(key))

    Path(DOWNLOAD_DIRECTORY).mkdir(exist_ok=True)

    try:
        video_file_path = Bucket().download(file_name, DOWNLOAD_DIRECTORY)
    except FileDoesNotExist as error:
        raise VideoDoesNotExist(str(error))

    def clean_up(response):
        Path(video_file_path).unlink(missing_ok=True)
        return response

    # HACK: It feels wrong to call this Flask function at the controller layer
    #       because at this point we should not care about neither requests nor
    #       responses, yet the framework does not provide any cleaner solution
    #       to the problem...
    after_this_request(clean_up)
    return video_file_path
