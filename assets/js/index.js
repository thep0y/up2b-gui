var $ = layui.$,
    form = layui.form,
    upload = layui.upload,
    layer = layui.layer,
    flow = layui.flow
var conf
var bedList = new Array
var allImages, pages
var pageSize = 12
var currentTagIndex = parseInt(localStorage.getItem("currentTagIndex"))


if (!isNaN(currentTagIndex)) {
    let ul = document.getElementsByClassName("layui-tab-title")[0]
    autoClick(ul.children[currentTagIndex])
}

//模拟点击，切换tab
function autoClick(el) {
    var evt = document.createEvent("MouseEvents");
    evt.initEvent("click", true, true);
    el.dispatchEvent(evt);
}


form.render()

window.addEventListener('pywebviewready', function () {
    showImageBeds()
})

// 页面刷新前
window.onbeforeunload = function (e) {
    let li = document.getElementsByClassName("layui-this")[0]
    let index = 0
    while (li) {
        li = li.previousSibling
        if (li != null && li.nodeName == "LI") {
            index++
        }    
    }
    localStorage.setItem("currentTagIndex", index)
}

var baseHTML = `<div class="layui-form-item">
<label class="layui-form-label">用户名</label>
<div class="layui-input-inline">
    <input type="text" name="username" id="username" required="" lay-verify="username"
        placeholder="请输入用户名" autocomplete="on" class="layui-input">
</div>
</div>
<div class="layui-form-item">
<label class="layui-form-label">密&nbsp;&nbsp;&nbsp;&nbsp;码</label>
<div class="layui-input-inline">
    <input type="password" name="password" id="password" required="" lay-verify="password"
        placeholder="请输入密码" autocomplete="off" class="layui-input">
</div>
</div>`

var gitHTML = `<div class="layui-form-item">
<label class="layui-form-label">私人令牌</label>
<div class="layui-input-inline">
    <input type="text" name="access-token" id="access-token" required=""
        lay-verify="access-token" placeholder="请输入私人令牌" autocomplete="off" class="layui-input">
</div>
</div>
<div class="layui-form-item">
<label class="layui-form-label">用户名</label>
<div class="layui-input-inline">
    <input type="text" name="username" id="username" required="" lay-verify="username"
        placeholder="请输入用户名" autocomplete="on" class="layui-input">
</div>
</div>
<div class="layui-form-item">
<label class="layui-form-label">仓库</label>
<div class="layui-input-inline">
    <input type="text" name="repository" id="repository" required="" lay-verify="repository"
        placeholder="请输入要使用的仓库" autocomplete="on" class="layui-input">
</div>
</div>
<div class="layui-form-item">
<label class="layui-form-label">目录</label>
<div class="layui-input-inline">
    <input type="text" name="path" id="path" required="" lay-verify="path"
        placeholder="请输入要保存的目录" autocomplete="on" class="layui-input">
</div>
</div>`


function showImageBeds() {
    pywebview.api.show_image_beds().then(function (response) {
        let chooseBed = document.getElementById("image-bed")
        let html = ""
        let beds = response.beds
        for (let i in beds) {
            html += '<option value ="' + beds[i] + '">' + i + '</option>'
        }
        if (response.selected != null) {
            chooseBed.innerHTML = html
            chooseBed.value = response.selected
            let status = document.getElementById("status")
            for (let i in beds) {
                bedList.push(i)
            }
            status.innerText = bedList[response.selected]
            status.setAttribute("data-id", response.selected)
            toggleImageBedConfHTML(response.selected.toString())
            let configedBeds = document.getElementById("configed-beds-list")
            let bedsListHTML = ""
            for (let i in response.auth_data) {
                if (response.auth_data[i]) {
                    if (i == response.selected) {
                        bedsListHTML += '<button type="button" class="layui-btn">' + bedList[i] + '</button>'
                    } else {
                        bedsListHTML += '<button type="button" class="layui-btn layui-btn-primary">' + bedList[i] + '</button>'
                    }
                }
            }
            configedBeds.innerHTML = bedsListHTML
        } else {
            chooseBed.innerHTML += html
        }
        form.render("select")
        renderAutomaticCompressionSwitch()
    })
}


