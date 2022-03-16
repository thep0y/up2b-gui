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
    <common-config :image-code="value" />
  </div>
  <div v-if="value === 1" id="settings-config">
    <common-config :image-code="value" />
  </div>
  <div v-if="value === 2" id="settings-config">
    <git-config :image-code="value" />
  </div>
  <div v-if="value === 3" id="settings-config">
    <git-config :image-code="value" />
  </div>
  <div class="tip custom-block">
    <ul>
      <li>所有配置都将保存到本地文件</li>
      <li>重复修改某图床的配置会覆盖之前的配置信息</li>
    </ul>
  </div>
  <el-divider content-position="center" />
  <div id="automatic-compression">
    <el-tooltip class="box-item" effect="dark" content="试验功能，可能不稳定" placement="top-start">
      <span class="label">自动压缩</span>
    </el-tooltip>
    <el-switch
      v-model="automaticCompression"
      class="mt-2"
      inline-prompt
      :active-icon="Check"
      :inactive-icon="Close"
      @change="toggleAutomaticCompression"
    />
  </div>
  <div id="select-image-bed">
    <fieldset>
      <legend>切换图床</legend>
      <div id="configed-beds-list" />
    </fieldset>
  </div>
</template>

<script setup lang='ts'>
import { ref, onBeforeMount } from 'vue'
import { Check, Close } from '@element-plus/icons-vue'
import { showImageBeds } from '../apis'
import { ImageBedsResponse } from '../apis/interfaces'
import CommonConfig from '../components/settings/CommonConfig.vue'
import GitConfig from '../components/settings/GitConfig.vue'
import { ElMessage } from 'element-plus'

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

const toggleAutomaticCompression = function (val: any): any {
  if (val) {
    ElMessage({
      message: '图片自动压缩功能尚不完善，如遇异常请关闭此功能',
      type: 'warning'
    })
  }
}

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
  background-color: var(--block-bg-color);
  border-radius: 4px;
  border-left: 5px solid var(--el-color-primary);
  margin: 20px 0;
  font-size: 0.9rem;
  font-weight: 300;
  text-align: left;
}

.custom-block ul {
  padding: 6px 0;
  padding-left: 24px;
}

#automatic-compression {
  height: 32px;
}

#automatic-compression span.label {
  line-height: 32px;
  height: 32px;
  align-items: center;
  vertical-align: middle;
  font-size: 18px;
  float: left;
  margin-left: 10px;
  font-weight: 300;
}

#automatic-compression .el-switch {
  float: left;
  margin-left: 8px;
}

#select-image-bed {
  margin-top: 30px;
}

#select-image-bed fieldset {
  min-height: 50px;
  margin-bottom: 10px;
  padding: 0;
  border-width: 1px;
  border-style: solid;
  border-color: #e6e6e6;
  text-align: left;
}

#select-image-bed legend {
  margin-left: 20px;
  padding: 0 10px;
  font-size: 18px;
  font-weight: 300;
}
</style>