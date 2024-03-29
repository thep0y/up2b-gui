<template>
    <el-upload
        ref="upload"
        :action="action"
        class="upload"
        list-type="picture-card"
        drag
        multiple
        :limit="20"
        accept="image/jpg, image/jpeg, image/png, image/gif"
        @exceed="exceed"
        @error="handleError"
        @success="handleSuccess"
    >
        <el-icon class="el-icon--upload">
            <upload-filled />
        </el-icon>
        <template #tip>
            <div class="el-upload__tip">
                支持拖拽或点击
                <br />最多保留
                <b>20</b>
                条上传记录
                <br />超过20条时请点击下面的按钮清空上传列表
            </div>
        </template>
        <template #file="{ file }">
            <div>
                <img
                    v-if="file.status !== 'uploading'"
                    class="el-upload-list__item-thumbnail"
                    :src="file.url"
                />

                <div v-if="file.status === 'uploading'" class="el-upload-list__item-info">
                    <el-progress
                        v-if="file.status === 'uploading'"
                        type="circle"
                        :stroke-width="6"
                        :percentage="Number(file.percentage)"
                    />
                </div>

                <label class="el-upload-list__item-status-label">
                    <el-icon class="el-icon el-icon--upload-success el-icon--check">
                        <Check />
                    </el-icon>
                </label>

                <span class="el-upload-list__item-actions">
                    <span
                        class="el-upload-list__item-preview"
                        @click="handlePictureCardPreview(file)"
                    >
                        <el-icon>
                            <zoom-in />
                        </el-icon>
                    </span>
                    <span
                        v-if="!disabled"
                        class="el-upload-list__item-delete"
                        @click="copyURL(file)"
                    >
                        <el-icon>
                            <CopyDocument />
                        </el-icon>
                    </span>
                    <span
                        v-if="!disabled"
                        class="el-upload-list__item-delete"
                        @click="handleRemove(file)"
                    >
                        <el-icon>
                            <Delete />
                        </el-icon>
                    </span>
                </span>
            </div>
        </template>
    </el-upload>
    <div style="height: 10px;" />
    <el-alert
        v-if="showExceedError.show"
        title="最多 20 张！"
        :description="`已上传 ${showExceedError.uploaded} 张，最多还可上传 ${showExceedError.remain} 张，但你选择了 ${showExceedError.selected} 张，可以点击下面的按钮清空上传列表`"
        type="error"
        show-icon
        @close="removeExceedAlert"
    />
    <el-tooltip class="box-item" effect="dark" content="清空已上传图片列表" placement="left">
        <el-button type="primary" :icon="Remove" circle @click="clearFiles" />
    </el-tooltip>
</template>

<script setup lang="ts">
import { ref, PropType } from 'vue'
import { ElMessage, UploadFile, UploadFiles } from 'element-plus'
import { UploadFilled, Remove, Check, ZoomIn, CopyDocument, Delete } from '@element-plus/icons-vue'
import { UploadAjaxError } from 'element-plus/es/components/upload/src/ajax';
import type { UploadResponse, ErrorResponse, ImageListType, ErrorObject } from '../apis';
import { previewInNewWindow, getAllImages, MessageDuration } from '../apis';

const props = defineProps({ imageList: { type: Array as PropType<ImageListType>, required: true } })

const action = import.meta.env.VITE_APP_BASE_API + '/upload'

const upload = ref()
const disabled = ref(false)

const handleRemove = (file: UploadFile) => {
    upload.value.handleRemove(file)
    ElMessage.warning('已在上传列表中移除，若想在图床中删除此图片请到图片列表页面操作')
}

const handlePictureCardPreview = (file: UploadFile) => {
    const img = new Image()
    img.src = file.url!

    const resp = file.response as UploadResponse

    previewInNewWindow({
        url: resp.url,
        width: img.width,
        height: img.height
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
            window.open(resp.url)
        }
    })
}

const showExceedError = ref({
    show: false,
    uploaded: 0,
    remain: 0,
    selected: 0
})
const exceed = (files: File[], uploadFiles: UploadFiles) => {
    showExceedError.value.show = true
    showExceedError.value.uploaded = uploadFiles.length
    showExceedError.value.remain = 20 - uploadFiles.length
    showExceedError.value.selected = files.length
}
const removeExceedAlert = () => {
    showExceedError.value = {
        show: false,
        uploaded: 0,
        remain: 0,
        selected: 0
    }
}

// 上传错误
const handleError = (error: Error) => {
    const resp: ErrorResponse = JSON.parse((error as UploadAjaxError).message)
    if ((resp.error as ErrorObject).status_code == 409) {
        ElMessage.error('上传太频繁，触发服务器并发限制，请稍后重新上传失败的图片')
    } else {
        if (typeof resp.error === 'string') {
            ElMessage({
                message: resp.error,
                type: 'error',
                duration: MessageDuration
            })
        } else {
            ElMessage({
                message: (resp.error as ErrorObject).image_path + ': ' + (resp.error as ErrorObject).status_code + ',   ' + (resp.error as ErrorObject).error,
                type: 'error',
                duration: MessageDuration
            })
        }
    }
}

const uploadedURLs = ref(([] as string[]))

const handleSuccess = (resp: UploadResponse) => {
    if (resp.success) {
        uploadedURLs.value.push(resp.url)
    } else {
        ElMessage({
            message: resp.image + ': ' + JSON.stringify(resp.error),
            type: 'error',
            duration: MessageDuration
        })
    }

    getAllImages((r) => {
        if (r.success) {
            let map: { [key: string]: boolean } = {}
            props.imageList.forEach(v => {
                map[v.url.split('?')[0]] = true
            })

            r.urls.forEach(v => {
                if (!map[v.url.split('?')[0]]) {
                    props.imageList.push(v)
                }
            })

            ElMessage({
                message: '已将上传成功的图片添加到图片列表',
                type: 'info',
                duration: MessageDuration
            })
        }
    })
}

const clearFiles = () => {
    upload.value.clearFiles()
}

const copyURL = (file: UploadFile) => {
    //@ts-ignore
    navigator.clipboard.writeText(file.response.url).then(() => {
        ElMessage.success('图片链接已复制到剪贴板')
    }).catch(r => {
        ElMessage.error(r)
    })
}
</script>

<style>
.upload .el-divider__text {
    color: var(--el-text-color-regular);
    font-size: 20px;
    font-weight: 300;
}

.upload {
    font-weight: 400;
    width: 100%;
}

.upload .el-upload {
    display: block;
}

.upload .el-upload-dragger {
    width: 100%;
    height: 100%;
    border: none;
}

#uploaded-preview img {
    margin: 10px;
    cursor: pointer;
}

li.el-upload-list__item > div {
    width: 100%;
}

.el-alert__title {
    float: left;
}

p.el-alert__description {
    float: left;
    width: 100%;
    text-align: left;
    font-weight: 400;
}
</style>