import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import getData from '@/components/getData'
import Login from '@/components/Login'
import test from '@/components/test'
import { TabPane } from 'element-ui'


Vue.use(Router)

let router = new Router (
  {
    routes: [
      {
        path: '/',
        name: 'HelloWorld',
        component: HelloWorld
      },
      {
        path: '/getData',
        name: 'getData',
        component: getData,
      },
      {
        path : '/login',
        name : 'Login',
        component : Login
      },
      {
        path : '/test',
        name : 'test',
        component : test
      }
    ]
  }
)


router.beforeEach((to, from, next) => {   // 使用钩子函数对路由进行权限跳转
  if (to.path == '/test') next();
  if (to.path == '/login') {
    localStorage.clear();
    next();
  }
  else if (to.path == '/') {
    localStorage.clear();
    next('/login');
  }
  else if (to.path == '/getData') {
    console.log(localStorage);
    if (localStorage.getItem('success_user') && localStorage.getItem('success_user') == 'success_passwd') {
      console.log(localStorage);
      alert('登录成功!');
      next();
    }
    else if (localStorage.length > 0){
      console.log(localStorage);
      localStorage.clear();
      alert("Wrong user or password!");
      next('/login');
    }
    else next('/login');
  }
})

export default router;