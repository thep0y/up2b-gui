<template>
    <div id="image-list">
        <ul class="el-upload-list el-upload-list--picture-card">
            <li
                v-for="item in imageList"
                :key="item.url"
                class="el-upload-list__item is-success"
                tabindex="0"
            >
                <div>
                    <el-image
                        class="el-upload-list__item-thumbnail"
                        fit="contain"
                        :src="item.url"
                        lazy
                    />
                    <span class="el-upload-list__item-actions">
                        <span
                            class="el-upload-list__item-preview"
                            @click="handlePicturePreview(item)"
                        >
                            <el-icon>
                                <zoom-in />
                            </el-icon>
                        </span>
                        <span class="el-upload-list__item-delete" @click="copyURL(item)">
                            <el-icon>
                                <CopyDocument />
                            </el-icon>
                        </span>
                        <span
                            class="el-upload-list__item-delete"
                            @click="handleRemove(item)"
                        >
                            <el-icon>
                                <Delete />
                            </el-icon>
                        </span>
                    </span>
                </div>
            </li>
        </ul>
    </div>
    <el-affix position="bottom" :offset="10">
        <el-tooltip class="box-item" effect="dark" content="刷新图片列表" placement="top">
            <el-button type="primary" circle @click="refreshImageList">
                <el-icon>
                    <Refresh />
                </el-icon>
            </el-button>
        </el-tooltip>
    </el-affix>
</template>

<script setup lang="ts">
import { PropType } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import { ZoomIn, CopyDocument, Delete, Refresh } from '@element-plus/icons-vue'
import type { ImageListType, ImageListItemType, DeleteParamsType, ErrorObject } from '../apis'
import { previewInNewWindow, deleteImage, MessageDuration, getAllImages } from '../apis';

const props = defineProps({ imageList: { type: Array as PropType<ImageListType>, required: true } })

const handlePicturePreview = (image: ImageListItemType) => {
    let width: number, height: number
    if ('width' in image) {
        width = image.width
        height = image.height
    } else {
        const img = new Image()
        img.src = image.url

        width = img.width
        height = img.height
    }

    previewInNewWindow({
        url: image.url.split('?')[0],
        width: width,
        height: height
    }, (r) => {
        if (r.success) {
            ElMessage({
                message: '已在新窗口中打开大图',
                type: 'success',
                duration: MessageDuration
            })
        } else {
            ElMessage({
                message: r.error,
                type: 'warning',
                duration: MessageDuration
            })
            window.open(image.url)
        }
    })
}

const copyURL = (image: ImageListItemType) => {
    navigator.clipboard.writeText(image.url.split('?')[0]).then(() => {
        ElMessage.success('图片链接已复制到剪贴板')
    }).catch(r => {
        ElMessage.error(r)
    })
}

const handleRemove = (image: ImageListItemType) => {
    const loading = ElLoading.service({
        lock: true,
        text: '正在删除...',
        background: 'rgba(255, 255, 255, 0.8)'
    })

    let params: DeleteParamsType
    if ('delete_url' in image && !('sha' in image)) {
        params = {
            delete_url: image.delete_url
        }
    } else if ('id' in image) {
        params = {
            id: image.id
        }
    } else {
        params = {
            sha: image.sha,
            delete_url: image.delete_url
        }
    }

    deleteImage(params, (r) => {
        loading.close()

        if (r.success) {
            props.imageList.splice(props.imageList.indexOf(image), 1)
            if (r.msg) {
                ElMessage.success(r.msg)
            } else {
                ElMessage.success('已删除')
            }
        } else {
            ElMessage.error(`删除失败：status_code=${(r.error as ErrorObject).status_code}, error=${(r.error as ErrorObject).error}`)
        }
    })
}

const refreshImageList = () => {
    const loading = ElLoading.service({
        lock: true,
        text: '正在更新图片列表',
        background: 'rgba(255, 255, 255, 0.8)'
    })

    getAllImages((r) => {
        loading.close()

        if (r.success) {
            props.imageList.splice(0, props.imageList.length)
            r.urls.forEach(v => {
                props.imageList.push(v)
            })
        } else {
            ElMessage.error((r.error as ErrorObject).error)
        }
    })
}

</script>

<style>
.block {
    border: 1px solid #c0ccda;
    border-radius: 6px;
    background-color: #fff;
    width: 148px;
    height: 148px;
    margin: 0 8px 8px 0;
    box-sizing: border-box;
    padding: 0;
}
#image-list > ul.el-upload-list--picture-card {
    margin: 0 0 0 8px;
    display: block;
}
</style>