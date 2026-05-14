<template>
	<div class="home-preview">




		<!-- 新闻资讯 -->
		<div id="animate_newsnews" class="news animate__animated">
			<div class="news_title_box">
				<span class="news_title">公告信息</span>
				<span class="news_subhead">{{'news'.toUpperCase()}}</span>
			</div>
			<div class="list list30 index-pv1">
				<div class="list30-div">
					<div class="list-body-left">
						<div class="list-item1" v-if="newsList.length" @click="toDetail('newsDetail', newsList[0])">
							<div class="img">
								<img :src="baseUrl + (newsList[0].picture?newsList[0].picture.split(',')[0]:'')">
							</div>
							<div class="infoBox">
								<div class="name">{{newsList[0].title}}</div>
								<div class="time-item">date：{{newsList[0].addtime}}</div>
							</div>
						</div>
						<div class="list-item2" v-if="newsList.length>1" @click="toDetail('newsDetail', newsList[1])">
							<div class="img">
								<img :src="baseUrl + (newsList[1].picture?newsList[1].picture.split(',')[0]:'')">
							</div>
							<div class="infoBox">
								<div class="name">{{newsList[1].title}}</div>
								<div class="time-item">date：{{newsList[1].addtime}}</div>
							</div>
						</div>
					</div>
					<div class="list-body-right">
						<div class="list-item" v-for="(item,index) in newsList" :key="index" @click="toDetail('newsDetail', item)" v-if="index>1&&index<(Number(3) + 2)">
							<div class="date-box">
								<div class="text">Day</div>
								<div class="day">{{item.addtime}}</div>
							</div>
							<div class="infoBox">
								<div class="name">{{item.title}}</div>
								<div class="desc">{{item.introduction}}</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="moreBtn" @click="moreBtn('news')">
				<span class="text">查看更多</span>
				<i class="icon iconfont icon-jiantou25"></i>
			</div>
		</div>
		<!-- 新闻资讯 -->
		<!-- 商品推荐 -->
		<div id="animate_recommendmusicinfo" class="recommend animate__animated">
			<div class="recommend_title_box">
				<span class="recommend_title">音乐信息推荐</span>
				<span class="recommend_subhead">{{'musicinfo'.toUpperCase()}} RECOMMEND</span>
			</div>
			<!-- 样式二 -->
			<div class="list list2 index-pv1">
				<div v-for="(item,index) in musicinfoRecommend" class="list-item animation-box" :key="index" @click="toDetail('musicinfoDetail', item)">
					<img v-if="preHttp(item.imgurl)&&preHttp2(item.imgurl)" :src="item.imgurl" alt="" />
					<img v-else-if="preHttp(item.imgurl)" :src="item.imgurl.split(',')[0]" alt="" />
					<img v-else :src="baseUrl + (item.imgurl?item.imgurl.split(',')[0]:'')" alt="" />
					<div class="item-info">
						<div class="name line1">{{item.songname}}</div>
						<div class="name line1">{{item.songstyle}}</div>
						<div class="name line1">{{item.singer}}</div>
						<div class="name line1">{{item.albumtitle}}</div>
						<div class="time_item">
							<span class="icon iconfont icon-shijian21"></span>
							<span class="label">发布时间：</span>
							<span class="text">{{item.addtime.split(' ')[0]}}</span>
						</div>
						<div class="collect_item">
							<span class="icon iconfont icon-shoucang10"></span>
							<span class="label">收藏量：</span>
							<span class="text">{{item.storeupnum}}</span>
						</div>
					</div>
				</div>
			</div>
			<div class="moreBtn" @click="moreBtn('musicinfo')">
				<span class="text">查看更多</span>
				<i class="icon iconfont icon-gengduo1"></i>
			</div>
		</div>
		<!-- 商品推荐 -->
	</div>
</template>

