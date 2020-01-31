from os import environ
from unittest.mock import patch, MagicMock

from http import HTTPStatus

environ['HOPSTER_SERVER_SECRET_KEY'] = 'Not really a secret, is it?'
from hopster.views.schedule import schedule, ScheduleErrorCode
from hopster.controllers.schedule import (InvalidJsonInput,
                                          IncompleteScheduleInput,
                                          InvalidTimeInput)


#------------------------------------------------------------------------------#
@patch('hopster.views.schedule.request', MagicMock())
class TestSchedule:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_json_input(self):
        with patch('hopster.views.schedule.schedule_',
                   side_effect=InvalidJsonInput):
            response, status = schedule()
            assert status == HTTPStatus.BAD_REQUEST
            assert response['error']['code'] == ScheduleErrorCode.INVALID_JSON

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_incomplete_schedule_input(self):
        with patch('hopster.views.schedule.schedule_',
                   side_effect=IncompleteScheduleInput):
            response, status = schedule()
            assert status == HTTPStatus.BAD_REQUEST
            assert response['error']['code'] == ScheduleErrorCode.MISSING_VALUES

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_time_input(self):
        with patch('hopster.views.schedule.schedule_',
                   side_effect=InvalidTimeInput):
            response, status = schedule()
            assert status == HTTPStatus.BAD_REQUEST
            assert response['error']['code'] == ScheduleErrorCode.INVALID_INPUT

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_enquiry(self):
        with patch('hopster.views.schedule.schedule_',
                   return_value={'video_file': 'file'}):
            response, status = schedule()
            assert status == HTTPStatus.OK
            assert response['video_file'] == 'file'
