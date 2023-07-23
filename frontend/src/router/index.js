import Vue from "vue";
import VueRouter from "vue-router";
import login from "@/views/login";
import home from "@/views/home";
import console from "@/views/console";
import task from "@/views/task";

const original = VueRouter.prototype.push;

VueRouter.prototype.push = function push(location) {
  return original.call(this, location).catch(err => err);
}

Vue.use(VueRouter);

const routes = [
  {
    path: "/login",
    meta: {
      title: "测试平台登录",
    },
    component: login,
  },
  {
    path: "/",
    name: "home",
    meta: {
      requireAuth: true,
    },
    component: home,
    redirect: "task/workspace",
    children: [
      {
        path: "task",
        name: "task",
        meta: {
          title: "任务调度",
        },
        component: task,
        redirect: "task/workspace",
        children: [
          {
            path: "workspace",
            meta: {
              title: "工作台",
            },
            component: () => import("@/views/task/Workspace.vue"),
          },
          {
            path: "taskManagement",
            name: "taskManagement",
            meta: {
              title: "任务管理",
            },
            component: () => import("@/views/task/TaskManagement.vue"),
            children: [
              {
                path: "addTask",
                name: "addTask",
                meta: {
                  title: "添加任务",
                },
                component: () => import("@/views/task/TaskEditor"),
              },
              {
                path: "editTask",
                name: "editTask",
                meta: {
                  title: "编辑任务",
                },
                component: () => import("@/views/task/TaskEditor"),
              },
              {
                path: "caseList",
                name: "caseList",
                meta: {
                  title: "用例列表",
                },
                component: () => import("@/views/task/CaseList"),
              },
              {
                path: "taskResult",
                name: "taskResult",
                meta: {
                  title: "任务运行结果",
                },
                component: () => import("@/views/task/TaskResult"),
              },
            ],
          },
          {
            path: "gitSync",
            meta: {
              title: "Git同步",
            },
            component: () => import("@/views/task/GitSync.vue"),
          },
        ],
      },
      {
        path: "console",
        name: "console",
        meta: {
          title: "后台管理",
        },
        component: console,
        redirect: "console/userManagement",
        children: [
          {
            path: "userManagement",
            meta: {
              title: "用户管理",
            },
            component: () => import("@/views/console/userManagement.vue"),
          },
          {
            path: "projectManagement",
            meta: {
              title: "项目管理",
            },
            component: () => import("@/views/console/ProjectManagement.vue"),
          },
        ],
      },
    ],
  },
];

const router = new VueRouter({
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(auth => auth.meta.requireAuth)) {
    let token = localStorage.getItem("token");
    if (token) {
      next();
    } else {
      next({
        path: "/login",
      });
    }
  } else {
    next();
  }
});
export default router;
