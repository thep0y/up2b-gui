<template>
    <el-input v-model="config.username" placeholder="请输入用户名">
        <template #prepend>用&ensp;户&ensp;名</template>
    </el-input>
    <el-input v-model="config.password" type="password" placeholder="请输入密码" show-password>
        <template #prepend>密&emsp;&emsp;码</template>
    </el-input>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { CommonConfig } from '../../apis'

const config = ref(({} as CommonConfig))
</script>
