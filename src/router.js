import { createWebHistory, createRouter } from 'vue-router'

import App from './App.vue';
import BookDetails from './components/page_components/book_page_components/BookDetails.vue';
import BorrowManagement from './components/page_components/edit_borrow_components/BorrowManagement.vue';
import PageNotFound from './components/views/PageNotFound.vue';
import LoginPage from './components/views/LoginPage.vue';
import BookManagement from './components/page_components/book_management_components/BookManagement.vue';
import BorrowTableUser from './components/page_components/user_borrow_components/BorrowTableUser.vue';
const routes = [
  { 
    path: '/', 
    component: App,
    children: [
      
      {
        path: 'book/:bookId',
        components: {
          default: BookDetails
        },
        props: {
          default: true
        }
      },
      {
        path: 'admin/manage-borrow',
        components: {
          default: BorrowManagement
        }
      },
      {
        path: 'admin/manage-books',
        components: {
          default: BookManagement
        }
      },
      {
        path: 'login',
        components: {
          default: LoginPage
        }
      },
      {
        path: 'user/borrows',
        components: {
          default: BorrowTableUser
        }
      },
      {
        path: '',
        components: {
          default: BorrowManagement
        },
        
      },
    ]
  },
  
  { path: "/:pathMatch(.*)*", name: "not-found", component: PageNotFound },
  // if you omit the last `*`, the `/` character in params will be encoded when resolving or pushing
  { path: "/:pathMatch(.*)", name: "bad-not-found", component: PageNotFound },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})