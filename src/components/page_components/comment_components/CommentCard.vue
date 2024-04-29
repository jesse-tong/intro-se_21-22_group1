<template>
<ul class="card" :key="comment.id">
    <li class="card-body">
        <div class="row">
            <div class="col-6 col-md-4 col-lg-3">
                <div class="input-group">
                    <label :for="'commentId' + comment.id" class="input-group-text"><span>Comment ID:</span></label>
                    <input disabled type="number" class="form-control" v-model="commentId" :id="'commentId' + comment.id"/>
                </div>
            </div>
            <div class="col-6 col-md-4 col-lg-3">
                <div class="input-group">
                    <label :for="'commentBookId' + comment.bookId" class="input-group-text"><span>Book ID:</span></label>
                    <input disabled type="number" class="form-control" v-model="commentBookId" :id="'commentBookId' + comment.bookId"/>
                </div>
            </div>
            <div class="col-6 col-md-4 col-lg-3">
                <div class="input-group">
                    <label :for="'commentUserId' + comment.userId" class="input-group-text"><span>User ID:</span></label>
                    <input disabled type="number" class="form-control" v-model="commentUserId" :id="'commentUserId' + comment.userId"/>
                </div>
            </div>
            <div class="col-6 col-md-4 col-lg-3">
                <div class="input-group">
                    <label :for="'commentUserName' + comment.name" class="input-group-text"><span>Username:</span></label>
                    <input disabled type="number" class="form-control" v-model="commentUsername" :id="'commentUserName' + comment.name"/>
                </div>
            </div>
        </div>
        <div class="input-group">
            <label :for="'commentRating' + comment.id" class="input-group-text" ><span>Rating:</span></label>
            <input class="form-control" type="number" min="0" max="10" v-model="commentRating" :class="{ editable: editable}" />
        </div>
        <div class="form-floating">
            <textarea class="form-control" v-model="commentContent"></textarea>
            <label :for="'commentContent' + comment.id"></label>
        </div>
        <div>
            <div v-if="accountStore.userId && accountStore.userId == commentUserId">
                <button class="btn btn-sm btn-primary me-2" @click="editable = true" v-if="editable === false">Edit</button>
                <button class="btn btn-sm btn-primary mx-3" @click="onConfirmEditComment()" v-else>Save</button>
                <button class="btn btn-sm btn-danger" @click="onDeleteComment()">Delete</button>
            </div>
            <div v-else-if="accountStore.isAdmin">
                <button class="btn btn-sm btn-danger" @click="onDeleteComment()">Delete</button>
            </div>
        </div>

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
                        text: "Save comment failed with error: " + err.response.data.error,
                        type: "error"
                    });
                    this.$emit('updateCommentList');
                }).finally(()=>{
                    this.$emit('updateCommentList');
                })   
            },
            onDeleteComment(){
                let params = new FormData()
                params.set('comment_id', this.commentId);
                axios.delete('/api/comment', {
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
                        text: "Delete comment failed with error: " + err.response.data.error,
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
