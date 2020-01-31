from os import environ
from unittest.mock import patch

from pytest import raises

environ['HOPSTER_SERVER_SECRET_KEY'] = 'Not really a secret, is it?'
from hopster.controllers.progress import progress, MissingArgument


#------------------------------------------------------------------------------#
class TestProgress:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_missing_argument(self):
        with raises(MissingArgument):
            progress({})

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_enquiry(self):
        with patch('hopster.controllers.progress.download_stream') as ds:
            ds.is_finished.return_value = False
            assert not progress({'reference': 'ref'})['is_finished']
            ds.is_finished.return_value = True
            assert progress({'reference': 'ref'})['is_finished']
