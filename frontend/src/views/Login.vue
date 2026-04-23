<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-12 col-md-6 col-lg-4">
        <div class="card shadow">
          <div class="card-body">
            <div class="d-flex align-items-center mb-3">
              <i class="bi bi-telephone-outbound-fill text-primary me-2" style="font-size: 1.5rem"></i>
              <h3 class="mb-0">登录</h3>
            </div>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <form @submit.prevent="submit">
              <div class="mb-3">
                <label class="form-label">账号</label>
                <div class="input-group">
                  <span class="input-group-text"><i class="bi bi-person"></i></span>
                  <input type="text" class="form-control" placeholder="请输入账号" v-model.trim="username" required>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">密码</label>
                <div class="input-group">
                  <span class="input-group-text"><i class="bi bi-lock"></i></span>
                  <input type="password" class="form-control" placeholder="请输入密码" v-model="password" required>
                </div>
              </div>
              <div class="form-check form-switch mb-3">
                <input class="form-check-input" type="checkbox" id="admin" v-model="admin">
                <label class="form-check-label" for="admin">管理员模式</label>
              </div>
              <div class="d-flex gap-2">
                <button class="btn btn-primary" type="submit" :disabled="loading">{{ loading ? '登录中...' : '登录' }}</button>
                <router-link class="btn btn-outline-secondary" to="/register">注册</router-link>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return { username:'', password:'', admin:false, error:'', loading:false }
  },
  methods:{
    async submit(){
      this.error=''
      this.loading=true
      try{
        const res = await fetch('/api/login',{method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({username:this.username, password:this.password, admin:this.admin})})
        const data = await res.json()
        if(!data.ok){ this.error = data.error || '登录失败'; return }
        this.$router.push('/dashboard')
      }catch(e){ this.error='网络错误' }
      finally{ this.loading=false }
    }
  }
}
</script>
