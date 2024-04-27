import {defineStore} from 'pinia';

export const useAccountStore = defineStore('account', {
    state: () => ({
      userId: null,
      name: null,
      role: null
    }),
    getters: {
        isAdmin: (state) => state.role.includes('admin'),
        loggedIn: (state) => (state.userId !== null),
        notLoggedIn: (state) => (state.userId === null)
    },
    actions: {
      // since we rely on `this`, we cannot use an arrow function
      setAccountInfo(userId, name, role) {

        this.$state.userId = userId; this.$state.name = name; this.$state.role = role;
        console.log(this.$state.role);
      },
      setLocalStorage(){
        if (this.$state.userId !== null){
            localStorage.setItem('userId', this.$state.userId);
        }
        
        if (this.$state.name !== null){
            localStorage.setItem('name', this.$state.name);
        }
        if (this.$state.role !== null){
            localStorage.setItem('role', this.$state.role);
        } 
      },
      setAccountFromLocal(){
        this.$state.userId = localStorage.getItem('userId');
        this.$state.name = localStorage.getItem('name');
        this.$state.role = localStorage.getItem('role');
      },
     
    },
});