function toggleImageBedConfHTML(code) {
    let confBlock = document.getElementById("image-bed-conf-block")
    switch (code) {
        case "":
            confBlock.innerHTML = ""
            break
        case "0":
            confBlock.innerHTML = baseHTML
            break;
        case "1":
            confBlock.innerHTML = baseHTML
            break;
        case "2":
            confBlock.innerHTML = gitHTML
            break;
        case "3":
            confBlock.innerHTML = gitHTML
            break;
        default:
            break;
    }
}

function renderAutomaticCompressionSwitch() {
    pywebview.api.automatic_compression_status().then((response) => {
        if (response.automatic_compression) {
            $("#toggle-automatic-compression input").prop("checked", true)
            $("#toggle-automatic-compression div.layui-form-switch").addClass("layui-form-onswitch")
            $("#toggle-automatic-compression divlayui-form-switch > em").text("开启")
        }
        form.render("checkbox")
        getAllImages()
    })
}

form.verify({
    "image-bed": function (value, item) {
        if (!value) {
            return "请选择图床"
        }
    },
    username: function (value, item) {
        if (!value) {
            return "用户名不能为空"
        }
    },
    password: function (value, item) {
        if (!value) {
            return "密码不能为空"
        }
    },
    "access-token": function (value, item) {
        if (!value) {
            return "私人令牌不能为空"
        }
    },
    repository: function (value, item) {
        if (!value) {
            return "仓库不能为空"
        }
    },
    path: function (value, item) {
        if (!value) {
            return "目录不能为空"
        }
    },
})

form.on("submit(init-image-bed)", function (data) {
    let loading = layer.load(1, {
        shade: [0.8, "#FFF"]
    })
    pywebview.api.init_image_bed(form.val("image-bed-form")).then(function (response) {
        if (response.success) {
            layer.close(loading)
            let confBlock = document.getElementById("image-bed-conf-block")
            confBlock.innerHTML = ''
            document.getElementById("image-bed").innerHTML = ""
            showImageBeds()
            layer.msg("已保存登录信息，可以去上传或管理图片了")
        }
    })
    return false
})

$("#configed-beds-list").on("click", "button.layui-btn-primary", (event) => {
    let bed = event.currentTarget.innerText
    let bedCode = bedList.indexOf(bed)
    pywebview.api.choose_image_bed(bedCode).then((response) => {
        if (response.success) {
            location.reload()
        }
    })
})

$("#upload").click(() => {
    let loading = layer.load(1, {
        shade: [0.8, "#FFF"]
    })
    pywebview.api.upload_images().then((response) => {
        if (response.success) {
            let imageURLs = response.image_urls
            let uploadedBlock = document.getElementById("uploaded-images")
            let html = ""
            let failed = []
            imageURLs.forEach((url, index) => {
                if (typeof url == "object") {
                    failed.push(url)
                } else {
                    html += '<img lay-src="' + url + '" onclick="copyImageURL(this)">'
                }
            })
            uploadedBlock.innerHTML = html
            //按屏加载图片
            flow.lazyimg({
                elem: '#uploaded-images img'
            });
            layer.close(loading)
            if (failed.length > 0) {
                let errMsg = ""
                failed.forEach((err, index) => {
                    errMsg += (index + 1) + ": " + err.image_path + " - " + err.error + "<br>"
                })
                errMsg += "<hr>点击上传成功的图片即可复制链接"
                layer.alert(errMsg)
            } else {
                if (imageURLs.length) {
                    layer.msg("图片渲染完毕后，点击图片即可复制链接")
                }
            }
        } else {
            layer.close(loading)
            layer.alert(response.error)
        }
    })
})

