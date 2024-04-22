import { createApp } from 'vue';
import { RouterLink, RouterView} from 'vue-router';
import App from './App.vue';
import './style.css';
import 'bootstrap/dist/css/bootstrap.min.css'; 
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import axios from 'axios';
import Notifications from '@kyvg/vue3-notification';
import { router } from './router';

axios.defaults.baseURL = 'http://localhost:5000'
const app = createApp(App)
app.use(Notifications)
app.use(router)
app.mount('#app')
