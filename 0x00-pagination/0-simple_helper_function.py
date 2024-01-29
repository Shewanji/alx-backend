#!/usr/bin/env python3
"""module for index_range function"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end indices for pagination.
    """

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return start_index, end_index
