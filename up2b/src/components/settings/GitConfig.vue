<template>
    <el-form ref="gitFormRef" :model="gitForm" status-icon :rules="rules">
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
import { ref } from 'vue';
import type { FormInstance } from 'element-plus'
import { GitConfig as GitForm } from '../../apis/interfaces'

const gitFormRef = ref<FormInstance>()
const gitForm = ref(({} as GitForm))

const rules = ref({
    token: [{ required: true, message: '请输入私人令牌', trigger: 'blur' }],
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    repo: [{ required: true, message: '请输入仓库名', trigger: 'blur' }],
    folder: [{ required: true, message: '请输入目录名', trigger: 'blur' }]
})

const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate((valid, fields) => {
        if (valid) {
            console.log('submit!')
        } else {
            console.log('error submit!', fields)
            return false
        }
    })
}

const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
}
</script>
