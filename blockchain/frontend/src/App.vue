<template>
  <div id="app">
    <!-- <img src="./assets/logo.png">
    <div id="nav">
      <router-link to="/">Home</router-link>
      <router-link to="/getData">Data</router-link>
      <router-link to="/login">Login</router-link>
    </div> -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
body{
  font-family: "微软雅黑";  /*  设置字体 */
  margin: 0px /* 去除上下的边距*/
}
</style>
