const tokenKey = 'fuckHHUJwt'; // 存在LocalStorage里面的jwt键值
const refreshKey = 'fuckHHUJwtR'
const getAccessToken = function() {
	let token = '';
	try {
		token = 'Bearer ' + uni.getStorageSync(tokenKey);
	} catch (e) {}
	return token;
}
const getRefreshToken = function() {
	let token = '';
	try {
		token = 'Bearer ' + uni.getStorageSync(refreshKey)
	} catch (e) {}
	return token;
}
const setAccessToken = (access_token) => {
	try {
		uni.setStorageSync(tokenKey, access_token);
		return true;
	} catch (e) {
		return false;
	}
}
const setRefreshToken = (refresh_token) => {
	try {
		uni.setStorageSync(refreshKey, refresh_token);
		return true;
	} catch (e) {
		return false;
	}
}
const clearAccessToken = function() {
	try {
		uni.removeStorageSync(tokenKey);
	} catch (e) {}
}
const clearRefreshToken = function() {
	try {
		uni.removeStorageSync(refreshKey);
	} catch (e) {}
}
export default {
	getAccessToken,
	setAccessToken,
	clearAccessToken,
	getRefreshToken,
	setRefreshToken,
	clearRefreshToken
}
