<template>
	<div>
		<div class="breadcrumb-preview">
			<el-breadcrumb :separator="'-'">
				<el-breadcrumb-item class="item1" to="/"><a>首页</a></el-breadcrumb-item>
				<el-breadcrumb-item class="item2" v-for="(item, index) in breadcrumbItem" :key="index"><a>{{item.name}}</a></el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div v-if="centerType " class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">
				<span class="icon iconfont icon-fanhui12"></span>
				<span class="text">返回</span>
			</el-button>
		</div>
		<div class="list-preview">
			<el-form :inline="true" :model="formSearch" class="list-form-pv">
				<el-form-item class="list-item" >
					<div class="lable">歌曲名称：</div>
					<el-input v-model="formSearch.songname" placeholder="歌曲名称" @keydown.enter.native="getList(1, curFenlei)" clearable></el-input>
				</el-form-item>
				<div class="list-btn-box">
					<el-button class="list-search-btn" v-if=" true " type="primary" @click="getList(1, curFenlei)">
						<span class="icon iconfont icon-fangdajing07"></span>
						搜索
					</el-button>
					<el-button class="list-add-btn" v-if="btnAuth('musicinfoforecast','新增')" type="primary" @click="add('/index/musicinfoforecastAdd')">
						<span class="icon iconfont icon-tianjia7"></span>
						新增
					</el-button>
					<el-button v-if="btnAuth('musicinfoforecast','预测')" class="list-forecastImg-btn" type="success" @click="forecastImgClick()">
						<span class="icon iconfont icon-xiaoliang6"></span>
						 预测  图表
					</el-button>
  
				</div>
			</el-form>
			<div class="list">
				<div class="list5">
					<div v-for="(item,index) in dataList" :key="index" class="list-item" @click.stop="toDetail(item)" >
						<div class="imgbox">
						</div>
						<div class="infoBox">
							<div class="name">{{item.songname}}</div>
							<div class="name">{{item.songstyle}}</div>
							<div class="bottomInfo">
								<div class="time_item">
									<span class="icon iconfont icon-shijian21"></span>
									<span class="label">发布时间：</span>
									<span class="text">{{item.addtime.split(' ')[0]}}</span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

	
			<el-pagination
				background
				id="pagination"
				class="pagination"
				:pager-count="7"
				:page-size="pageSize"
				prev-text="<"
				next-text=">"
				:hide-on-single-page="true"
				:layout='["total","prev","pager","next","sizes","jumper"].join()'
				:total="total"
				:page-sizes="pageSizes"
				@current-change="curChange"
				@size-change="sizeChange"
				@prev-click="prevClick"
				@next-click="nextClick"
				></el-pagination>
		</div>
		<el-dialog title="预览图" :visible.sync="previewVisible" width="50%">
			<img :src="previewImg" alt="" style="width: 100%;">
		</el-dialog>
		<el-dialog title="可视化图表" :visible.sync="forecastVisible" width="50%">
			<div style="display: flex;flex-wrap:wrap">
				<el-image v-for="item in forecastImgList" :key="item" :src="baseUrl + item" lazy></el-image>
			</div>
		</el-dialog>
	</div>
