[电报群](https://t.me/pytimg)

# TIMG

基于[pywebview](https://github.com/r0x0r/pywebview)和[timg](https://github.com/thep0y/timg)写的图床管理软件。

![demo](https://cdn.jsdelivr.net/gh/thep0y/image-bed/md/timg-gui-demo.webp)

## 特点

> Linux系统暂时不更新，用户少，所以懒得弄，虽然我是在linux上写的。
>
> 等有linux用户反馈的时候，我再补充linux的相关说明和文件。

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

## 安装

将项目克隆到本地：

```shell
git clone https://github.com/thep0y/timg-gui.git
```

进入项目根目录后，安装所需依赖：

```shell
pip install -r requirements.txt
```

仅在`Windows 10`和`ArchLinux(KDE)`上测试。

**windows上使用Python3.9时需注意**

截止目前(2021.02.26)，pythonnet的支持3.9的wheel并未上传到pypi，所以需要手动下载安装。

[Python Extension Packages for Windows - Christoph Gohlke (uci.edu)](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pythonnet)

## 使用

进入项目根目录，执行：

```shell
python main.py
```

此时就可以上传图片、查看图片和管理图片了。

当然，第一次使用需要在配置图床，**配置**或**修改**后的图床会被设置为当前正在使用的图床。

## 附言

因为依赖`timg`，所以也就可以根据[timg](https://github.com/thep0y/timg)的README在`Typora`中使用。

## 当前发现的一些问题

- [x] windows上以edge chromium运行时，如果是两列图片的宽度，点击复制按钮图片布局会变成靠左的一列，linux上无此问题。暂未发现原因在哪儿。

