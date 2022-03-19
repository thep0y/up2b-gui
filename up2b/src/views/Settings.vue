<template>
  <div
    id="select-beds"
    class="el-input el-input--default el-input-group el-input-group--prepend"
  >
    <div class="el-input-group__prepend">选择图床</div>
    <el-select
      v-model="selectedCode"
      placeholder="Select"
      size="large"
      style="display: block;"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
  </div>
  <el-divider content-position="center">配置</el-divider>
  <div v-if="imageBedTypes[selectedCode] === 1" id="settings-config">
    <common-config :image-code="selectedCode" :tags="configBedTags" />
  </div>
  <div v-if="imageBedTypes[selectedCode] === 2" id="settings-config">
    <git-config :image-code="selectedCode" :tags="configBedTags" />
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
      @change="toggleAC"
    />
  </div>
  <div id="select-image-bed">
    <fieldset>
      <legend>切换图床</legend>
      <div id="configed-beds-list">
        <el-tag
          v-for="tag in configBedTags"
          :key="tag.index"
          class="mx-1"
          type="success"
          :effect="tag.effect"
          @click="selectImageBed(tag)"
        >{{ tag.name }}</el-tag>
      </div>
    </fieldset>
  </div>
</template>

<script setup lang='ts'>
import { ref, onBeforeMount } from 'vue'
import { ElMessage } from 'element-plus'
import { Check, Close } from '@element-plus/icons-vue'
import {
  showImageBeds,
  chooseImageBed,
  toggleAutomaticCompression,
  ImageBedsResponse,
  Tag,
  ImageCodes,
  MessageDuration
} from '../apis'
import CommonConfig from '../components/settings/CommonConfig.vue'
import GitConfig from '../components/settings/GitConfig.vue'

interface Option {
  value: number,
  label: string
}

let imageBedTypes: number[] = []

const selectedCode = ref(-1)

const options = ref(([] as Option[]))
const configBedTags = ref(([] as Tag[]))
const automaticCompression = ref(false)

const update = (resp: ImageBedsResponse) => {
  selectedCode.value = resp.selected
  for (let key in resp.beds) {
    options.value.push({
      value: resp.beds[key],
      label: key
    })
  }
  resp.auth_data.forEach((v, i) => {
    if (Object.keys(v).length > 0) {
      imageBedTypes.push(v.type)

      configBedTags.value.push({
        index: i,
        name: ImageCodes[i],
        effect: selectedCode.value === i ? 'dark' : 'plain'
      })
    }
  })
}

if (import.meta.env.DEV) {
  showImageBeds(update)
} else {
  onBeforeMount(() => window.addEventListener('pywebviewready', () => {
    showImageBeds(update)
  }))
}

const toggleAC = function (val: any): any {
  toggleAutomaticCompression(val ? 1 : 0, (r) => {
    if (r.success) {
      ElMessage({
        message: '图片自动压缩功能尚不完善，如遇异常请关闭此功能',
        type: 'warning',
        duration: MessageDuration
      })
    } else {
      ElMessage({
        message: '已关闭图片自动压缩',
        type: 'success',
        duration: MessageDuration
      })
    }
  })
}

const selectImageBed = (tag: Tag) => {
  if (tag.effect === 'dark') {
    return
  }

  configBedTags.value.forEach(v => {
    if (tag.index == v.index) {
      v.effect = 'dark'
    } else {
      if (v.effect === 'dark') {
        v.effect = 'plain'
      }
    }
  })

  chooseImageBed(tag.index, (r) => {
    if (r.success) {
      ElMessage({
        message: '图床切换到 ' + tag.name,
        type: 'success',
        duration: MessageDuration
      })
    } else {
      ElMessage({
        message: r.error,
        type: 'error',
        duration: MessageDuration
      })
    }
  })
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

#configed-beds-list {
  padding: 10px;
}

#configed-beds-list .el-tag {
  margin: 10px;
  height: 32px;
}

#configed-beds-list .el-tag .el-tag__content {
  font-weight: 300;
}

#configed-beds-list .el-tag.el-tag--plain {
  cursor: pointer;
}
</style>