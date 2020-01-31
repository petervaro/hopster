from http import HTTPStatus
from enum import IntEnum

from flask import request

from hopster.controllers.download import (download as download_,
                                          MissingArgument,
                                          VideoDoesNotExist)


#------------------------------------------------------------------------------#
class _DownloadErrorCode(IntEnum):
    MISSING_FILE_NAME = 100
    VIDEO_DOES_NOT_EXIST = 200


#------------------------------------------------------------------------------#
def download():
    status = HTTPStatus.OK

    try:
        response = download_(dict(request.args))
    except MissingArgument as error:
        status = HTTPStatus.BAD_REQUEST
        response = {'error': {'message': f'Missing argument: {error}',
                              'code': _DownloadErrorCode.MISSING_FILE_NAME}}
    except VideoDoesNotExist as error:
        status = HTTPStatus.BAD_REQUEST
        response = {'error': {'message': f'Video does not exist: {error}',
                              'code': _DownloadErrorCode.VIDEO_DOES_NOT_EXIST}}

    return response, status


#------------------------------------------------------------------------------#
if __debug__:
    DownloadErrorCode = _DownloadErrorCode
