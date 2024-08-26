import { createWebHistory, createRouter } from 'vue-router'

import App from './App.vue';
import BookDetails from './components/page_components/book_page_components/BookDetails.vue';
import BorrowManagement from './components/page_components/borrow_management_components/BorrowManagement.vue';
import PageNotFound from './components/views/PageNotFound.vue';
import LoginPage from './components/views/LoginPage.vue';
import BookManagement from './components/page_components/book_management_components/BookManagement.vue';
import BookByAuthors from './components/page_components/book_page_components/BookByAuthors.vue';
import BookByGenres from './components/page_components/book_page_components/BookByGenres.vue';
import NavBar from './components/page_components/NavBar.vue';
import RegisterPage from './components/views/RegisterPage.vue';
import AdvancedSearch from './components/page_components/advanced_search_components/AdvancedSearch.vue';
import UserProfile from './components/page_components/user_settings_components/UserProfile.vue';
import UserSettings from './components/page_components/user_settings_components/UserSettings.vue';
import LibraryPolicyPage from './components/views/LibraryPolicyPage.vue';
import Footer from './components/views/Footer.vue';
import HomePage from './components/views/HomePage.vue';
import ReportPage from './components/page_components/report_page_components/ReportPage.vue';
import LibraryPoliciesSettings from './components/page_components/library_policies_settings_components/LibraryPoliciesSettings.vue';
import ArticleManagement from './components/page_components/article_management_components/ArticleManagement.vue';
import ArticlePage from './components/page_components/ArticlePage.vue';
import ArticleListUser from './components/page_components/article_management_components/ArticleListUser.vue';
import RecentEventArticleList from './components/page_components/article_management_components/RecentEventArticleList.vue';
import SearchWebsitePage from './components/page_components/article_management_components/SearchWebsitePage.vue';

const routes = [
  { 
    path: '/', 
    components: {
      footer: Footer,
      default: App,
      NavBar: NavBar
    },
    children: [
      {
        path: 'book/by-author',
        components: {
          default: BookByAuthors
        }
      },
      {
        path: 'book/by-genre',
        components: {
          default: BookByGenres
        }
      },
      {
        path: '/book/advanced-search',
        components: {
          default: AdvancedSearch
        }
      },
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
        path: 'admin/policies-settings',
        components: {
          default: LibraryPoliciesSettings
        }
      },
      {
        path: 'admin/article-management',
        components: {
          default: ArticleManagement
        }
      },
      {
        path: 'login',
        components: {
          default: LoginPage
        },
        name: 'Login'
      },
      {
        path: 'register',
        components: {
          default: RegisterPage
        }
      },
      {
        path: 'register/:role',
        components: {
          default: RegisterPage,

        },
        props: {
          default: true
        }
      },
      {
        path: 'user/profile/:userId',
        components:{
          default: UserProfile
        },
        props: {
          default: true
        }
      },
      {
        path: 'article/:articleId',
        components:{
          default: ArticlePage
        },
        props: {
          default: true
        }
      },
      {
        path: 'recent-events',
        components:{
          default: RecentEventArticleList
        }
      },
      {
        path: 'search-website',
        components:{  
          default: SearchWebsitePage
        }
      },
      {
        path: 'articles',
        components:{
          default: ArticleListUser
        },
      },
      {
        path: 'user/profile',
        components:{
          default: UserProfile
        }
      },
      {
        path: 'user/settings',
        components:{
          default: UserSettings
        }
      },
      {
        path: 'library-policies',
        components:{
          default: LibraryPolicyPage
        }
      },
      {
        path: 'admin/reports',
        components: {
          default: ReportPage
        }
      },
      {
        path: '',
        components: {
          default: HomePage
        },
        
      },
      {
        path: ':pathMatch(.*)*',
        name: 'not-found-inner',
        components: {
          default: PageNotFound
        }
      },
      {
        path: ':pathMatch(.*)',
        name: 'bad-not-found-inner',
        components: {
          default: PageNotFound
        }
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