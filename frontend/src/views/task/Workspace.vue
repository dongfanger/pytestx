<template>
  <div style="height: 100%; overflow: auto;">
    <div style="text-align: left; font-size: 14px; margin-left: 20px">
      <br />
      <br />
      <h3>
        <span style="background-color:#FFE500;">下载</span>
      </h3>
      <br />
      <el-form :model="downloadForm" ref="searchForm" :inline="true">
        <el-form-item label="项目名称" prop="keyword">
          <el-input v-model="downloadForm.projectName" placeholder="项目名称"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="scaffold" type="primary">项目脚手架</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Workspace",
  data() {
    return {
      downloadForm: {
        projectName: "",
      },
    }
  },
  methods: {
    scaffold() {
      let params = {"projectName": this.downloadForm.projectName};
      this.$http
          .post(`/tasks/scaffold`, params, { responseType: "blob" })
          .then(res => {
            let blob = new Blob([res.data], { type: "application/zip" });
            let url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = res.headers["content-disposition"].split("=")[1];
            link.click();
            URL.revokeObjectURL(url);
            window.URL.revokeObjectURL(url);
          })
    },
  },
};
</script>

<style>
pre {
  width: 800px;
  margin-top: 10px;
}
</style>
