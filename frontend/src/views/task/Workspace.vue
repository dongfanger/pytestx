<template>
  <div style="height: 100%; overflow: auto;">
    <div style="text-align: left; font-size: 14px; margin-left: 20px">
      <br />
      <br />
      <h3>
        <span style="background-color:#FFE500;">下载</span>
      </h3>
      <br />
      <p>
        <a href="#" @click="scaffold"><b>项目脚手架</b></a>
        <br />
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Workspace",
  methods: {
    scaffold() {
      let params = {};
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
