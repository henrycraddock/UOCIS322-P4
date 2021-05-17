"""
Nose tests for acp_times.py
"""

# Importing acp_times adapted from instructions here: https://csatlas.com/python-import-file-module/
import sys
import os

curr_dir = os.path.dirname(__file__)
acp_dir = os.path.join(curr_dir, '..')
sys.path.append(acp_dir)

from acp_times import open_time, close_time

import nose
from nose.tools import assert_raises
import arrow
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

date = arrow.get('2021-05-15T00:00:00')


def test_simple():
    """Test simple actions on the 0-200 km range"""
    assert open_time(60, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T01:46'
    assert close_time(60, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T04:00'
    assert open_time(120, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T03:32'
    assert close_time(120, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T08:00'
    assert open_time(175, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T05:09'
    assert close_time(175, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T11:40'


def test_close_brevets():
    """Test that the proper closing times are used for entire brevets, which may be
    different than the time that would normally be calculated"""
    assert close_time(200, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T13:30'
    assert close_time(300, 300, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T20:00'
    assert close_time(400, 400, date).format('YYYY-MM-DDTHH:mm') == '2021-05-16T03:00'
    assert close_time(600, 600, date).format('YYYY-MM-DDTHH:mm') == '2021-05-16T16:00'
    assert close_time(1000, 1000, date).format('YYYY-MM-DDTHH:mm') == '2021-05-18T03:00'


def test_zero():
    """Test the algorithm for control distance of 0"""
    assert open_time(0, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T00:00'
    assert close_time(0, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T01:00'


def test_valid_distance():
    """Test if an error is raised if the control distance is not valid
    Example of assert_raises from here: https://programtalk.com/python-examples/nose.tools.assert_raises/"""
    assert close_time(240, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T13:30'
    assert_raises(ValueError, open_time, 241, 200, date)
    assert close_time(360, 300, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T20:00'
    assert_raises(ValueError, open_time, 361, 300, date)
    assert close_time(480, 400, date).format('YYYY-MM-DDTHH:mm') == '2021-05-16T03:00'
    assert_raises(ValueError, open_time, 481, 400, date)
    assert close_time(720, 600, date).format('YYYY-MM-DDTHH:mm') == '2021-05-16T16:00'
    assert_raises(ValueError, open_time, 721, 600, date)
    assert close_time(1200, 1000, date).format('YYYY-MM-DDTHH:mm') == '2021-05-18T03:00'
    assert_raises(ValueError, open_time, 1201, 1000, date)


def test_negative():
    """Test that an error is raised if a negative distance is given"""
    assert_raises(ValueError, open_time, -10, 200, date)


def test_under_60():
    """Test calculations of controls under 60 km"""
    assert close_time(10, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T01:30'
    assert close_time(20, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T02:00'
    assert close_time(30, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T02:30'
    assert close_time(40, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T03:00'
    assert close_time(50, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T03:30'
    assert close_time(60, 200, date).format('YYYY-MM-DDTHH:mm') == '2021-05-15T04:00'
