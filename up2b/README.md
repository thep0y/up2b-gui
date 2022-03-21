# UP2B 页面

用 Vue3 + Element-Plus 写的界面，搭配 Vite 开发。

## 开发

开发模式执行：

```bash
yarn dev
```

但此模式若想正常运行还需搭配后端：

```bash
cd ..
python -m server
```

然后用浏览器打开http://localhost:3000就能调试了。

## 编译

最终需要使用的是编译后静态文件：

```bash
yarn build
```

静态文件会输出到本仓库项目的根目录的`assets`目录。

