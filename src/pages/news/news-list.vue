<template>
	<div>
		<div class="breadcrumb-preview">
			<el-breadcrumb :separator="'-'">
				<el-breadcrumb-item class="item1" to="/"><a>首页</a></el-breadcrumb-item>
				<el-breadcrumb-item class="item2" v-for="(item, index) in breadcrumbItem" :key="index"><a>{{item.name}}</a></el-breadcrumb-item>
			</el-breadcrumb>
		</div>
	
		<div class="news-preview-pv">
			<el-form :inline="true" :model="formSearch" class="list-form-pv">
				<el-form-item class="search-item">
					<el-input v-model="title" placeholder="标题"></el-input>
				</el-form-item>
				<el-button class="search-btn" type="primary" @click="getNewsList(1)">
					<span class="icon iconfont icon-chakan14"></span>
					搜索
				</el-button>
			</el-form>
			
			<!-- category -->
			<div v-if="newsList.length" class="list8 index-pv1">
				<div class="list-body-top">
					<div class="list-item1" @click="toNewsDetail(newsList[0])">
						<img :src="baseUrl + (newsList[0].picture?newsList[0].picture.split(',')[0]:'')">
						<div class="infoBox">
							<div class="name">{{newsList[0].title}}</div>
							<div class="desc">{{newsList[0].introduction}}</div>
							<div class="time">{{newsList[0].addtime.split(' ')[0]}}</div>
						</div>
					</div>
					<div class="list-body-right" v-if="newsList.length > 1">
						<div class="list-item" v-for="item,index in newsList" v-if="index > 0 && index < 5" @click="toNewsDetail(item)">
							<div class="time_item">
								<div class="day">{{item.addtime.split(" ")[0].split("-")[2]}}</div>
								<div class="year">{{item.addtime.split(" ")[0].split("-")[0] + '-' + item.addtime.split(" ")[0].split("-")[1]}}</div>
							</div>
							<div class="infoBox">
								<div class="name">{{item.title}}</div>
								<div class="desc">{{item.introduction}}</div>
								<span class="icon iconfont icon-gengduo1"></span>
							</div>
						</div>
					</div>
				</div>
				<div class="list-body" v-if="newsList.length > 4">
					<div class="list-item" v-for="item,index in newsList" v-if="index > 4" @click="toNewsDetail(item)">
						<div class="name">{{item.title}}</div>
						<div class="time">{{item.addtime.split(" ")[0]}}</div>
					</div>
				</div>
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
				@current-change="curChange"
				@size-change="sizeChange"
				@prev-click="prevClick"
				@next-click="nextClick"
				></el-pagination>
		</div>
	</div>
</template>

