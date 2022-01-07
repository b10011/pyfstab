import re


class InvalidEntry(Exception):
    """
    Raised when a string cannot be generated because of the Entry is invalid.
    """


class InvalidFstabLine(Exception):
    """
    Raised when a line is invalid in fstab. This doesn't just mean that the
    Entry will be invalid but also that the system can not process the fstab
    file fully either.
    """


_valid_tag_types = {"LABEL", "UUID", "PARTLABEL", "PARTUUID", "ID"}


def _split_device_string(string):
    try:
        tag_type, tag_value = string.split("=", 1)

        if tag_type in _valid_tag_types:
            return (tag_type, tag_value)
        else:
            return (None, string)

    except ValueError:
        return (None, string)


class Entry:
    """
    Handles parsing and formatting fstab line entries.

    :var device:
        (str or None) -
        Fstab device (1st parameter in the fstab entry)

    :var dir:
        (str or None) -
        Fstab device (2nd parameter in the fstab entry)

    :var type:
        (str or None) -
        Fstab device (3rd parameter in the fstab entry)

    :var options:
        (str or None) -
        Fstab device (4th parameter in the fstab entry)

    :var dump:
        (int or None) -
        Fstab device (5th parameter in the fstab entry)

    :var fsck:
        (int or None) -
        Fstab device (6th parameter in the fstab entry)

    :var valid:
        (bool) -
        Whether the Entry is valid or not. Can be checked with "if entry:".
    """

    def __init__(
        self,
        _device=None,
        _dir=None,
        _type=None,
        _options=None,
        _dump=None,
        _fsck=None,
    ):
        """
        :param _device:
            Fstab device (1st parameter in the fstab entry).
            Tuple/list in form of (type, value) is also accepted
            (e.g. ("UUID", "1234567890"))
        :type _device: Union[str, tuple, list]

        :param _dir: Fstab device (2nd parameter in the fstab entry)
        :type _dir: str

        :param _type: Fstab device (3rd parameter in the fstab entry)
        :type _type: str

        :param _options: Fstab device (4th parameter in the fstab entry)
        :type _options: str

        :param _dump: Fstab device (5th parameter in the fstab entry)
        :type _dump: int

        :param _fsck: Fstab device (6th parameter in the fstab entry)
        :type _fsck: int
        """
        # Use setters and getters for these
        self._device = None
        self._device_tag_type = None
        self._device_tag_value = None

        self.device = _device
        self.dir = _dir
        self.type = _type
        self.options = _options
        self.dump = _dump
        self.fsck = _fsck

        self.valid = True
        self.valid &= self._device is not None
        self.valid &= isinstance(self._device, (str, tuple, list))
        self.valid &= self.dir is not None
        self.valid &= self.type is not None
        self.valid &= self.options is not None
        self.valid &= self.dump is not None
        self.valid &= self.fsck is not None

    @property
    def device(self):
        """
        :return: device part string (e.g. "UUID=1234")
        """
        return self._device

    @device.setter
    def device(self, value):
        """
        :param value: new device string or tuple/list (e.g. "ID=123"
            or ("ID", "123"))
        :type value: Union[str, tuple, list]
        """
        if isinstance(value, str):
            (
                self._device_tag_type,
                self._device_tag_value,
            ) = _split_device_string(value)
            self._device = value
        elif isinstance(value, (tuple, list)):
            self._device_tag_type, self._device_tag_value = value
            self._device = "{}={}".format(
                self._device_tag_type, self.device_tag_value
            )
        else:
            # For unknown values
            self._device = value
            self._device_tag_type = None
            self._device_tag_value = None

    @property
    def device_tag_type(self):
        """
        :return: device tag's type part string (e.g. "UUID" in "UUID=1234")
        """
        return self._device_tag_type

    @device_tag_type.setter
    def device_tag_type(self, value):
        """
        :param value: new device tag's type part (e.g. "UUID")
        :type value: str
        """
        self.device = (value, self.device_tag_value)

    @property
    def device_tag_value(self):
        """
        :return: device tag's value part string (e.g. "1234" in "UUID=1234")
        """
        return self._device_tag_value

    @device_tag_value.setter
    def device_tag_value(self, value):
        """
        :param value: new device tag's value part (e.g. "123" in "ID=123")
        :type value: str
        """
        self.device = (self.device_tag_type, value)

    def read_string(self, line):
        """
        Parses an entry from a string

        :param line: Fstab entry line.
        :type line: str

        :return: self
        :rtype: Entry

        :raises InvalidEntry: If the data in the string cannot be parsed.
        """
        line = line.strip()
        if line and not line[0] == "#":
            parts = re.split(r"\s+", line)

            if len(parts) == 6:
                [_device, _dir, _type, _options, _dump, _fsck] = parts

                _dump = int(_dump)
                _fsck = int(_fsck)

                self.device = _device
                self.dir = _dir
                self.type = _type
                self.options = _options
                self.dump = _dump
                self.fsck = _fsck

                self.valid = True
                return self
            else:
                raise InvalidFstabLine()

        self.device = None
        self.dir = None
        self.type = None
        self.options = None
        self.dump = None
        self.fsck = None

        self.valid = False

        raise InvalidEntry("Entry cannot be parsed")

    def write_string(self):
        """
        Formats the Entry into fstab entry line.

        :return: Fstab entry line.
        :rtype: str

        :raises InvalidEntry:
            A string cannot be generated because the entry is invalid.
        """
        if self:
            return "{} {} {} {} {} {}".format(
                self.device,
                self.dir,
                self.type,
                self.options,
                self.dump,
                self.fsck,
            )
        else:
            raise InvalidEntry("Entry cannot be formatted")

    def __bool__(self):
        return self.valid

    def __str__(self):
        return self.write_string()

    def __repr__(self):
        try:
            return "<Entry {}>".format(str(self))
        except InvalidEntry:
            return "<Entry Invalid>"
