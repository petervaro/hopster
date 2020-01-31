from os import environ
from unittest.mock import patch, MagicMock

from http import HTTPStatus

environ['HOPSTER_SERVER_SECRET_KEY'] = 'Not really a secret, is it?'
from hopster.views.download import download, DownloadErrorCode
from hopster.controllers.download import MissingArgument, VideoDoesNotExist


#------------------------------------------------------------------------------#
@patch('hopster.views.download.request', MagicMock())
class TestDownload:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_missing_argument(self):
        with patch('hopster.views.download.download_',
                   side_effect=MissingArgument):
            response, status = download()
            assert status == HTTPStatus.BAD_REQUEST
            assert response['error']['code'] == DownloadErrorCode.MISSING_FILE_NAME

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_video_does_not_exist(self):
        with patch('hopster.views.download.download_',
                   side_effect=VideoDoesNotExist):
            response, status = download()
            assert status == HTTPStatus.BAD_REQUEST
            assert response['error']['code'] == DownloadErrorCode.VIDEO_DOES_NOT_EXIST

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_enquiry(self):
        with patch('hopster.views.download.download_', return_value='.'):
            response, status = download()
            assert status == HTTPStatus.OK
            assert response == '.'
