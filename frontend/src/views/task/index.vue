<template>
  <NavLeft>
    <div slot="menuItem">
      <el-menu-item index="/task/workspace">
        <i class="el-icon-s-home"></i>
        <span slot="title">工作台</span>
      </el-menu-item>
      <el-menu-item index="/task/taskManagement">
        <i class="el-icon-s-management"></i>
        <span slot="title">任务管理</span>
      </el-menu-item>
    </div>
  </NavLeft>
</template>
<script>
import NavLeft from "@/components/NavLeft";

export default {
  components: {
    NavLeft,
  },
  mounted() {
    this.saveProject();
  },
  methods: {
    saveProject() {
      let localProjectList = JSON.parse(localStorage.getItem("projectList"));
      if (!localProjectList) {
        this.$http
          .get("/tasks/projects/cur")
          .then(({ data: { projectList, curProject } }) => {
            if (projectList) {
              localStorage.setItem("projectList", JSON.stringify(projectList));
              let localCurProject = JSON.parse(localStorage.getItem("curProject"));
              if (!localCurProject) {
                this.curProjectId = curProject.curProjectId;
                this.curProjectName = curProject.curProjectName;
                localStorage.setItem("curProject", JSON.stringify(curProject));
              }
            }
          })
          .finally(() => {});
      }
    },
  },
};
</script>
