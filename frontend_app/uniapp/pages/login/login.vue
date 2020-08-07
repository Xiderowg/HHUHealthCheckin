<template>
	<view class="content">
		<image class="image" mode="widthFix" src="../../static/img/logo.jpg" />
		<view class="input-group">
			<view class="input-row border">
				<text class="title">账 号：</text>
				<m-input class="m-input" type="text" clearable focus v-model="username" placeholder="请输入账号"></m-input>
			</view>
			<view class="input-row">
				<text class="title">密 码：</text>
				<m-input type="password" displayable v-model="password" placeholder="请输入密码"></m-input>
			</view>
			<view class="input-row">
				<text class="title">验证码：</text>
				<m-input class="m-input" type="text" v-model="usercode" placeholder="请输入验证码"></m-input>
				<valid-code v-model="validcode" :refresh="refreshcode" />
			</view>
		</view>
		<view class="btn-row">
			<button type="primary" class="primary" @tap="bindLogin">登录</button>
		</view>
		<view class="action-row">
			<navigator url="../reg/reg">注册账号</navigator>
			<!-- <navigator url="../pwd/pwd">忘记密码</navigator> -->
		</view>
		<view class="copyright-row">
			<text>© 2020 Edward Linus All Rights Reserved.</text>
		</view>
	</view>
</template>

<script>
	// import service from '../../service.js';
	import {
		login,
		readInfo
	} from '../../utils/auth.js';
	import {
		mapState,
		mapMutations
	} from 'vuex'
	import mInput from '../../components/m-input.vue'
	import validCode from '../../components/valid-code.vue'

	export default {
		components: {
			mInput,
			validCode
		},
		data() {
			return {
				providerList: [],
				username: '',
				password: '',
				usercode: '',
				validcode: '',
				refreshcode: 0,
				positionTop: 0,
				isDevtools: false,
			}
		},
		computed: mapState(['forcedLogin']),
		methods: {
			...mapMutations(['login']),
			initPosition() {
				/**
				 * 使用 absolute 定位，并且设置 bottom 值进行定位。软键盘弹出时，底部会因为窗口变化而被顶上来。
				 * 反向使用 top 进行定位，可以避免此问题。
				 */
				this.positionTop = uni.getSystemInfoSync().windowHeight - 100;
			},
			bindLogin() {
				/**
				 * 客户端对账号信息进行一些必要的校验。
				 * 实际开发中，根据业务需要进行处理，这里仅做示例。
				 */
				if (this.username.length < 5) {
					uni.showToast({
						icon: 'none',
						title: '账号最短为 5 个字符'
					});
					return;
				}
				if (isNaN(parseInt(this.username))) {
					uni.showToast({
						icon: 'none',
						title: '账号只可由数字组成，即你的学号'
					})
				}
				if (this.password.length < 6) {
					uni.showToast({
						icon: 'none',
						title: '密码最短为 6 个字符'
					});
					return;
				}
				// 检查验证码
				if (String.prototype.toUpperCase(this.usercode) !== String.prototype.toUpperCase(this.validcode)) {
					uni.showToast({
						icon: 'none',
						title: '验证码不正确，请检查'
					});
					this.refreshCode = Math.random();
					return;
				}
				// 登录逻辑
				const data = {
					username: this.username,
					password: this.password
				};
				login(data)
					.then(res => this.toMain(this.username))
					.catch(err => {
						uni.showToast({
							icon: 'none',
							title: '用户账号或密码不正确',
						});
					});
				// const validUser = service.getUsers().some(function(user) {
				// 	return data.username === user.account && data.password === user.password;
				// });
				// if (validUser) {
				// 	this.toMain(this.username);
				// } else {
				// 	uni.showToast({
				// 		icon: 'none',
				// 		title: '用户账号或密码不正确',
				// 	});
				// }
			},
			// getUserInfo({
			// 	detail
			// }) {
			// 	if (detail.userInfo) {
			// 		this.toMain(detail.userInfo.nickName);
			// 	} else {
			// 		uni.showToast({
			// 			icon: 'none',
			// 			title: '登陆失败'
			// 		});
			// 	}
			// },
			toMain(userName) {
				this.login(userName);
				// 获取用户的信息
				readInfo().then(res => {
					// 更新到store里面
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
				})
				/**
				 * 强制登录时使用reLaunch方式跳转过来
				 * 返回首页也使用reLaunch方式
				 */
				if (this.forcedLogin) {
					uni.reLaunch({
						url: '../main/main',
					});
				} else {
					uni.navigateBack();
				}

			}
		},
		onReady() {
			this.initPosition();
			// #ifdef MP-WEIXIN
			this.isDevtools = uni.getSystemInfoSync().platform === 'devtools';
			// #endif
		}
	}
</script>

<style>
	.action-row,
	.copyright-row {
		display: flex;
		flex-direction: row;
		justify-content: center;
	}

	.copyright-row {
		position: absolute;
		bottom: 0;
		right: 0;
		left: 0;
		margin: auto;
	}

	.copyright-row text {
		line-height: normal;
		color: #C8C7CC;
		font-size: small;
	}

	.action-row navigator {
		color: #007aff;
		padding: 0 10px;
	}

	.oauth-row {
		display: flex;
		flex-direction: row;
		justify-content: center;
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
	}

	.oauth-image {
		position: relative;
		width: 50px;
		height: 50px;
		border: 1px solid #dddddd;
		border-radius: 50px;
		margin: 0 20px;
		background-color: #ffffff;
	}

	.oauth-image image {
		width: 30px;
		height: 30px;
		margin: 10px;
	}

	.oauth-image button {
		position: absolute;
		left: 0;
		top: 0;
		width: 100%;
		height: 100%;
		opacity: 0;
	}
	.image {
		margin:0;
		width: 100%;
	}
</style>
