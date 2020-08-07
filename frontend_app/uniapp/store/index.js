import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
	state: {
		/**
		 * 是否需要强制登录
		 */
		forcedLogin: true,
		hasLogin: false,
		userName: "",
		userEmail: "",
		userID: -1,
		isAdmin: false
	},
	mutations: {
		login(state, userName) {
			state.userName = userName || '新用户';
			state.userEmail = '';
			state.hasLogin = true;
		},
		logout(state) {
			state.userName = "";
			state.userEmail = "";
			state.userID=-1;
			state.isAdmin = false;
			state.hasLogin = false;
		},
		userInfo(state, data) {
			state.isAdmin = data.isAdmin || false;
			state.userID = data.userID;
			state.userEmail=data.userEmail;
		}
	}
})

export default store
