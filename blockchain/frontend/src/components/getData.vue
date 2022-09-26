<template>
  <div>
    <!-- <div class="line"></div> -->
    <!-- <el-header> -->
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect"
      background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
      <el-menu-item index="1">论坛舆情管理系统</el-menu-item>
      <el-submenu index="2">
        <template slot="title">论坛数据管理</template>
        <el-menu-item index="2-1" @click="getData">数据获取</el-menu-item>
        <input type="file" ref="upload" accept=".json" class="file" @change="getJsonFile" v-show="false" />
        <el-menu-item index="2-2" @click="inputData">数据上传</el-menu-item>
        <el-menu-item index="2-3" @click="deleteData">数据清除</el-menu-item>
        <el-menu-item index="2-4" @click="download">数据下载</el-menu-item>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title">安全检测</template>
        <el-menu-item index="3-1" @click="sqlDetect">SQL注入</el-menu-item>
        <el-menu-item index="3-2" @click="xssDetect">XSS</el-menu-item>
        <el-menu-item index="3-3" @click="rceDetect">RCE</el-menu-item>
        <el-menu-item index="3-4" @click="freeDetect">自定义检测</el-menu-item>
      </el-submenu>
      <el-menu-item index="4" class="div"></el-menu-item>
      <el-menu-item index="5">欢迎，管理员</el-menu-item>
      <el-menu-item index="6" @click="emit">退出登录</el-menu-item>
    </el-menu>
    <!-- </el-header> -->
    <el-container>
      <el-main>
        <el-row>
          <el-col>
            <div class="divide"></div>
            <el-select v-model="value" placeholder="请选择" class="select">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <el-input placeholder="请输入搜索内容" v-model="input" class="search" clearable>
            </el-input>
            <el-button type="primary" icon="el-icon-search" @click="search">搜索</el-button>
            <div class="divide"></div>
            <el-table :data="tableData" height="400" border class="table" :header-cell-style="topClass">
              <el-table-column prop="id" label="区块号" width="180" class="top" align="center"></el-table-column>
              <el-table-column prop="name" label="评论人" width="180" class="top" align="center"></el-table-column>
              <el-table-column prop="commentSubject" label="评论主题" class="top" align="center"></el-table-column>
              <el-table-column prop="commentText" label="评论内容" class="top" align="center"></el-table-column>
              <el-table-column prop="hash" label="数据哈希值" class="top" align="center"></el-table-column>
              <el-table-column fixed="right" label="操作" width=80px align="center">
                <template slot-scope="scope">
                  <el-button @click.native.prevent="deleteRow(scope.$index, tableData)" type="text" size="small">
                    移除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
import FileSaver from "file-saver";

