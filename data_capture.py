from typing import Optional, List

MAX_VALUE = 1000


def is_positive_integer_until_max_value(num: int = 0) -> bool:
    if isinstance(num, int) and 0 <= num <= MAX_VALUE:
        return True
    else:
        raise ValueError(f'Value should be a Positive Integer less than {MAX_VALUE}')


class DataCapture:
    def __init__(self, max_value: int = 1000) -> None:
        self.max_value = max_value
        self.frequencies = {}
        self.max_num = 0
        self.freq_sum = 0

    def add(self, num: int) -> None:
        """
        Adds a number to the frequencies dictionary and updates the frequency sum.

        Parameters:
            num (int): The number to be added to the frequencies dictionary.

        Returns:
            None
        """
        if is_positive_integer_until_max_value(num):
            self.frequencies[num] = self.frequencies.get(num, 0) + 1
            self.freq_sum += 1
            if num > self.max_num:
                self.max_num = num

    def build_stats(self):
        """
        Build the statistics for the given frequencies.

        Returns:
            Stats: The statistics object containing less, between and greater values for each frequency.
        """
        return Stats(self.frequencies, self.freq_sum, self.max_num)


class Stats:

    def __init__(self, frequencies: dict, total: int, max_num: int) -> None:
        if not frequencies:
            raise ValueError("There's no data to build stats for")

        self.frequencies = frequencies
        self.stats = {}

        self.prefix_sum = [0] * (max_num + 1)

        total_lt = 0
        total_gt = total

        for num in range(max_num + 1):
            frequency = self.frequencies.get(num, 0)
            self.stats[num] = {'count_lt': total_lt, 'count_gt': total_gt - frequency, 'value': num}
            total_lt += frequency
            total_gt -= frequency
            self.prefix_sum[num] = total_lt

    def between(self, lower: int, upper: int) -> int:
        """
        Calculate the sum of integers between a lower and upper bound.

        Parameters:
            lower (int): The lower bound of the range.
            upper (int): The upper bound of the range.

        Returns:
            int: The total number of values between the lower and upper bounds.
        """
        if (
                is_positive_integer_until_max_value(upper)
                and is_positive_integer_until_max_value(lower)
        ):
            # reordering parameter values
            if lower > upper:
                lower, upper = upper, lower

            if lower > 0:
                return self.prefix_sum[upper] - self.prefix_sum[lower - 1]
            else:
                return self.prefix_sum[upper]

    def less(self, num: int) -> Optional[int]:
        """
        Get the count of numbers in the collection that are less than the given number.

        Parameters:
            num (int): The number to compare.

        Returns:
            int or None: The count of numbers in the collection that are less than the given number, or None if the number is not a positive integer until the max value.
        """
        if is_positive_integer_until_max_value(num):
            return self.stats.get(num).get('count_lt', 0)

    def greater(self, num: int) -> Optional[int]:
        """
        Get the count of numbers in the collection that are grater than the given number.

        Args:
            num (int): The number to compare.

        Returns:
            int or None: The count of numbers in the collection where `num` is greater than the specific value. Returns `None` if `num` is not a positive integer or exceeds the maximum value.

        """
        if is_positive_integer_until_max_value(num):
            return self.stats.get(num).get('count_gt', 0)
