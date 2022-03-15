<template>
    <el-form ref="commonFormRef" :model="commonForm" status-icon :rules="rules">
        <el-form-item prop="username">
            <el-input v-model="commonForm.username" placeholder="请输入用户名">
                <template #prepend>用&ensp;户&ensp;名</template>
            </el-input>
        </el-form-item>
        <el-form-item prop="password">
            <el-input
                v-model="commonForm.password"
                type="password"
                placeholder="请输入密码"
                show-password
            >
                <template #prepend>密&emsp;&emsp;码</template>
            </el-input>
        </el-form-item>
        <el-form-item>
            <el-button @click="resetForm(commonFormRef)">清空</el-button>
            <el-button type="primary" @click="submitForm(commonFormRef)">确认</el-button>
        </el-form-item>
    </el-form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { FormInstance } from 'element-plus'
import { CommonConfig as CommonForm } from '../../apis/interfaces'

const commonFormRef = ref<FormInstance>()
const commonForm = ref(({} as CommonForm))

const rules = ref({
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
})

const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate((valid, fields) => {
        if (valid) {
            console.log(commonForm.value.username, commonForm.value.password)
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
