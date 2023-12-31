<template>
  <div>
    <project style="float: left; margin-right: 10px"
             v-if="$route.name === 'taskManagement' || $route.name === 'addTask'"
             @changeProject="changeProject"></project>
    <project style="float: left; margin-right: 10px" v-if="$route.name === 'editTask'"
             @changeProject="changeProject"
             :project-disabled="true"></project>
    <div class="task-manage-index" v-if="$route.name === 'taskManagement'">
      <div style="float: left" class="control-list">
        <el-button type="primary" icon="el-icon-plus" @click="addTask">
          新增任务
        </el-button>
      </div>
      <div style="clear: both" class="content-info" :loading="tableLoading">
        <div class="content-header">
          <div class="info-name">
            全部任务
          </div>
        </div>

        <el-form size="medium" :inline="true" :model="searchForm" class="search-form" ref="searchForm">
          <el-form-item label="任务名称">
            <el-input v-model="searchForm.name" placeholder="模糊匹配" style="width: 400px"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button icon="el-icon-search" @click="search" type="primary">搜索</el-button>
            <el-button icon="el-icon-refresh-left" @click="resetSearchForm">重置</el-button>
          </el-form-item>
        </el-form>

        <div class="content-table">
          <el-table :header-cell-style="{
            background: 'rgba(144, 147, 153, 0.06)',
            color: 'rgba(0, 0, 0, 0.65)',
            fontSize: '14px',
          }" :data="tableData" style="width: 100%">
            <el-table-column prop="id" label="任务ID" width="80px" align="center" show-overflow-tooltip></el-table-column>
            <el-table-column label="任务名称" prop="name" show-overflow-tooltip></el-table-column>
            <el-table-column label="执行目录" prop="directory" show-overflow-tooltip></el-table-column>
            <el-table-column prop="report" label="报告" width="180px" align="center"
                             show-overflow-tooltip>
              <template slot-scope="scope">
                <div :style="reportStyle()" @click="openReport(scope.row)">
                  查看
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="runUserNickname" label="运行人员" width="180px" align="center"
                             show-overflow-tooltip></el-table-column>
            <el-table-column prop="runTime" label="运行时间" width="180px" align="center"
                             show-overflow-tooltip></el-table-column>
            <el-table-column label="操作" width="230px">
              <template slot-scope="scope">
                <div>
                  <el-button type="success" icon="el-icon-video-play" size="mini" plain
                             @click="runTask(scope.row)" :loading="scope.row.loading"></el-button>
                  <el-button type="primary" icon="el-icon-edit-outline" size="mini" @click="gotoTaskEditor(scope.row)"
                             plain></el-button>
                  <el-button type="danger" icon="el-icon-document-delete" size="mini" @click="deleteTask(scope.row)"
                             plain></el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div class="content-footer clear">
          <div class="block page-list self-right">
            <vue-pagination :currentPage="searchForm.page" :pageSize="searchForm.perPage" :totalNum="total"
                            @sizeChange="pageSizeChange" @currentPageChange="pageChange"/>
          </div>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>
<script>
import Project from "@/components/Project";
import {isProjectExisted} from "@/utils/commonMethods";

export default {
  data() {
    return {
      searchForm: {
        page: 1,
        perPage: 10,
        name: "",
      },
      total: 0,
      tableData: [],
      tableLoading: false,
      isRefreshing: false
    };
  },
  components: {Project},
  methods: {
    async getTableData() {
      let keys = Object.keys(this.searchForm);
      let params = [];
      keys.forEach(key => {
        let value = this.searchForm[key];
        if (value) {
          params.push(`${key}=${this.searchForm[key]}`);
        }
      });
      let curProject = JSON.parse(localStorage.getItem("curProject"));
      let projectId = curProject.curProjectId;
      if (projectId) {
        params.push(`projectId=${projectId}`);
      }
      let url = "/tasks?" + params.join("&");
      this.tableLoading = true;
      await this.$http.get(url).then(async ({data}) => {
        this.tableData = data.items || [];
        this.total = data.totalNum;
        if (!data.items && data.totalNum > 0 && this.searchForm.page > 1) {
          this.searchForm.page--;
          await this.getTableData();
        }
      });

      this.tableLoading = false;
    },
    addTask() {
      if (!isProjectExisted()) {
        this.$notifyMessage(`请先创建项目`, {type: "error"});
        return;
      }
      localStorage.removeItem("taskInfo");
      this.$router.push({
        name: "addTask",
      });
    },
    search() {
      this.searchForm.page = 1;
      this.getTableData();
    },
    reportStyle() {
      return {color: "blue", cursor: "pointer", "text-decoration": "underline"};
    },
    openReport(row) {
      let userInfo = JSON.parse(localStorage.getItem("userInfo"));
      window.open(`${process.env.VUE_APP_apiServer}/api/tasks/${row.id}/${userInfo.id}/report`, '_blank');
    },
    runTask(row) {
      this.$set(row, "loading", true);
      let curProject = JSON.parse(localStorage.getItem("curProject"));
      let curProjectId = curProject.curProjectId;
      let runUserNickname = JSON.parse(localStorage.getItem("userInfo")).nickname;
      let params = {
        curProjectId,
        runUserNickname,
      };
      this.$http.post(`/tasks/${row.id}/run`, params).then(({data: {msg}}) => {
        this.$notifyMessage(msg, {type: "success"});
        this.getTableData();
        this.$set(row, "loading", false);
      });
    },
    deleteTask(row) {
      this.$confirm("确认删除该任务吗？", "提示", {
        confirmButtonText: "确认",
        cancelButtonText: "取消",
        confirmButtonClass: "el-button--danger",
        type: "warning",
      }).then(async () => {
        this.tableLoading = true;
        let url = `/tasks/${row.id}`;
        await this.$http.delete(url).then(async () => {
          this.$notifyMessage("删除成功", {type: "success"});
          await this.getTableData();
        });
        this.tableLoading = false;
      });
    },
    resetSearchForm() {
      this.searchForm = {
        page: 1,
        perPage: 10,
        name: "",
      };
      this.getTableData();
    },
    changeProject() {
      this.resetSearchForm();
    },
    pageSizeChange(val) {
      this.searchForm.perPage = val;
      this.getTableData();
    },
    pageChange(val) {
      this.searchForm.page = val;
      this.getTableData();
    },
    gotoTaskEditor(row) {
      let rowInfo = JSON.stringify(row);
      localStorage.setItem("taskInfo", rowInfo);
      this.$router.push({
        name: "editTask",
      });
    },
  },
  watch: {
    $route: {
      handler(to) {
        if (to.name === "taskManagement") {
          this.getTableData();
        }
      },
      immediate: true,
    },
  },
};
</script>
<style>
.content-table .el-table td {
  height: 64px;
  line-height: 64px;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
