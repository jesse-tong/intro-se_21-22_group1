import {defineStore} from 'pinia';

export const useSearchQueryStore = defineStore('searchQuery', {
    state: () => ({
      title: '',
      isbn: '',
      description: '',
    }),
    getters: {
        
    },
    actions: {
      // since we rely on `this`, we cannot use an arrow function
      clearQueries(){
        this.$state.title = '';
        this.$state.isbn = '';
        this.$state.description = '';
      },
      saveSearchQuery(title, isbn, description){
        this.$state.title = title;
        this.$state.isbn = isbn;
        this.$state.description = description;
      }
    },
});