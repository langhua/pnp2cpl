# pnp2cpl

这是一个小工具，用于把Fritzing导出的Gerber文件中的*_pnp.xy文件，转换成CPL文件。这个CPL文件，在淘宝等选用贴片服务时，会用到。


## 使用方法
1. 下载本工具，解压。
2. 把Fritzing导出的Gerber文件放在本工具目录下。
3. 运行`python pnp2cpl.py`。
4. 转换完成后，会在本工具目录下生成`*.cpl`文件。


## 开发
本项目遵循[Apache License 2.0](LICENSE.txt)。代码主要由Copilot生成。建议使用VSCode进行后续开发。


## 参考资料
1. [How to generate BOM and CPL from Fritzing?](https://jlcpcb.com/help/article/how-to-generate-bom-and-cpl-from-fritzing)