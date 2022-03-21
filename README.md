[电报群](https://t.me/py_up2b)

# up2b

基于[pywebview](https://github.com/r0x0r/pywebview)和[up2b](https://github.com/thep0y/up2b)写的图床管理软件。

正在重构的动图演示：

<video src="https://raw.githubusercontent.com/thep0y/up2b-gui/main/multimedia-files/demo.mov"></video>

## 特点

支持以下图床的管理：

- sm.ms
- imgtu.com
- gitee.com
- github.com

理论上支持图片的自动压缩，但肯定不完美，超过图床限制大小的图片依然建议手动调整。

当前为测试版，功能有：

- 上传图片
  - 多图上传，一次最多上传10张图片
  - 上传成功后单击图片即可复制图片链接
- 查看所有图片
  - 12张图片为一组
  - 单击图片可查看原图
    - 直接拖拽原图到本地可保存为本地图片
  - 单击复制按钮复制图片链接
  - 单击删除按钮在图床里删除此图
    - 批量删除功能未实现
- 一键切换图床
- 自动压缩图片
  - 仅对jpg和png格式的图片有效
  - 此功能不实用，不建议开启

## 开发调试

重构后增加开发模式，可以实现前后端分离分别运行开发而互不影响。

前端运行：

```bash
cd up2b
yarn dev
```

后端运行：

```bash
python -m server
```

前后端在开发模式中都支持热重载（热更新），方便开发调试。

## 安装

### 1 源码安装

将项目克隆到本地：

```shell
git clone https://github.com/thep0y/up2b-gui.git
```

进入项目根目录后，安装所需依赖：

```shell
pip install -r requirements.txt
```

仅在`Windows 10`和`ArchLinux(KDE)`上测试。

**windows上使用Python3.9时需注意**

截止目前(2021.02.26)，pythonnet的支持3.9的wheel并未上传到pypi，所以需要手动下载安装。

[Python Extension Packages for Windows - Christoph Gohlke (uci.edu)](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pythonnet)

### 2 二进制文件

仅限windows10系统，在release里下载最新版即可。

#### 或自行打包

打包为一个exe：

```po
pyinstaller -windowed -F -y -n up2b --version-file version --collect-binaries clr_loader --clean -i ./assets/favicon.ico --add-data "assets;assets" main.py
```

打包为一个目录：

```powershell
pyinstaller -windowed -y -n up2b --version-file version --collect-binaries clr_loader --clean -i ./assets/favicon.ico --add-data "assets;assets" main.py
```

### 3 Linux安装脚本一键安装（默认使用qt）

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/thep0y/up2b-gui/main/install.sh)"
```

## 使用

本项目提供路过图床(imgtu.com)的测试账号用于体验，用户名和密码皆为`timg_test`，请勿将测试账号用于非法用途。



进入项目根目录，执行：

```shell
python main.py
```

此时就可以上传图片、查看图片和管理图片了。

当然，第一次使用需要在配置图床，**配置**或**修改**后的图床会被设置为当前正在使用的图床。

图片上传成功后，记得点击椭圆形的图床按钮刷新才能在`所有图片`里加载（未来会改为上传成功后即添加到`所有图片`里）

## 附言

因为依赖`up2b`，所以也就可以根据[up2b](https://github.com/thep0y/up2b)的README在`Typora`中使用。

