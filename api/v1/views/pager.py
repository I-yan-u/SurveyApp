#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""
from typing import List, Dict


class Pager:
    """Pager class to paginate a database.
    """
    DATA_FILE = "0x00-pagination/Popular_Baby_Names.csv"

    def __init__(self, response):
        self.__dataset = self.dataset(response)
        self.__indexed_dataset = None
        self.__datalength = None

    def dataset(self, response: List) -> List[List]:
        """Cached dataset
        """
        self.__dataset = None
        self.__dataset = response
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.__dataset
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
            self.__datalength = len(self.__indexed_dataset)
        return self.__indexed_dataset, self.__datalength

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Get hypermedia object with provided index
        """
        data_set, data_length = self.indexed_dataset()
        assert index < len(self.__indexed_dataset)
        start = index
        while start not in data_set:
            start += 1

        data = []
        try:
            for i in range(start, start + page_size):
                data.append(data_set[i])
        except KeyError:
            pass

        return {
            'index': index,
            'data': data,
            'page_size': page_size,
            'next_index': start + page_size,
            'data_length': data_length
        }
