<template>
    <el-input v-model="config.token" type="password" placeholder="请输入私人令牌">
        <template #prepend>私人令牌</template>
    </el-input>
    <el-input v-model="config.username" placeholder="请输入用户名">
        <template #prepend>用&ensp;户&ensp;名</template>
    </el-input>
    <el-input v-model="config.repo" placeholder="请输入要使用的仓库" show-password>
        <template #prepend>仓&emsp;&emsp;库</template>
    </el-input>
    <el-input v-model="config.folder" placeholder="请输入要保存的目录" show-password>
        <template #prepend>目&emsp;&emsp;录</template>
    </el-input>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { GitConfig } from '../../apis'

const config = ref(({} as GitConfig))
</script>
