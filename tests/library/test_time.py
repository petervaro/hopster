from os import environ

from pytest import raises

environ['HOPSTER_SERVER_SECRET_KEY'] = 'Not really a secret, is it?'
from hopster.library.time import (Time,
                                  InvalidTimeString,
                                  InvalidValueForArithmeticOperation)


#------------------------------------------------------------------------------#
class TestTime:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_string(self):
        string = 'not-a-time'
        with raises(InvalidTimeString):
            t = Time.from_str(string)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_string(self):
        t = Time.from_str('00:12:34.56')
        assert str(t) == '00:12:34.560000'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_invalid_right_hand_side(self):
        with raises(TypeError):
            Time(0, 0, 1) - 'not-a-time'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_greater_right_hand_side(self):
        t1 = Time(0, 0, 1)
        t2 = Time(0, 0, 2)

        assert t1 < t2
        with raises(InvalidValueForArithmeticOperation):
            t1 - t2

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_valid_right_hand_side(self):
        t1 = Time(0, 0, 3)
        t2 = Time(0, 0, 1)

        assert t1 - t2 == Time(0, 0, 2)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def test_convertion(self):
        t = Time(0, 1, 2, 3)
        assert t == Time.from_str(str(t))
