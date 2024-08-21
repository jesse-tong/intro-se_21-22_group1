import { createApp } from 'vue';
import { RouterLink, RouterView} from 'vue-router';
import App from './App.vue';

import 'bootstrap/dist/css/bootstrap.min.css'; 
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap/dist/js/bootstrap.bundle';
import "bootstrap-icons/font/bootstrap-icons.css";


import './style.css';
import './css/custom.css';
import './css/elearning_style.css'

import axios from 'axios';
import { createPinia } from 'pinia'
import Notifications, { useNotification } from '@kyvg/vue3-notification';
import { router } from './router';
import VueExcelEditor from 'vue3-excel-editor';



import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js'
import { useAccountStore } from './components/stores/LoginInfoStore';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement);

var apiSite;
if (import.meta.env.VITE_API_POINT !== undefined){
  apiSite = import.meta.env.VITE_API_POINT; 
}else {
  apiSite = 'http://localhost:5173';
}

var nominatimServer, tileServer;
if (import.meta.env.VITE_OSM_NOMINATIM_SERVER !== undefined 
  && import.meta.env.VITE_OSM_TILE_SERVER !== undefined){
    nominatimServer = import.meta.env.VITE_OSM_NOMINATIM_SERVER;
    tileServer = import.meta.env.VITE_OSM_TILE_SERVER;
}

axios.defaults.baseURL = apiSite;
axios.defaults.withCredentials = true;


const pinia = createPinia()

const app = createApp(App)
app.config.globalProperties = {
    apiSite: apiSite,
    daysOfWeek: ['Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday'],
    nominatimServer: nominatimServer,
    tileServer: tileServer
}
app.use(Notifications)
app.use(pinia)


const notify = useNotification();

router.beforeEach(async (to, from) => {
    const accountStore = useAccountStore();
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



app.use(router);
app.use(VueExcelEditor);

app.mount('#app')
