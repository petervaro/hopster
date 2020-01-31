from dateutil.parser import parse, ParserError
from datetime import time

from hopster.error import LibraryError


#------------------------------------------------------------------------------#
class TimeError(LibraryError): pass
#------------------------------------------------------------------------------#
class InvalidTimeString(TimeError): pass
#------------------------------------------------------------------------------#
class InvalidValueForArithmeticOperation(TimeError): pass


#------------------------------------------------------------------------------#
class Time(time):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @classmethod
    def from_str(cls, input_):
        try:
            time = parse(input_).time()
        except (TypeError, ParserError) as error:
            raise InvalidTimeString(str(error))
        return cls(time.hour, time.minute, time.second, time.microsecond)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __sub__(self, other):
        if self < other:
            raise InvalidValueForArithmeticOperation(
                f'{self!r} is lesser than {other!r}')

        if self.microsecond >= other.microsecond:
            second = 0
            microsecond = self.microsecond - other.microsecond
        else:
            second, microsecond = \
                divmod(self.microsecond + other.microsecond, 1_000_000)

        second += other.second

        if self.second >= second:
            minute = 0
            second = self.second - second
        else:
            minute, second = divmod(self.second + second, 60)

        minute += other.minute

        if self.minute >= minute:
            hour = 0
            minute = self.minute - minute
        else:
            hour, minute = divmod(self.minute + minute, 60)

        hour = self.hour - other.hour - hour
        return self.__class__(hour, minute, second, microsecond)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        return f'{self.__class__.__name__}({self})'
