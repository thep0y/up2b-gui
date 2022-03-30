# up2b

基于[pywebview](https://github.com/r0x0r/pywebview)和[up2b](https://github.com/thep0y/up2b)写的图床管理软件。

演示视频：

https://user-images.githubusercontent.com/51874567/159233149-22a09854-32ab-4b59-bd9a-36d285cc4561.mov

## 特点

支持以下图床的管理：

- sm.ms
- imgtu.com
- github.com

理论上支持图片的自动压缩，但肯定不完美，超过图床限制大小的图片依然建议手动调整。

当前为测试版，功能有：

- 上传图片
  - 上传页面最多保留 20 条上传记录
  - 上传成功后鼠标在缩略图上悬浮可复制图片链接
- 查看所有图片
  - 缩略图上有图片预览按钮
    - 直接拖拽原图到本地可保存为本地图片
  - 单击复制按钮复制图片链接
  - 单击删除按钮在图床里删除此图
    - 批量删除功能未实现
- 一键切换图床
- 自动压缩图片
  - 仅对 jpg 和 png 格式的图片有效
  - 此功能不实用，不建议开启

## 开发调试

重构后增加开发模式，可以实现前后端分离分别运行开发而互不影响。

前端运行开发服务器：

```bash
cd up2b
yarn dev
```

后端运行开发服务器：

```bash
python -m server
```

前后端在开发模式中都支持热重载（热更新），方便开发调试。

## 安装

### 二进制文件

支持 windows、macOS、debian系发行版，在 release 里下载[最新版](https://github.com/thep0y/up2b-gui/releases/latest)即可。

linux第一次启动时由于需要安装一些依赖会比较慢，耐心等待软件界面弹出，之后就可以即时启动。

### 或自行打包

手动打包需要先编译静态文件（前端），前端的目录是本项目中的`up2b`目录，可根据里面的 REAME 测试或编译。

以 windows 为例。

打包为一个 exe：

```powershell
pyinstaller -windowed -F -y -n up2b --version-file version --collect-binaries clr_loader --clean -i ./assets/favicon.ico --add-data "assets;assets" main.py
```

打包为一个目录：

```powershell
pyinstaller -windowed -y -n up2b --version-file version --collect-binaries clr_loader --clean -i ./assets/favicon.ico --add-data "assets;assets" main.py
```

## 试用

本项目提供路过图床(imgtu.com)的测试账号用于体验，用户名和密码皆为`timg_test`，请勿将测试账号用于非法用途。

此时就可以上传图片、查看图片和管理图片了。

当然，第一次使用需要在配置图床，**配置**或**修改**后的图床会被设置为当前正在使用的图床。

图片上传成功后，自动在`图片列表`里加载。