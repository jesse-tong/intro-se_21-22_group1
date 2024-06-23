import { createApp } from 'vue';
import { RouterLink, RouterView} from 'vue-router';
import App from './App.vue';
import './style.css';
import 'bootstrap/dist/css/bootstrap.min.css'; 
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import "bootstrap-icons/font/bootstrap-icons.css";
import 'font-awesome/css/font-awesome.min.css';
import axios from 'axios';
import { createPinia } from 'pinia'
import Notifications, { useNotification } from '@kyvg/vue3-notification';
import { router } from './router';

import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js'
import { useAccountStore } from './components/stores/LoginInfoStore';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement);

axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.withCredentials = true;

const pinia = createPinia()

const app = createApp(App)
app.config.globalProperties = {
    apiSite: 'http://localhost:5000',
    daysOfWeek: ['Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']
}
app.use(Notifications)
app.use(pinia)

const accountStore = useAccountStore();
const notify = useNotification();

router.beforeEach(async (to, from) => {
    if (
      // make sure the user is authenticated
      !accountStore.isAdmin &&
      //Check if the page is an admin-only one, avoid an infinite redirect
      to.fullPath.includes('/admin/') && to.name !== 'Login'
    ) {
      // notifies user that the page is admin-only redirect the user to the login page
      notify.notify({
        title: 'Admin-only page!',
        text: 'Page with path ' + to.fullPath + ' is only for admin, please login to an admin account!',
        type: 'error'
      });
      return { name: 'Login' }
    }
})

app.use(router)

app.mount('#app')
