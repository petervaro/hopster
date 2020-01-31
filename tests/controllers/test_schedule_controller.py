from os import environ
from unittest.mock import patch

from pytest import raises

environ['HOPSTER_SERVER_SECRET_KEY'] = 'Not really a secret, is it?'
from hopster.controllers.schedule import (schedule,
                                          InvalidJsonInput,
                                          IncompleteScheduleInput,
                                          InvalidTimeInput)


#------------------------------------------------------------------------------#
class TestSchedule:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_input(self):
        with raises(InvalidJsonInput):
            schedule('not-json')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_incomplete_input(self):
        with raises(IncompleteScheduleInput):
            schedule('{}')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_time_values(self):
        with raises(InvalidTimeInput):
            schedule('{"video_id": "id", "start": "not-a-time"}')
        with raises(InvalidTimeInput):
            schedule('{"video_id": "id", "stop": "not-a-time"}')

        from hopster.library.stream import BoundValueError
        with patch('hopster.controllers.schedule.Stream',
                   side_effect=BoundValueError) as stream, \
             raises(InvalidTimeInput):
                schedule('{"video_id": "id", "start": "00:59:59", "stop": "00:01:00"}')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_video_already_in_bucket(self):
        from hopster.controllers.schedule import Bucket
        with patch.object(Bucket, '__contains__', return_value=True):
            video_file = schedule('{"video_id": "id"}')['video_file']
            assert video_file == 'id_from_start_till_end.mp4'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_video_not_in_bucket(self):
        from hopster.controllers.schedule import Bucket, download_stream
        with patch.object(Bucket, '__contains__', return_value=False), \
             patch.object(download_stream, 'fork') as fork:
                video_file = schedule('{"video_id": "id"}')['video_file']
                assert fork.call_count == 1
                assert video_file == 'id_from_start_till_end.mp4'
