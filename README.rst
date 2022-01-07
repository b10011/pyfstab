**MIT-licensed libary for parsing and creating fstab files**

|pypi| |docs| |license|

Features
========

* Unlike Canonical's fstab Python library, this actually works with Python 3
  and does not have a cancerous license (GPLv3)
* Small

Installation
============

:code:`pip3 install pyfstab`

Examples
========

.. code:: python3
   
   # Import the classes
   from pyfstab import Fstab

   # Read the file
   with open("/etc/fstab", "r") as f:
       fstab = Fstab().read_file(f)

   # List all devices/identifiers of fstab entries
   for entry in fstab.entries:
       print(entry.device)

   # List all mountpoints of CIFS mounts
   for entry in fstab.entries_by_type["cifs"]:
       print(entry.dir)

   # Print filesystem type for mount at /mnt/disk
   print(fstab.entry_by_dir["/mnt/disk"].type)

   # List all mount options for device UUID=123456
   for entry in fstab.entries_by_device["UUID=123456"]:
       print(entry.options)

   # Print Tag value for all entries with device defined as
   # UUID=something or ID=something
   for entry in fstab.entries:
       if entry.device_tag_type in {"UUID", "ID"}:
           print(entry.device_tag_value)

   # Change device tag type from UUID= to ID=
   entry.device_tag_type = "ID"

   # Change device tag value from "123456" to "4321"
   # (Changes from "ID=123456" to "ID=4321")
   entry.device_tag_value = "4321"

   # Print new device string (it's "ID=4321" now)
   print(entry.device)

   # Set both tag type and value at the same time in both valid ways
   entry.device = ("UUID", "11223344")
   entry.device = "UUID=11223344"

   # Add an entry (does not update entries_by_device/type/dir)
   # but it will be printed when formatting the fstab object
   fstab.entries.append(
       Entry(
           "/dev/sdg4",
           "/mnt/disk",
           "ext4",
           "rw,relatime",
           0,
           0
       )
   )

   # Remove all entries except ext*
   fstab.entries = [
       entry
       for entry in fstab.entries
       if entry.type.startswith("ext")
   ]

   # Print and write the formatted fstab file
   formatted = str(fstab)
   print(formatted)
   with open("/etc/myfstab", "w") as f:
       f.write(formatted)

Contributing
============

* Send any issues to GitHub's issue tracker.
* Before sending a pull request, format it with `Black`_ (-Sl79)
* Any changes must be updated to the documentation
* All pull requests must be tested with tox (if you are using pyenv, add the installed versions for py35-py38 and pypy3 to .python-version at the root of this repository before running tox)


.. _`Black`: https://github.com/psf/black

.. |pypi| image:: https://img.shields.io/pypi/v/pyfstab.svg
    :alt: PyPI
    :target: https://pypi.org/project/pyfstab/
.. |docs| image:: https://readthedocs.org/projects/pyfstab/badge/?version=latest
    :alt: Read the Docs
    :target: http://pyfstab.readthedocs.io/en/latest/
.. |license| image:: https://img.shields.io/github/license/b10011/pyfstab.svg
    :alt: License
    :target: https://github.com/b10011/pyfstab/blob/master/LICENSE
