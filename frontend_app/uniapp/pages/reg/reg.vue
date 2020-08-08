<template>
	<view class="content">
		<view class="input-group">
			<view class="input-row border">
				<text class="title">账号：</text>
				<m-input type="text" focus clearable v-model="username" placeholder="请输入账号"></m-input>
			</view>
			<view class="input-row border">
				<text class="title">密码：</text>
				<m-input type="password" displayable v-model="password" placeholder="请输入密码"></m-input>
			</view>
			<view class="input-row">
				<text class="title">邮箱：</text>
				<m-input type="text" clearable v-model="email" placeholder="请输入邮箱"></m-input>
			</view>
			<view class="input-row">
				<text class="title">验证码：</text>
				<m-input class="m-input" type="text" v-model="usercode" placeholder="请输入验证码"></m-input>
				<valid-code v-on:validCodeUpdate="validCodeUpdate" :refresh="refreshcode" />
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
	import {
		register
	} from '../../utils/auth.js';

	export default {
		components: {
			mInput,
			validCode
		},
		data() {
			return {
				username: '',
				password: '',
				email: '',
				usercode: '',
				validcode: '',
				refreshcode: 0
			}
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
					})
				}
				if (this.password.length < 3) {
					uni.showToast({
						icon: 'none',
						title: '密码最短为 3 个字符'
					});
					return;
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
						title: '注册成功，即将返回'
					});
					uni.navigateBack({
						delta: 1
					});
				}).catch(err => {
					debugger;
					uni.showToast({
						title: '注册失败，用户名已经被注册。'
					});
				})


			}
		}
	}
</script>

<style>

</style>
