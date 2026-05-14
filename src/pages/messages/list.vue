<template>
	<div :style='{"width":"100%","padding":"20px 10% 40px","margin":"10px auto","position":"relative","background":"none"}'>
		<div class="section-title" :style='{"padding":"0","borderColor":"#e61f4d","margin":"10px auto","color":"#000000","textAlign":"center","borderWidth":"0 0 0px","display":"none","width":"100%","lineHeight":"32px","fontSize":"30px","borderStyle":"solid","fontWeight":"600"}'>在线反馈</div>
		<el-form :model="form" :rules="rules" ref="form" label-width="65px" label-position="left">
			<el-form-item label="留言" prop="content">
				<editor
					myQuillEditor="content"
					v-model="form.content" 
					class="editor" 
					action="file/upload">
				</editor>
			</el-form-item>
			<el-form-item label="图片" prop="cpicture">
				<file-upload
					tip="点击上传图片"
					action="file/upload"
					:limit="1"
					:multiple="true"
					:fileUrls="form.cpicture?form.cpicture:''"
					@change="cpictureUploadChange"
				></file-upload>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="submitForm('form')">立即提交</el-button>
				<el-button @click="resetForm('form')">重置</el-button>
			</el-form-item>
		</el-form>
		<div class="section-content">
			<el-tabs v-model="activeName" type="card" @tab-click="getInfo(1)">
				<el-tab-pane label="全局" name="first"></el-tab-pane>
				<el-tab-pane label="个人" name="second"></el-tab-pane>
			</el-tabs>
			<span v-for="item in infoList" :key="item.id">
				<div class="header-block">
					<el-avatar v-if="item.avatarurl" :size="50" :src="$config.baseUrl + item.avatarurl"></el-avatar>
					<el-avatar v-if="!item.avatarurl" :size="50" :src="require('@/assets/touxiang.png')"></el-avatar>
					<span class="userinfo">用户：{{item.username}}</span>
				</div>
				<div class="content-block-ask">
					<div class="ql-snow ql-editor" v-html="item.content"></div>
				</div>
				<div class="content-block-asktime">
					{{item.addtime}}
				</div>
				<div v-if="item.cpicture" class="content" style="margin: 0;flex: 1;">
					<img style="max-width: 300px;max-height: 300px;border: 2px solid #EEEEEE;margin:8px 0 0 50px;" :src="$config.baseUrl+item.cpicture">
				</div>
				<div class="content-block-reply" v-if="item.reply">
					回复：<div class="ql-snow ql-editor" v-html="item.reply"></div>
				</div>
				<div v-if="item.rpicture" class="content" style="margin: 0;flex: 1;">
					<img style="max-width: 300px;max-height: 300px;border: 2px solid #EEEEEE;margin:8px 0 0 50px;" :src="$config.baseUrl+item.rpicture">
				</div>
				<div v-if="userid==item.userid" class="content-block-del" @click="delClick(item.id)">删除</div>
				<el-divider></el-divider>
			</span>
		</div>
		<el-pagination
			background
			id="pagination" class="pagination"
			:pager-count="7"
			:page-size="pageSize"
			:page-sizes="pageSizes"
			prev-text="<"
			next-text=">"
			:hide-on-single-page="true"
			:layout='["total","prev","pager","next","sizes","jumper"].join()'
			:total="total"
			:style='{"padding":"0","margin":"20px auto","whiteSpace":"nowrap","color":"#333","textAlign":"center","background":"none","width":"100%","fontSize":"16px","fontWeight":"500","order":"50"}'
			@current-change="curChange"
			@prev-click="prevClick"
			@size-change="sizeChange"
			@next-click="nextClick"
		></el-pagination>
	  
	</div>
</template>

<script>
	export default {
		//数据集合
		data() {
			return {
				layouts: '',
				form: {
					content: '',
					userid: Number(localStorage.getItem('frontUserid')),
					username: localStorage.getItem('username')
				},
				total: 1,
				pageSize: 20,
				pageSizes: [],
				totalPage: 1,
				rules: {
					content: [
						{ required: true, message: '请输入内容', trigger: 'blur' }
					]
				},
				infoList: [],
				userid: localStorage.getItem('frontUserid'),
				activeName: 'first',
			}
		},
		created() {
			this.getInfo(1);
		},
		//方法集合
		methods: {
			getInfo(page) {
				let params = {
					page, limit: this.pageSize,sort:"addtime", order:"desc"
				}
				if(this.activeName=='second') {
					params.userid = this.userid
				}
				this.$http.get('messages/list', {params: params}).then(res => {
					if (res.data.code == 0) {
						this.infoList = res.data.data.list;
						this.total = res.data.data.total;
						this.pageSize = Number(res.data.data.pageSize);
						this.totalPage = res.data.data.totalPage;
						if(this.pageSizes.length==0){
							this.pageSizes = [this.pageSize, this.pageSize*2, this.pageSize*3, this.pageSize*5];
						}
					}
				});
			},
			curChange(page) {
				this.getInfo(page);
			},
			prevClick(page) {
				this.getInfo(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getInfo(1);
			},
			nextClick(page) {
				this.getInfo(page);
			},
			cpictureUploadChange(fileUrls) {
				this.form.cpicture = fileUrls;
			},
			submitForm(formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {
						if(this.form.cpicture!=null) {
							this.form.cpicture = this.form.cpicture.replace(new RegExp(this.$config.baseUrl,"g"),"");
						}
						this.form.avatarurl = localStorage.getItem('frontHeadportrait')?localStorage.getItem('frontHeadportrait'):'';
						this.$http.post('messages/add', this.form).then(res => {
							if (res.data.code == 0) {
								this.$message({
									type: 'success',
									message: '留言成功!',
									duration: 1500,
									onClose: () => {
										window.location.reload();
									}
								});
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
			delClick(id){
				this.$confirm('是否删除此在线反馈？')
					.then(_ => {
						this.$http.post('messages/delete', [id]).then(res => {
							if (res.data.code == 0) {
								this.$message({
									type: 'success',
									message: '删除成功!',
									duration: 1500,
									onClose: () => {
										this.getInfo(1)
									}
								});
							}
						});
					}).catch(_ => {});
			},
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.section {
		width: 900px;
		margin: 0 auto;
	}
	.el-form {
		background: #fff;
		padding: 10px;
	}
	.section-content {
		margin-top: 50px;
		background: #fff;
		padding: 10px;
	}
	.section-pagination {
		margin-top: 30px;
		text-align: center;
	}
	.header-block {
		height: 50px;
		line-height: 50px;
		display: flex;
	}
	.userinfo {
		align-self: center;
		margin-left: 15px;
	}
	.content-block-ask, .content-block-reply {
		margin-left: 65px;
		margin-top: 15px;
	}
	.content-block-asktime{
		width: 100%;
		text-align: right;
		color: #999;
	}
	.content-block-del{
		width: 100%;
		text-align: right;
		color: #999;
		cursor: pointer;
	}
	.content-block-reply {
		margin-top: 30px;
	}
	.z-box {
		width: 100% !important;
	}
	.editor {
				border: 0px solid #ddd;
				border-radius: 4px;
				box-shadow: none;
				outline: none;
				margin: 30px 0 0 0;
				color: #333;
				background: #FFF;
				width: 100%;
				clear: both;
				font-size: 14px;
				line-height: 32px;
			}
	.editor /deep/.ql-toolbar {
		background: none;
	}
	.editor /deep/.ql-container {
		background: none;
		min-height: 180px;
	}
	.editor /deep/.ql-container .ql-blank::before {
		color: #999;
	}
  
</style>
