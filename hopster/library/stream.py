from subprocess import run
from pathlib import Path

from hopster.library.time import Time
from hopster.error import LibraryError


#------------------------------------------------------------------------------#
class StreamError(LibraryError): pass
#------------------------------------------------------------------------------#
class BoundTypeError(StreamError): pass
#------------------------------------------------------------------------------#
class BoundValueError(StreamError): pass


#------------------------------------------------------------------------------#
class Stream:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, video_ref,
                       video_url,
                       start=None,
                       stop=None,
                       output_format='mp4'):
        # Set defaults
        self._ref = video_ref
        self._url = video_url
        self._start = None
        self._stop = None
        self._format = 'mp4'

        # Set optional values
        self.start = start
        self.stop = stop

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def start(self):
        return self._start

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @start.setter
    def start(self, start):
        # Check if `start` has the right type and it is lesser than`stop`
        try:
            if start is not None:
                if self._stop is not None and \
                   self._stop < start:
                        raise BoundValueError(
                            f'`start` ({start}) is expected to be '
                            f'lesser than `stop` ({self._stop})')
                elif not isinstance(start, Time):
                    raise TypeError
        # If `start` is neither `None` nor `Time`
        except TypeError:
            raise BoundTypeError(
                '`start` is expected to be: `hopster.time.Time`, '
                f'but got: {start.__class__.__name__}')

        self._start = start

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def stop(self):
        return self._stop

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @stop.setter
    def stop(self, stop):
        # Check if `stop` has the right type and it is greater than`start`
        try:
            if stop is not None:
                if self._start is not None and \
                   self._start > stop:
                        raise BoundValueError(
                            f'`stop` ({stop}) is expected to be '
                            f'greater than `start` ({self._start})')
                elif not isinstance(stop, Time):
                    raise TypeError
        # If `stop` is neither `None` nor `Time`
        except TypeError:
            raise BoundTypeError(
                '`stop` is expected to be: `hopster.time.Time`, '
                f'but got: {stop.__class__.__name__}')

        self._stop = stop

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def output_file_name(self):
        file_name = self._ref

        try:
            file_name = f'{file_name}_from_{self._start:%H%M%S%f}'
        except (ValueError, TypeError):
            file_name += '_from_start'

        try:
            file_name = f'{file_name}_till_{self._stop:%H%M%S%f}'
        except (ValueError, TypeError):
            file_name += '_till_end'

        return f'{file_name}.{self._format}'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def download(self, destination='.'):
        command = ['ffmpeg', '-y', '-i', self._url]

        if self._start is not None:
            command.extend(('-ss', str(self._start)))
            if self._stop is not None:
                command.extend(('-t', str(self._stop - self._start)))
        elif self._stop is not None:
            command.extend(('-t', str(self._stop)))

        output_file_path = f'{destination}/{self.output_file_name}'
        command.append(output_file_path)

        run(command)
        return output_file_path
