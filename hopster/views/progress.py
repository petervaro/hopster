from http import HTTPStatus
from enum import IntEnum

from flask import request

from hopster.controllers.progress import (progress as progress_,
                                          MissingArgument)


#------------------------------------------------------------------------------#
class _ProgressErrorCode(IntEnum):
    MISSING_ARGUMENT = 100


#------------------------------------------------------------------------------#
def progress():
    status = HTTPStatus.OK
    try:
        response = progress_(dict(request.args))
    except MissingArgument as error:
        status = HTTPStatus.BAD_REQUEST
        response = {'error': {'message': f'Missing argument: {error}',
                              'code': _ProgressErrorCode.MISSING_ARGUMENT}}

    return response, status


#------------------------------------------------------------------------------#
if __debug__:
    ProgressErrorCode = _ProgressErrorCode
