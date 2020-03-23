from typing import Union


class IdMap:
    """Helper class to store a mapping from strings to ids."""

    def __init__(self):
        self.str_to_id = {}
        self.id_to_str = []

    def __len__(self):
        """Return number of terms stored in the IdMap"""
        return len(self.id_to_str)

    def _get_str(self, i: int) -> str:
        """Returns the string corresponding to a given id (`i`)."""
        # Out of range error will be thrown automatically,
        # no need to handle it separately
        return self.id_to_str[i]

    def _get_id(self, s: str) -> int:
        """Returns the id corresponding to a string (`s`). """
        if s not in self.str_to_id:
            raise KeyError("String not registered in IdMap")
        return self.str_to_id[s]

    def insert_str(self, s: str) -> int:
        """Inserts a new string in the IdMap and returns its id"""
        index = len(self.id_to_str)
        self.str_to_id[s] = index
        self.id_to_str.append(s)
        return index

    def __getitem__(self, key: Union[int, str]) -> Union[str, int]:
        """If `key` is a integer, use _get_str;
           If `key` is a string, use _get_id;"""
        if type(key) is int:
            return self._get_str(key)
        elif type(key) is str:
            return self._get_id(key)
        else:
            raise TypeError
