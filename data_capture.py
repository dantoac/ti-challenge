from typing import Optional, List


class DataCapture:
    def __init__(self, max_value: int = 1000) -> None:
        self.max_value = max_value
        self.frequencies = {}

    def add(self, num: int) -> None:
        if not isinstance(num, int):
            raise TypeError('Value needs to be an integer')
        elif 0 <= num < self.max_value:
            self.frequencies[num] = self.frequencies.get(num, 0) + 1
        else:
            raise ValueError(f'Integer value should be a positive integer less than {self.max_value}')

    def build_stats(self):
        return Stats(self.frequencies)


class Stats:

    def __init__(self, frequencies: List[dict]) -> None:
        if not frequencies:
            raise ValueError("There's no data to build stats for")

        self.frequencies = frequencies
        self.stats = {}
        max_num = max(self.frequencies)

        self.prefix_sum = [0] * (max_num + 1)

        total_lt = 0
        total_gt = sum(self.frequencies.values())

        for num, frequency in sorted(self.frequencies.items()):
            self.stats[num] = {'count_lt': total_lt, 'count_gt': total_gt - frequency, 'value': num}
            total_lt += frequency
            total_gt -= frequency
            self.prefix_sum[num] = total_lt

    def between(self, lower: int, upper: int) -> int:
        if not (self.frequencies.get(lower) or self.frequencies.get(upper)):
            raise ValueError("Unkown value")
        if lower > 0:
            return self.prefix_sum[upper] - self.prefix_sum[lower - 1]
        else:
            return self.prefix_sum[upper]

    def less(self, num: int) -> Optional[int]:
        if self.stats[num]:
            return self.stats[num].get('count_lt', 0)

    def greater(self, num: int) -> Optional[int]:
        if self.stats[num]:
            return self.stats[num].get('count_gt', 0)
