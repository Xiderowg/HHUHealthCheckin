<template>
	<view class="content">
		<uni-notice-bar showIcon="true" text="用户名为学号,邮箱填写注册时使用的邮箱.如果无法重置密码,请电邮xiderowg@foxmail.com解决."></uni-notice-bar>
		<view class="input-group">
			<view class="input-row">
				<text class="title">用户名：</text>
				<m-input type="text" focus clearable v-model="username" placeholder="请输入用户名"></m-input>
			</view>
			<view class="input-row">
				<text class="title">邮箱：</text>
				<m-input type="text" focus clearable v-model="email" placeholder="请输入邮箱"></m-input>
			</view>
			<view class="input-row border">
				<text class="title">新密码：</text>
				<m-input type="password" displayable v-model="newpass" placeholder="请输入密码"></m-input>
			</view>
			<view class="input-row">
				<text class="title">验证码：</text>
				<m-input class="m-input" type="text" v-model="usercode" placeholder="请输入验证码"></m-input>
				<valid-code v-model="validcode" :refresh="refreshcode" />
			</view>
		</view>

		<view class="btn-row">
			<button type="primary" class="primary" @tap="resetPWD">提交</button>
		</view>
	</view>
</template>

<script>
	import {resetPassword} from '../../utils/auth.js'
	import mInput from '../../components/m-input.vue';
	import validCode from '../../components/valid-code.vue'
	import uniNoticeBar from '../../components/uni-notice-bar/uni-notice-bar.vue'

	export default {
		components: {
			mInput,
			uniNoticeBar,
			validCode
		},
		data() {
			return {
				email: '',
				username: '',
				newpass: '',
				usercode: '',
				validcode: '',
				refreshcode: 0
			}
		},
		methods: {
			resetPWD() {
				// 检查邮箱
				if (this.email.length < 3 || !~this.email.indexOf('@')) {
					uni.showToast({
						icon: 'none',
						title: '邮箱地址不合法',
					});
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
				// 检查密码
				if (this.newpass.length < 6) {
					uni.showToast({
						icon: 'none',
						title: '密码最短为 6 个字符'
					});
					return;
				}
				// 构造数据
				const data = {
					username: this.username,
					email: this.email,
					newpassword: this.newpass
				}
				resetPassword(data).then(res => {
					uni.showToast({
						icon: 'none',
						title: '密码已重置，请重新登陆。',
						duration: 2000
					});
					setTimeout(()=>{uni.navigateBack({
						delta: 1
					})},2000);
				}).catch(err => {
					uni.showToast({
						icon: 'none',
						title: '重置失败，用户名/邮箱不匹配或用户未注册',
						duration: 2000
					});
					this.refreshCode = Math.random();
				});
			}
		}
	}
</script>

<style>

</style>
