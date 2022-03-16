<template>
    <el-upload
        class="upload"
        drag
        action="https://jsonplaceholder.typicode.com/posts/"
        multiple
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
</template>

<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue'

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
</style>