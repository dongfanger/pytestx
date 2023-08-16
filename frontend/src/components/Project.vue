<template>
  <el-form :inline="true">
    <el-form-item label="" v-if="showProject">
      <el-select v-model="curProjectName" @change="changeProject" @click.native="getProjectList">
        <el-option v-for="(item, index) in projectList" :key="index" :label="item.projectName" :value="item.projectName"></el-option>
      </el-select>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: "Project",
  props: {
    showProject: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      projectList: [],
      curProjectId: "",
      curProjectName: "",
    };
  },
  created() {
    this.getCurProject();
  },
  methods: {
    getProjectList() {
      let localProjectList = JSON.parse(localStorage.getItem("projectList"));
      if (localProjectList) {
        this.projectList = localProjectList;
      }
    },
    getCurProject() {
      let localCurProject = JSON.parse(localStorage.getItem("curProject"));
      if (localCurProject) {
        this.curProjectId = localCurProject.curProjectId;
        this.curProjectName = localCurProject.curProjectName;
      }
    },
    changeProject() {
      let curProject = {};
      this.projectList.forEach(item => {
        if (item.projectName === this.curProjectName) {
          this.curProjectId = item.projectId;
        }
      });
      curProject["curProjectId"] = this.curProjectId;
      curProject["curProjectName"] = this.curProjectName;
      localStorage.setItem("curProject", JSON.stringify(curProject));
      this.$emit("changeProject");
    },
  },
};
</script>

<style scoped></style>
