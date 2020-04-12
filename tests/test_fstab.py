import pytest
from context import Fstab, Entry, InvalidFstabLine, InvalidEntry
import io

normal_spaces = """
UUID=1234567890 / ext4 rw,relatime 0 1
UUID=1231231231 none swap defaults,pri=-2 0 0
"""

normal_tabs = """
UUID=1234567890	/         	ext4      	rw,relatime	0 1
UUID=1231231231	none      	swap      	defaults,pri=-2	0 0
"""

comments = """
# Hello world
UUID=1234567890 / ext4 rw,relatime 0 1
#     Testing  # out
    # Weird test #
UUID=1231231231 none swap defaults,pri=-2 0 0
"""

bad_file = """
hello world
"""

normal_spaces_tight = (
    "UUID=1234567890 / ext4 rw,relatime 0 1\n"
    "UUID=1231231231 none swap defaults,pri=-2 0 0"
)

many_devices_single_dir = """
UUID=1234567890 /my/directory ext4 rw,relatime 0 1
UUID=1231231231 /my/directory ext4 rw,relatime 0 1
"""

single_device_many_dirs = """
UUID=1234567890 /my/directory1 ext4 rw,relatime 0 1
UUID=1234567890 /my/directory2 ext4 rw,relatime 0 1
"""


def test_normal_spaces():
    fstab = Fstab().read_string(normal_spaces)

    assert len(fstab.entries) == 2

    assert fstab.entries[0].device == "UUID=1234567890"
    assert fstab.entries[0].dir == "/"
    assert fstab.entries[0].type == "ext4"
    assert fstab.entries[0].options == "rw,relatime"
    assert fstab.entries[0].dump == 0
    assert fstab.entries[0].fsck == 1

    assert fstab.entries[1].dir == "none"


def test_normal_tabs():
    fstab = Fstab().read_string(normal_tabs)

    assert len(fstab.entries) == 2

    assert fstab.entries[0].device == "UUID=1234567890"
    assert fstab.entries[0].dir == "/"
    assert fstab.entries[0].type == "ext4"
    assert fstab.entries[0].options == "rw,relatime"
    assert fstab.entries[0].dump == 0
    assert fstab.entries[0].fsck == 1

    assert fstab.entries[1].dir == "none"


def test_empty():
    fstab = Fstab().read_string("")

    assert len(fstab.entries) == 0


def test_comments():
    fstab = Fstab().read_string(comments)

    assert len(fstab.entries) == 2

    assert fstab.entries[0].device == "UUID=1234567890"
    assert fstab.entries[0].dir == "/"
    assert fstab.entries[0].type == "ext4"
    assert fstab.entries[0].options == "rw,relatime"
    assert fstab.entries[0].dump == 0
    assert fstab.entries[0].fsck == 1

    assert fstab.entries[1].dir == "none"


def test_bad_file():
    with pytest.raises(InvalidFstabLine):
        Fstab().read_string(bad_file)


def test_file_handle_read():
    handle = io.StringIO(comments)

    fstab = Fstab().read_file(handle)

    assert len(fstab.entries) == 2

    assert fstab.entries[0].device == "UUID=1234567890"
    assert fstab.entries[0].dir == "/"
    assert fstab.entries[0].type == "ext4"
    assert fstab.entries[0].options == "rw,relatime"
    assert fstab.entries[0].dump == 0
    assert fstab.entries[0].fsck == 1

    assert fstab.entries[1].dir == "none"


def test_file_handle_write():
    handle = io.StringIO()

    fstab = Fstab().read_string(normal_spaces_tight)

    assert len(fstab.entries) == 2

    assert fstab.entries[0].device == "UUID=1234567890"
    assert fstab.entries[0].dir == "/"
    assert fstab.entries[0].type == "ext4"
    assert fstab.entries[0].options == "rw,relatime"
    assert fstab.entries[0].dump == 0
    assert fstab.entries[0].fsck == 1

    assert fstab.entries[1].dir == "none"

    fstab.write_file(handle)

    handle.seek(0, 0)

    res = handle.read()

    assert res == normal_spaces_tight


def test_many_devices_single_dir_only_valid():
    fstab = Fstab().read_string(many_devices_single_dir, only_valid=True)

    assert len(fstab.entries) == 1

    assert fstab.entries[0].device == "UUID=1231231231"


def test_many_devices_single_dir():
    fstab = Fstab().read_string(many_devices_single_dir, only_valid=False)

    assert len(fstab.entries) == 2

    assert fstab.entries[0].device == "UUID=1234567890"


def test_single_device_many_dirs_only_valid():
    fstab = Fstab().read_string(single_device_many_dirs, only_valid=True)

    assert len(fstab.entries) == 2

    assert fstab.entries[0].device == "UUID=1234567890"


def test_single_device_many_dirs():
    fstab = Fstab().read_string(single_device_many_dirs, only_valid=False)

    assert len(fstab.entries) == 2

    assert fstab.entries[0].device == "UUID=1234567890"


def test_many_devices_single_dir_filehandle_only_valid():
    handle = io.StringIO(many_devices_single_dir)

    fstab = Fstab().read_file(handle, only_valid=True)

    assert len(fstab.entries) == 1

    assert fstab.entries[0].device == "UUID=1231231231"


def test_many_devices_single_dir_filehandle():
    handle = io.StringIO(many_devices_single_dir)

    fstab = Fstab().read_file(handle, only_valid=False)

    assert len(fstab.entries) == 2

    assert fstab.entries[0].device == "UUID=1234567890"


def test_fstab_bool():
    fstab = Fstab()
    assert not fstab

    fstab.read_string(comments)
    assert fstab


def test_fstab_repr():
    fstab = Fstab()
    assert repr(fstab) == "<Fstab [0 entries]>"

    fstab.read_string(comments)
    assert repr(fstab) == (
        "<Fstab [2 entries]\n"
        "  UUID=1234567890 / ext4 rw,relatime 0 1\n"
        "  UUID=1231231231 none swap defaults,pri=-2 0 0\n"
        ">"
    )


def test_invalid_entry():
    entry = Entry()
    with pytest.raises(InvalidEntry):
        entry.write_string()

    with pytest.raises(InvalidFstabLine):
        entry.read_string("Hello world")

    assert repr(entry) == "<Entry Invalid>"

    entry.read_string("UUID=1234567890 / ext4 rw,relatime 0 1")

    assert repr(entry) == "<Entry UUID=1234567890 / ext4 rw,relatime 0 1>"
