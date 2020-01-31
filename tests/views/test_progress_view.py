from os import environ
from unittest.mock import patch, MagicMock

from http import HTTPStatus

environ['HOPSTER_SERVER_SECRET_KEY'] = 'Not really a secret, is it?'
from hopster.views.progress import progress, ProgressErrorCode
from hopster.controllers.progress import MissingArgument


#------------------------------------------------------------------------------#
@patch('hopster.views.progress.request', MagicMock())
class TestProgress:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_missing_argument(self):
        with patch('hopster.views.progress.progress_',
                   side_effect=MissingArgument):
            response, status = progress()
            assert status == HTTPStatus.BAD_REQUEST
            assert response['error']['code'] == ProgressErrorCode.MISSING_ARGUMENT

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_enquiry(self):
        with patch('hopster.views.progress.progress_',
                   return_value={'is_finished': True}):
            response, status = progress()
            assert status == HTTPStatus.OK
            assert response['is_finished']
