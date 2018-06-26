# xboxpy

[See issues](https://github.com/XboxDev/xboxpy/issues) to find out how to help us!
You can also create a new issue if you have trouble with xboxpy.

## Tips

* All stuff is internally imported by the `xboxpy` module. So: `import xboxpy`
* You can define the interface you want to use using environment variable 'XBOX_IF':
  * 'XBDM' (default)
  * 'nxdk-rdt`
  * 'gdb' (auto-detected if the `gdb` module exists)
* Some interfaces will also allow you to specify the target Xbox using the 'XBOX' environment variable ('Host:Port')

Not all interfaces support all functionality at this point.
