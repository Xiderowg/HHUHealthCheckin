<template>
	<view class="content">
		<view class="input-group">
			<view class="input-row border">
				<text class="title">邮 箱：</text>
				<m-input class="m-input" type="text" clearable focus v-model="email" placeholder="请输入邮箱"></m-input>
			</view>
			<view class="input-row">
				<text class="title">新 密 码：</text>
				<m-input type="password" displayable v-model="password" placeholder="请输入密码"></m-input>
			</view>
			<view class="input-row">
				<text class="title">重复密码：</text>
				<m-input type="password" displayable v-model="confirmPassword" placeholder="请再一次输入密码"></m-input>
			</view>
			<view class="input-row">
				<text class="title">验 证 码：</text>
				<m-input class="m-input" type="text" v-model="usercode" placeholder="请输入验证码"></m-input>
				<valid-code v-model="validcode" :refresh="refreshcode" />
			</view>
			<view class="input-row">
				<button type="primary" class="primary" @tap="userUpdate">更新信息</button>
			</view>
		</view>
		<view class="btn-row">
			<button type="primary" class="primary" @tap="userCheckin">手动签到</button>
			<button v-if="isAdmin" type="default" @tap="adminCheckin">全员签到</button>
			<button v-if="!hasLogin" type="primary" class="primary" @tap="bindLogin">登录</button>
			<button v-if="hasLogin" type="default" @tap="bindLogout">退出登录</button>
		</view>
	</view>
</template>

<script>
	import {
		adminCheckin,
		userCheckin
	} from '../../utils/checkin.js'
	import {
		updateInfo
	} from '../../utils/auth.js'
	import {
		mapState,
		mapMutations
	} from 'vuex'

	export default {
		computed: {
			...mapState(['hasLogin', 'forcedLogin', 'isAdmin', 'userName', 'userID', 'userEmail'])
		},
		data() {
			return {
				username: userName,
				usermail: userEmail,
				password: '',
				confirmPassword: '',
				usercode: ''
				validcode: '',
				refreshcode: 0
			}
		},
		methods: {
			...mapMutations(['logout']),
			bindLogin() {
				uni.navigateTo({
					url: '../login/login',
				});
			},
			bindLogout() {
				this.logout();
				/**
				 * 如果需要强制登录跳转回登录页面
				 */
				if (this.forcedLogin) {
					uni.reLaunch({
						url: '../login/login',
					});
				}
			},
			adminCheckin() {
				/**
				 * 全体用户打卡
				 */
				adminCheckin()
					.then(res => {
						uni.showToast({
							icon: 'success',
							title: res
						});
					}).catch(err => {
						uni.showToast({
							icon: 'none',
							title: err
						});
					});
			},
			userCheckin() {
				/**
				 * 用户打卡
				 */
				userCheckin()
					.then(res => {
						uni.showToast({
							icon: 'success',
							title: res
						});
					}).catch(err => {
						uni.showToast({
							icon: 'none',
							title: err
						});
					});
			},
			userUpdate() {
				/**
				 * 用户信息更新
				 */
				// 检查密码
				if (this.password.length < 6) {
					uni.showToast({
						icon: 'none',
						title: '密码最短为 6 个字符'
					});
					return;
				}
				if (this.password !== this.confirmPassword) {
					uni.showToast({
						icon: 'none',
						title: '两次输入的密码不一致，请检查'
					})
				}
				// 检查验证码
				if (String.prototype.toUpperCase(this.usercode) != String.prototype.toUpperCase(this.validcode)) {
					uni.showToast({
						icon: 'none',
						title: '验证码不正确，请检查'
					});
					this.refreshCode = Math.random();
					return;
				}
				// 更新信息
				const data = {
					username: this.username,
					email: this.usermail,
					password: this.password
				};
				updateInfo(data).then(res => {
					uni.showToast({
						title: '用户信息更新成功'
					});
				}).catch(err => {
					uni.showToast({
						title: '用户信息更新失败'
					});
				});
			}
		}
	}
</script>

<style>

</style>
