<template>
	<div>

		<div class="container" :style="{'backgroundImage': indexBgUrl?`url(${$config.baseUrl + indexBgUrl})`:''}">
			<el-form class='rgs-form animate__animated animate__' v-if="pageFlag=='security1'">
				<div class="rgs-form2">
					<div class="title">找回密码</p></div>
					<el-form-item class="list-item" prop="username">
						<div class="label">账号：</div>
						<el-input v-model="forgetForm.username" placeholder="请您输入账号" />
					</el-form-item>
					<div class="register-btn">
						<div class="register-btn1">
							<el-button class="register_btn" type="primary" @click="getSecurity()">下一步</el-button>
						</div>
						<div class="register-btn2">
							<router-link class="has_btn" to="/login">已有账号，直接登录</router-link>
						</div>
					</div>
				</div>
				<div class="idea1">欢迎注册</div>
				<div class="idea2"></div>
			</el-form>
			<el-form class='rgs-form animate__animated animate__' v-if="pageFlag=='security2'">
				<div class="rgs-form2">
					<div class="title">找回密码</p></div>
					<el-form-item class="list-item" prop="pquestion">
						<div class="label">密保问题：</div>
						<el-input readonly v-model="registerForm.pquestion" placeholder="密保问题" />
					</el-form-item>
					<el-form-item class="list-item" prop="myanswer">
						<div class="label">密保答案：</div>
						<el-input v-model="registerForm.myanswer" placeholder="请您输入密保答案" />
					</el-form-item>
					<div class="register-btn">
						<div class="register-btn1">
							<el-button class="register_btn" type="primary" @click="validateSecurity()">下一步</el-button>
						</div>
						<div class="register-btn2">
							<router-link class="has_btn" to="/login">已有账号，直接登录</router-link>
						</div>
					</div>
				</div>
				<div class="idea1">欢迎注册</div>
				<div class="idea2"></div>
			</el-form>
			<el-form class='rgs-form animate__animated animate__' v-if="pageFlag=='security3'">
				<div class="rgs-form2">
					<div class="title">找回密码</p></div>
					<el-form-item class="list-item" prop="newpassword">
						<div class="label">新密码：</div>
						<el-input v-model="registerForm.newpassword" type="password" placeholder="请您输入新密码" />
					</el-form-item>
					<el-form-item class="list-item" prop="repassword">
						<div class="label">确认密码：</div>
						<el-input v-model="registerForm.repassword" type="password" placeholder="请您确认密码" />
					</el-form-item>
					<div class="register-btn">
						<div class="register-btn1">
							<el-button class="register_btn" type="primary" @click="updatePassword()">修改密码</el-button>
						</div>
						<div class="register-btn2">
							<router-link class="has_btn" to="/login">已有账号，直接登录</router-link>
						</div>
					</div>
				</div>
				<div class="idea1">欢迎注册</div>
				<div class="idea2"></div>
			</el-form>
			<el-form class='rgs-form animate__animated animate__' v-if="pageFlag=='register'" ref="registerForm" :model="registerForm" :rules="rules">
				<div class="rgs-form2">
					<div class="title">基于Spark的在线音乐平台用户听歌偏好与推荐分析系统的设计与实现注册</p></div>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="zhanghao">
						<div class="label" :class="changeRules('zhanghao')?'required':''">账号：</div>
						<el-input v-model="registerForm.zhanghao" :readonly="ro.zhanghao" placeholder="请输入账号" />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="xingming">
						<div class="label" :class="changeRules('xingming')?'required':''">姓名：</div>
						<el-input v-model="registerForm.xingming" :readonly="ro.xingming" placeholder="请输入姓名" />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="mima">
						<div class="label" :class="changeRules('mima')?'required':''">密码：</div>
						<el-input v-model="registerForm.mima" type="password" placeholder="请输入密码"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="mima2">
						<div class="label" :class="changeRules('mima')?'required':''">确认密码：</div>
						<el-input v-model="registerForm.mima2" type="password" placeholder="请再次输入密码" />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="xingbie">
						<div class="label" :class="changeRules('xingbie')?'required':''">性别：</div>
						<el-select filterable v-model="registerForm.xingbie" placeholder="请选择性别" :disabled="ro.xingbie">
							<el-option
								v-for="(item,index) in yonghuxingbieOptions"
								:key="index"
								:label="item"
								:value="item">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="lianxifangshi">
						<div class="label" :class="changeRules('lianxifangshi')?'required':''">联系方式：</div>
						<el-input v-model="registerForm.lianxifangshi" :readonly="ro.lianxifangshi" placeholder="请输入联系方式" />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="touxiang">
						<div class="label" :class="changeRules('touxiang')?'required':''">头像：</div>
						<file-upload
							tip="点击上传头像"
							action="file/upload"
							:limit="1"
							:multiple="true"
							:fileUrls="registerForm.touxiang?registerForm.touxiang:''"
							@change="yonghutouxiangUploadChange"
						></file-upload>
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="pquestion">
						<div class="label" :class="changeRules('pquestion')?'required':''">密保问题：</div>
						<el-input v-model="registerForm.pquestion" :readonly="ro.pquestion" placeholder="请输入密保问题" />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'" prop="panswer">
						<div class="label" :class="changeRules('panswer')?'required':''">密保答案：</div>
						<el-input v-model="registerForm.panswer" :readonly="ro.panswer" placeholder="请输入密保答案" />
					</el-form-item>
					<div class="register-btn">
						<div class="register-btn1">
							<el-button class="register_btn" type="primary" @click="submitForm('registerForm')">注册</el-button>
						</div>
						<div class="register-btn2">
							<router-link class="has_btn" to="/login">已有账号，直接登录</router-link>
						</div>
					</div>
				</div>
				<div class="idea1">欢迎注册</div>
				<div class="idea2"></div>
			</el-form>
		</div>
	</div>
