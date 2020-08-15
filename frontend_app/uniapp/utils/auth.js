import jwt from './jwt.js'
import {
	http
} from './http.js'
import store from '../store/index.js'

const login = function(data) {
	return new Promise((resolve, reject) => {
		var response = http.post('/auth/login', data)
			.then(res => {
				// debugger;
				jwt.setAccessToken(res.data.access_token);
				jwt.setRefreshToken(res.data.refresh_token);
				resolve();
			}).catch(err => {
				// debugger;
				reject("登录失败");
			})
	});
}

const register = function(data) {
	return new Promise((resolve, reject) => {
		var response = http.post('/users/create', data)
			.then(res => {
				// console.log(res.data);
				resolve();
			}).catch(err => {
				debugger;
				reject("注册失败");
			})
	})
}

const readInfo = function() {
	return new Promise((resolve, reject) => {
		// console.log(jwt.getAccessToken());
		var response = http.get('/users', {
				custom: {
					auth: true
				}
			})
			.then(res => {
				// console.log(res);
				// 请求成功则返回用户是否为管理员以及用户的id
				resolve({
					is_admin: res.data.user.is_admin,
					id: res.data.user.id,
					email: res.data.user.email,
					username: res.data.user.username
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
		http.put("/users", data, {
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

const readNotice = function(data) {
	return new Promise((resolve, reject) => {
		http.get("/notice").then(res => {
			resolve(res.data.msg);
		}).catch(err => {
			reject("获取公告信息失败");
		});
	});
}

const resetPassword = function(data) {
	return new Promise((resolve, reject) => {
		http.post("/users/reset", data).then(res => {
			resolve(res);
		}).catch(err => {
			reject(err);
		})
	});
};

const removeInactiveUser = function() {
	return new Promise((resolve, reject) => {
		http.delete("/users/inactive",{}, {
			custom: {
				auth: true
			}
		}).then(res => {
			resolve(res);
		}).catch(err => {
			reject(err);
		})
	})
}


export {
	login,
	readInfo,
	updateInfo,
	register,
	resetPassword,
	readNotice,
	removeInactiveUser
}
