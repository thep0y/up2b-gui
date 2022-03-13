<template>
  <div
    id="select-beds"
    class="el-input el-input--default el-input-group el-input-group--prepend"
  >
    <div class="el-input-group__prepend">选择图床</div>
    <el-select v-model="value" placeholder="Select" size="large" style="display: block;">
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </div>
  <el-divider content-position="center">配置</el-divider>
  <div id="settings-config">
    <common-config />
    <git-config />
  </div>
</template>

<script setup lang='ts'>
import { ref, onBeforeMount } from 'vue'
import { showImageBeds, ImageBedsResponse } from '../apis'
import CommonConfig from '../components/settings/CommonConfig.vue'
import GitConfig from '../components/settings/GitConfig.vue'

interface Option {
  value: number,
  label: string
}

const value = ref(-1)
const options = ref(([] as Option[]))

function update(resp: ImageBedsResponse) {
  value.value = resp.selected
  for (let key in resp.beds) {
    options.value.push({
      value: resp.beds[key],
      label: key
    })
  }
}

onBeforeMount(() => window.addEventListener('pywebviewready', () => { showImageBeds(update) }))
</script>

<style>
#select-beds .el-input-group__prepend,
#settings-config .el-input-group__prepend {
  --info: #909399;
  color: var(--info);
}

#select-beds .el-input__inner {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  margin-right: 3px;
  box-shadow: 0 0 0 1px
    var(--el-input-border-color, var(--el-border-color-base)) inset;
}
</style>