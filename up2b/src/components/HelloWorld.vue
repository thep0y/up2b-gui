<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from "element-plus"

defineProps<{ msg: string }>()

const count = ref(0)
const input = ref("element-plus")

const curDate = ref('')

const toast = () => {
  ElMessage.success("你好")
}
</script>

<template>
  <h1>{{ msg }}</h1>

  <el-button @click="toast">El 消息</el-button>
  <el-button type="primary" @click="count++">count = {{ count }}</el-button>
  <el-button type="success" @click="count++">count = {{ count }}</el-button>
  <el-button type="warning" @click="count++">count = {{ count }}</el-button>
  <el-button type="danger" @click="count++">count = {{ count }}</el-button>
  <el-button type="info" @click="count++">count = {{ count }}</el-button>
  <br />
  <el-input v-model="input" style="width: 200px; margin: 20px;" />
  <el-tag>标签 1</el-tag>
  <br />
  <el-date-picker v-model="curDate" type="date" placeholder="选择日期"></el-date-picker>
  <p>例如，我们可以自定义一个绿色的主颜色</p>
  <p>
    编辑
    <code>components/Helloword.vue</code>来测试组件。
  </p>
  <p>
    编辑
    <code>styles/element.var.scss</code>来测试 scss 变量。
  </p>

  <p>
    完整示例
    <a href="https://www.baidu.com" target="_blank">el官网</a>
  </p>
</template>

<style scoped>
.el-button {
  margin: 4px;
}
</style>
