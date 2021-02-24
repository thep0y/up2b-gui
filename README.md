# TIMG

基于[pywebview](https://github.com/r0x0r/pywebview)和[timg](https://github.com/thep0y/timg)写的图床管理软件。

## 特点

支持以下图床的管理：

- sm.ms
- imgtu.com
- gitee.com
- github.com

理论上支持图片的自动压缩，但肯定不完美，超过图床限制大小的图片依然建议手动调整。

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

## 使用

进入项目根目录，执行：

```shell
python main.py
```

此时就可以上传图片、查看图片和管理图片了。