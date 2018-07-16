# xboxpy

[See issues](https://github.com/XboxDev/xboxpy/issues) to find out how to help us!
You can also create a new issue if you have trouble with xboxpy.


### Install

*If you don't have it already, install [a Python 3 release](https://www.python.org/downloads/) of your choice.*
*Also [ensure you have pip for Python 3 installed](https://pip.pypa.io/en/stable/installing/).*

Simply run:

```
pip3 install --user -U git+https://github.com/XboxDev/xboxpy.git#egg=xboxpy
```

Now xboxpy should be installed and ready for use!


### Use

All code is internally imported by the `xboxpy` module.
So all you have to do is: `import xboxpy`.

You can choose the interface you want to use using environment variable 'XBOX_IF':

  * 'XBDM' (default) - part of the official Xbox Development Kit Debug Kernel by Microsoft.
  * 'nxdk-rdt' - [nxdk-rdt is an open-source Xbox Remote Dev Tool](https://github.com/XboxDev/nxdk-rdt).
  * 'gdb' - can be used to [interface with gdb](https://sourceware.org/gdb/onlinedocs/gdb/Python.html).

Some interfaces will also allow you to specify the target Xbox using the 'XBOX' environment variable ('Host:Port').
Not all interfaces support all functionality at this point.


### Develop

Clone xboxpy [using git](https://git-scm.com/) and install it from the the local folder in editable mode:

```
git clone https://github.com/XboxDev/xboxpy.git
pip3 install --user -e ./xboxpy
```

Now you can make changes to the code locally.
All projects using xboxpy will automatically use your modified version.


### Contribute

Once you are happy with your changes, you should contribute to the official version of xboxpy!

[Fork xboxpy on GitHub](https://github.com/XboxDev/xboxpy) and [send a Pull Request to us](https://github.com/XboxDev/xboxpy/pulls).


---

(c)2018 XboxDev maintainers

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

*Contact us for other licensing options.*
