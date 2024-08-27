<template>
    <div class="row">
        <div class="col-12">
            <h5 class="section-title bg-light-subtle text-center text-primary px-3 mt-3">User Management</h5>
        </div>
        <div class="col-12">
            <div class="mt-3 mx-3">
                <SearchUser @search-user="searchUser" v-model:searchUserId="searchUserId" v-model:searchUserName="searchUserName" v-model:searchUserEmail="searchUserEmail"/>
                <table class="table table-bordered mt-3">
                    <thead>
                        <tr>
                            <th scope="col">User ID</th>
                            <th scope="col">Username</th>
                            <th scope="col">Email</th>
                            <th scope="col">Role</th>
                            <th scope="col">Restriction</th>
                            <th scope="col">Restriction actions</th>
                            <th scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <UserTableRow v-for="user in searchResultUser" :user="user":key="user.id" @user-edited="searchUser"/>
                    </tbody>
                </table>
                <ul class="component-pagination">
                    <li class="pagination-arrow arrow-left me-1">
                        <div class="page-link" @click="currentPage = currentPage > 1 ? currentPage - 1 : 1" id="prevPageButton"><i class="bi bi-chevron-left"></i></div>
                    </li>
                    <li class="page-item">
                        <li class="pagination-number current-number" ><input type="number" style="margin: 0 5px; max-width: 50px;" 
                            v-model.number="currentPage" min="1"/></li>
                    </li>
                    <li class="pagination-arrow arrow-left ms-1">
                        <div class="page-link" @click="currentPage = currentPage < maxPage ? currentPage + 1 : maxPage" id="nextPageButton"><i class="bi bi-chevron-right"></i></div>
                    </li>
                </ul>
            </div>
        </div>
    </div>  
</template>
<script>
import SearchUser from '../borrow_management_components/SearchUser.vue';
import UserTableRow from './UserTableRow.vue';
import axios from 'axios';
export default {
    components: {
        SearchUser: SearchUser,
        UserTableRow: UserTableRow
    },
    data() {
        return {
            searchResultUser: [],
            searchUserId: null,
            searchUserName: null,
            searchUserEmail: null,
            currentPage: 1,
        };
    },
    methods: {
        searchUser() {
            
            let searchParams = {};
            if (this.searchUserId !== '' && this.searchUserId !== null){
                searchParams.user_id = this.searchUserId;
            }

            if (this.searchUserName !== '' && this.searchUserName !== null){
                searchParams.name = this.searchUserName;
            }

            if (this.searchUserEmail !== '' && this.searchUserEmail !== null){
                searchParams.email = this.searchUserEmail;
            }
            searchParams.page = this.currentPage; searchParams.limit = 10;
            // Update searchResultUser and clear searchResultBooks
            axios.get('/api/search-user', {
            params: searchParams
            }).then(response => {
            if (!response.data || !response.data.success){
                this.$notify({
                    title: "Unknown error",
                    text: "Unknown error, this can be server or network error.",
                    type: "error"
                });
                return;
            }
            if (response.data.success === true){
                this.searchResultUser = response.data.result;
            }else {
                this.$notify({
                title: "Search user error",
                text: "Search user with error: " + response.data.error,
                type: "error"
                });
                return;
            }
            }).catch(err=>{
            this.$notify({
                title: "Search user error",
                text: "Search user with error: " + err.response.data.error,
                type: "error"
            });
            return;
            });
        }
    },
    watch: {
        currentPage: {
            handler: function(){
                this.searchUser();
            },
            immediate: true
        }
    }
}
</script>