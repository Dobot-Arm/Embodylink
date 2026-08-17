# 说明
此工具主要是在 `Ubuntu 20.04.6版本`中使用

# Ubuntu系统安装
略过

# 开发环境安装
## Qt安装
 - 选择的安装版本是：`qt-opensource-linux-x64-5.12.12.run`[https://download.qt.io/archive/qt/5.12/5.12.12/](https://download.qt.io/archive/qt/5.12/5.12.12/)
 - 按照向导一路安装即可。

## Python环境的安装
 1. 更新系统中的包管理器，以确保是最新的库和包
    ```
    sudo apt update
    sudo apt upgrade
    ```
2. 安装构建Python所需的依赖包
    ```
    sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl
    ```
3. 从官方Python网站下载Python 3.8.20的源码包。
    ```
    切换到你自己要安装的路径
    cd /usr/src
    sudo wget https://www.python.org/ftp/python/3.8.20/Python-3.8.20.tgz
    ```

4. 解压下载的tar包并进入解压后的目录。
    ```
    sudo tar xzf Python-3.8.20.tgz
    cd Python-3.8.20
    ```

5. 运行./configure脚本以配置Python的编译选项
    ```
    sudo ./configure --enable-optimizations
    ```

6. 编译并安装Python
    ```
    sudo make -j 4
    sudo make altinstall
    ```

7. 安装完成后验证安装是否成功：`python3.8 --version`

8. 如果希望使用python3命令来调用Python 3.8，可以通过以下方式更新
    ```
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.8 1

    后续可以使用以下方式
    python3 --version
    ```

9. 如果有多个python环境需要编译不同版本，那么可以通过如下方式来切换版本号
    ```
    sudo ln -sf /usr/local/bin/python3.8 /usr/bin/python3
    sudo ln -sf /usr/local/bin/pip3.8 /usr/bin/pip3
    echo "已切换到Python 3.8"
    python3 --version
    pip3 --version
    
    
    sudo ln -sf /usr/local/bin/python3.10 /usr/bin/python3  
    sudo ln -sf /usr/local/bin/pip3.10 /usr/bin/pip3
    echo "已切换到Python 3.10"
    python3 --version
    pip3 --version
    
    
    有时候切换版本后，发现版本号依然不对，这时候要看看是不是当前用户目录也配置了，假设当前用户目录是/home/linux，则
    ls -la /home/linux/.local/bin/pip*
    rm -f /home/linux/.local/bin/pip*
    
    有时候通过pyinstaller进行打包时，发现这版本也没有切换过来，直接做法：
    先删除
    rm -f $HOME/.local/bin/pyinstaller*
    再安装
    pip3 install pyinstaller
    查看版本
    head -1 $(which pyinstaller)
    ```
    

# 程序发布
## 主程序`EmbodyLink`打包发布
>* 在`EmbodyLink`执行文件所在的目录执行以下命令，复制一些依赖包：
>    ```shell
>    linuxdeployqt EmbodyLink -appimage
>    ```
>* 执行命令压缩 `tar czvf EmbodyLink.tar.gz ./EmbodyLink`
>* 将压缩包发给用户即可。

# 开源许可证

项目开源地址：[https://github.com/Dobot-Arm/Embodylink](https://github.com/Dobot-Arm/Embodylink)

除另有明确声明的第三方组件外，本项目自有代码依据 GNU General Public
License version 3（`GPL-3.0-only`）发布。完整许可证正文见 [LICENSE](license/LICENSE)。

第三方组件仍适用其各自的许可证，不因本项目采用 GPLv3 而改变。相关说明见
[THIRD_PARTY_LICENSES.md](license/THIRD_PARTY_LICENSES.md)。向本项目提交的贡献，除另有
书面约定外，也按 `GPL-3.0-only` 发布。
