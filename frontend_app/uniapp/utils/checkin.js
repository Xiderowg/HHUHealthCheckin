import jwt from './jwt.js'
import {
	http
} from './http.js'

const adminCheckin = function() {
	return new Promise((resolve, reject) => {
		http.post("/checkin/all",{}, {
			custom: {
				auth: true
			}
		}).then(res => {
			resolve("签到任务开始");
		}).catch(err => {
			reject("签到任务失败");
		});
	});
}

const userCheckin = function() {
	return new Promise((resolve, reject) => {
		http.post("/checkin",{}, {
			custom: {
				auth: true
			}
		}).then(res => {
			resolve("签到任务开始");
		}).catch(err => {
			reject("签到任务失败");
		});
	});
}

const loadCheckinData = function() {
	return new Promise((resolve, reject) => {
		http.get("/users/data", {
				custom: {
					auth: true
				}
			})
			.then(res => {
				resolve(res.data.checkin_data);
			}).catch(err => {
				reject("获取打卡信息失败");
			})
	});
}

export {
	adminCheckin,
	userCheckin,
	loadCheckinData
}
