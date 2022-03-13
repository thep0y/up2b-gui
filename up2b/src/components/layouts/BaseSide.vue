<template>
  <el-menu
    router
    class="el-menu-vertical-demo"
    default-active="/imageList"
    :collapse="isCollapse"
    @open="handleOpen"
    @close="handleClose"
  >
    <el-menu-item v-for="item in menus" :index="item.path">
      <el-icon v-if="item.path == $router.options.routes[0].path">
        <upload />
      </el-icon>
      <el-icon v-else-if="item.path == $router.options.routes[1].path">
        <icon-menu />
      </el-icon>
      <el-icon v-else-if="item.path == $router.options.routes[2].path">
        <setting />
      </el-icon>
      <template #title>{{ item.text }}</template>
    </el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from "vue-router"
import {
  Upload,
  Menu as IconMenu,
  Setting,
} from '@element-plus/icons-vue'
const isCollapse = ref(true)
const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

const texts = ["上传图片", "图片列表", "设置"]

let menus: { path: string, text: string }[] = []
const router = useRouter()
console.log(router.options.routes[1].path)
router.options.routes.forEach((v, i) => {
  menus.push({
    path: v.path,
    text: texts[i]
  })
})
</script>
