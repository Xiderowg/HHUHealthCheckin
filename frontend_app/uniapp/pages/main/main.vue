<template>
	<view class="content">
		<uni-notice-bar scrollable="true" :speed="noticeSpeed" single="true" showClose="true" showIcon="true" :text="newNotice"></uni-notice-bar>
		<view v-if="hasLogin" class="hello">
			<view class="qiun-bg-white qiun-title-bar qiun-common-mt">
				<view class="qiun-title-dot-light">
					您好 {{userName}}，您已成功登录。
				</view>
			</view>
			<view class="qiun-bg-white qiun-title-bar qiun-common-mt">
				<view class="qiun-title-dot-light">打卡统计信息</view>
			</view>
			<view class="chart">
				<canvas canvas-id="canvasArcbar1" id="canvasArcbar1" class="charts3"></canvas>
				<canvas canvas-id="canvasArcbar2" id="canvasArcbar2" class="charts3" style="margin-left: 350rpx;"></canvas>
			</view>
			<view class="qiun-bg-white qiun-title-bar qiun-common-mt">
				<view class="normal_height">最近一次打卡时间：{{lastCheckin|formatDate}}</view>
				<view class="normal_height">总打卡次数： {{totalCount}}</view>
				<view class="normal_height">成功打卡次数： {{successCount}}</view>
				<view class="normal_height">失败打卡次数： {{failCount}}</view>
			</view>
			<view class="btn-row">
				<button type="primary" class="primary" @tap="updateData">刷新数据</button>
			</view>
		</view>
		<view v-else class="hello">
			<view>
				您好 游客，请登录查看更多信息。
			</view>
		</view>
	</view>
</template>

