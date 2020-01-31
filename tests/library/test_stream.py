from os import environ
from unittest.mock import patch

from pytest import raises

environ['HOPSTER_SERVER_SECRET_KEY'] = 'Not really a secret, is it?'
from hopster.library.time import Time
from hopster.library.stream import Stream, BoundTypeError, BoundValueError


#------------------------------------------------------------------------------#
class TestStream:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_start_type(self):
        with raises(BoundTypeError):
            Stream('ref', 'url', start='not-a-time')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_stop_type(self):
        with raises(BoundTypeError):
            Stream('ref', 'url', stop='not-a-time')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_start_value(self):
        t1 = Time(0, 0, 1)
        t2 = Time(0, 0, 2)
        assert t1 < t2
        s = Stream('ref', 'url', start=t1, stop=t2)
        t3 = Time(0, 0, 3)
        assert t3 > t2
        with raises(BoundValueError):
            s.start = t3

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_stop_value(self):
        t1 = Time(0, 0, 2)
        t2 = Time(0, 0, 1)
        assert t1 > t2
        with raises(BoundValueError):
            Stream('ref', 'url', start=t1, stop=t2)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_output_file_name(self):
        s = Stream('file', 'url')
        assert s.output_file_name == 'file_from_start_till_end.mp4'
        s.start = Time(1, 2, 3)
        assert s.output_file_name == f'file_from_010203000000_till_end.mp4'
        s.stop = Time(4, 5, 6)
        assert s.output_file_name == f'file_from_010203000000_till_040506000000.mp4'
        s.start = None
        assert s.output_file_name == f'file_from_start_till_040506000000.mp4'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @patch('hopster.library.stream.run')
    def test_download(self, run):
        s = Stream('file', 'url')
        s.download()
        run.assert_called_with([
            'ffmpeg', '-y',
                      '-i', 'url',
                      './file_from_start_till_end.mp4'])

        s.start = Time(1, 2, 3)
        s.download()
        run.assert_called_with([
            'ffmpeg', '-y',
                      '-i', 'url',
                      '-ss', '01:02:03',
                      './file_from_010203000000_till_end.mp4'])

        s.stop = Time(4, 5, 6)
        s.download()
        run.assert_called_with([
            'ffmpeg', '-y',
                      '-i', 'url',
                      '-ss', '01:02:03',
                      # NOTE: This is duration not `stop`!
                      '-t', '03:03:03',
                      './file_from_010203000000_till_040506000000.mp4'])

        s.start = None
        s.download()
        run.assert_called_with([
            'ffmpeg', '-y',
                      '-i', 'url',
                      '-t', '04:05:06',
                      './file_from_start_till_040506000000.mp4'])
