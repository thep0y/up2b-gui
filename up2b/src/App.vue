<template>
  <el-tabs type="border-card" class="title-tabs" stretch @tab-click="getAllImagesEvent">
    <el-tab-pane>
      <template #label>
        <span class="custom-tabs-label">
          <el-icon>
            <upload />
          </el-icon>
          <span>上传图片</span>
        </span>
      </template>
      <uploader :image-list="imageListRef" />
    </el-tab-pane>
    <el-tab-pane lazy>
      <template #label>
        <span class="custom-tabs-label">
          <el-icon>
            <icon-menu />
          </el-icon>
          <span>
            图片列表
            <el-tag
              v-if="imageListRef.length > 0"
              id="counter-tag"
              type="success"
              effect="dark"
            >{{ imageListRef.length }}</el-tag>
          </span>
        </span>
      </template>
      <image-list-vue v-if="imageListRef.length > 0" :image-list="imageListRef" />
      <el-empty v-else description="空空如也" />
    </el-tab-pane>
    <el-tab-pane>
      <template #label>
        <span class="custom-tabs-label">
          <el-icon>
            <setting />
          </el-icon>
          <span>设置</span>
        </span>
      </template>
      <settings :image-list="imageListRef" />
    </el-tab-pane>
  </el-tabs>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { TabsPaneContext } from 'element-plus'
import { ElLoading, ElMessage } from 'element-plus'
import {
  Upload,
  Menu as IconMenu,
  Setting
} from '@element-plus/icons-vue'
import Uploader from './views/Uploader.vue'
import ImageListVue from './views/ImageList.vue';
import Settings from './views/Settings.vue'
import { getAllImages, ImageListType } from './apis'

const imageListRef = ref<ImageListType>([])

const getAllImagesEvent = (pane: TabsPaneContext) => {
  if (pane.index !== '1') {
    return
  }

  if (imageListRef.value.length == 0) {
    const loading = ElLoading.service({
      lock: true,
      text: '正在获取图片列表',
      background: 'rgba(255, 255, 255, 0.8)'
    })

    getAllImages((r) => {
      loading.close()

      if (r.success) {
        imageListRef.value = r.urls
      } else {
        if (typeof r.error === 'string') {
          ElMessage.error(r.error)
        } else {
          ElMessage.error(`状码码：${r.error.status_code}\n错误：${r.error.error}`)
        }
      }
    })
  }
}

</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}
#app .el-tabs {
  height: calc(100% - 3px);
}
.element-plus-logo {
  width: 50%;
}
.title-tabs > .el-tabs__content {
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
.title-tabs .custom-tabs-label .el-icon {
  vertical-align: middle;
}
.title-tabs .custom-tabs-label span {
  vertical-align: middle;
  margin-left: 4px;
}
.el-tabs__content {
  height: calc(100% - 66px);
}
.el-tab-pane {
  height: 100%;
}
.el-empty {
  height: 100%;
}
.el-tabs__content {
  overflow: auto;
}
#counter-tag {
  height: 18px;
  padding: 0 3px;
}
#counter-tag .el-tag__content {
  margin-left: 0;
}
</style>
