<template>
    <el-form
        ref="commonFormRef"
        v-loading.fullscreen.lock="loading"
        element-loading-text="正在保存配置信息..."
        :model="commonForm"
        status-icon
        :rules="rules"
    >
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
import { ElMessage, FormInstance } from 'element-plus'
import { CommonConfig as CommonForm, InitCommonImageBedParams, Tag } from '../../apis/interfaces'
import { initImageBeds } from '../../apis'
import { ImageCodes } from '../../apis/consts'
import { addTag, switchTag } from './common'

const props = defineProps({ imageCode: { type: Number, required: true }, tags: { type: Array, required: true } })

const commonFormRef = ref<FormInstance>()
const commonForm = ref(({} as CommonForm))

const loading = ref(false)
const openLoading = () => {
    loading.value = true
}
const rules = ref({
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
})

const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate((valid) => {
        if (valid) {
            openLoading()

            const data: InitCommonImageBedParams = {
                'image-bed': props.imageCode,
                username: commonForm.value.username,
                password: commonForm.value.password
            }
            initImageBeds(data, function (r) {
                loading.value = false
                if (r.success) {
                    ElMessage({
                        message: `已保存或更新 ${ImageCodes[props.imageCode]} 配置信息`,
                        type: 'success'
                    })
                    formEl.resetFields()

                    // TODO: 配置保存后清空图片列表

                    addTag(props.tags as Tag[], props.imageCode)
                    switchTag(props.tags as Tag[], props.imageCode)
                } else {
                    ElMessage.error(r.error)
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
