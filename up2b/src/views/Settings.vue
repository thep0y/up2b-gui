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
  <!-- TODO: 应该添加图床类型，用来判断应该用什么组件，只用 v-if 太麻烦 -->
  <div v-if="value === 0" id="settings-config">
    <common-config />
  </div>
  <div v-if="value === 1" id="settings-config">
    <common-config />
  </div>
  <div v-if="value === 2" id="settings-config">
    <git-config />
  </div>
  <div v-if="value === 3" id="settings-config">
    <git-config />
  </div>
  <div class="tip custom-block">重复修改某图床的配置会覆盖之前的配置信息</div>
  <el-divider content-position="center" />
  <div id="automatic-compression">
    <el-tooltip class="box-item" effect="dark" content="试验功能，可能不稳定" placement="top-start">
      <span class="label">自动压缩</span>
    </el-tooltip>
    <el-switch
      v-model="automaticCompression"
      class="mt-2"
      style="margin-left: 24px"
      inline-prompt
      :active-icon="Check"
      :inactive-icon="Close"
    />
  </div>
</template>

<script setup lang='ts'>
import { ref, onBeforeMount } from 'vue'
import { Check, Close } from '@element-plus/icons-vue'
import { showImageBeds } from '../apis'
import { ImageBedsResponse } from '../apis/interfaces'
import CommonConfig from '../components/settings/CommonConfig.vue'
import GitConfig from '../components/settings/GitConfig.vue'

interface Option {
  value: number,
  label: string
}

const value = ref(-1)
const options = ref(([] as Option[]))
const automaticCompression = ref(false)

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

#settings-config button {
  display: block;
  margin: 0 auto;
}

.custom-block {
  padding: 8px 16px;
  background-color: var(--block-bg-color);
  border-radius: 4px;
  border-left: 5px solid var(--el-color-primary);
  margin: 20px 0;
  font-size: 0.9rem;
  text-align: left;
}

#automatic-compression span.label {
  line-height: 32px;
  height: 32px;
  align-items: center;
  vertical-align: middle;
  font-size: 18px;
  float: left;
}

#automatic-compression .el-switch {
  float: left;
}
</style>