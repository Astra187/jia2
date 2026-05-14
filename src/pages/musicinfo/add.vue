




































<template>
	<div class="add-update-preview">
		<el-form
			class="add-update-form"
			ref="ruleForm"
			:model="ruleForm"
			:rules="rules"
			label-width="200px"
			>
			<el-form-item class="add-item" label="歌曲名称" prop="songname">
				<el-input v-model="ruleForm.songname" 
					placeholder="歌曲名称" clearable :readonly="ro.songname"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="歌曲风格" prop="songstyle">
				<el-input v-model="ruleForm.songstyle" 
					placeholder="歌曲风格" clearable :readonly="ro.songstyle"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="歌手姓名" prop="singer">
				<el-input v-model="ruleForm.singer" 
					placeholder="歌手姓名" clearable :readonly="ro.singer"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="专辑名称" prop="albumtitle">
				<el-input v-model="ruleForm.albumtitle" 
					placeholder="专辑名称" clearable :readonly="ro.albumtitle"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="封面" v-if="type!='cross' || (type=='cross' && !ro.imgurl)" prop="imgurl">
				<file-upload
					tip="点击上传封面"
					action="file/upload"
					:limit="3"
					:multiple="true"
					:disabled="ro.imgurl"
					:fileUrls="ruleForm.imgurl?ruleForm.imgurl:''"
					@change="imgurlUploadChange"
					></file-upload>
			</el-form-item>
			<el-form-item class="add-item" v-else label="封面" prop="imgurl">
				<img v-if="ruleForm.imgurl.substring(0,4)=='http'" class="upload-img" v-bind:key="index" :src="ruleForm.imgurl.split(',')[0]">
				<img v-else class="upload-img" v-bind:key="index" v-for="(item,index) in ruleForm.imgurl.split(',')" :src="baseUrl+item">
			</el-form-item>
			<el-form-item class="add-item" label="播放量" prop="playcount">
				<el-input v-model.number="ruleForm.playcount" 
					placeholder="播放量" clearable :readonly="ro.playcount"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="作者" prop="author">
				<el-input v-model="ruleForm.author" 
					placeholder="作者" clearable :readonly="ro.author"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="收藏量" prop="favcount">
				<el-input v-model.number="ruleForm.favcount" 
					placeholder="收藏量" clearable :readonly="ro.favcount"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="分享量" prop="sharecount">
				<el-input v-model.number="ruleForm.sharecount" 
					placeholder="分享量" clearable :readonly="ro.sharecount"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="评论数" prop="commentcount">
				<el-input v-model.number="ruleForm.commentcount" 
					placeholder="评论数" clearable :readonly="ro.commentcount"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="歌曲数" prop="songcount">
				<el-input v-model.number="ruleForm.songcount" 
					placeholder="歌曲数" clearable :readonly="ro.songcount"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="歌单" prop="playlist">
				<el-input v-model="ruleForm.playlist" 
					placeholder="歌单" clearable :readonly="ro.playlist"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="时长" prop="durtime">
				<el-input v-model="ruleForm.durtime" 
					placeholder="时长" clearable :readonly="ro.durtime"></el-input>
			</el-form-item>
			<el-form-item class="add-item" label="介绍" prop="albumdesc">
				<el-input
					type="textarea"
					:rows="8"
					:disabled="ro.albumdesc"
					placeholder="介绍"
					v-model="ruleForm.albumdesc">
					</el-input>
			</el-form-item>
			<el-form-item class="add-item" label="来源" prop="detailurl">
				<el-input
					type="textarea"
					:rows="8"
					:disabled="ro.detailurl"
					placeholder="来源"
					v-model="ruleForm.detailurl">
					</el-input>
			</el-form-item>

			<el-form-item class="add-btn-item">
				<el-button class="submitBtn"  type="primary" @click="onSubmit(null)">
					<span class="icon iconfont icon-xiugai13"></span>
					<span class="text">提交信息</span>
				</el-button>
				<el-button class="closeBtn" @click="back()">
					<span class="icon iconfont icon-shanchu7"></span>
					<span class="text">取消</span>
				</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				id: '',
				baseUrl: '',
				ro:{
					songname : false,
					songstyle : false,
					singer : false,
					albumtitle : false,
					imgurl : false,
					playcount : false,
					author : false,
					favcount : false,
					sharecount : false,
					commentcount : false,
					songcount : false,
					playlist : false,
					durtime : false,
					albumdesc : false,
					detailurl : false,
					clicktime : false,
					discussnum : false,
					storeupnum : false,
				},
				type: '',
				userTableName: localStorage.getItem('UserTableName'),
				ruleForm: {
					songname: '',
					songstyle: '',
					singer: '',
					albumtitle: '',
					imgurl: '',
					playcount: '',
					author: '',
					favcount: '',
					sharecount: '',
					commentcount: '',
					songcount: '',
					playlist: '',
					durtime: '',
					albumdesc: '',
					detailurl: '',
					clicktime: '',
					discussnum: '',
					storeupnum: '',
				},

				rules: {
					songname: [
					],
					songstyle: [
					],
					singer: [
					],
					albumtitle: [
					],
					imgurl: [
					],
					playcount: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					author: [
					],
					favcount: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					sharecount: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					commentcount: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					songcount: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					playlist: [
					],
					durtime: [
					],
					albumdesc: [
					],
					detailurl: [
					],
					clicktime: [
					],
					discussnum: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
					storeupnum: [
						{ validator: this.$validate.isIntNumer, trigger: 'blur' },
					],
				},
				centerType: false,
			};
		},
		computed: {
			sessionForm() {
				return JSON.parse(localStorage.getItem('sessionForm'))
			},



		},
		components: {
		},
		created() {
			if(this.$route.query.centerType){
				this.centerType = true
			}
			//this.bg();
			let type = this.$route.query.type ? this.$route.query.type : '';
			this.init(type);
			this.baseUrl = this.$config.baseUrl;
		},
		methods: {
			getMakeZero(s) {
				return s < 10 ? '0' + s : s;
			},
			// 下载
			download(file ){
				window.open(`${file}`)
			},
			// 初始化
			init(type) {
				this.type = type;
				if(type=='cross'){
					var obj = JSON.parse(localStorage.getItem('crossObj'));
					for (var o in obj){
						if(o=='songname'){
							this.ruleForm.songname = obj[o];
							this.ro.songname = true;
							continue;
						}
						if(o=='songstyle'){
							this.ruleForm.songstyle = obj[o];
							this.ro.songstyle = true;
							continue;
						}
						if(o=='singer'){
							this.ruleForm.singer = obj[o];
							this.ro.singer = true;
							continue;
						}
						if(o=='albumtitle'){
							this.ruleForm.albumtitle = obj[o];
							this.ro.albumtitle = true;
							continue;
						}
						if(o=='imgurl'){
							this.ruleForm.imgurl = obj[o]?obj[o].split(",")[0]:'';
							this.ro.imgurl = true;
							continue;
						}
						if(o=='playcount'){
							this.ruleForm.playcount = obj[o];
							this.ro.playcount = true;
							continue;
						}
						if(o=='author'){
							this.ruleForm.author = obj[o];
							this.ro.author = true;
							continue;
						}
						if(o=='favcount'){
							this.ruleForm.favcount = obj[o];
							this.ro.favcount = true;
							continue;
						}
						if(o=='sharecount'){
							this.ruleForm.sharecount = obj[o];
							this.ro.sharecount = true;
							continue;
						}
						if(o=='commentcount'){
							this.ruleForm.commentcount = obj[o];
							this.ro.commentcount = true;
							continue;
						}
						if(o=='songcount'){
							this.ruleForm.songcount = obj[o];
							this.ro.songcount = true;
							continue;
						}
						if(o=='playlist'){
							this.ruleForm.playlist = obj[o];
							this.ro.playlist = true;
							continue;
						}
						if(o=='durtime'){
							this.ruleForm.durtime = obj[o];
							this.ro.durtime = true;
							continue;
						}
						if(o=='albumdesc'){
							this.ruleForm.albumdesc = obj[o];
							this.ro.albumdesc = true;
							continue;
						}
						if(o=='detailurl'){
							this.ruleForm.detailurl = obj[o];
							this.ro.detailurl = true;
							continue;
						}
						if(o=='clicktime'){
							this.ruleForm.clicktime = obj[o];
							this.ro.clicktime = true;
							continue;
						}
						if(o=='discussnum'){
							this.ruleForm.discussnum = obj[o];
							this.ro.discussnum = true;
							continue;
						}
						if(o=='storeupnum'){
							this.ruleForm.storeupnum = obj[o];
							this.ro.storeupnum = true;
							continue;
						}
					}
				}else if(type=='edit'){
					this.info()
				}

				if (localStorage.getItem('raffleType') && localStorage.getItem('raffleType') != null) {
					localStorage.removeItem('raffleType')
					setTimeout(() => {
						this.onSubmit(null)
					}, 300)
				}
			},

			// 多级联动参数
			// 多级联动参数
			async info() {
				await this.$http.get(`musicinfo/detail/${this.$route.query.id}`, {emulateJSON: true}).then(res => {
					if (res.data.code == 0) {
						this.ruleForm = res.data.data;
					}
				});
			},
			// 提交
			async onSubmit(subMitType=null) {
				await this.$refs["ruleForm"].validate(async valid => {
					if(valid) {
						if(!this.ruleForm.id) {
							delete this.ruleForm.userid
						}
						if(this.type=='cross'){
							var statusColumnName = localStorage.getItem('statusColumnName');
							var statusColumnValue = localStorage.getItem('statusColumnValue');
							if(statusColumnName && statusColumnName!='') {
								var obj = JSON.parse(localStorage.getItem('crossObj'));
								if(!statusColumnName.startsWith("[")) {
									for (var o in obj){
										if(o==statusColumnName){
											obj[o] = statusColumnValue;
										}
									}
									var table = localStorage.getItem('crossTable');
									await this.$http.post(table+'/update', obj).then(res => {});
								}
							}
						}

						await this.$http.post(`musicinfo/${this.ruleForm.id?'update':this.centerType?'save':'add'}`, this.ruleForm).then(async res => {
							if (res.data.code == 0) {
								await this.$message({
									message: '操作成功',
									type: 'success',
									duration: 1500,
									onClose: () => {
										this.$router.go(-1);
										
									}
								});
							} else {
								this.$message({
									message: res.data.msg,
									type: 'error',
									duration: 1500
								});
							}
						});
					}
				});
			},
			// 获取uuid
			getUUID () {
				return new Date().getTime();
			},
			// 返回
			back() {
				this.$router.go(-1);
			},
			imgurlUploadChange(fileUrls) {
				this.ruleForm.imgurl = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
			},
		}
	};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.add-update-preview {
		padding: 20px 10% 40px;
		margin: 10px auto;
		background: none;
		width: 100%;
		position: relative;
		.add-update-form {
			border: 0px solid #eee;
			border-radius: 10px;
			padding: 40px 20% 20px 10%;
			background: none;
			width: 100%;
			position: relative;
			.add-item.el-form-item {
				border: 1px solid #707070;
				padding: 0;
				margin: 0 0 24px;
				background: none;
				/deep/ .el-form-item__label {
					padding: 0 0px 0 10px;
					color: #333;
					white-space: nowrap;
					font-weight: 500;
					width: 200px;
					font-size: 16px;
					line-height: 40px;
					text-align: left;
				}
				/deep/ .el-form-item__content {
					margin-left: 200px;
				}
				.el-input {
					width: 100%;
				}
				.el-input /deep/ .el-input__inner {
					border: 0px solid #eee;
					border-radius: 0px;
					padding: 0 12px;
					box-shadow: none;
					outline: none;
					color: #666;
					background: none;
					width: 100%;
					font-size: 16px;
					height: 40px;
				}
				.el-input /deep/ .el-input__inner[readonly="readonly"] {
					border: 0;
					cursor: not-allowed;
					border-radius: 4px;
					padding: 0 12px;
					box-shadow: none;
					outline: none;
					color: #999;
					background: none;
					width: 100%;
					font-size: 16px;
					height: 40px;
				}
				.el-input-number /deep/ .el-input__inner {
					text-align: left;
					border: 0px solid #eee;
					border-radius: 0px;
					padding: 0 12px;
					box-shadow: none;
					outline: none;
					color: #666;
					background: none;
					width: 100%;
					font-size: 16px;
					height: 40px;
				}
				.el-input-number /deep/ .is-disabled .el-input__inner {
					text-align: left;
					border: 0;
					cursor: not-allowed;
					border-radius: 4px;
					padding: 0 12px;
					box-shadow: none;
					outline: none;
					color: #999;
					background: none;
					width: 100%;
					font-size: 16px;
					height: 40px;
				}
				.el-input-number /deep/ .el-input-number__decrease {
					display: none;
				}
				.el-input-number /deep/ .el-input-number__increase {
					display: none;
				}
				.el-select {
					width: 100%;
				}
				.el-select /deep/ .el-input__inner {
					border: 0px solid #eee;
					border-radius: 0px;
					padding: 0 10px;
					box-shadow: none;
					outline: none;
					color: rgba(64, 158, 255, 1);
					background: none;
					width: 100%;
					font-size: 14px;
					height: 40px;
				}
				.el-select /deep/ .is-disabled .el-input__inner {
					border: 0;
					cursor: not-allowed;
					border-radius: 4px;
					padding: 0 10px;
					box-shadow: none;
					outline: none;
					color: #999;
					background: none;
					width: 100%;
					font-size: 14px;
					height: 40px;
				}
				.el-date-editor {
					width: 100%;
				}
				.el-date-editor /deep/ .el-input__inner {
					border: 0px solid #eee;
					border-radius: 0px;
					padding: 0 10px 0 30px;
					box-shadow: none;
					outline: none;
					color: #666;
					background: none;
					width: 100%;
					font-size: 16px;
					height: 40px;
				}
				.el-date-editor /deep/ .el-input__inner[readonly="readonly"] {
					border: 0;
					cursor: not-allowed;
					border-radius: 4px;
					padding: 0 10px 0 30px;
					box-shadow: none;
					outline: none;
					color: #999;
					background: none;
					width: 100%;
					font-size: 16px;
					height: 40px;
				}
				/deep/ .el-upload--picture-card {
					background: transparent;
					border: 0;
					border-radius: 0;
					width: auto;
					height: auto;
					line-height: initial;
					vertical-align: middle;
				}
				/deep/ .upload .upload-img {
					border: 1px solid #eee;
					cursor: pointer;
					border-radius: 0px;
					color: #999;
					width: 80px;
					font-size: 26px;
					line-height: 80px;
					text-align: center;
					height: 80px;
				}
				/deep/ .el-upload-list .el-upload-list__item {
					border: 1px solid #eee;
					cursor: pointer;
					border-radius: 0px;
					color: #999;
					width: 80px;
					font-size: 26px;
					line-height: 80px;
					text-align: center;
					height: 80px;
					font-size: 14px;
					line-height: 1.8;
				}
				/deep/ .el-upload .el-icon-plus {
					border: 1px solid #eee;
					cursor: pointer;
					border-radius: 0px;
					color: #999;
					width: 80px;
					font-size: 26px;
					line-height: 80px;
					text-align: center;
					height: 80px;
				}
				/deep/ .el-upload__tip {
					color: #666;
					font-size: 16px;
				}
				.el-textarea /deep/ .el-textarea__inner {
					border: 0px solid #eee;
					border-radius: 0px;
					padding: 12px;
					box-shadow: none;
					outline: none;
					color: #666;
					background: none;
					width: 100%;
					font-size: 16px;
					height: auto;
				}
				.el-textarea /deep/ .el-textarea__inner[readonly="readonly"] {
					border: 0;
					cursor: not-allowed;
					border-radius: 4px;
					padding: 12px;
					box-shadow: none;
					outline: none;
					color: #999;
					background: none;
					width: 100%;
					font-size: 16px;
					height: auto;
				}
				/deep/ .el-input__inner::placeholder {
					color: #123;
					font-size: 16px;
				}
				/deep/ textarea::placeholder {
					color: #123;
					font-size: 16px;
				}
				.editor {
					background-color: none;
					border-radius: 0;
					padding: 0;
					box-shadow: none;
					margin: 0;
					width: 100%;
					border-color: #ccc;
					border-width: 0;
					border-style: solid;
					height: auto;
				}
				.editor /deep/.ql-toolbar {
					border: 0px solid #eee;
					background: none;
					border-width: 0px 0px 0;
				}
				.editor /deep/.ql-container {
					border: 0px solid #eee;
					background: none;
					min-height: 180px;
				}
				.editor /deep/.ql-container .ql-blank::before {
					color: #999;
					background: none;
				}
				.upload-img {
					object-fit: cover;
					width: 120px;
					height: 120px;
				}
				.viewBtn {
					border: 0;
					cursor: pointer;
					padding: 0 20px;
					margin: 10px;
					color: #fff;
					display: inline-block;
					font-size: 14px;
					line-height: 34px;
					border-radius: 4px;
					outline: none;
					background: #ABDE53;
					width: auto;
					height: 34px;
				}
				.viewBtn:hover {
					opacity: 0.7;
				}
				.unviewBtn {
					border: 0;
					cursor: pointer;
					padding: 0 20px;
					margin: 10px;
					color: #666;
					display: inline-block;
					font-size: 14px;
					line-height: 34px;
					border-radius: 4px;
					outline: none;
					background: #ABDE53;
					width: auto;
					height: 34px;
				}
				.unviewBtn:hover {
					opacity: 0.8;
				}
			}
			.add-btn-item {
				padding: 0;
				margin: 20px auto;
				width: 100%;
				text-align: center;
				.submitBtn {
					border: 0;
					cursor: pointer;
					border-radius: 20px;
					padding: 0 20px;
					margin: 0 20px 0 0;
					outline: none;
					background: #ABDE53;
					display: inline-block;
					width: auto;
					font-size: 14px;
					line-height: 40px;
					height: 40px;
					.icon {
						color: rgba(255, 255, 255, 1);
					}
					.text {
						color: rgba(255, 255, 255, 1);
						font-size: 16px;
					}
				}
				.submitBtn:hover {
					opacity: 0.7;
					.icon {
						color: #fff;
					}
					.text {
						color: #fff;
					}
				}
				.closeBtn {
					border: 0px solid #ff000020;
					cursor: pointer;
					padding: 0 15px 0 10px;
					margin: 0 20px 0 0;
					display: inline-block;
					font-size: 16px;
					line-height: 40px;
					border-radius: 20px;
					outline: none;
					background: #ABDE53;
					width: auto;
					min-width: 120px;
					height: 40px;
					.icon {
						color: #FFF;
						font-size: 18px;
					}
					.text {
						color: #FFF;
						font-size: 16px;
					}
				}
				.closeBtn:hover {
					opacity: 0.7;
					.icon {
					}
					.text {
					}
				}
			}
		}
	}
	.el-date-editor.el-input {
		width: auto;
	}
</style>
