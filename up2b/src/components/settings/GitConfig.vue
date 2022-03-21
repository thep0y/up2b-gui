<template>
    <el-form
        ref="gitFormRef"
        v-loading.fullscreen.lock="loading"
        :model="gitForm"
        status-icon
        :rules="rules"
    >
        <el-form-item prop="token">
            <el-input
                v-model="gitForm.token"
                type="password"
                placeholder="请输入私人令牌"
                show-password
            >
                <template #prepend>私人令牌</template>
            </el-input>
        </el-form-item>
        <el-form-item prop="username">
            <el-input v-model="gitForm.username" placeholder="请输入用户名">
                <template #prepend>用&ensp;户&ensp;名</template>
            </el-input>
        </el-form-item>
        <el-form-item prop="repo">
            <el-input v-model="gitForm.repo" placeholder="请输入要使用的仓库">
                <template #prepend>仓&emsp;&emsp;库</template>
            </el-input>
        </el-form-item>
        <el-form-item prop="folder">
            <el-input v-model="gitForm.folder" placeholder="请输入要保存的目录">
                <template #prepend>目&emsp;&emsp;录</template>
            </el-input>
        </el-form-item>
        <el-form-item>
            <el-button @click="resetForm(gitFormRef)">清空</el-button>
            <el-button type="primary" @click="submitForm(gitFormRef)">确认</el-button>
        </el-form-item>
    </el-form>
</template>

<script setup lang="ts">
import { ref, PropType } from 'vue';
import { FormInstance, ElMessage } from 'element-plus'
import type { ImageListType, GitConfig as GitForm, InitGitImageBedParams, Tag } from '../../apis'
import { initImageBeds, ImageCodes } from '../../apis'
import { addAndSwitchAndClear } from './settings'

const props = defineProps({ imageList: { type: Array as PropType<ImageListType>, required: true }, imageCode: { type: Number, required: true }, tags: { type: Array, required: true } })

const gitFormRef = ref<FormInstance>()
const gitForm = ref(({} as GitForm))

const rules = ref({
    token: [{ required: true, message: '请输入私人令牌', trigger: 'blur' }],
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    repo: [{ required: true, message: '请输入仓库名', trigger: 'blur' }],
    folder: [{ required: true, message: '请输入目录名', trigger: 'blur' }]
})

let loading = ref(false)
const openLoading = () => {
    loading.value = true
}
const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate((valid) => {
        if (valid) {
            openLoading()

            const data: InitGitImageBedParams = {
                'image-bed': props.imageCode,
                token: gitForm.value.token,
                username: gitForm.value.username,
                repo: gitForm.value.repo,
                folder: gitForm.value.folder
            }
            initImageBeds(data, function (r) {
                loading.value = false
                if (r.success) {
                    ElMessage({
                        message: `已保存或更新 ${ImageCodes[props.imageCode]} 配置信息`,
                        type: 'success'
                    })
                    formEl.resetFields()

                    addAndSwitchAndClear(props.tags as Tag[], props.imageCode, props.imageList)
                } else {
                    ElMessage.error(`配置保存失败：${r.error}`)
                }
            })
        } else {
            return false
        }
    })
}

const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
}
</script>