</template>
<script>
	import axios from 'axios';
	import {
		Loading
	} from 'element-ui';
	export default {
		//数据集合
		data() {
			return {
				layouts: '',
				swiperIndex: -1,
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '歌曲热度预测'
					}
				],
				formSearch: {
					songname: '',
				},
				fenlei: [],
				dataList: [],
				total: 1,
				pageSize: 10,
				pageSizes: [],
				totalPage: 1,
				curFenlei: '全部',
				isPlain: false,
				indexQueryCondition: '',
				timeRange: [],
				centerType:false,
				previewImg: '',
				previewVisible: false,
				sortType: 'id',
				sortOrder: 'desc',
				forecastVisible: false,
				forecastImgList: [],
			}
		},
		async created() {
			if(this.$route.query.centerType&&this.$route.query.centerType!=0){
				this.centerType = true
			}
			this.baseUrl = this.$config.baseUrl;
			if(this.centerType) {
			}
			await this.getFenlei();
			this.getList(1, '全部');
		},
		watch:{
			$route(newValue){
				this.getList(1, newValue.query.homeFenlei);
			}
		},
		computed: {
			role(){
				return localStorage.getItem('frontRole');
			},
			username() {
				return localStorage.getItem('username')
			}
		},
		//方法集合
		methods: {
			queryChange(arr){
				for(let x in arr) {
					if(arr[x] == this.role) {
						return true
					}
				}
				return false
			},
			add(path) {
				let query = {}
				if(this.centerType){
					query.centerType = 1
				}
				this.$router.push({path: path,query:query});
			},
			async getFenlei() {
			},
			getList(page, fenlei, ref = '') {
				let params = {
					page,
					limit: this.pageSize,
				};
				let searchWhere = {};
				if (this.formSearch.songname != ''&&this.formSearch.songname != undefined) searchWhere.songname = '%' + this.formSearch.songname + '%';
				let user = JSON.parse(localStorage.getItem('sessionForm'))
				if (this.sortType) searchWhere.sort = this.sortType
				if (this.sortOrder) searchWhere.order = this.sortOrder
				this.$http.get(`musicinfoforecast/${this.centerType?'page':'list'}`, {params: Object.assign(params, searchWhere)}).then(async res => {
					if (res.data.code == 0) {
						this.dataList = res.data.data.list;
						this.total = Number(res.data.data.total);
						this.pageSize = Number(res.data.data.pageSize);
						this.totalPage = res.data.data.totalPage;
						if(this.pageSizes.length==0){
							this.pageSizes = [this.pageSize, this.pageSize*2, this.pageSize*3, this.pageSize*5];
						}
					}
				});
			},
			curChange(page) {
				this.getList(page);
			},
			prevClick(page) {
				this.getList(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getList(1);
			},
			nextClick(page) {
				this.getList(page);
			},
			imgPreView(url){
				this.previewImg = url
				this.previewVisible = true
			},
			toDetail(item) {
				let params = {
					id: item.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/musicinfoforecastDetail', query: params});
			},
			btnAuth(tableName,key){
				if(this.centerType){
					return this.isBackAuth(tableName,key)
				}else{
					return this.isAuth(tableName,key)
				}
			},
			backClick() {
				this.$router.push({path: '/index/center'});
			},
			forecastImgClick(){
				this.forecastImgList = []
				let loading = null
				loading = Loading.service({
					target: this.$refs['roleMenuBox'],
					fullscreen: false,
					text: '图表生成中...'
				})
				this.$http.get('musicinfoforecast/forecastimgs').then(res=>{
					if (loading) loading.close()
					if(res.data&&res.data.code==0){
						if(res.data.data) {
							let arr = []
							arr = JSON.parse(JSON.stringify(res.data.data))
							this.$message({
								message: "操作成功！",
								type: "success",
								duration: 1500,
								onClose: () => {
									this.forecastImgList = arr
									this.forecastVisible = true
									this.$forceUpdate()
								}
							});
						}else {
							this.$message({
								message: "请先完成预测！",
								type: "error",
								duration: 1500
							});
						}
					}else {
						this.$message({
							message: "请先完成预测！",
							type: "error",
							duration: 1500
						});
					}
				},err=>{
					if (loading) loading.close()
					this.$message({
						message: "请先完成预测！",
						type: "error",
						duration: 1500
					});
				})
			},

			chapterClick (row){
				let params = {
					refid: row.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/chaptermusicinfoforecast', query: params});
			},
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.list-preview {
		padding: 0 10%;
		margin: 0px auto;
		align-content: flex-start;
		background: #F2F2F2;
		display: flex;
		width: 100%;
		align-items: flex-start;
		position: relative;
		flex-wrap: wrap;
		.list-form-pv {
			padding: 30px 0;
			margin: 20px auto;
			background: url(http://codegen.caihongy.cn/20251216/36e52c1d98044722ab9c9270207179e6.png) no-repeat center/100% 100%;
			display: flex;
			width: 100%;
			border-color: #ddd;
			border-width: 0px;
			justify-content: center;
			align-items: center;
			border-style: solid;
			flex-wrap: wrap;
			height: auto;
			.list-item {
				margin: 0 5px 0 0;
				/deep/.el-form-item__content {
					padding: 5px;
					background: #FFF;
					display: flex;
					border-color: #707070;
					border-width: 0 0 1px;
					border-style: solid;
				}
				.lable {
					padding: 0;
					color: #333;
					white-space: nowrap;
					display: inline-block;
					width: auto;
					line-height: 42px;
				}
				.el-input {
					width: 100%;
				}
				.datetimerange {
					border: 0px solid #ddd;
					border-radius: 2px;
					padding: 3px 0px;
					outline: none;
					background: #fff;
					width: auto;
					justify-content: center;
				}
				.el-input /deep/ .el-input__inner {
					border: none;
					border-radius: 2px;
					padding: 0 10px;
					margin: 0;
					outline: none;
					color: #333;
					background: none;
					width: 140px;
					font-size: 14px;
					line-height: 42px;
					height: 42px;
				}
				.el-select {
					width: 100%;
				}
				.el-select /deep/ .el-input__inner {
					border: 0px solid #ddd;
					border-radius: 2px;
					padding: 0 10px;
					margin: 0;
					outline: none;
					color: #333;
					background: none;
					width: 140px;
					font-size: 14px;
					line-height: 42px;
					height: 42px;
				}
				.el-date-editor {
					width: 100%;
				}
				.el-date-editor /deep/ .el-input__inner {
					border: 0px solid #ddd;
					border-radius: 2px;
					padding: 0 30px;
					margin: 0;
					outline: none;
					color: #333;
					background: none;
					width: 140px;
					font-size: 14px;
					line-height: 42px;
					height: 42px;
				}
			}
			.list-btn-box {
				margin: 20px 0;
				display: flex;
				flex-wrap: wrap;
			}
			.list-search-btn {
				cursor: pointer;
				border: 0;
				border-radius: 20px;
				padding: 0px 20px;
				margin: 0 10px 10px 0;
				outline: none;
				color: #fff;
				background: #ABDE53;
				width: auto;
				font-size: 15px;
				line-height: 38px;
				height: 38px;
				.icon {
					margin: 0 3px 0 0;
					color: #fff;
					font-size: 14px;
				}
			}
			.list-add-btn {
				cursor: pointer;
				border: 0;
				border-radius: 20px;
				padding: 0px 20px;
				margin: 0 10px 10px 0;
				outline: none;
				color: #fff;
				background: #ABDE53;
				width: auto;
				font-size: 15px;
				line-height: 38px;
				height: 38px;
				.icon {
					margin: 0 3px 0 0;
					color: #FFF;
					font-size: 14px;
				}
			}
			.list-forecastImg-btn {
				cursor: pointer;
				border: 0;
				border-radius: 20px;
				padding: 0px 20px;
				margin: 0 10px 10px 0;
				outline: none;
				color: #fff;
				background: #ABDE53;
				width: auto;
				font-size: 15px;
				line-height: 38px;
				height: 38px;
				.icon {
					margin: 0 10px 0 0;
					color: #fff;
					font-size: 14px;
				}
			}
		}
		.list {
			margin: 20px 0 0;
			background: none;
			flex: 1;
			width: 100%;
			order: 4;
			.index-pv1 .animation-box {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				z-index: initial;
			}
				
			.index-pv1 .animation-box:hover {
				transform: rotate(0) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
				z-index: 1;
			}
				
			.index-pv1 .animation-box img {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
			}
			
			.index-pv1 .animation-box img:hover {
				transform: rotate(0) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
			}
			.list5 {
				margin: 0px auto 20px -10px;
				color: #999;
				display: flex;
				width: calc(100% + 20px);
				font-size: 14px;
				flex-wrap: wrap;
				.list-item {
					border: 0px solid #eee;
					border-radius: 14px;
					padding: 0px;
					margin: 0 10px 20px;
					overflow: hidden;
					background: #fff;
					display: block;
					width: calc(20% - 20px);
					position: relative;
					.imgbox {
						padding: 20px;
						overflow: hidden;
						width: auto;
						.image {
							filter: saturate(150%);
							transform: rotate(0deg);
							margin: 0 0 5px;
							object-fit: cover;
							display: block;
							width: 100%;
							opacity: 0.9;
							height: 210px;
						}
					}
					.infoBox {
						padding: 20px ;
						left: 0px;
						bottom: 0;
						background: none;
						width: 100%;
						font-size: 14px;
						position: inherit;
						transition: all 0.5s;
						.name {
							margin: 0 0 10px;
							overflow: hidden;
							color: #000;
							white-space: nowrap;
							width: 100%;
							font-size: 18px;
							line-height: 24px;
							text-overflow: ellipsis;
							text-align: center;
						}
						.price {
							color: #000000;
							width: 100%;
							font-size: 30px;
							text-align: left;
							.price_text {
								color: #000000;
								font-size: 30px;
							}
						}
						.bottomInfo {
							display: flex;
							justify-content: center;
							flex-wrap: wrap;
							.time_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.publisher_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.like_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.collect_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
							.view_item {
								padding: 0;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									line-height: 1.5;
								}
								.text {
									line-height: 1.5;
								}
							}
						}
					}
				}
				.list-item:hover {
					cursor: pointer;
					.imgbox {
						.image {
							transform: scale(1.05);
							ilter: saturate(100%);
							opacity: 1;
							transition: all 200ms linear;
						}
					}
					.infoBox {
						bottom: 0px;
						background: #FFFFFF;
						font-size: 14px;
						.name {
						}
						.price {
							.price_text {
							}
						}
						.bottomInfo {
							display: flex;
							justify-content: center;
							flex-wrap: wrap;
							.time_item {
								.icon {
								}
								.label {
								}
								.text {
								}
							}
							.publisher_item {
								.icon {
								}
								.label {
								}
								.text {
								}
							}
							.like_item {
								.icon {
								}
								.label {
								}
								.text {
								}
							}
							.collect_item {
								.icon {
								}
								.label {
								}
								.text {
								}
							}
							.view_item {
								.icon {
								}
								.label {
								}
								.text {
								}
							}
						}
					}
				}
			}
		}
	}
</style>
