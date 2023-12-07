import pytest
from data_capture import DataCapture, Stats


@pytest.fixture()
def sample_input():
    return [3, 9, 3, 4, 6]  # [3, 3, 4, 6, 9]


@pytest.fixture()
def capture():
    capture = DataCapture()
    return capture


@pytest.fixture()
def stats(capture, sample_input):
    for d in sample_input:
        capture.add(d)
    stats = capture.build_stats()
    return stats


class TestDataCapture:

    def test_add_succeed(self, capture):
        capture.add(9)
        stats = capture.build_stats()
        assert stats.less(9) == 0

    def test_add_wrong_value(self, capture):
        with pytest.raises(ValueError):
            capture.add(1001)
        with pytest.raises(ValueError):
            capture.add(-1)
        with pytest.raises(ValueError):
            capture.add('string')
        with pytest.raises(ValueError):
            capture.add(3.14)
        with pytest.raises(ValueError):
            capture.add([])
        with pytest.raises(ValueError):
            capture.add({})
        with pytest.raises(ValueError):
            capture.add(None)


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
        assert stats.stats[2] == {'count_lt': 0, 'count_gt': 5, 'value': 2}
        assert stats.stats[5] == {'count_lt': 2, 'count_gt': 3, 'value': 5}
        assert stats.stats[7] == {'count_lt': 4, 'count_gt': 0, 'value': 7}

    def test_counting_less_than(self, stats):
        assert stats.less(4) == 2
        assert stats.less(6) == 3
        with pytest.raises(ValueError):
            assert stats.less(-4) == None
            assert stats.less(0) == None
            assert stats.less(9999) == None

    def test_counting_greater_than(self, stats):
        assert stats.greater(3) == 3
        assert stats.greater(4) == 2
        with pytest.raises(ValueError):
            assert stats.greater(-4) == None
            assert stats.greater(0) == None
            assert stats.greater(9999) == None

    def test_counting_between(self, stats):
        assert stats.between(6, 3) == 4
        assert stats.between(3, 6) == 4
        assert stats.between(3, 3) == 2

    def test_unknown_values_between(self, stats):
        stats.between(2, 8) == None