function copyImageURL(element) {
    let url = element.getAttribute("data-url")
    if (!url) {
        url = element.getAttribute("src")
    }
    let input = document.createElement("input")
    document.body.appendChild(input)
    input.setAttribute('readonly', 'readonly')
    input.setAttribute('value', url)
    input.select()
    input.setSelectionRange(0, 9999)
    if (document.execCommand('copy')) {
        document.execCommand('copy')
        layer.msg('图片链接已复制到剪贴板')
    }
    document.body.removeChild(input)
}

$("#toggle-automatic-compression").on("click", ".layui-form-switch", function (event) {
    let ac = event.currentTarget.previousElementSibling.checked
})

form.on("switch(aac)", function (data) {
    pywebview.api.toggle_automatic_compression(data.elem.checked).then((response) => {
        console.log(response)
    })
})


// TODO: 下一步应该直接利用webview和保存的认证信息，利用webview窗口完成上传，这样的话就可以支持拖拽操作了
// upload.render({
//     elem: '#upload'
//     ,url:"/"
//     ,choose: function(obj){
//         console.log(obj)
//         obj.preview(function(index, file, result) {
//             // console.log(index)
//             // console.log(file)
//             // console.log(result)
//         })
//     }
//     ,error: function(index, upload){
//     //当上传失败时，你可以生成一个“重新上传”的按钮，点击该按钮时，执行 upload() 方法即可实现重新上传
//     }
//     // ,done: function(res){
//     //   layer.msg('上传成功');
//     //   layui.$('#uploadView').removeClass('layui-hide').find('img').attr('src', res.files.file);
//     //   console.log(res)
//     // }
// });

form.on("select", function (data) {
    toggleImageBedConfHTML(data.value)
})


function getAllImages() {
    pywebview.api.get_all_images().then((response) => {
        allImages = response.images
        let status = document.getElementById("status")
        status.innerHTML += '<span id="images-count" class="layui-badge layui-bg-gray">' + allImages.length + '</span>'
        pages = ~~(allImages.length / pageSize) + 1
        let bedCode = document.getElementById("status").getAttribute("data-id")
        /*  // 所有图片分页加载
        flow.load({
            elem: '#all-images' //流加载容器
                ,
            done: function (page, next) { //执行下一页的回调
                let imageArr = pagination(pageSize, page, allImages)
                var lis = []
                imageArr.forEach((value, index) => {
                    let li = '<li><img src="'
                    switch (bedCode) {
                        case "0":
                            li += value.url + '" delete-url="' + value.delete_url + '" data-width="' + value.width + '" data-height="' + value.height
                            break
                        case "1":
                            li += value.display_url + '" data-id="' + value.id + '" data-width="' + value.width + '" data-height="' + value.height + '" data-url="' + value.url
                            break
                        case "2":
                        case "3":
                            li += value.url + '" delete-url="' + value.delete_url + '" data-sha="' + value.sha
                            break
                    }
                    li += '" onclick="viewImage(this)"></img><button type="button" class="layui-btn layui-btn-sm copy-url" title="复制链接" onclick="copyImageURL(this.parentNode.firstElementChild)"><i class="layui-icon layui-icon-file"></i></button><button type="button" class="layui-btn layui-btn-sm delete-image" title="删除"><i class="layui-icon layui-icon-delete"></i></button></li>'
                    lis.push(li)
                })
                next(lis.join(''), page < pages)
            }
        });
        */
        // 所有图片 按当前屏区域加载
        let allImagesTag = document.getElementById("all-images")
        let html = ""
        allImages.forEach((value) => {
            let li = '<li><img lay-src="'
            switch (bedCode) {
                case "0":
                    li += value.url + '" delete-url="' + value.delete_url + '" data-width="' + value.width + '" data-height="' + value.height
                    break
                case "1":
                    li += value.display_url + '" data-id="' + value.id + '" data-width="' + value.width + '" data-height="' + value.height + '" data-url="' + value.url
                    break
                case "2":
                case "3":
                    li += value.url + '" delete-url="' + value.delete_url + '" data-sha="' + value.sha
                    break
            }
            li += '" onclick="viewImage(this)"></img><button type="button" class="layui-btn layui-btn-sm copy-url" title="复制链接" onclick="copyImageURL(this.parentNode.firstElementChild)"><i class="layui-icon layui-icon-file"></i></button><button type="button" class="layui-btn layui-btn-sm delete-image" title="删除"><i class="layui-icon layui-icon-delete"></i></button></li>'
            html += li
        })
        allImagesTag.innerHTML = html
        flow.lazyimg({
            elem: '#all-images img'
        });
    })
}

