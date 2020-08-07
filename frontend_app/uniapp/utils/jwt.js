const tokenKey = 'fuckHHUJwt'; // 存在LocalStorage里面的jwt键值
const getAccessToken = function() {
	let token = '';
	try {
		token = 'Bearer ' + uni.getStorageSync(tokenKey);
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
const clearAccessToken = function() {
	try {
		uni.removeStorageSync(tokenKey);
	} catch (e) {}
}
export default {
	getAccessToken,
	setAccessToken,
	clearAccessToken
}
