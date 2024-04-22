import { createMemoryHistory, createRouter } from 'vue-router'

import App from './App.vue';
import BookDetails from './components/page_components/BookDetails.vue';
import HelloWorld from './components/HelloWorld.vue';

const routes = [
  { path: '/', component: App,

  },
  { path: "/:pathMatch(.*)*", name: "not-found", component: HelloWorld },
  // if you omit the last `*`, the `/` character in params will be encoded when resolving or pushing
  { path: "/:pathMatch(.*)", name: "bad-not-found", component: HelloWorld },
]

export const router = createRouter({
  history: createMemoryHistory(),
  routes,
})