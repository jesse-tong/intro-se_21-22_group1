import { createWebHistory, createRouter } from 'vue-router'

import App from './App.vue';
import BookDetails from './components/page_components/book_page_components/BookDetails.vue';
import BorrowManagement from './components/page_components/edit_borrow_components/BorrowManagement.vue';
import PageNotFound from './components/views/PageNotFound.vue';
import LoginPage from './components/views/LoginPage.vue';
import BookManagement from './components/page_components/book_management_components/BookManagement.vue';
import BorrowTableUser from './components/page_components/user_borrow_components/BorrowTableUser.vue';
import BookByAuthors from './components/page_components/book_page_components/BookByAuthors.vue';
import BookByGenres from './components/page_components/book_page_components/BookByGenres.vue';
import NavBar from './components/page_components/NavBar.vue';
import RegisterPage from './components/views/RegisterPage.vue';
const routes = [
  { 
    path: '/', 
    component: App,
    children: [
      {
        path: 'book/by-author',
        components: {
          NavBar: NavBar,
          default: BookByAuthors
        }
      },
      {
        path: 'book/by-genre',
        components: {
          NavBar: NavBar,
          default: BookByGenres
        }
      },
      {
        path: 'book/:bookId',
        components: {
          NavBar: NavBar,
          default: BookDetails
        },
        props: {
          default: true
        }
      },
      {
        path: 'admin/manage-borrow',
        components: {
          NavBar: NavBar,
          default: BorrowManagement
        }
      },
      {
        path: 'admin/manage-books',
        components: {
          NavBar: NavBar,
          default: BookManagement
        }
      },
      {
        path: 'login',
        components: {
          NavBar: NavBar,
          default: LoginPage
        }
      },
      {
        path: 'register',
        components: {
          NavBar: NavBar,
          default: RegisterPage
        }
      },
      {
        path: 'register/:role',
        components: {
          NavBar: NavBar,
          default: RegisterPage,

        },
        props: {
          default: true
        }
      },
      {
        path: 'user/borrows',
        components: {
          NavBar: NavBar,
          default: BorrowTableUser
        }
      },
      {
        path: '',
        components: {
          NavBar: NavBar,
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