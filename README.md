# 泰山俯卧撑检测系统说明文档

## 环境配置

Linux环境下，打开终端，输入以下命令，编译生成.so文件

```bash
$ g++ loop.cpp -fPIC -shared -o loop.so
```

Windows环境下，打开终端，输入以下命令，编译生成.dll文件

```bash
$ g++ --share loop.cpp -o loop.dll
```

对于生成的.so或.dll文件，放在目录下。

找到Project.py 中的loop类，根据当前系统环境选择对应的文件名（默认为windows环境）

```python
# FOR LINUX, command: g++ loop.cpp -fPIC -shared -o loop.so 
# _file = 'loop.so' 
# FOR Windows, command: g++ --share loop.cpp -o loop.dll |
 _file = 'loop.dll'
```

## 程序运行


# Taishan_Preprocess
For data preprocessing in Taishan PUSH-UP Detection Project.


Before running the programme, you should compile the loop.cpp, then genetate loop.so (Linux) or loop.dll (Windows)


## Environment

To run in Linux

```bash
$ g++ loop.cpp -fPIC -shared -o loop.so
```


To run in Windows

```bash
$ g++ --share loop.cpp -o loop.dll
```