<script>
	export default {
		//数据集合
		data() {
			return {
				baseUrl: this.$config.baseUrl,
				breadcrumbItem: [
				  {
					name: '公告信息'
				  }
				],
				newsList: [],
				total: 1,
				pageSize: 10,
				pageSizes: [],
				totalPage: 1,
				layouts: '',
				title: '',
			}
		},
		created() {
			this.getNewsList(1);
		},
		//方法集合
		methods: {
			getNewsList(page) {
				let params = {page, limit: this.pageSize,sort:'addtime',order:'desc'};
				let searchWhere = {};
				if(this.title != '') searchWhere.title = '%' + this.title + '%';
				this.$http.get('news/list', {params: Object.assign(params, searchWhere)}).then(res => {
					if (res.data.code == 0) {
						this.newsList = res.data.data.list;
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
				this.getNewsList(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getNewsList(1);
			},
			prevClick(page) {
				this.getNewsList(page);
			},
			nextClick(page) {
				this.getNewsList(page);
			},
			toNewsDetail(item) {
				this.$router.push({path: '/index/newsDetail', query: {id: item.id}});
			}
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.news-preview-pv {
				padding: 0 10%;
				margin: 0px auto;
				align-content: flex-start;
				display: flex;
				width: 100%;
				align-items: flex-start;
				position: relative;
				flex-wrap: wrap;
				.list-form-pv {
						padding: 10px;
						background: none;
						display: flex;
						width: 100%;
						justify-content: center;
						align-items: center;
						flex-wrap: wrap;
						height: auto;
						.search-item {
								margin: 0 10px;
								.el-input {
										width: 100%;
									}
				.el-input /deep/ .el-input__inner {
										border: 1px solid #ddd;
										border-radius: 4px;
										padding: 0 10px;
										margin: 0;
										outline: none;
										color: #333;
										width: 500px;
										font-size: 16px;
										line-height: 42px;
										height: 42px;
									}
			}
			.search-btn {
								cursor: pointer;
								border: 0;
								border-radius: 30px;
								padding: 0px 15px;
								margin: 0 10px 0 0;
								outline: none;
								color: #fff;
								background: #ABDE53;
								width: auto;
								font-size: 16px;
								line-height: 42px;
								height: 42px;
								.icon {
										margin: 0 3px 0 0;
										color: #fff;
										font-size: 16px;
									}
			}
		}
		.category-list {
						border: 0px solid #eee;
						padding: 0px 0 20px;
						margin: 20px 30px 0 0;
						background: #F2F2F2;
						display: flex;
						width: 299px;
						justify-content: center;
						flex-wrap: wrap;
						height: auto;
						order: 3;
						.item {
								cursor: pointer;
								padding: 5px 10px;
								margin: 10px auto 0;
								color: #333;
								font-size: 16px;
								border-color: #efefef;
								line-height: 50px;
								background: #fff;
								width: 88%;
								border-width: 0 0 0px 0;
								border-style: solid;
								text-align: center;
								height: auto;
							}
			
			.item:hover {
								color: #fff;
								background: #BFF267;
							}
			
			.item.active {
								padding: 5px 10px;
								margin: 10px auto 0;
								color: #fff;
								background: #BFF267;
								width: 88%;
							}
		}
		.list8 {
						padding: 20px;
						background: url(http://codegen.caihongy.cn/20251216/4ad7a6ab37d44f85907c7a012f46bedf.png) no-repeat center /100% 100%;
						width: calc(100% - 350px);
						height: auto;
						order: 4;
						.list-body-top {
								display: flex;
								width: 100%;
								justify-content: space-between;
								height: auto;
								.list-item1 {
										cursor: pointer;
										width: 45%;
										position: relative;
										height: auto;
										order: -1;
										img {
												padding: 20px;
												background: #030203;
												object-fit: cover;
												display: block;
												width: 100%;
												height: 400px;
											}
					.infoBox {
												padding: 10px;
												z-index: 9;
												background: #BFF267;
												width: 100%;
												.name {
														overflow: hidden;
														color: #000;
														white-space: nowrap;
														font-weight: 600;
														width: 100%;
														font-size: 15px;
														line-height: 32px;
														text-overflow: ellipsis;
													}
						.desc {
														max-height: 48px;
														overflow: hidden;
														color: #000;
														width: 100%;
														font-size: 14px;
														line-height: 24px;
													}
						.time {
														color: #000;
														width: 100%;
														font-size: 14px;
														line-height: 1.5;
														text-align: left;
													}
					}
				}
				.list-body-right {
										padding: 0 0 0 0px;
										width: 50%;
										height: auto;
										.list-item {
												cursor: pointer;
												padding: 0 10px 0 0;
												margin: 0 0 10px;
												background: #F2F2F2;
												display: flex;
												width: 100%;
												border-color: #efefef;
												border-width: 0 0 1px;
												justify-content: center;
												align-items: center;
												border-style: solid;
												height: 100px;
												.time_item {
														border: 0px solid #efefef;
														padding: 10px 0;
														margin: 0 0px 0 0;
														flex-direction: column;
														background: #BFF267;
														display: flex;
														width: 100px;
														justify-content: center;
														align-items: center;
														height: 100%;
														.day {
																color: #333;
																font-size: 20px;
																line-height: 1.5;
															}
							.year {
																color: #333;
																font-size: 14px;
																line-height: 1.5;
															}
						}
						.infoBox {
														padding: 10px 10px 0;
														background: url(http://codegen.caihongy.cn/20251216/24c9c6fb66304d18be6272e05441abba.png) no-repeat center /100% 100%;
														flex: 1;
														height: 100%;
														.name {
																overflow: hidden;
																color: #FFF;
																white-space: nowrap;
																font-weight: 600;
																width: 100%;
																font-size: 15px;
																line-height: 32px;
																text-overflow: ellipsis;
															}
							.desc {
																max-height: 48px;
																overflow: hidden;
																color: #FFF;
																width: 100%;
																font-size: 14px;
																line-height: 24px;
															}
							.icon {
																color: #999;
																display: none;
																font-size: 14px;
																line-height: 20px;
																float: right;
															}
						}
					}
				}
			}
			.list-body {
								margin: 20px 0 0 0;
								display: flex;
								width: 100%;
								flex-wrap: wrap;
								height: auto;
								.list-item {
										cursor: pointer;
										padding: 20px 10px;
										margin: 0 0px 10px 0px;
										flex-direction: column;
										background: url(http://codegen.caihongy.cn/20251216/24c9c6fb66304d18be6272e05441abba.png) no-repeat center /100% 100%;
										display: flex;
										width: 100%;
										border-color: #efefef;
										border-width: 0 0 1px;
										justify-content: space-between;
										border-style: solid;
										.name {
												overflow: hidden;
												color: #FFF;
												white-space: nowrap;
												flex: 1;
												font-weight: 500;
												width: 100%;
												font-size: 15px;
												line-height: 32px;
												text-overflow: ellipsis;
											}
					.time {
												padding: 0 0 0 30px;
												color: #BFF267;
												font-size: 14px;
												line-height: 40px;
												text-align: right;
											}
				}
			}
		}
	}
	
	.index-pv1 .animation-box {
		transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
		z-index: initial;
	}
	
	.index-pv1 .animation-box:hover {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(6px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
				z-index: 1;
	}
	
	.index-pv1 .animation-box img {
		transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
	}
	
	.index-pv1 .animation-box img:hover {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
			}
</style>