// 所有图片的数组分页
function pagination(pageSize, currentPage, arr) {
    var skipNum = (currentPage - 1) * pageSize;
    var newArr = (skipNum + pageSize >= arr.length) ? arr.slice(skipNum, arr.length) : arr.slice(skipNum, skipNum + pageSize);
    return newArr;
}

function viewImage(element) {
    let url = "",
        width = "",
        height = ""
    let bedCode = document.getElementById("status").getAttribute("data-id")
    switch (bedCode) {
        case "0":
            url = element.getAttribute("src")
            width = element.getAttribute("data-width")
            height = element.getAttribute("data-height")
            break
        case "1":
            url = element.getAttribute("data-url")
            width = element.getAttribute("data-width")
            height = element.getAttribute("data-height")
            break
        case "2":
        case "3": {
            url = element.getAttribute("src")
            let img = new Image()
            img.src = url
            if (img.complete) {
                width = img.width
                height = img.height
                img.onload = function () {};
            } else {
                img.onload = function () {
                    width = img.width
                    height = img.height
                    img.onload = function () {};
                }
            }
            break
        }
    }
    pywebview.api.view_image_in_new_windows(url, Number(width), Number(height))
}

$("#all-images").on("click", ".delete-image", function (event) {
    let loading = layer.load(1, {
        shade: [0.8, "#FFF"]
    })
    let imagesCountTag = document.getElementById("images-count")
    let imagesCount = imagesCountTag.innerText
    let allImages = document.getElementById("all-images")
    let bedCode = document.getElementById("status").getAttribute("data-id")
    let imgParent = event.currentTarget.parentNode
    switch (bedCode) {
        case "0": {
            let delete_url = imgParent.firstElementChild.getAttribute("delete-url")
            pywebview.api.delete_image(delete_url).then((response) => {
                layer.close(loading)
                if (response.success) {
                    layer.msg("删除成功")
                    allImages.removeChild(imgParent)
                    imagesCountTag.innerText = imagesCount - 1
                } else {
                    layer.alert("删除失败")
                }
            })
            break
        }
        case "1": {
            let imageID = imgParent.firstElementChild.getAttribute("data-id")
            pywebview.api.delete_image(imageID).then((response) => {
                layer.close(loading)
                if (response.success) {
                    layer.msg("删除成功")
                    allImages.removeChild(imgParent)
                    imagesCountTag.innerText = imagesCount - 1
                } else {
                    layer.alert("删除失败：" + response.error)
                }
            })
            break
        }
        case "2":
        case "3": {
            let sha = imgParent.firstElementChild.getAttribute("data-sha")
            let delete_url = imgParent.firstElementChild.getAttribute("delete-url")
            pywebview.api.delete_image(sha, delete_url).then((response) => {
                layer.close(loading)
                if (response.success) {
                    layer.msg("删除成功")
                    allImages.removeChild(imgParent)
                    imagesCountTag.innerText = imagesCount - 1
                } else {
                    layer.alert("删除失败")
                }
            })
            break
        }
    }
})

$("#status").click((event) => {
    if (document.getElementById("status").getAttribute("data-id") !== null) {
        location.reload()
    }
})


