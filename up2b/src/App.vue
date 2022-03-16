<template>
  <el-tabs type="border-card" class="title-tabs" stretch>
    <el-tab-pane>
      <template #label>
        <span class="custom-tabs-label">
          <el-icon>
            <upload />
          </el-icon>
          <span>上传图片</span>
        </span>
      </template>
      <uploader />
    </el-tab-pane>
    <el-tab-pane>
      <template #label>
        <span class="custom-tabs-label">
          <el-icon>
            <icon-menu />
          </el-icon>
          <span>图片列表</span>
        </span>
      </template>
      <image-list-vue />
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
      <settings />
    </el-tab-pane>
  </el-tabs>
</template>

<script setup lang="ts">
import {
  Upload,
  Menu as IconMenu,
  Setting
} from '@element-plus/icons-vue'
import Uploader from './views/Uploader.vue'
import ImageListVue from './views/ImageList.vue';
import Settings from './views/Settings.vue'

</script>

<style type="text/css">
#app {
  font-family: -apple-system, "PingFang SC", sans-serif;
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
  padding: 32px;
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
</style>
