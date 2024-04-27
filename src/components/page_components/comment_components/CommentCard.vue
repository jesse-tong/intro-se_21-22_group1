<template>
<ul class="card" :key="comment.id">
    <li class="card-body">
        <label :for="'commentId' + comment.id" class="input-group-text"><span>Comment ID:</span></label>
        <input disabled type="number" class="form-control" v-model="commentId" :id="'commentId' + comment.id"/>
        <div>
            <div v-if="accountStore.userId && comment.userId === accountStore.userId">
                <button class="btn btn-sm btn-primary me-2" @click="selectedCommentId = comment.id" v-if="editable === false">Edit</button>
                <button class="btn btn-sm btn-primary mx-3" @click="onConfirmEditComment()" v-else>Save</button>
                <button class="btn btn-sm btn-danger" @click="onDeleteComment()">Delete</button>
            </div>
        <div v-else-if="accountStore.isAdmin">
            <button class="btn btn-sm btn-danger" @click="onDeleteComment()">Delete</button>
        </div>
        </div>

        <span class="badge bg-primary rounded-pill">Rating: {{ comment.rating }}</span>
    </li>
</ul>
</template>
<script>
    import { useAccountStore } from '../../stores/LoginInfoStore';
    import { mapStores } from 'pinia';
    import axios from 'axios';
    export default {
        props: {
            comment: {
                type: Object,
                required: true
            }
        },
        data(){
            return {
                editable: false,
                commentId: this.$props.comment.id,
                commentUsername: this.$props.comment.name,
                commentBookId: this.$props.comment.bookId,
                commentUserId: this.$props.comment.userId,
                commentContent: this.$props.comment.comment,
                commentRating: this.$props.comment.rating
            }

        },
        computed: {
            ...mapStores(useAccountStore)
        },
        methods: {
            onConfirmEditComment(){
                axios.putForm('/api/comment', {
                    comment_id: this.commentId,
                    comment: this.commentContent,
                    rating: this.commentRating
                }).then(response=> {
                    if (!response.data || response.data == undefined || !response.data.success){
                        this.$notify({
                            title: "Save editted comment failed",
                            text: "Save editted comment failed with unknown error, this can be from network or server",
                            type: "error"
                        });
  
                        return;
                    }
                    if (response.data.success === true){
                        this.$notify({
                            title: "Save editted comment successfully!",
                            text: "Save editted comment successfully!",
                            type: "success"
                        });
                        
                    }else{
                        this.$notify({
                            title: "Save comment failed",
                            text: "Save comment failed with error: " + response.data.error,
                            type: "error"
                        });
                        
                    }   
                }).catch(err=>{
                    this.$notify({
                        title: "Save comment failed",
                        text: "Save comment failed with error: " + err.status,
                        type: "error"
                    })
                }).finally(()=>{
                    this.$emit('updateCommentList');
                })   
            },
            onDeleteComment(){
                let params = new FormData()
                params.set('comment_id', this.commentId);
                axios.delete('/api/book', {
                    data: params
                }).then(response=> {
                    if (!response.data || response.data == undefined || !response.data.success){
                        this.$notify({
                            title: "Delete comment failed",
                            text: "Delete comment failed with unknown error, this can be from network or server",
                            type: "error"
                        });
  
                        return;
                    }
                    if (response.data.success === true){
                        this.$notify({
                            title: "Delete comment successfully!",
                            text: "Delete comment successfully!",
                            type: "success"
                        });
                        
                    }else{
                        this.$notify({
                            title: "Delete comment failed",
                            text: "Delete comment failed with error: " + response.data.error,
                            type: "error"
                        });
                        
                    }   
                }).catch(err=>{
                    this.$notify({
                        title: "Delete comment failed",
                        text: "Delete comment failed with error: " + err.status,
                        type: "error"
                    })
                }).finally(()=>{
                    this.$emit('updateCommentList');
                })
            }
        },
        emits: ['updateCommentList']
    }
</script>
