# 重要说明
## 1. `teleoperateapp`代码后期不再进行维护修改，而是直接使用项目内`teleoperateapp\teleoperate_sever`目录的代码。
## 2. `teleoperate_sever`代码主要由`算法`、`嵌入式`维护，上位机基本不做修改，除非它的改动涉及到了上位机的修改。
## 3. 虽然`teleoperateapp`代码不再维护，但是`算法`那边提供的库我们依然要替换更新。


# 说明
此目录下的工程都是`DobotRXStudio`依赖的独立的工具。

## `pklparserapp`
- 为`pkl`转`json`的工具。
- 因为`c++`很难解析`pkl`格式文件，所以使用`python`转好了后直接用。如果找到了c++库，考虑是否替换。
- 打包时，不要打包成一个独立的文件，否则运行时解压，可能因为权限问题导致无法解压资源，从而运行失败，请使用以下方式打包

    ```
    pyinstaller --name pklparserapp main.py
    ```

## `robotformatapp`
- 训练格式转换工具，将采集的原始数据转为算法训练需要的各种格式
- 因为`c++`很难将采集的数据转换为训练需要的各种格式文件，所以使用`python`转好了后直接用。如果找到了c++库，考虑是否替换。
- 打包时，不要打包成一个独立的文件，否则运行时解压，可能因为权限问题导致无法解压资源，从而运行失败，请使用以下方式打包

    ```
    #pyinstaller --name robotformatapp main.py
    pyinstaller main.spec
    ```
