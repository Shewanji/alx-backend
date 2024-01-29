#!/usr/bin/env python3
"""module for index_range function"""

import csv
import math
from typing import List, Tuple, Any, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def index_range(self, page: int, page_size: int) -> Tuple[int, int]:
        """
        Calculate the start and end indices for pagination.
        """

        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        return start_index, end_index

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieve a specific page of the dataset based on pagination parameters
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = self.index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]

    def get_hyper(
            self,
            page: int = 1,
            page_size: int = 10
    ) -> Dict[str, Any]:
        """Retrieve hypermedia information about the dataset
        based on pagination parameters.
        """

        current_page = page
        total_pages = math.ceil(len(self.dataset()) / page_size)
        next_page = current_page + 1 if current_page < total_pages else None
        prev_page = current_page - 1 if current_page > 1 else None

        return {
            'page_size': len(self.get_page(page, page_size)),
            'page': current_page,
            'data': self.get_page(page, page_size),
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages,
        }
