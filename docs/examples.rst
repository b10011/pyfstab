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