<script>
import 'animate.css'
import Swiper from "swiper";

	export default {
		//数据集合
		data() {
			return {
				baseUrl: '',
				newsList: [],
				musicinfoRecommend: [],





			}
		},
		created() {
			this.baseUrl = this.$config.baseUrl;
			this.getNewsList();
			this.getList();
		},
		mounted() {
			window.addEventListener('scroll', this.handleScroll)
			setTimeout(()=>{
				this.handleScroll()
			},100)
			
			this.swiperChanges()
		},
		beforeDestroy() {
			window.removeEventListener('scroll', this.handleScroll)
		},
		computed: {
			username() {
				return localStorage.getItem('username')
			}
		},
		//方法集合
		methods: {
			swiperChanges() {
				setTimeout(()=>{
				},750)
			},


			handleScroll() {
				let arr = [
					{id:'about',css:'animate__'},
					{id:'system',css:'animate__'},
					{id:'animate_recommendmusicinfo',css:'animate__'},
					{id:'animate_newsnews',css:'animate__'},
				]
			
				for (let i in arr) {
					let doc = document.getElementById(arr[i].id)
					if (doc) {
						let top = doc.offsetTop
						let win_top = window.innerHeight + window.pageYOffset
						// console.log(top,win_top)
						if (win_top > top && doc.classList.value.indexOf(arr[i].css) < 0) {
							// console.log(doc)
							doc.classList.add(arr[i].css)
						}
					}
				}
			},
			preHttp(str) {
				return str && str.substr(0,4)=='http';
			},
			preHttp2(str) {
				return str && str.split(',w').length>1;
			},
			getNewsList() {
				let data = {
					page: 1,
					limit: 5,
					sort: 'addtime',
					order: 'desc'
				}
				this.$http.get('news/list', {params: data}).then(res => {
					if (res.data.code == 0) {
						this.newsList = res.data.data.list;
					
					}
				});
			},
			getList() {
				let autoSortUrl = "";
				let data = {}
				autoSortUrl = "musicinfo/autoSort";
				if(localStorage.getItem('frontToken')) {
					autoSortUrl = "musicinfo/autoSort2";
				}
				data = {
					page: 1,
					limit: 6,
				}
				this.$http.get(autoSortUrl, {params: data}).then(res => {
					if (res.data.code == 0) {
						this.musicinfoRecommend = res.data.data.list;
					}
				});
			
			},
			toDetail(path, item) {
				this.$router.push({path: '/index/' + path, query: {id: item.id, storeupType: 1}});
			},
			moreBtn(path) {
				this.$router.push({path: '/index/' + path});
			}
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.home-preview {
		margin: 0 auto;
		overflow: hidden;
		display: flex;
		width: 100%;
		justify-content: space-between;
		flex-wrap: wrap;
		.news {
			padding: 0px 11% 40px;
			margin: 50px auto;
			background: url(http://codegen.caihongy.cn/20251216/7eb35595cc24437fbf941d62418032dd.png) no-repeat center /80% 100%;
			width: 100%;
			position: relative;
			order: 12;
			.news_title_box {
				margin: 20px auto;
				display: flex;
				width: 100%;
				flex-wrap: wrap;
				.news_title {
					padding: 0;
					color: #BFF267;
					background: none;
					font-weight: 600;
					display: block;
					width: 100%;
					font-size: 30px;
					line-height: 1.5;
					text-align: center;
					order: 2;
				}
				.news_subhead {
					margin: 0;
					color: #FFFFFF;
					font-weight: 500;
					display: block;
					width: 100%;
					font-size: 22px;
					line-height: 2;
					text-align: center;
					order: 2;
				}
			}
			.index-pv1 .animation-box:hover {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
				z-index: 1;
			}
			.index-pv1 .animation-box img:hover {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
			}
			.list30 {
				padding: 20px 0;
				overflow: hidden;
				clear: both;
				width: 100%;
				.list30-div {
					padding: 0;
					margin: 0 auto;
					overflow: hidden;
					width: 100%;
					clear: both;
					.list-body-left {
						margin: -15px 0 0 10px;
						overflow: hidden;
						width: calc(50% - 10px);
						float: right;
						.list-item1 {
							margin: 15px 2% 0 0;
							background: #BFF267;
							display: block;
							width: 49%;
							float: left;
							transition: all 0.5s;
							.img {
								padding: 20px;
								overflow: hidden;
								background: #030203;
								width: 100%;
								height: auto;
								img {
									object-fit: cover;
									width: 100%;
									transition: 0.3s;
									height: 250px;
								}
							}
							.infoBox {
								padding: 27px 15px;
								.name {
									margin: 0;
									overflow: hidden;
									white-space: nowrap;
									font-weight: normal;
									font-size: 16px;
									text-overflow: ellipsis;
								}
								.time-item {
									margin: 10px 0 0;
									opacity: 0.6;
								}
							}
						}
						.list-item1:hover {
							cursor: pointer;
							color: #fff;
						}
						.list-item2 {
							margin: 15px 0 0;
							background: #BFF267;
							display: block;
							width: 49%;
							float: left;
							transition: all 0.5s;
							.img {
								padding: 20px;
								overflow: hidden;
								background: #030203;
								width: 100%;
								height: auto;
								img {
									object-fit: cover;
									width: 100%;
									transition: 0.3s;
									height: 250px;
								}
							}
							.infoBox {
								padding: 27px 15px;
								.name {
									margin: 0;
									overflow: hidden;
									white-space: nowrap;
									font-weight: normal;
									font-size: 16px;
									text-overflow: ellipsis;
								}
								.time-item {
									margin: 10px 0 0;
									opacity: 0.6;
								}
							}
						}
						.list-item2:hover {
							cursor: pointer;
							color: #fff;
						}
					}
					.list-body-right {
						margin: -10px 0 0;
						flex-direction: column;
						display: flex;
						width: calc(50% - 10px);
						float: right;
						.list-item {
							margin: 10px 0 10px;
							overflow: hidden;
							color: #FFF;
							background:  linear-gradient( 359deg, #393939 0%, #232323 100%);
							flex: 1;
							display: block;
							transition: all 0.5s;
							.date-box {
								padding: 25px 15px;
								color: #000;
								background: #BFF267;
								width: 125px;
								font-size: 15px;
								float: left;
								text-align: right;
								.text {
									text-transform: uppercase;
									display: block;
									font-size: 18px;
								}
								.day {
								}
							}
							.infoBox {
								padding: 15px;
								margin: 0 0 0 125px;
								.name {
									margin: 0;
									overflow: hidden;
									white-space: nowrap;
									font-weight: normal;
									font-size: 16px;
									text-overflow: ellipsis;
								}
								.desc {
									margin: 5px 0 0;
									overflow: hidden;
									opacity: 0.6;
									height: 40px;
								}
							}
						}
						.list-item:hover {
							cursor: pointer;
							color: #fff;
						}
					}
				}
			}
			.moreBtn {
				border: 1px solid #BBB38E;
				cursor: pointer;
				border-radius: 0px;
				margin: 15px auto 0;
				background: none;
				display: none;
				width: 120px;
				line-height: 36px;
				text-align: center;
				.text {
					margin: 0;
					color: #BBB38E;
					font-size: 16px;
					order: 2;
				}
				.icon {
					color: #999;
					background: none;
					display: none;
					width: 23px;
					font-size: 16px;
					height: 7px;
				}
			}
		}
		.recommend {
			padding: 20px 10% 60px;
			margin: 0 auto 0;
			background: url(http://codegen.caihongy.cn/20251215/50d99423b8904b1691da6dcb45ec88af.png)no-repeat;
			width: 100%;
			position: relative;
			order: 4;
			.recommend_title_box {
				padding: 50px ;
				margin: 20px auto;
				background: url(http://codegen.caihongy.cn/20251216/09375e11e7514aa59e4c60da9de5e935.png) no-repeat center/100% 100%;
				display: flex;
				width: 100%;
				justify-content: flex-start;
				flex-wrap: wrap;
				.recommend_title {
					padding: 0;
					color: #BFF267;
					background: none;
					font-weight: 600;
					display: block;
					width: 100%;
					font-size: 30px;
					line-height: 1.5;
					text-align: left;
					order: 2;
				}
				.recommend_subhead {
					margin: 0;
					color: #FFFFFF;
					font-weight: 500;
					display: block;
					width: auto;
					font-size: 22px;
					line-height: 30px;
					text-align: left;
					order: 2;
				}
			}
			.index-pv1 .animation-box {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				z-index: initial;
			}
			
			.index-pv1 .animation-box:hover {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, -4px, 0px);
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
			.list2 {
				margin: -50px 0 0 0px;
				color: #666;
				background: none;
				display: flex;
				width: calc(100%);
				font-size: 14px;
				flex-wrap: wrap;
				height: auto;
				.list-item {
					cursor: pointer;
					border-radius: 20px;
					padding: 20px;
					margin: 0 10px 20px;
					background: #fff;
					display: flex;
					width: calc(50% - 20px);
					position: relative;
					height: auto;
					img {
						object-fit: cover;
						display: inline-block;
						width: 200px;
						height: 200px;
					}
					.item-info {
						padding: 10px;
						overflow: hidden;
						align-content: center;
						flex: 1;
						display: flex;
						width: 280px;
						align-items: center;
						flex-wrap: wrap;
						height: auto;
						.name {
							padding: 0 10px;
							overflow: hidden;
							color: #333;
							white-space: nowrap;
							font-weight: 600;
							width: 100%;
							font-size: 16px;
							line-height: 32px;
							text-overflow: ellipsis;
						}
						.price {
							padding: 0 10px;
							margin: 10px 0;
							color: #000000;
							font-weight: bold;
							width: 100%;
							font-size: 30px;
							line-height: 30px;
						}
						.time_item {
							padding: 0 10px;
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
							padding: 0 10px;
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
							padding: 0 10px;
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
							padding: 0 10px;
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
							padding: 0 10px;
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
			.moreBtn {
				border: 0px solid #ddd;
				cursor: pointer;
				border-radius: 0px;
				margin: 0px auto 0;
				top: 0;
				background: #6aac5a;
				display: none;
				width: 120px;
				line-height: 40px;
				justify-content: center;
				position: absolute;
				right: 7%;
				.text {
					margin: 0 5px 0 0;
					color: #fff;
					font-size: 16px;
					order: 2;
				}
				.icon {
					margin: 0 10px 0 0;
					color: #fff;
					display: none;
					width: auto;
					font-size: 18px;
					height: 7px;
				}
			}
		}
	}
</style>
