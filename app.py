from flask import Flask, request, redirect, url_for, session, jsonify, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key = "replace-this-secret"

users = {
    "admin": {"password": "admin123", "phone": "00000000000", "invite": "ADMIN", "role": "admin"}
}

call_logs = [
    {"caller": "123456", "callee": "15355080978", "start": "2025-12-15 12:16:55", "end": "2025-12-15 12:17:58", "result": "stage5正常挂断", "storage": "/records/2025-12-15-0900.mp3"},
    # {"caller": "13800000003", "callee": "13900000004", "start": "2025-11-02 10:23", "end": "2025-11-02 10:29", "result": "stage3被叫挂断", "storage": "/records/2025-11-02-1023.mp3"},
    # {"caller": "13800000005", "callee": "13900000006", "start": "2025-11-03 14:00", "end": "2025-11-03 14:11", "result": "stage5正常挂断", "storage": "/records/2025-11-03-1400.mp3"},
    # {"caller": "13800000007", "callee": "13900000008", "start": "2025-11-04 09:10", "end": "2025-11-04 09:20", "result": "stage5正常挂断", "storage": "/records/2025-11-04-0910.mp3"},
    # {"caller": "13800000009", "callee": "13900000010", "start": "2025-11-04 15:30", "end": "2025-11-04 15:34", "result": "stage1被叫挂断", "storage": "/records/2025-11-04-1530.mp3"},
    # {"caller": "13800000011", "callee": "13900000012", "start": "2025-11-05 11:00", "end": "2025-11-05 11:18", "result": "stage5正常挂断", "storage": "/records/2025-11-05-1100.mp3"},
    # {"caller": "13800000013", "callee": "13900000014", "start": "2025-11-05 16:40", "end": "2025-11-05 16:55", "result": "stage5正常挂断", "storage": "/records/2025-11-05-1640.mp3"},
    # {"caller": "13800000015", "callee": "13900000016", "start": "2025-11-06 08:50", "end": "2025-11-06 09:02", "result": "stage5正常挂断", "storage": "/records/2025-11-06-0850.mp3"},
    # {"caller": "13800000017", "callee": "13900000018", "start": "2025-11-06 13:13", "end": "2025-11-06 13:20", "result": "未接听", "storage": "/records/2025-11-06-1313.mp3"},
    # {"caller": "13800000019", "callee": "13900000020", "start": "2025-11-07 10:05", "end": "2025-11-07 10:22", "result": "stage5正常挂断", "storage": "/records/2025-11-07-1005.mp3"},
    # {"caller": "13800000021", "callee": "13900000022", "start": "2025-11-07 19:30", "end": "2025-11-07 19:33", "result": "未接听", "storage": "/records/2025-11-07-1930.mp3"},
    # {"caller": "13800000023", "callee": "13900000024", "start": "2025-11-08 09:30", "end": "2025-11-08 09:47", "result": "stage5正常挂断", "storage": "/records/2025-11-08-0930.mp3"},
    # {"caller": "13800000025", "callee": "13900000026", "start": "2025-11-08 14:00", "end": "2025-11-08 14:10", "result": "接通并完成沟通", "storage": "/records/2025-11-08-1400.mp3"},
    # {"caller": "13800000027", "callee": "13900000028", "start": "2025-11-09 10:10", "end": "2025-11-09 10:16", "result": "stage5正常挂断", "storage": "/records/2025-11-09-1010.mp3"},
    # {"caller": "13800000029", "callee": "13900000030", "start": "2025-11-09 17:00", "end": "2025-11-09 17:12", "result": "stage3主叫挂断", "storage": "/records/2025-11-09-1700.mp3"}

]

tasks = [
    {"phone": "15355080978", "name": "张三", "gender": "男", "risk": "刷单返利"},
    {"phone": "13900000004", "name": "李四", "gender": "女", "risk": "冒充熟人转账"},
    {"phone": "13900000006", "name": "王五", "gender": "男", "risk": "虚假投资"},
    {"phone": "13900000008", "name": "赵六", "gender": "男", "risk": "贷款欺诈"},
    {"phone": "13900000010", "name": "钱七", "gender": "女", "risk": "冒充熟人转账"},
    {"phone": "13900000012", "name": "孙八", "gender": "男", "risk": "刷单返利"},
    {"phone": "13900000014", "name": "周九", "gender": "女", "risk": "贷款欺诈"},
    {"phone": "13900000016", "name": "吴十", "gender": "男", "risk": "刷单返利"},
    {"phone": "13900000018", "name": "郑一", "gender": "女", "risk": "冒充熟人转账"},
    {"phone": "13900000020", "name": "王二", "gender": "男", "risk": "刷单返利"},
    {"phone": "13900000022", "name": "李三", "gender": "女", "risk": "贷款欺诈"},
    {"phone": "13900000024", "name": "陈四", "gender": "男", "risk": "刷单返利"}
]

