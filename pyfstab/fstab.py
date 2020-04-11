from .entry import Entry, InvalidEntry, InvalidFstabLine
from collections import defaultdict


class Fstab:
    """
    Handles reading, parsing, formatting and writing of fstab files.

    :var entries:
        (list[Entry]) -
        List of entries.
        When writing to a file, entries are listed from this list.

    :var entries_by_device:
        (dict[str, list[Entry]]) -
        Fstab entries by device.

    :var entry_by_dir:
        (dict[str, Entry]) -
        Fstab entry by directory.

    :var entries_by_type:
        (dict[str, list[Entry]]) -
        Fstab entries by type.
    """

    def __init__(self):
        self.entries = []

        # A single device can have multiple mountpoints
        self.entries_by_device = defaultdict(list)

        # If multiple devices have same mountpoint, only the last entry in the
        # fstab file is taken into consideration
        self.entry_by_dir = dict()

        # And the most obvious one, many entries can have mountpoints of same
        # type
        self.entries_by_type = defaultdict(list)

    def read_string(self, data, only_valid=False):
        """
        Parses entries from a data string

        :param data: Contents of the fstab file
        :type data: str

        :param only_valid:
            Skip the entries that do not actually mount. For example, if device
            A is mounted to directory X and later device B is mounted to
            directory X, the A mount to X is undone by the system.
        :type only_valid: bool

        :return: self
        :rtype: Fstab
        """
        for line in reversed(data.splitlines()):
            try:
                entry = Entry().read_string(line)
                if entry and (
                    not only_valid or entry.dir not in self.entry_by_dir
                ):
                    self.entries.insert(0, entry)
                    self.entries_by_device[entry.device].insert(0, entry)
                    self.entry_by_dir[entry.dir] = entry
                    self.entries_by_type[entry.type].insert(0, entry)
            except InvalidEntry:
                pass

        return self

    def read_file(self, handle, only_valid=False):
        """
        Parses entries from a file

        :param handle: File handle
        :type handle: file

        :param only_valid:
            Skip the entries that do not actually mount. For example, if device
            A is mounted to directory X and later device B is mounted to
            directory X, the A mount to X is undone by the system.
        :type only_valid: bool

        :return: self
        :rtype: Fstab
        """
        self.read_string(handle.read(), only_valid)

        return self

    def write_file(self, handle):
        """
        Parses entries in data string

        :param path: File handle
        :type path: file

        :return: self
        :rtype: Fstab
        """
        handle.write(str(self))

        return self

    def __str__(self):
        return "\n".join(str(entry) for entry in self.entries)

    def __repr__(self):
        res = "<Fstab [{} entries]".format(len(self.entries))

        if self.entries:
            res += "\n"
            for entry in self.entries:
                res += "  {}\n".format(entry)

        res += ">"

        return res
