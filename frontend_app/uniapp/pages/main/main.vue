<template>
	<view class="content">
		<view v-if="hasLogin" class="hello">
			<view class="qiun-bg-white qiun-title-bar qiun-common-mt">
				<view class="qiun-title-dot-light">
					您好 {{userName}}，您已成功登录。
				</view>
			</view>
			<view class="qiun-bg-white qiun-title-bar qiun-common-mt" >
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
			<view class="title">
				您好 游客。
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
	import uCharts from '../../components/u-charts/u-charts.js';
	var _self;

	export default {
		mounted() {
			_self = this;
			this.cWidth3 = uni.upx2px(350);
			this.cHeight3 = uni.upx2px(350);
			this.arcbarWidth = uni.upx2px(24);
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
			} else {
				// 用户已经登录了
				this.updateData()
			}
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
				userName: this.$store.state.userName,
				
			}
		},
		computed: {
			successCount: function() {
				return this.totalCount - this.failCount;
			},
			successRatio: function() {
				return this.totalCount > 0 ? Math.round(this.successCount / this.totalCount, 1) : 1;
			},
			failRatio: function() {
				return this.totalCount > 0 ? Math.round(this.failCount / this.totalCount, 1) : 0;
			}
		},
		methods: {
			updateData(){
				loadCheckinData().then(res => {
					this.lastCheckin = new Date(res.last_checkin_time);
					this.totalCount = res.total_checkin_count;
					this.failCount = res.total_fail_count;
					this.fillData();
				}).catch(err => {
					console.log("加载打卡数据失败")
				});
			},
			fillData(){
				let Arcbar1 = {
					series: [{color:"#2fc25b",data:this.successRatio,name:"打卡成功率"}]
				};
				let Arcbar2 = {
					series:  [{color:"#ff5500",data:this.failRatio,name:"打卡失败率"}]
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
	.qiun-bg-white {
		background: #FFFFFF;
	}
	.qiun-title-bar {
		width: 96%;
		padding: 15rpx 2%;
		flex-wrap: nowrap;
	}
	.qiun-common-mt {
		margin-top: 20rpx;
	}
	
	.qiun-title-dot-light {
		border-left: 10rpx solid #0ea391;
		padding-left: 10rpx;
		font-size: 32rpx;
		color: #000000
	}
	.normal_height{
		line-height: 150%;
	}
	.btn-row {
		margin-top: 10px;
		padding: 10px;
	}
</style>
