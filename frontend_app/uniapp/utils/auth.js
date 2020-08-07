import jwt from './jwt.js'
import {
	http
} from './http.js'
import store from '../store/index.js'

const login = function(data) {
	return new Promise((resolve, reject) => {
		var response = http.post('/auth/login', data)
			.then(res => {
				jwt.setAccessToken(res.data.access_token);
				resolve();
			}).catch(err => {
				reject("登录失败");
			})
	});
}

const register = function(data) {
	return new Promise((resolve, reject) => {
		response = http.post('/users/create', data)
			.then(res => {
				resolve();
			}).catch(err => {
				reject("注册失败");
			})
	})
}

const readInfo = function() {
	return new Promise((resolve, reject) => {
		var response = http.get('/users', {
				custom: {
					auth: true
				}
			})
			.then(res => {
				console.log(res);
				// 请求成功则返回用户是否为管理员以及用户的id
				resolve({
					is_admin: res.data.user.is_admin,
					id: res.data.user.id,
					email: res.data.user.email
				});
			}).catch(err => {
				debugger;
				// 请求出现问题
				reject("请求权限失败");
			})
	});
}

const updateInfo = function(data) {
	return new Promise((resolve, reject) => {
		http.post("/users", data, {
				custom: {
					auth: true
				}
			})
			.then(res => {
				resolve();
			}).catch(err => {
				reject("更新用户信息失败");
			});
	});
}


export {
	login,
	readInfo,
	updateInfo,
	register
}
