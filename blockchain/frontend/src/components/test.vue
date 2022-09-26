<template>
  <div>
    <input type="file" ref="upload" accept=".txt" class="file" @change="getTxtList" v-show="false"/>
<el-button size="mini" type="primary" @click="uploadTxt" class="mb20">上传文件</el-button>
  </div>
</template>
<script>

export default {
  data() {
    return {
      fileList: [],
    }
  },
  methods: {
    uploadTxt() {
      this.$refs.upload.click()
    },
    /**
     * 上传txt文件并解析
     */
    getTxtList(event) {
      let fileSelect = event.target.files[0]//找到文件上传的元素
      let reader = new FileReader()
      if (typeof FileReader === 'undefined') {
        this.$message.error('您的浏览器不支持FileReader接口')
        return
      }
      reader.readAsText(fileSelect, ['gb2312', 'utf-8'])
      const _this = this
      reader.onload = function () {
        _this.$nextTick(() => {
            console.log(reader.result, "reader.result");
      })
      }
    }
  },
}
</script>