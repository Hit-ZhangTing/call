<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-12 col-md-6 col-lg-4">
        <div class="card shadow">
          <div class="card-body">
            <div class="d-flex align-items-center mb-3">
              <i class="bi bi-person-plus-fill text-primary me-2" style="font-size: 1.5rem"></i>
              <h3 class="mb-0">注册</h3>
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
              <div class="mb-3">
                <label class="form-label">手机号</label>
                <div class="input-group">
                  <span class="input-group-text"><i class="bi bi-telephone"></i></span>
                  <input type="text" class="form-control" placeholder="选填" v-model="phone">
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">邀请码</label>
                <div class="input-group">
                  <span class="input-group-text"><i class="bi bi-ticket-perforated"></i></span>
                  <input type="text" class="form-control" placeholder="选填" v-model="invite">
                </div>
              </div>
              <div class="d-flex gap-2">
                <button class="btn btn-primary" type="submit" :disabled="loading">{{ loading ? '注册中...' : '注册' }}</button>
                <router-link class="btn btn-outline-secondary" to="/">返回登录</router-link>
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
    return { username:'', password:'', phone:'', invite:'', error:'', loading:false }
  },
  methods:{
    async submit(){
      this.error=''
      this.loading=true
      try{
        const res = await fetch('/api/register',{method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({username:this.username, password:this.password, phone:this.phone, invite:this.invite})})
        const data = await res.json()
        if(!data.ok){ this.error = data.error || '注册失败'; return }
        this.$router.push('/')
      }catch(e){ this.error='网络错误' }
      finally{ this.loading=false }
    }
  }
}
</script>
