from typing import Optional

MAX_VALUE = 1000


def is_positive_integer_until_max_value(num: int) -> bool:
    """
    Check if a given number is a positive integer within the maximum value.

    :param num: The number to be checked.
    :return: True if the number is a positive integer within the maximum value, False otherwise.
    """
    return isinstance(num, int) and 0 <= num <= MAX_VALUE


class DataCapture:
    def __init__(self, max_value: int = 1000) -> None:
        self.max_value = max_value
        self.frequencies = {}
        self.max_num = 0
        self.freq_sum = 0
        self.min_num = 0

    def add(self, num: int) -> None:
        """
        :param num: The number to be added to the frequencies dictionary.
        :return: None

        This method adds the given number to the frequencies dictionary. It increments the frequency count of the number
        in the dictionary by 1. It also updates the total frequency sum.

        If the number is greater than the current maximum number (self.max_num), it updates the maximum number.

        If the number is smaller than the current minimum number (self.min_num), it updates the minimum number.

        Note: The method assumes that the input number is a positive integer and doesn't perform any validation.

        Example usage:
            obj = ClassName()
            obj.add(10)
        """
        if not is_positive_integer_until_max_value(num):
            return False
        else:
            self.frequencies[num] = self.frequencies.get(num, 0) + 1
            self.freq_sum += 1
            if num > self.max_num:
                self.max_num = num
            if num < self.min_num:
                self.min_num = num

    def build_stats(self):
        """
        Generate a Stats object using the frequencies and max_num attributes.

        Returns:
            Stats: A Stats object initialized with the frequencies and max_num attributes.
        """
        return Stats(self.frequencies, self.max_num)


class Stats:

    def __init__(self, frequencies: dict, max_num: int) -> None:
        """
        Initializes a new instance of the class.

        Parameters:
            frequencies (dict): A dictionary containing the frequencies of numbers.
            max_num (int): The maximum number to calculate frequencies for.

        Raises:
            ValueError: If the frequencies dictionary is empty.

        Returns:
            None
        """
        if not frequencies:
            raise ValueError("There's no data to build stats for")
        self.frequencies = frequencies
        self.stats = {}
        self.max_num = max_num
        self.less_count = [0] * (self.max_num + 2)
        self.greater_count = [0] * (self.max_num + 2)
        # calculate less count
        for i in range(1, self.max_num + 2):
            self.less_count[i] = self.less_count[i - 1] + frequencies.get(i - 1, 0)
        # calculate greater count
        for i in range(self.max_num, -1, -1):
            self.greater_count[i] = self.greater_count[i + 1] + frequencies.get(i + 1, 0)

    def less(self, num: int) -> Optional[int]:
        """
        Return the value from the `less_count` list at the given index `num` if the `num` is a positive integer within the maximum value. Otherwise, return None.

        Parameters:
            num (int): The index of the value to be returned from the `less_count` list.

        Returns:
            Optional[int]: The value from the `less_count` list at the given index `num`, or None if `num` is not a positive integer within the maximum value.
        """
        if is_positive_integer_until_max_value(num):
            return self.less_count[num]

    def greater(self, num: int) -> Optional[int]:
        """
        Retrieve the greater count for a given number.

        Args:
            num (int): The number to check.

        Returns:
            Optional[int]: The greater count for the given number, if it is a positive integer until the maximum value. Otherwise, None.
        """
        if is_positive_integer_until_max_value(num):
            return self.greater_count[num]

    def between(self, lower: int, upper: int) -> int:
        """
        Calculates the number of elements in the `less_count` array between the given `lower` and `upper` values.

        Args:
            lower (int): The lower bound of the range.
            upper (int): The upper bound of the range.

        Returns:
            int: The number of elements in the `less_count` array between `lower` and `upper`.
        """
        if (
                is_positive_integer_until_max_value(lower)
                and is_positive_integer_until_max_value(upper)
        ):

            # reordering parameter values
            if lower > upper:
                lower, upper = upper, lower

            if upper > self.max_num:
                # this is to make sure that we always get an index if the upper bound parameter is greater than the maximum value captured
                upper = self.max_num

            return self.less_count[upper + 1]
