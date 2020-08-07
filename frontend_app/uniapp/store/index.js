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
		login(state, userName, userEmail) {
			state.userName = userName || '新用户';
			state.userEmail = userEmail || '';
			state.hasLogin = true;
		},
		logout(state) {
			state.userName = "";
			state.userEmail = "";
			state.userID=-1;
			state.isAdmin = false;
			state.hasLogin = false;
		},
		userInfo(state, isAdmin, id) {
			state.isAdmin = isAdmin || false;
			state.userID = id || -1;
		}
	}
})

export default store