<script>
	import {
		mapState
	} from 'vuex'
	import {
		loadCheckinData
	} from '../../utils/checkin.js'
	import {
		readInfo,
		readNotice
	} from '../../utils/auth.js';
	import uCharts from '../../components/u-charts/u-charts.js';
	import uniNoticeBar from '../../components/uni-notice-bar/uni-notice-bar.vue'
	var _self;

	export default {
		components: {
			uniNoticeBar
		},
		mounted() {
			_self = this;
			this.cWidth3 = uni.upx2px(350);
			this.cHeight3 = uni.upx2px(350);
			this.arcbarWidth = uni.upx2px(24);
			// 获取公告信息
			readNotice()
				.then(res => this.newNotice = res)
				.catch(err => console.log(err));
			// 检查用户是否登录
			this.onLoadCheck();
		},
		data() {
			return {
				failCount: 0,
				totalCount: 0,
				lastCheckin: new Date(1970, 1, 1),
				cWidth3: '', //圆弧进度图
				cHeight3: '', //圆弧进度图
				arcbarWidth: '', //圆弧进度图，进度条宽度,此设置可使各端宽度一致
				pixelRatio: 1,
				hasLogin: this.$store.state.hasLogin,
				noticeSpeed: 10,
				newNotice: '',
			}
		},
		computed: {
			userName: function() {
				return this.$store.state.userName;
			},
			successCount: function() {
				return this.totalCount - this.failCount;
			},
			successRatio: function() {
				return this.totalCount > 0 ? (this.successCount / this.totalCount).toFixed(2) : 1;
			},
			failRatio: function() {
				return this.totalCount > 0 ? (this.failCount / this.totalCount).toFixed(2) : 0;
			}
		},
		methods: {
			async onLoadCheck() {
				this.hasLogin = await this.updateData();
				if (!this.hasLogin) {
					// 说明用户未登录
					uni.showModal({
						title: '未登录',
						content: '您未登录，需要登录后才能继续',
						/**
						 * 如果需要强制登录，不显示取消按钮
						 */
						showCancel: !this.forcedLogin,
						success: (res) => {
							if (res.confirm) {
								/**
								 * 如果需要强制登录，使用reLaunch方式
								 */
								if (this.forcedLogin) {
									uni.reLaunch({
										url: '../login/login'
									});
								} else {
									uni.navigateTo({
										url: '../login/login'
									});
								}
							}
						}
					});
				} else if (!this.$store.state.hasLogin) {
					// 如果用户之前登陆过，那重新读取下数据
					// 获取用户的信息
					readInfo().then(res => {
						// 更新到store里面
						this.$store.commit('login', res.username);
						this.$store.commit("userInfo", {
							isAdmin: res.is_admin,
							userID: res.id,
							userEmail: res.email
						});
						console.log("更新用户信息成功")
					}).catch(err => {
						debugger;
						// 请求失败，默认用户为匿名用户，且不是管理员
						this.$store.commit("userInfo", {
							isAdmin: false,
							userId: -1,
							userEmail: ''
						});
					});
				}
			},
			updateData() {
				return new Promise((resolve, reject) => {
					loadCheckinData().then(res => {
						this.lastCheckin = new Date(res.last_checkin_time);
						this.totalCount = res.total_checkin_count;
						this.failCount = res.total_fail_count;
						this.fillData();
						resolve(true);
					}).catch(err => {
						console.log("加载打卡数据失败，用户可能未登录")
						resolve(false);
					});
				})
			},
			// updateData(){
			// 	loadCheckinData().then(res => {
			// 		this.lastCheckin = new Date(res.last_checkin_time);
			// 		this.totalCount = res.total_checkin_count;
			// 		this.failCount = res.total_fail_count;
			// 		this.fillData();
			// 	}).catch(err => {
			// 		console.log("加载打卡数据失败，用户可能未登录")
			// 	});
			// },
			fillData() {
				let Arcbar1 = {
					series: [{
						color: "#2fc25b",
						data: this.successRatio,
						name: "打卡成功率"
					}]
				};
				let Arcbar2 = {
					series: [{
						color: "#ff5500",
						data: this.failRatio,
						name: "打卡失败率"
					}]
				};
				this.showArcbar("canvasArcbar1", Arcbar1);
				this.showArcbar2("canvasArcbar2", Arcbar2);
			},
			showArcbar(canvasId, chartData) {
				new uCharts({
					$this: _self,
					canvasId: canvasId,
					type: 'arcbar',
					fontSize: 11,
					title: {
						name: Math.round(chartData.series[0].data * 100) + '%',
						color: chartData.series[0].color,
						fontSize: 25 * _self.pixelRatio
					},
					subtitle: {
						name: chartData.series[0].name,
						color: '#666666',
						fontSize: 15 * _self.pixelRatio
					},
					extra: {
						arcbar: {
							type: 'default',
							width: _self.arcbarWidth * _self.pixelRatio, //圆弧的宽度
						}
					},
					background: '#FFFFFF',
					pixelRatio: _self.pixelRatio,
					series: chartData.series,
					animation: false,
					width: _self.cWidth3 * _self.pixelRatio,
					height: _self.cHeight3 * _self.pixelRatio,
					dataLabel: true,
				});

			},
			showArcbar2(canvasId, chartData) {
				new uCharts({
					$this: _self,
					canvasId: canvasId,
					type: 'arcbar',
					fontSize: 11,
					title: {
						name: Math.round(chartData.series[0].data * 100) + '%',
						color: chartData.series[0].color,
						fontSize: 25 * _self.pixelRatio
					},
					subtitle: {
						name: chartData.series[0].name,
						color: '#666666',
						fontSize: 15 * _self.pixelRatio
					},
					extra: {
						arcbar: {
							type: 'default',
							width: _self.arcbarWidth * _self.pixelRatio, //圆弧的宽度
							backgroundColor: '#ffe3e8',
							startAngle: 1.25,
							endAngle: 0.75
						}
					},
					background: '#FFFFFF',
					pixelRatio: _self.pixelRatio,
					series: chartData.series,
					animation: false,
					width: _self.cWidth3 * _self.pixelRatio,
					height: _self.cHeight3 * _self.pixelRatio,
					dataLabel: true,
				});

			}
		}
	}
</script>

<style>
	.hello {
		display: flex;
		flex: 1;
		flex-direction: column;
	}

	.title {
		margin-top: 28rpx;
		background-color: #FFFFFF;
	}

	.chart {
		width: 100%;
		height: 350rpx;
		background-color: #FFFFFF;
		position: relative;
	}

	.charts3 {
		position: absolute;
		width: 350rpx;
		height: 350rpx;
		background-color: #FFFFFF;
	}


	.btn-row {
		margin-top: 10px;
		padding: 10px;
	}
</style>
