import {defineStore} from 'pinia';

export const useAccountStore = defineStore('account', {
    state: () => ({
      userId: null,
      name: null,
      role: null,
      isRestricted: false
    }),
    getters: {
        isAdmin: (state) => {
            if (state.role !== null){
                return state.role.includes('admin');
            }else {
                return false;
            }
        },
        loggedIn: (state) => (state.userId !== null && state.isRestricted === false),
        notLoggedIn: (state) => (state.userId === null || state.isRestricted === true),
        isLoginRemember: (state) => (state.userId !== null && localStorage.getItem('userId') === state.userId)
    },
    actions: {
      // since we rely on `this`, we cannot use an arrow function
      setAccountInfo(userId, name, role, isRestricted) {
        this.$state.userId = userId; this.$state.name = name; this.$state.role = role; 
        this.$state.isRestricted = isRestricted; 
      },
      setLocalStorage(){
        if (this.$state.userId !== null){
            localStorage.setItem('userId', this.$state.userId);
        }
        if (this.$state.isRestricted !== null){
          localStorage.setItem('isRestricted', this.$state.isRestricted);
        }
        if (this.$state.name !== null){
            localStorage.setItem('name', this.$state.name);
        }
        if (this.$state.role !== null){
            localStorage.setItem('role', this.$state.role);
        } 
      },
      setSessionStorage(){
        if (this.$state.userId !== null){
          sessionStorage.setItem('userId', this.$state.userId);
        }
        if (this.$state.isRestricted !== null){
            sessionStorage.setItem('isRestricted', this.$state.isRestricted);
        }
        if (this.$state.name !== null){
            sessionStorage.setItem('name', this.$state.name);
        }
        if (this.$state.role !== null){
            sessionStorage.setItem('role', this.$state.role);
        } 
      },
      setAccountFromLocal(){
        this.$state.userId = sessionStorage.getItem('userId');
        this.$state.name = sessionStorage.getItem('name');
        this.$state.role = sessionStorage.getItem('role');
        this.$state.isRestricted = sessionStorage.getItem('isRestricted');
        if (this.$state.userId === null && this.$state.name === null && this.$state.role === null){
          localStorage.setItem('userId', this.$state.userId);
          localStorage.setItem('name', this.$state.name);
          localStorage.setItem('role', this.$state.role);
          localStorage.setItem('isRestricted', this.$state.isRestricted);
        }
      },
      clearSessionStorage(){
        sessionStorage.clear();
      },
      clearLocalStorage(){
        localStorage.clear();
      },
      clearStoredData(){
        this.$state.userId = null; this.$state.name = null; this.$state.role = null;
        this.$state.isRestricted = false;
      },
    },
});
