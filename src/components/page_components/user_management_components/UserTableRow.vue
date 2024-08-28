<template>
    <tr>
        <td>{{ user.id }}</td>
        <td>{{ user.name }}</td>
        <td>{{ user.email }}</td>
        <td v-if="editing === false"><span class="badge" 
            :class="[user.role == 'admin' ? 'bg-danger' : user.role == 'mod' || user.role == 'staff' ? 'bg-warning' : 'bg-info']">{{ user.role }}</span></td>
        <td v-if="editing === true">
            <select v-model="editingRole" class="form-select">
                <option value="admin">Admin</option>
                <option value="user">User</option>
            </select>
        </td>
        <td class="text-center" v-if="editingIsRestricted === true"><h6 class="badge bg-danger">Is Restricted</h6></td>
        <td class="text-center" v-else><h6 class="badge bg-primary">Not Restricted</h6></td>
        <td class="text-center">
            <button class="btn btn-danger" v-if="editingIsRestricted === false && editing === true" @click="editingIsRestricted = true">Restrict user</button>
            <button class="btn btn-success" v-if="editingIsRestricted === true && editing === true" @click="editingIsRestricted = false">Remove restriction</button>
        </td>
        <td>
            <button class="btn btn-primary" v-if="editing === false" @click="editing = true">Edit</button>
            <button class="btn btn-success" v-if="editing === true" @click="onSaveEdit">Save</button>
        </td>
    </tr>
</template>
<script>
import axios from 'axios';

    export default {
        props: {
            user: {
                type: Object,
                required: true
            }
        },
        data(){
            return {
                editing: false,
                editingRole: this.user.role,
                editingIsRestricted: this.user.isRestricted
            }
        },
        methods: {
            onSaveEdit(){
                axios.postForm('/api/change-user-role-and-restriction', {
                    user_id: this.user.id,
                    role: this.editingRole,
                    is_restricted: this.editingIsRestricted
                }).then(response => {
                    this.editing = false;
                    this.$emit('user-edited');
                    if (response && response.data && response.data.result && response.data.success === true){
                        this.$notify({
                            title: 'Success',
                            text: 'User edited successfully',
                            type: 'success'
                        });
                    } else {
                        this.$notify({
                            title: 'Error',
                            text: 'Failed to edit user with error: ' + response.data.error,
                            type: 'error'
                        });
                    }
                }).catch(error => {
                    this.$notify({
                        title: 'Error',
                        text: 'Failed to edit user',
                        error: 'error'
                    });
                });
                this.editing = false;
            }
        },
        emits: ['user-edited']
    }
</script>