</div>
</template>

<script>
	import 'animate.css';

export default {
    //数据集合
    data() {
		return {
            pageFlag : '',
			tableName: '',
			registerForm: {},
			forgetForm: {},
			rules: {},
			ro: {},
			requiredRules: {},
            yonghuxingbieOptions: [],
			indexBgUrl: '',
		}
    },
	mounted() {
		if(this.$route.query.pageFlag=='register'){
			this.tableName = this.$route.query.role;
			if(this.tableName=='yonghu'){
				this.registerForm = {
					zhanghao: '',
					xingming: '',
					mima: '',
					mima2: '',
					xingbie: '',
					lianxifangshi: '',
					touxiang: '',
					pquestion: '',
					panswer: '',
					status: '',
				}
				this.ro = {
					zhanghao: false,
					xingming: false,
					mima: false,
					xingbie: false,
					lianxifangshi: false,
					touxiang: false,
					pquestion: false,
					panswer: false,
					status: false,
				}
			}
			if ('yonghu' == this.tableName) {
				this.rules.zhanghao = [{ required: true, message: '请输入账号', trigger: 'blur' }];
				this.requiredRules.zhanghao = [{ required: true, message: '请输入账号', trigger: 'blur' }]
				this.rules.xingming = [{ required: true, message: '请输入姓名', trigger: 'blur' }];
				this.requiredRules.xingming = [{ required: true, message: '请输入姓名', trigger: 'blur' }]
				this.rules.mima = [{ required: true, message: '请输入密码', trigger: 'blur' }];
				this.requiredRules.mima = [{ required: true, message: '请输入密码', trigger: 'blur' }]
				this.yonghuxingbieOptions = "男,女".split(',');
				this.rules.lianxifangshi = [{ required: true, validator: this.$validate.isMobile, trigger: 'blur' }];
				this.rules.pquestion = [{ required: true, message: '请输入密保问题', trigger: 'blur' }];
				this.requiredRules.pquestion = [{ required: true, message: '请输入密保问题', trigger: 'blur' }]
				this.rules.panswer = [{ required: true, message: '请输入密保答案', trigger: 'blur' }];
				this.requiredRules.panswer = [{ required: true, message: '请输入密保答案', trigger: 'blur' }]
				this.rules.status = [{ required: true, validator: this.$validate.isIntNumer, trigger: 'blur' }];
			}
		}
	},
    created() {
		this.$http.get('config/info?name=fRegisterBackgroudImg',).then(rs=>{this.indexBgUrl = rs.data.data?rs.data.data.value:''})
		this.pageFlag = this.$route.query.pageFlag;
    },
    //方法集合
    methods: {
		changeRules(name){
			if(this.requiredRules[name]){
				return true
			}
			return false
		},
		// 获取uuid
		getUUID () {
			return new Date().getTime();
		},
        // 下二随
		yonghutouxiangUploadChange(fileUrls) {
			this.registerForm.touxiang = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
		},

		// 多级联动参数


//获取密保问题
		getSecurity(){
			this.tableName = 'yonghu'
			if(!this.tableName) {
				this.$message.error("请选择角色");
				return false
			}
			if(!this.forgetForm.username){
				this.$message.error("请输入账号");
				return false
			}
			this.$http({
				url: this.tableName+`/security?username=` + this.forgetForm.username,
				method: "get",
			}).then(({
				data
			}) => {
				if (data.data && data.code === 0) {
					this.registerForm = data.data;
					this.pageFlag="security2"
				} else {
					if(!data.data) {
						this.$message.error("用户不存在");
					} else {
						this.$message.error(data.msg);
					}
				}
			});
		},
		//验证密保问题
		validateSecurity(){
			let that = this
			if(this.registerForm.panswer!=this.registerForm.myanswer){
				this.$message.error("答案输入不正确");
				return false
			}
			this.$message.success("答案正确");
			setTimeout(()=>{
				this.pageFlag="security3";
			},1000)
		},
		// 修改密码
		updatePassword() {
			if (!this.registerForm.newpassword) {
				this.$message.error("请输入新密码");
				return;
			}
			if (this.registerForm.newpassword != this.registerForm.repassword) {
				this.$message.error("两次密码输入不一致");
				return;
			}
			this.registerForm.mima = this.registerForm.newpassword;
			this.registerForm.password = this.registerForm.newpassword;
			this.$http.post(this.tableName+`/update`, this.registerForm).then(res => {
			  if (res.data.code === 0) {
				this.$message({
					message: "密码修改成功",
					type: "success",
					duration: 1500,
					onClose: () => {
					  this.$router.push('/login');
					}
				});
			  } else {
				this.$message.error(res.data.msg);
			  }
			});
		},
		submitForm(formName) {
			this.$refs[formName].validate((valid) => {
				if (valid) {
					var url=this.tableName+"/register";
					if(`yonghu` == this.tableName && this.registerForm.mima!=this.registerForm.mima2) {
						this.$message.error(`两次密码输入不一致`);
						return
					}
					this.$http.post(url, this.registerForm).then(res => {
						if (res.data.code === 0) {
							this.$message({
								message: '注册成功',
								type: 'success',
								duration: 1500,
								onClose: () => {
									this.$router.push('/login');
								}
							});
						} else {
							this.$message.error(res.data.msg);
						}
					});
				} else {
					return false;
				}
			});
		},
		resetForm(formName) {
			this.$refs[formName].resetFields();
		},
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.container {
		background-repeat: no-repeat;
		background-size: 100% 100% !important;
		background: url(http://codegen.caihongy.cn/20251215/7b78273542ca44c7907bec2473e6db02.png);
		display: flex;
		width: 100%;
		min-height: 100vh;
		justify-content: center;
		align-items: center;
		background-position: center center;
		position: relative;
		background: url(http://codegen.caihongy.cn/20251215/7b78273542ca44c7907bec2473e6db02.png);
		.rgs-form {
			border: 1px solid #707070;
			border-radius: 10px;
			padding: 40px 40px;
			margin: 0px auto;
			z-index: 10;
			background:  rgba(255,255,255,0.8);
			display: flex;
			width: 1100px;
			height: auto;
			.rgs-form2 {
				width: 70%;
				.title {
					padding: 0;
					margin: 0 0 10px 0;
					color: #000000;
					white-space: nowrap;
					font-weight: 600;
					font-size: 20px;
					border-color: #04a44b50;
					line-height: 56px;
					text-shadow: none;
					background: none;
					width: 100%;
					border-width: 0px 0 0px;
					border-style: solid;
					text-align: left;
					height: 60px;
				}
				.subtitle {
					margin: 0 0 10px 0;
					text-shadow: 4px 4px 2px rgba(64, 158, 255, .5);
					color: rgba(64, 158, 255, 1);
					width: 100%;
					font-size: 20px;
					line-height: 44px;
					text-align: center;
				}
				.list-item {
					padding: 0;
					margin: 15px auto 0;
					width: 100%;
					border-color: #ddd;
					border-width: 0 0 0px;
					position: relative;
					border-style: solid;
					height: auto;
					/deep/.el-form-item__content {
						padding: 0 0 0 120px;
						display: block;
						width: 100%;
						.label {
							padding: 0 5px 0 0;
							z-index: 9;
							color: #333;
							left: 0;
							width: 120px;
							font-size: 16px;
							line-height: 40px;
							position: absolute !important;
							text-align: right;
						}
						
						.required {
							position: relative;
						}
						.required::after{
							color: red;
							left: 110px;
							position: absolute;
							content: "*";
						}
						.el-input {
							border-radius: 100px;
							flex: 1;
							background: rgba(255,255,255,0.3);
							width: 100%;
						}
						.el-input .el-input__inner {
							border: 0;
							border-radius: 0 20px 20px 0;
							padding: 0 10px;
							box-shadow: none;
							outline: none;
							color: #666;
							background: none;
							width: 100%;
							font-size: 14px;
							height: 40px;
						}
						.el-input .el-input__inner:focus {
							border: 0;
							border-radius: 0 20px 20px 0;
							padding: 0 10px;
							box-shadow: none;
							outline: none;
							color: #666;
							background: none;
							width: 100%;
							font-size: 14px;
							height: 40px;
						}
						.el-input-number {
							border-radius: 100px;
							flex: 1;
							background: rgba(255,255,255,0.3);
							width: 100%;
						}
						.el-input-number .el-input__inner {
							text-align: left;
							border: 0;
							border-radius: 0 20px 20px 0;
							padding: 0 10px;
							box-shadow: none;
							outline: none;
							color: #666;
							background: none;
							width: 100%;
							font-size: 14px;
							height: 40px;
						}
						.el-input-number .el-input-number__decrease {
							display: none;
						}
						.el-input-number .el-input-number__increase {
							display: none;
						}
						.el-select {
							border-radius: 100px;
							flex: 1;
							background: rgba(255,255,255,0.3);
							width: 100%;
						}
						.el-select .el-input__inner {
							border: 0;
							border-radius: 0 20px 20px 0;
							padding: 0 10px;
							box-shadow: none;
							outline: none;
							color: #666;
							background: none;
							width: 100%;
							font-size: 16px;
							height: 40px;
						}
						.el-select .el-input__inner:focus {
							border: 0;
							border-radius: 0 20px 20px 0;
							padding: 0 10px;
							box-shadow: none;
							outline: none;
							color: #666;
							background: none;
							width: 100%;
							font-size: 16px;
							height: 40px;
						}
						.el-date-editor {
							border-radius: 100px;
							flex: 1;
							background: rgba(255,255,255,0.3);
							width: 100%;
						}
						.el-date-editor .el-input__inner {
							border: 0;
							border-radius: 0 20px 20px 0;
							padding: 0 10px 0 30px;
							box-shadow: none;
							outline: none;
							color: #666;
							background: none;
							width: 100%;
							font-size: 16px;
							height: 40px;
						}
						.el-date-editor .el-input__inner:focus {
							border: 0;
							border-radius: 0 20px 20px 0;
							padding: 0 10px 0 30px;
							box-shadow: none;
							outline: none;
							color: #666;
							background: none;
							width: 100%;
							font-size: 16px;
							height: 40px;
						}
						.el-upload--picture-card {
							background: transparent;
							border: 0;
							border-radius: 0;
							width: auto;
							height: auto;
							line-height: initial;
							vertical-align: middle;
						}
						.upload .upload-img {
							border: 1px solid #ddd;
							cursor: pointer;
							border-radius: 4px;
							color: #999;
							background: rgba(255,255,255,.2);
							object-fit: cover;
							width: 60px;
							font-size: 22px;
							line-height: 60px;
							text-align: center;
							height: 60px;
						}
						.el-upload-list .el-upload-list__item {
							border: 1px solid #ddd;
							cursor: pointer;
							border-radius: 4px;
							color: #999;
							background: rgba(255,255,255,.2);
							object-fit: cover;
							width: 60px;
							font-size: 22px;
							line-height: 60px;
							text-align: center;
							height: 60px;
							font-size: 14px;
							line-height: 1.8;
						}
						.el-upload .el-icon-plus {
							border: 1px solid #ddd;
							cursor: pointer;
							border-radius: 4px;
							color: #999;
							background: rgba(255,255,255,.2);
							object-fit: cover;
							width: 60px;
							font-size: 22px;
							line-height: 60px;
							text-align: center;
							height: 60px;
						}
						.el-upload__tip {
							color: #999;
							font-size: 16px;
						}
						.emailInput {
							border: 0;
							border-radius: 0 20px 20px 0;
							padding: 0 10px;
							box-shadow: none;
							margin: 0;
							outline: none;
							color: #666;
							background: none;
							flex: 1;
							width: 100%;
							font-size: 14px;
							height: 40px;
						}
						.emailInput:focus {
							border: 0;
							border-radius: 0 20px 20px 0;
							padding: 0 10px;
							box-shadow: none;
							outline: none;
							color: #666;
							flex: 1;
							background: none;
							width: 100%;
							font-size: 16px;
							height: 40px;
						}
						.el-btn {
							border: 0;
							cursor: pointer;
							padding: 0 15px;
							margin: 0 0 5px;
							color: #fff;
							font-size: 15px;
							float: right;
							border-radius: 2px;
							box-shadow: 0 0 0px rgba(64, 158, 255, .5);
							outline: none;
							background: #ABDE53;
							width: auto;
							height: 40px;
						}
						.el-btn:hover {
							opacity: 0.8;
						}
						
						.el-input__inner::placeholder {
							color: #999;
							font-size: 16px;
						}
						input::placeholder {
							color: #999;
							font-size: 16px;
						}
						.editor {
							border-radius: 50px;
							padding: 10px;
							margin: 20px;
							background: rgba(255,255,255,0.3);
							width: 100%;
							height: auto;
						}
						.editor .ql-toolbar {
							border: none;
							box-shadow: none;
							background: none;
						}
						.editor .ql-container {
							border: none;
							background: none;
						}
						.editor .ql-container .ql-blank::before {
							color: #999;
						}
					}
				}
				.register-btn {
					padding: 0;
					margin: 20px 0 0;
					width: 100%;
					text-align: center;
				}
				.register-btn1 {
					display: inline-block;
					width: 50%;
					text-align: center;
				}
				.register-btn2 {
					display: inline-block;
					width: 100%;
					text-align: center;
				}
				.register_btn {
					cursor: pointer;
					padding: 0 20px;
					margin: 0 20px 20px 0;
					color: #fff;
					display: inline-block;
					text-decoration: none;
					font-size: 20px;
					border-color: #ff6f3c50;
					line-height: 50px;
					border-radius: 2px;
					background: #ABDE53;
					width: 100%;
					border-width: 0 0 0px;
					border-style: solid;
					min-width: 120px;
					height: 50px;
				}
				.register_btn:hover {
					opacity: 0.8;
				}
				.has_btn {
					cursor: pointer;
					padding: 0;
					color: #000;
					text-decoration: none;
					display: inline-block;
					font-size: 16px;
				}
				.has_btn:hover {
					opacity: 0.8;
				}
			}
			.idea1 {
				padding: 30px 0;
				margin: auto;
				background: none;
				font-weight: 500;
				display: block;
				width: 30%;
				font-size: 40px;
				height: 40px;
				order: -1;
			}
			.idea2 {
				background: blue;
				display: none;
				width: 100%;
				height: 40px;
			}
		}
	}
	
	::-webkit-scrollbar {
		display: none;
	}
</style>
