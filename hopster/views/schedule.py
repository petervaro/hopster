from http import HTTPStatus
from enum import IntEnum

from flask import request

from hopster.controllers.schedule import (schedule as schedule_,
                                          InvalidJsonInput,
                                          IncompleteScheduleInput,
                                          InvalidTimeInput)


#------------------------------------------------------------------------------#
class _ScheduleErrorCode(IntEnum):
    INVALID_JSON = 100
    MISSING_VALUES = 200
    INVALID_INPUT = 300


#------------------------------------------------------------------------------#
def schedule():
    status = HTTPStatus.OK

    try:
        response = schedule_(request.data)
    except InvalidJsonInput as error:
        status = HTTPStatus.BAD_REQUEST
        response = {'error': {'message': f'Invalid JSON for `schedule`: {error}',
                              'code': _ScheduleErrorCode.INVALID_JSON}}
    except IncompleteScheduleInput as error:
        status = HTTPStatus.BAD_REQUEST
        response = {'error': {'message': f'Values are missing: {error}',
                              'code': _ScheduleErrorCode.MISSING_VALUES}}
    except InvalidTimeInput as error:
        status = HTTPStatus.BAD_REQUEST
        response = {'error': {'message': f'Invalid time for `schedule`: {error}',
                              'code': _ScheduleErrorCode.INVALID_INPUT}}

    return response, status


#------------------------------------------------------------------------------#
if __debug__:
    ScheduleErrorCode = _ScheduleErrorCode
