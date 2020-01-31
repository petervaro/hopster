from json import loads, JSONDecodeError
from pathlib import Path

from hopster.error import ServerError
from hopster.constants import VIDEOS_DIRECTORY
from hopster.tasks.download import download_stream
from hopster.library.stream import Stream, StreamError
from hopster.library.time import Time, TimeError
from hopster.dummy.bucket import Bucket


#------------------------------------------------------------------------------#
class ScheduleError(ServerError): pass
#------------------------------------------------------------------------------#
class InvalidJsonInput(ScheduleError): pass
#------------------------------------------------------------------------------#
class InvalidTimeInput(ScheduleError): pass
#------------------------------------------------------------------------------#
class IncompleteScheduleInput(ScheduleError): pass


#------------------------------------------------------------------------------#
def _construct_video_url(video_id):
    return f'http://85072-c.ooyala.com/{video_id}/DOcJ-FxaFrRg4gtDEwOjIwbTowODE7WK'


#------------------------------------------------------------------------------#
def schedule(raw_stream_details):
    try:
        stream_details = loads(raw_stream_details)
    except JSONDecodeError as error:
        raise InvalidJsonInput(str(error))

    try:
        video_id = stream_details['video_id']
    except KeyError as key:
        raise IncompleteScheduleInput(key)

    bounds = {'start': None, 'stop': None}
    for bound in bounds:
        try:
            bounds[bound] = Time.from_str(stream_details[bound])
        except TimeError as error:
            raise InvalidTimeInput(str(error))
        except KeyError:
            continue

    try:
        stream = Stream(video_ref=video_id,
                        video_url=_construct_video_url(video_id),
                        **bounds)
    except StreamError as error:
        raise InvalidTimeInput(str(error))

    video_file = stream.output_file_name

    if video_file not in Bucket():
        download_stream.fork(reference=video_file,
                             args=(stream, VIDEOS_DIRECTORY))

    return {'video_file': video_file}
