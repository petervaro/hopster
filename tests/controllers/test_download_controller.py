from os import environ
from unittest.mock import patch

from pytest import raises

environ['HOPSTER_SERVER_SECRET_KEY'] = 'Not really a secret, is it?'
from hopster.controllers.download import (download,
                                          MissingArgument,
                                          VideoDoesNotExist)


#------------------------------------------------------------------------------#
class TestDownload:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_missing_argument(self):
        with raises(MissingArgument):
            download({})

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @patch('hopster.controllers.download.after_this_request')
    def test_valid_download(self, hook):
        from hopster.controllers.download import Bucket
        with patch.object(Bucket, 'download', return_value='path'):
            assert download({'video_file': 'file'}) == 'path'
            assert hook.call_count == 1
