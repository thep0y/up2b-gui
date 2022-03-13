<template>
    <el-upload
        class="upload-demo"
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
    <el-divider content-position="left">已上传的图片</el-divider>
</template>

<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue'

</script>

<style>
.el-divider__text {
    color: var(--el-text-color-regular);
    font-size: 18px;
}
</style>