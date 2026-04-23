<template>
  <div>
    <nav class="navbar navbar-light bg-light px-3">
      <span class="navbar-brand"><i class="bi bi-speedometer2 text-primary me-2"></i>工作台</span>
      <div class="ms-auto d-flex align-items-center gap-3">
        <span v-if="user" class="d-flex align-items-center gap-2">
          <span class="rounded-circle bg-primary text-white d-inline-flex justify-content-center align-items-center" style="width:28px;height:28px">{{ user.username.slice(0,1).toUpperCase() }}</span>
          <span>当前用户：{{ user.username }}（{{ user.role }}）</span>
        </span>
        <button class="btn btn-outline-secondary btn-sm" @click="logout">退出登录</button>
      </div>
    </nav>
    <div class="d-flex" style="min-height: calc(100vh - 56px)">
      <div class="border-end p-3 sidebar">
        <div class="list-group">
          <a class="list-group-item list-group-item-action" :class="{ 'active-link': tab==='calls' }" href="#" @click.prevent="switchTab('calls')"><i class="bi bi-telephone-outbound me-2"></i>通话记录表</a>
          <a class="list-group-item list-group-item-action" :class="{ 'active-link': tab==='tasks' }" href="#" @click.prevent="switchTab('tasks')"><i class="bi bi-list-task me-2"></i>任务表</a>
          <a class="list-group-item list-group-item-action" :class="{ 'active-link': tab==='scripts' }" href="#" @click.prevent="switchTab('scripts')"><i class="bi bi-chat-left-text me-2"></i>话术表</a>
        </div>
      </div>
      <div class="flex-grow-1 p-4">
        <div v-if="tab==='calls'">
          <h5 class="mb-3">通话记录表</h5>
          <div class="mb-2 d-flex justify-content-end">
            <button class="btn btn-outline-primary btn-sm" @click="exportCalls">导出</button>
          </div>
          <div class="table-responsive">
            <table class="table table-striped table-hover align-middle">
              <thead>
                <tr>
                  <th>主叫手机号</th>
                  <th>被叫手机号</th>
                  <th>通话开始时间</th>
                  <th>通话结束时间</th>
                  <th>外呼结果评价</th>
                  <th>存储地址</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="r in viewData" :key="r.storage">
                  <td>{{ r.caller }}</td>
                  <td>{{ r.callee }}</td>
                  <td>{{ r.start }}</td>
                  <td>{{ r.end }}</td>
                  <td><span class="badge" :class="resultBadge(r.result)">{{ r.result }}</span></td>
                  <td>{{ r.storage }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else-if="tab==='tasks'">
          <h5 class="mb-3">任务表</h5>
          <div class="mb-2 d-flex justify-content-end">
            <input ref="taskImportInput" type="file" accept=".csv,.json" class="d-none" @change="handleImportFile">
            <button class="btn btn-outline-primary btn-sm" @click="triggerTaskImport">导入</button>
          </div>
          <div class="table-responsive">
            <table class="table table-striped table-hover align-middle">
              <thead>
                <tr>
                  <th>被叫手机号</th>
                  <th>姓名</th>
                  <th>性别</th>
                  <th>风险类别</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="r in viewData" :key="r.phone">
                  <td>{{ r.phone }}</td>
                  <td>{{ r.name }}</td>
                  <td>{{ r.gender }}</td>
                  <td><span class="badge" :class="riskBadge(r.risk)">{{ r.risk }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else>
          <h5 class="mb-3">话术表</h5>
          <div class="table-responsive">
            <table class="table table-striped table-hover align-middle">
              <thead>
                <tr>
                  <th>话术文本</th>
                  <th>话术类别</th>
                  <th>对话阶段</th>
                  <th>话术分支</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(r,idx) in viewData" :key="idx">
                  <td>{{ r.text }}</td>
                  <td>{{ r.category }}</td>
                  <td>{{ r.stage }}</td>
                  <td>{{ r.branch }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="d-flex align-items-center justify-content-between mt-3">
          <div class="d-flex align-items-center gap-2">
            <span>每页显示</span>
            <select class="form-select form-select-sm" style="width:110px" v-model.number="pageSize" @change="onPageSizeChange">
              <option :value="5">5</option>
              <option :value="10">10</option>
              <option :value="20">20</option>
              <option :value="50">50</option>
            </select>
            <span class="text-muted">共 {{ data.length }} 条</span>
          </div>
          <nav>
            <ul class="pagination pagination-sm mb-0">
              <li class="page-item" :class="{ disabled: page<=1 }">
                <a class="page-link" href="#" @click.prevent="prevPage">上一页</a>
              </li>
              <li v-for="p in pageNumbers" :key="p" class="page-item" :class="{ active: p===page }">
                <a class="page-link" href="#" @click.prevent="gotoPage(p)">{{ p }}</a>
              </li>
              <li class="page-item" :class="{ disabled: page>=pageCount }">
                <a class="page-link" href="#" @click.prevent="nextPage">下一页</a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return { user:null, tab:'calls', data:[], loading:false, page:1, pageSize:10 }
  },
  async created(){
    const me = await fetch('/api/me')
    if(me.status===401){ this.$router.push('/'); return }
    const j = await me.json()
    this.user = j.user
    this.fetchData()
  },
  methods:{
    resultBadge(t){
      const x = String(t)
      if(x.includes('未接') || x.includes('失败')) return 'bg-secondary'
      if(x.includes('回访')) return 'bg-warning text-dark'
      return 'bg-success'
    },
    riskBadge(t){
      const x = String(t)
      if(x.includes('高')) return 'bg-danger'
      if(x.includes('中')) return 'bg-warning text-dark'
      return 'bg-success'
    },
    async fetchData(){
      this.loading=true
      let url = '/api/call_logs'
      if(this.tab==='tasks') url = '/api/tasks'
      if(this.tab==='scripts') url = '/api/scripts'
      const res = await fetch(url)
      const j = await res.json()
      this.data = j.data || []
      this.page = 1
      this.loading=false
    },
    switchTab(t){ this.tab=t; this.fetchData() },
    async logout(){
      await fetch('/api/logout',{method:'POST'})
      this.$router.push('/')
    },
    onPageSizeChange(){ this.page = 1 },
    prevPage(){ if(this.page>1) this.page-- },
    nextPage(){ if(this.page<this.pageCount) this.page++ },
    gotoPage(p){ if(p>=1 && p<=this.pageCount) this.page = p }
    ,triggerTaskImport(){
      const el = this.$refs.taskImportInput
      if(el) el.click()
    }
    ,async handleImportFile(e){
      const file = e.target.files && e.target.files[0]
      if(!file) return
      const ext = (file.name.split('.').pop() || '').toLowerCase()
      const text = await file.text()
      let rows = []
      try{
        if(ext==='json'){
          const j = JSON.parse(text)
          if(Array.isArray(j)) rows = j
        }else{
          rows = this.parseCSV(text)
        }
      }catch(err){
      }
      if(!Array.isArray(rows) || rows.length===0){ return }
      const payload = rows.map(r=>({
        phone: r.phone || r.被叫手机号 || r["被叫手机号"],
        name: r.name || r.姓名 || r["姓名"],
        gender: r.gender || r.性别 || r["性别"],
        risk: r.risk || r.风险类别 || r["风险类别"]
      })).filter(x=>x.phone)
      try{
        const res = await fetch('/api/tasks/import',{
          method:'POST', headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ data: payload })
        })
        if(res.ok){
          await this.fetchData()
          this.page = 1
        }else{
          this.data = payload
          this.page = 1
        }
      }catch(err){
        this.data = payload
        this.page = 1
      }finally{
        e.target.value = ''
      }
    }
    ,parseCSV(text){
      const lines = text.split(/\r?\n/).filter(l=>l.trim().length>0)
      if(lines.length===0) return []
      const header = lines[0].split(',').map(h=>h.trim())
      const out = []
      for(let i=1;i<lines.length;i++){
        const cols = lines[i].split(',')
        const obj = {}
        for(let j=0;j<header.length;j++){
          obj[header[j]] = (cols[j]||'').trim()
        }
        out.push(obj)
      }
      return out
    }
    ,exportCalls(){
      if(this.tab!=='calls' || !this.data || this.data.length===0) return
      const header = ['主叫手机号','被叫手机号','通话开始时间','通话结束时间','外呼结果评价','存储地址']
      const rows = this.data.map(r=>[
        r.caller||'', r.callee||'', r.start||'', r.end||'', r.result||'', r.storage||''
      ])
      const csv = [header.join(','), ...rows.map(x=>x.map(v=>String(v).replace(/"/g,'""')).join(','))].join('\n')
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = '通话记录.csv'
      a.click()
      URL.revokeObjectURL(url)
    }
  },
  computed:{
    pageCount(){ return Math.max(1, Math.ceil(this.data.length / this.pageSize)) },
    viewData(){
      const start = (this.page-1) * this.pageSize
      return this.data.slice(start, start + this.pageSize)
    },
    pageNumbers(){
      const arr = []
      for(let i=1;i<=this.pageCount;i++) arr.push(i)
      return arr
    }
  }
}
</script>
