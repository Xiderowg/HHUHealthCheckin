import Vue from 'vue'
import App from './App'

import store from './store'
import {
	http
} from './utils/http.js'

Vue.config.productionTip = false

Vue.prototype.$store = store
Vue.prototype.$http = http

App.mpType = 'app'

Vue.filter('formatDate', function(value) {
  if (value instanceof Date) {
    var hours = value.getHours();
    var minutes = value.getMinutes();
	minutes = minutes < 10 ? '0'+minutes : minutes;
	var strTime = hours + ':' + minutes;
	return value.getFullYear() +"/"  +(value.getMonth()+1)+"/" + value.getDate() + "  " + strTime;
  }
  return value.toString();
});

const app = new Vue({
	store,
	...App
})
app.$mount()
