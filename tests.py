import pytest
from data_capture import DataCapture, Stats, is_positive_integer_until_max_value


@pytest.fixture()
def sample_input():
    return [3, 9, 3, 4, 6]


@pytest.fixture()
def capture():
    capture = DataCapture()
    return capture


@pytest.fixture()
def using_sample_input(capture, sample_input):
    for d in sample_input:
        capture.add(d)
    stats = capture.build_stats()
    return stats


class TestDataCapture:

    def test_validation_is_positive_integer_until_max_value(self):
        assert is_positive_integer_until_max_value(1001) is False
        assert is_positive_integer_until_max_value(-1) is False
        assert is_positive_integer_until_max_value("asdf") is False
        assert is_positive_integer_until_max_value(0)
        assert is_positive_integer_until_max_value(1000)

    def test_add_succeed(self, capture):
        capture.add(9)
        stats = capture.build_stats()
        assert stats.less(9) == 0

    def test_add_wrong_value(self, capture):
        assert capture.add('string') is False
        assert capture.add(3.14) is False
        assert capture.add([]) is False
        assert capture.add({}) is False
        assert capture.add(None) is False


class TestBuildStats:

    def test_empty_stats(self, capture):
        with pytest.raises(ValueError):
            stats = capture.build_stats()
        assert capture.frequencies == {}

    def test_build_stats(self, capture):
        capture.add(5)
        capture.add(2)
        capture.add(7)
        capture.add(2)
        capture.add(5)
        capture.add(7)
        capture.add(7)
        stats = capture.build_stats()
        assert stats.frequencies == {5: 2, 2: 2, 7: 3}

    def test_counting_less_than(self, using_sample_input):
        assert using_sample_input.less(4) == 2
        assert using_sample_input.less(6) == 3
        assert using_sample_input.less(7) == 4

        assert using_sample_input.less(-4) is None
        assert using_sample_input.less(0) is 0
        assert using_sample_input.less(9999) is None

    def test_counting_greater_than(self, using_sample_input):
        assert using_sample_input.greater(3) == 3
        assert using_sample_input.greater(4) == 2
        assert using_sample_input.greater(10) == 0

        assert using_sample_input.greater(-4) is None
        assert using_sample_input.greater(0) == 5
        assert using_sample_input.greater(9999) is None

    def test_counting_between(self, using_sample_input):
        assert using_sample_input.between(1, 10) == 5
        assert using_sample_input.between(6, 3) == 4
        assert using_sample_input.between(3, 6) == 4
        assert using_sample_input.between(3, 3) == 2