scripts = [
    {"text": "是的", "vector": "[---]", "category": "肯定", "stage": "0", "branch": "Any"},
    {"text": "不是", "vector": "[---]", "category": "否定", "stage": "0", "branch": "Any"},
    {"text": "我没接到啊", "vector": "[---]", "category": "肯定", "stage": "0", "branch": "Any"},
    {"text": "好像有", "vector": "[---]", "category": "否定", "stage": "0", "branch": "Any"},
    {"text": "我不太记得了", "vector": "[---]", "category": "不确定", "stage": "0", "branch": "Any"},
    {"text": "不用了谢谢", "vector": "[---]", "category": "不确定", "stage": "0", "branch": "Any"},
    {"text": "之前接到一个刷单的电话", "vector": "[---]", "category": "肯定", "stage": "2", "branch": "刷单返利"},
    {"text": "之前有个说自己是哪个银行的说百分之1的利率贷款50万", "vector": "[---]", "category": "肯定", "stage": "2", "branch": "贷款欺诈"},
    {"text": "之前有个冒充我爸要我转钱的", "vector": "[---]", "category": "肯定", "stage": "2", "branch": "冒充熟人转账"},
    {"text": "有个说刷单日入1000的", "vector": "[---]", "category": "否定", "stage": "2", "branch": "刷单返利"},
    {"text": "我没转钱给他", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "Any"},
    {"text": "他让我先转200给他,然后说能日入1000,我就给他转了200", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "刷单返利"},
    {"text": "我没转", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "Any"},
    {"text": "是的", "vector": "[---]", "category": "肯定", "stage": "0", "branch": "Any"},
    {"text": "不是", "vector": "[---]", "category": "否定", "stage": "0", "branch": "Any"},
    {"text": "我没接到啊", "vector": "[---]", "category": "肯定", "stage": "0", "branch": "Any"},
    {"text": "好像有", "vector": "[---]", "category": "否定", "stage": "0", "branch": "Any"},
    {"text": "我不太记得了", "vector": "[---]", "category": "不确定", "stage": "0", "branch": "Any"},
    {"text": "不用了谢谢", "vector": "[---]", "category": "不确定", "stage": "0", "branch": "Any"},
    {"text": "之前接到一个刷单的电话", "vector": "[---]", "category": "肯定", "stage": "2", "branch": "刷单返利"},
    {"text": "之前有个说自己是哪个银行的说百分之1的利率贷款50万", "vector": "[---]", "category": "2", "stage": "2", "branch": "贷款欺诈"},
    {"text": "之前有个冒充我爸要我转钱的", "vector": "[---]", "category": "肯定", "stage": "2", "branch": "冒充熟人转账"},
    {"text": "有个说刷单日入1000的", "vector": "[---]", "category": "否定", "stage": "2", "branch": "刷单返利"},
    {"text": "我没转钱给他", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "Any"},
    {"text": "他让我先转200给他,然后说能日入1000,我就给他转了200", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "刷单返利"},
    {"text": "我没转", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "Any"},
    {"text": "是的", "vector": "[---]", "category": "肯定", "stage": "0", "branch": "Any"},
    {"text": "不是", "vector": "[---]", "category": "否定", "stage": "0", "branch": "Any"},
    {"text": "我没接到啊", "vector": "[---]", "category": "肯定", "stage": "0", "branch": "Any"},
    {"text": "好像有", "vector": "[---]", "category": "否定", "stage": "0", "branch": "Any"},
    {"text": "我不太记得了", "vector": "[---]", "category": "不确定", "stage": "0", "branch": "Any"},
    {"text": "不用了谢谢", "vector": "[---]", "category": "不确定", "stage": "0", "branch": "Any"},
    {"text": "之前接到一个刷单的电话", "vector": "[---]", "category": "肯定", "stage": "2", "branch": "刷单返利"},
    {"text": "之前有个说自己是哪个银行的说百分之1的利率贷款50万", "vector": "[---]", "category": "2", "stage": "2", "branch": "贷款欺诈"},
    {"text": "之前有个冒充我爸要我转钱的", "vector": "[---]", "category": "肯定", "stage": "2", "branch": "冒充熟人转账"},
    {"text": "有个说刷单日入1000的", "vector": "[---]", "category": "否定", "stage": "2", "branch": "刷单返利"},
    {"text": "我没转钱给他", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "Any"},
    {"text": "他让我先转200给他,然后说能日入1000,我就给他转了200", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "刷单返利"},
    {"text": "我没转", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "Any"},
    {"text": "是的", "vector": "[---]", "category": "肯定", "stage": "0", "branch": "Any"},
    {"text": "不是", "vector": "[---]", "category": "否定", "stage": "0", "branch": "Any"},
    {"text": "我没接到啊", "vector": "[---]", "category": "肯定", "stage": "0", "branch": "Any"},
    {"text": "好像有", "vector": "[---]", "category": "否定", "stage": "0", "branch": "Any"},
    {"text": "我不太记得了", "vector": "[---]", "category": "不确定", "stage": "0", "branch": "Any"},
    {"text": "不用了谢谢", "vector": "[---]", "category": "不确定", "stage": "0", "branch": "Any"},
    {"text": "之前接到一个刷单的电话", "vector": "[---]", "category": "肯定", "stage": "2", "branch": "刷单返利"},
    {"text": "之前有个说自己是哪个银行的说百分之1的利率贷款50万", "vector": "[---]", "category": "2", "stage": "2", "branch": "贷款欺诈"},
    {"text": "之前有个冒充我爸要我转钱的", "vector": "[---]", "category": "肯定", "stage": "2", "branch": "冒充熟人转账"},
    {"text": "有个说刷单日入1000的", "vector": "[---]", "category": "否定", "stage": "2", "branch": "刷单返利"},
    {"text": "我没转钱给他", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "Any"},
    {"text": "他让我先转200给他,然后说能日入1000,我就给他转了200", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "刷单返利"},
    {"text": "我没转", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "Any"},
    {"text": "是的", "vector": "[---]", "category": "肯定", "stage": "0", "branch": "Any"},
    {"text": "不是", "vector": "[---]", "category": "否定", "stage": "0", "branch": "Any"},
    {"text": "我没接到啊", "vector": "[---]", "category": "肯定", "stage": "0", "branch": "Any"},
    {"text": "好像有", "vector": "[---]", "category": "否定", "stage": "0", "branch": "Any"},
    {"text": "我不太记得了", "vector": "[---]", "category": "不确定", "stage": "0", "branch": "Any"},
    {"text": "不用了谢谢", "vector": "[---]", "category": "不确定", "stage": "0", "branch": "Any"},
    {"text": "之前接到一个刷单的电话", "vector": "[---]", "category": "肯定", "stage": "2", "branch": "刷单返利"},
    {"text": "之前有个说自己是哪个银行的说百分之1的利率贷款50万", "vector": "[---]", "category": "2", "stage": "2", "branch": "贷款欺诈"},
    {"text": "之前有个冒充我爸要我转钱的", "vector": "[---]", "category": "肯定", "stage": "2", "branch": "冒充熟人转账"},
    {"text": "有个说刷单日入1000的", "vector": "[---]", "category": "否定", "stage": "2", "branch": "刷单返利"},
    {"text": "我没转钱给他", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "Any"},
    {"text": "他让我先转200给他,然后说能日入1000,我就给他转了200", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "刷单返利"},
    {"text": "我没转", "vector": "[---]", "category": "不确定", "stage": "3", "branch": "Any"},

]

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.post("/api/login")
def api_login():
    data = request.get_json(force=True)
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    admin_mode = bool(data.get("admin"))
    user = users.get(username)
    if user and user["password"] == password:
        if admin_mode and user.get("role") != "admin":
            return jsonify({"ok": False, "error": "管理员模式仅限管理员账号"}), 403
        session["user"] = {"username": username, "role": user.get("role", "user")}
        return jsonify({"ok": True, "user": session["user"]})
    return jsonify({"ok": False, "error": "账号或密码错误"}), 401

@app.post("/api/register")
def api_register():
    data = request.get_json(force=True)
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    phone = data.get("phone") or ""
    invite = data.get("invite") or ""
    if not username or not password:
        return jsonify({"ok": False, "error": "账号与密码为必填"}), 400
    if username in users:
        return jsonify({"ok": False, "error": "账号已存在"}), 409
    users[username] = {"password": password, "phone": phone, "invite": invite, "role": "user"}
    return jsonify({"ok": True})

@app.get("/api/me")
def api_me():
    u = session.get("user")
    if not u:
        return jsonify({"ok": False}), 401
    return jsonify({"ok": True, "user": u})

@app.post("/api/logout")
def api_logout():
    session.clear()
    return jsonify({"ok": True})

@app.get("/api/call_logs")
def api_call_logs():
    return jsonify({"ok": True, "data": call_logs})

@app.get("/api/tasks")
def api_tasks():
    return jsonify({"ok": True, "data": tasks})

@app.get("/api/scripts")
def api_scripts():
    return jsonify({"ok": True, "data": scripts})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
