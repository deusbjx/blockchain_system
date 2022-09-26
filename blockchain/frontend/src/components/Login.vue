<template>
  <div class="login-container">
    <el-card class="login-card">
    <el-form ref="form" :model="form" label-width="70px" class="login-form">
      <h2 class="login-title">论坛舆情管理系统</h2>
      <el-form-item label="用户名">
        <el-input v-model="form.username" ref="getUsername"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" ref="getPassword"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">登录</el-button>
      </el-form-item>
    </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      form: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    onSubmit() {
      let username = this.$refs.getUsername.value;
      let password = this.$refs.getPassword.value;
      let that = this;
      let path = '/api/login';
      let params = new URLSearchParams();
      params.append('username', username)
      params.append('password', password)
      axios.post(path,params).then(function(response) {
          let msg = response.data;
          if (msg.isLogin == -1) {
            localStorage.setItem(username,password);
            alert("Wrong user or password!");
          }
          else if (msg.isLogin == 0) {
            alert("Bad Hacker!");
          }
          else {
            localStorage.setItem('success_user','success_passwd');
            that.$router.push({path:'/getData'});
          }
        })
        .catch(function(error) {
          alert("Error " + error);
        });
    }
  }
};
</script>

<style>

.login-form {
  position: relative;
  width: 350px;
  margin: auto; /* 上下间距160px，左右自动居中*/
  background-color: rgba(186, 153, 153, 0); /* 透明背景色 */
  padding: 0px;
  border-radius: 0px; /* 圆角 */
}

.login-card {
  width: 500px;
  height: 300px;
  background-color: rgb(253, 250, 247);
  background: rgba(255, 255, 255, 0.2);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  text-align: center;
  justify-content: center;
  align-items: center;
}

.login-card p {
  margin: auto;
}

/* 背景 */
.login-container {
  position:absolute;
  top: 0;
  left: 0;
  width:100%;
  height:100%;
  z-index:-10;
  zoom: 1;
  background-color: #fff;
  background: url(../assets/binbin.jpg);
  background-size: 100%;
  -webkit-background-size: cover;
  -o-background-size: cover;
  background-position: center 0;
  display: flex;
  align-items: center;
  text-align: center;
}

/* 标题 */
.login-title {
  color: #303133;
  text-align: center;
}
</style>