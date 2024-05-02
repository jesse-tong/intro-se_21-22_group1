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
import AdvancedSearch from './components/page_components/search_page_components/AdvancedSearch.vue';
import UserProfile from './components/views/UserProfile.vue';
import UserSettings from './components/views/UserSettings.vue';
import LibraryPolicyPage from './components/views/LibraryPolicyPage.vue';
import Footer from './components/views/Footer.vue';
import HomePage from './components/views/HomePage.vue';
import BookCarousel from './components/page_components/homepage_components/BookCarousel.vue';

const routes = [
  { 
    path: '/', 
    components: {
      footer: Footer,
      default: App
    },
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
        path: '/book/advanced-search',
        components: {
          NavBar: NavBar,
          default: AdvancedSearch
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
        path: 'user/profile',
        components:{
          NavBar: NavBar,
          default: UserProfile
        }
      },
      {
        path: 'user/settings',
        components:{
          NavBar: NavBar,
          default: UserSettings
        }
      },
      {
        path: 'library-policies',
        components:{
          NavBar: NavBar,
          default: LibraryPolicyPage
        }
      },
      {
        path: '',
        components: {
          NavBar: NavBar,
          default: HomePage
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