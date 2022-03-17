<template>
    <el-upload
        class="upload"
        drag
        action="/upload"
        multiple
        :limit="10"
        @exceed="exceed"
        @error="handleError"
        @success="handleSuccess"
    >
        <el-icon class="el-icon--upload">
            <upload-filled />
        </el-icon>
        <div class="el-upload__text">
            将图片拖拽到此虚线框内或
            <em>点击上传</em>
        </div>
        <template #tip>
            <div class="el-upload__tip">一次最多上传10张图片</div>
        </template>
    </el-upload>
    <div style="height: 10px;" />
    <el-divider content-position="left">已上传的图片</el-divider>
    <div id="uploaded-preview">
        <el-image
            v-for="url in uploadedURLs"
            :key="url"
            style="width: 100px;"
            :src="url"
            fit="cover"
            @click="copyURL"
        />
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadFiles } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { MessageDuration } from '../apis/consts';
import { UploadAjaxError } from 'element-plus/es/components/upload/src/ajax';
import { UploadResponse } from '../apis/interfaces';

const exceed = (files: File[], uploadFiles: UploadFiles) => {
    ElMessage({
        message: '最多上传 10 张图片，你选择了 ' + files.length + ' 张',
        type: 'error',
        duration: MessageDuration
    })

    if (uploadFiles.length > 0) {
        uploadFiles = []
    }
}

const handleError = (error: Error) => {
    const resp = JSON.parse((error as UploadAjaxError).message)
    ElMessage({
        message: resp.error,
        type: 'error',
        duration: MessageDuration
    })
}

const uploadedURLs = ref(([] as string[]))

const handleSuccess = (resp: UploadResponse) => {
    uploadedURLs.value.push(resp.url)
}

const copyURL = (e: MouseEvent) => {
    //@ts-ignore
    const url: string = e.target.attributes.src.value
    navigator.clipboard.writeText(url).then(() => {
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
}

#uploaded-preview img {
    margin: 10px;
    cursor: pointer;
}
</style>