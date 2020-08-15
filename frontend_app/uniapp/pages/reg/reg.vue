<template>
	<view class="content">
		<uni-notice-bar showIcon="true" text="使用信息门户的学号和密码进行注册，邮箱请使用常用邮箱，一个邮箱对应一个用户，用户名不可修改，如果您在注册邮箱时填错了用户名，请等待3日后系统自动销号再重新注册。注册完毕后每日服务器会定时定点为您打卡并发送邮件，请注意查收，若未收到邮件，请尝试手动打卡。"></uni-notice-bar>
		<image class="image" mode="widthFix" src="../../static/img/logo.jpg" />
		<view class="input-group">
			<view class="input-row border">
				<text class="title">账号：</text>
				<m-input type="text" focus clearable v-model="username" placeholder="请输入账号"></m-input>
			</view>
			<view class="input-row border">
				<text class="title">密码：</text>
				<m-input type="password" displayable v-model="password" placeholder="请输入密码"></m-input>
			</view>
			<view class="input-row border">
				<text class="title">重复：</text>
				<m-input type="password" displayable v-model="passwordConfirm" placeholder="请再次输入密码"></m-input>
			</view>
			<view class="input-row">
				<text class="title">邮箱：</text>
				<m-input type="text" clearable v-model="email" placeholder="请输入邮箱"></m-input>
			</view>
			<view class="input-row">
				<text class="title">验证码：</text>
				<m-input class="m-input" type="text" v-model="usercode" placeholder="请输入验证码"></m-input>
				<valid-code v-model="validcode" :refresh="refreshcode" />
			</view>
		</view>
		<view class="btn-row">
			<button type="primary" class="primary" @tap="register">注册</button>
		</view>
	</view>
</template>

<script>
	// import service from '../../service.js';
	import mInput from '../../components/m-input.vue';
	import validCode from '../../components/valid-code.vue'
	import uniNoticeBar from '../../components/uni-notice-bar/uni-notice-bar.vue'
	import {
		register
	} from '../../utils/auth.js';

	export default {
		components: {
			mInput,
			validCode,
			uniNoticeBar
		},
		data() {
			return {
				username: '',
				password: '',
				passwordConfirm: '',
				email: '',
				usercode: '',
				validcode: '',
				refreshcode: 0
			}
		},
		mounted() {
			uni.showModal({
				title: '免责声明',
				content: '我不能保证打卡程序的高可用性，因此存在打不上卡的风险。您在注册账号以后，由于未打卡而造成的任何后果，我对此不负任何责任，3000字检讨和我莫得关系，望悉知。',
				showCancel: false
			});
		},
		methods: {
			register() {
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
					});
					return;
				}
				if (this.password.length < 3) {
					uni.showToast({
						icon: 'none',
						title: '密码最短为 3 个字符'
					});
					return;
				}
				if (this.passwordConfirm !== this.password) {
					uni.showToast({
						icon: 'none',
						title: '两次输入密码不一致，请检查'
					})
					return;
				}
				// 检查验证码
				if (this.usercode.toUpperCase() !== this.validcode.toUpperCase()) {
					uni.showToast({
						icon: 'none',
						title: '验证码不正确，请检查'
					});
					this.refreshCode = Math.random();
					return;
				}
				if (this.email.length < 3 || !~this.email.indexOf('@')) {
					uni.showToast({
						icon: 'none',
						title: '邮箱地址不合法'
					});
					return;
				}
				const data = {
					username: this.username,
					password: this.password,
					email: this.email
				}
				// service.addUser(data);
				register(data).then(res => {
					uni.showToast({
						icon: 'none',
						title: '注册成功，即将返回'
					});
					uni.navigateBack({
						delta: 1
					});
				}).catch(err => {
					uni.showToast({
						icon: 'none',
						title: '注册失败，用户名或邮箱已经被注册。',
						duration: 3000
					});
					this.refreshCode = Math.random();
				})


			}
		}
	}
</script>

<style>
	.image {
		margin: 0;
		width: 100%;
	}
</style>
