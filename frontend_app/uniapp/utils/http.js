import Request from '@/js_sdk/luch-request/luch-request/index.js'
import jwt from './jwt.js' // JWT管理

const http = new Request();
const baseUrl = "http://127.0.0.1:5000";

/* 设置全局配置 */
http.setConfig((config) => {
	config.baseURL = baseUrl; //设置 api 地址
	config.custom = {
		loading: true // 默认有loading
	}
	return config;
})

/* 请求之前拦截器 */
http.interceptors.request.use((config) => {
	if (config.custom.loading) {
		uni.showLoading({
			title: '加载中...'
		});
	}
	if (config.custom.auth) {
		// 需要权限认证的路由 需携带自定义参数 {custom: {auth: true}}
		config.header.Authorization = jwt.getAccessToken();
	}
	return config;
}, config => {
	return Promise.reject(config);
})

http.interceptors.response.use((response) => { /* 请求之后拦截器 */
	// console.log(response);
	if (response.config.custom.loading) {
		uni.hideLoading()
	}
	return response;
}, (response) => {
	// 请求错误做点什么
	if (response.config.custom.loading) {
		uni.hideLoading()
	}
	if (response.statusCode == 403) {
		uni.showToast({
			title: "您没有权限进行此项操作",
			icon: "none"
		});
	} else if (response.statusCode == 500 || response.statusCode == 400) {
		uni.showToast({
			title: "服务器开小差了，请稍后再试或联系QQ609741313反馈问题",
			icon: "none"
		})
	}
	return response
})

export {
	http
}