export default {
  name: "my-first-vue",
  data() {
    return {
      serverResponse: "resp",
      tableData: [],
      originData: [],
      sqlDict: ['select', '\'', 'union', 'and', 'or', 'update', 'extract', 'order'],
      xssDict: ['<', '>', 'script', 'alert', 'document', 'cookie'],
      rceDict: ['GET', 'POST', 'system', 'eval', '@', 'echo', '$', 'asp', 'aspx', 'php', 'dnslog', 'request'],
      activeIndex: "1",
      input: "",
      options: [
        {
          value: "评论人",
          label: "评论人",
        },
        {
          value: "评论主题",
          label: "评论主题",
        },
        {
          value: "评论内容",
          label: "评论内容",
        },
      ],
      value: "",
    };
  },
  methods: {
    inputData() {
      this.$refs.upload.click();
    },
    getJsonFile(event) {
      function escape2Html(str) {
        var arrEntities = { 'lt': '<', 'gt': '>', 'nbsp': ' ', 'amp': '&', 'quot': '"' };
        return str.replace(/&(lt|gt|nbsp|amp|quot);/ig, function (all, t) {
          return arrEntities[t];
        });
      }

      let fileSelect = event.target.files[0];//找到文件上传的元素
      let name = fileSelect.name.replace(/.+\./, "");
      const isJson = name === 'json';
      if (!isJson) {
        this.$message.error('上传文件只能是JSON数据格式!');
        return;
      }
      let reader = new FileReader();
      if (typeof FileReader === 'undefined') {
        this.$message.error('您的浏览器不支持FileReader接口');
        return;
      }
      reader.readAsText(fileSelect, ['gb18030', 'utf-8']);
      let that = this;
      let uploadData = [];
      //console.log(uploadData);
      reader.onload = e => {
        uploadData = e.target.result;
        console.log(uploadData);
        let params = new URLSearchParams();
        let path = '/api/uploadData';
        params.append('json_data', uploadData);
        axios.post(path,params).then(function(response) {
          let msg = response.data;
          let tableData = [];
          for (let block in msg) {
            if (block == "Block0") continue;
            let tData = {};
            tData["id"] = escape2Html(block);
            tData["name"] = escape2Html(msg[block]["data"]["Author"]);
            tData["commentSubject"] = escape2Html(msg[block]["data"]["Subject"]);
            tData["commentText"] = escape2Html(msg[block]["data"]["Message"]);
            tData["hash"] = escape2Html(msg[block]["hash"]);
            tableData.push(tData);
          }
          //console.log(that.tableData);
          that.tableData = tableData;
          that.originData = tableData;
          that.$alert("上传成功!");
        })
        .catch(function(error) {
          alert("Error " + error);
        });
      }
      //console.log(uploadData);
    },
    beforeAvatarUpload(file) {
      let name = file.name.replace(/.+\./, "");
      alert(name);
      const isJson = name === 'json';
      if (!isJson) {
        this.$message.error('上传文件只能是JSON数据格式!');
      }
      return isJson;
    },
    freeDetect() {
      this.$prompt('请输入需要测试的攻击语句', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValidator: (value) => {       // 点击按钮时，对文本框里面的值进行验证
          if (!value) {
            return '输入不能为空';
          }
        },
        // beforeClose: (action, instance, done) => {
        //           if(action === 'confirm' && !ipReg.test(instance.inputValue)){
        //               that.$message(msg);
        //           }else{
        //               done();
        //           } 
        // }
      }).then(({ value }) => {
        let flag = true;
        for (let i = 0; i < this.sqlDict.length; i++) {
          let s = this.sqlDict[i];
          if (value.indexOf(s) != -1) {
            flag = false;
            break;
          }
        }
        for (let i = 0; i < this.xssDict.length; i++) {
          if (flag == false) break;
          let s = this.xssDict[i];
          if (value.indexOf(s) != -1) {
            flag = false;
            break;
          }
        }
        for (let i = 0; i < this.rceDict.length; i++) {
          let s = this.rceDict[i];
          if (value.indexOf(s) != -1) {
            flag = false;
            break;
          }
        }
        if (flag == false) {
          alert("此语句存在威胁，请注意!");
        }
        else {
          alert("此语句为安全语句");
        }
        this.freeDetect();
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消'
        });
      });
    },
    sqlDetect() {
      let attackList = [];
      for (let i = 0; i < this.tableData.length; i++) {
        for (let j = 0; j < this.sqlDict.length; j++) {
          let s = this.sqlDict[j];
          console.log(s);
          if (this.tableData[i]["name"].indexOf(s) != -1 || this.tableData[i]["commentSubject"].indexOf(s) != -1 || this.tableData[i]["commentText"].indexOf(s) != -1) {
            attackList.push(i + 1);
            break;
            //this.$alert("Block"+(i+1)+"疑存在sql注入，请注意!","警告");
            //return;
          }
        }
      }
      if (attackList.length > 0) {
        let log = "";
        for (let i = 0; i < attackList.length; i++) {
          if (i < attackList.length - 1) {
            log += "Block" + attackList[i] + ",";
          }
          else log += "Block" + attackList[i];
        }
        this.$alert(log + "疑存在sql注入,请注意!", "警告");
      }
      else {
        this.$alert("无sql注入威胁", "提示");
      }
    },
    xssDetect() {
      let attackList = [];
      for (let i = 0; i < this.tableData.length; i++) {
        for (let j = 0; j < this.xssDict.length; j++) {
          let s = this.xssDict[j];
          //console.log(s);
          if (this.tableData[i]["name"].indexOf(s) != -1 || this.tableData[i]["commentSubject"].indexOf(s) != -1 || this.tableData[i]["commentText"].indexOf(s) != -1) {
            attackList.push(i + 1);
            break;
            //this.$alert("Block"+(i+1)+"疑存在sql注入，请注意!","警告");
            //return;
          }
        }
      }
      if (attackList.length > 0) {
        let log = "";
        for (let i = 0; i < attackList.length; i++) {
          if (i < attackList.length - 1) {
            log += "Block" + attackList[i] + ",";
          }
          else log += "Block" + attackList[i];
        }
        this.$alert(log + "疑存在xss攻击,请注意!", "警告");
      }
      else {
        this.$alert("无xss攻击威胁", "提示");
      }
    },
    rceDetect() {
      let attackList = [];
      for (let i = 0; i < this.tableData.length; i++) {
        for (let j = 0; j < this.rceDict.length; j++) {
          let s = this.rceDict[j];
          console.log(s);
          if (this.tableData[i]["name"].indexOf(s) != -1 || this.tableData[i]["commentSubject"].indexOf(s) != -1 || this.tableData[i]["commentText"].indexOf(s) != -1) {
            attackList.push(i + 1);
            break;
            //this.$alert("Block"+(i+1)+"疑存在sql注入，请注意!","警告");
            //return;
          }
        }
      }
      if (attackList.length > 0) {
        let log = "";
        for (let i = 0; i < attackList.length; i++) {
          if (i < attackList.length - 1) {
            log += "Block" + attackList[i] + ",";
          }
          else log += "Block" + attackList[i];
        }
        this.$alert(log + "疑存在远程命令执行,请注意!", "警告");
      }
      else {
        this.$alert("无rce攻击威胁", "提示");
      }
    },
    deleteData() {
      this.$confirm('是否清空全部数据?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if (this.tableData.length == 0 || this.originData.length == 0) {
          this.$alert("数据为空!", "提示");
          return;
        }
        this.tableData = [];
        this.originData = [];
        this.$message({
          type: 'success',
          message: '清空成功!'
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消清空'
        });
      });
    },
    deleteRow(index, rows) {
      //console.log(this.tableData[index]);
      this.$confirm('是否删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        //console.log(tableData[index]);
        rows.splice(index, 1);
        //this.tableData[index] = {};
        this.$message({
          type: 'success',
          message: '删除成功!'
        });
        console.log(this.tableData);
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },

    search() {
      let that = this;
      if (that.value == "") {
        that.$alert("请选择查询内容");
        return;
      }
      if (that.input == "") {
        that.$alert("请输入查询内容");
        return;
      }
      //if (that.originData.length != 0) console.log(that.originData[0].length);
      if (
        that.originData.length == 0 ||
        Object.keys(that.originData[0]).length == 0
      ) {
        that.$alert("查询失败");
        return;
      }
      let tmpData = [];
      let searchContext = that.input;
      //console.log(searchContext);
      let flag = -1;
      if (that.value == "评论人") {
        for (let i = 0; i < that.originData.length; i++) {
          //console.log(that.originData[i]["name"]+" "+searchContext+" "+(that.tableData[i]["name"] == searchContext));
          if (that.originData[i]["name"] == searchContext) {
            flag = 0;
            tmpData.push(that.originData[i]);
          }
        }
      } else if (that.value == "评论主题") {
        for (let i = 0; i < that.originData.length; i++) {
          if (
            that.originData[i]["commentSubject"].indexOf(searchContext) != -1
          ) {
            flag = 0;
            tmpData.push(that.originData[i]);
          }
        }
      } else if (this.value == "评论内容") {
        for (let i = 0; i < that.originData.length; i++) {
          if (that.originData[i]["commentText"].indexOf(searchContext) != -1) {
            flag = 0;
            tmpData.push(that.originData[i]);
          }
        }
      }
      if (flag == -1) {
        that.$alert("查询失败!");
        return;
      }
      that.tableData = tmpData;
      that.$alert("查询成功");
    },

    emit() {
      this.$confirm("是否退出当前账户?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$message({
            type: "success",
            message: "登出成功!",
          });
          localStorage.clear();
          this.$router.push({ path: "/login" });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消登出",
          });
        });
    },
    topClass() {
      return "color:black;font-size:15px";
    },
    download() {
      let that = this;
      if (
        that.tableData.length == 0 ||
        Object.keys(that.tableData[0]).length == 0
      ) {
        alert("数据为空!");
        return;
      }
      let data = JSON.stringify(that.tableData);
      let blob = new Blob([data], { type: "application/json" });
      FileSaver.saveAs(blob, "论坛数据.json");
    },
    getData() {
      function escape2Html(str) {
        var arrEntities = { 'lt': '<', 'gt': '>', 'nbsp': ' ', 'amp': '&', 'quot': '"' };
        return str.replace(/&(lt|gt|nbsp|amp|quot);/ig, function (all, t) {
          return arrEntities[t];
        });
      }
      //console.log(this.$data.tableData);
      let that = this;
      // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address
      const path = "/api/getData";
      axios
        .get(path)
        .then(function (response) {
          // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
          // 可以直接通过 response.data 取key-value
          // 坑一：这里不能直接使用 this 指针，不然找不到对象
          let msg = response.data;
          console.log(msg);
          // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
          that.serverResponse = msg;
          let tableData = [];
          for (let block in msg) {
            if (block == "Block0") continue;
            let tData = {};
            tData["id"] = escape2Html(block);
            tData["name"] = escape2Html(msg[block]["data"]["Author"]);
            tData["commentSubject"] = escape2Html(msg[block]["data"]["Subject"]);
            tData["commentText"] = escape2Html(msg[block]["data"]["Message"]);
            tData["hash"] = escape2Html(msg[block]["hash"]);
            tableData.push(tData);
          }
          //console.log(that.tableData);
          that.tableData = tableData;
          that.originData = tableData;
          that.$alert("获取数据成功!");
        })
        .catch(function (error) {
          alert("Error " + error);
        });
    },
  },
};
</script>

<style>
.select {
  width: 110px;
}

.search {
  width: 400px;
}

.emi {
  height: 500px;
}

.div {
  width: 900px;
}

.divide {
  height: 20px;
}

.table {
  margin: 0 auto;
  width: 90%;
  border: 2px solid;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.box-card {
  width: 480px;
}
</style>