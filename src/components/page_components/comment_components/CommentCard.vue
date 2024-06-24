<template>
<ul class="card" :key="comment.id" data-testid="commentCard">
    <li class="card-body">
        <div class="row">
            <div class="col-6 col-md-6 col-lg-4 mt-2">
                <div class="input-group">
                    <label :for="'commentId' + comment.id" class="input-group-text"><span>Comment ID:</span></label>
                    <input disabled type="number" class="form-control" v-model="commentId" :id="'commentId' + comment.id"/>
                </div>
            </div>
            <div class="col-6 col-md-6 col-lg-4 mt-2">
                <div class="input-group">
                    <label :for="'commentBookId' + comment.bookId" class="input-group-text"><span>Book ID:</span></label>
                    <input disabled type="number" class="form-control" v-model="commentBookId" :id="'commentBookId' + comment.bookId" aria-label="Comment's book ID"/>
                </div>
            </div>
            <div class="col-6 col-md-6 col-lg-4 mt-2">
                <div class="input-group">
                    <label :for="'commentUserId' + comment.userId" class="input-group-text"><span>User ID:</span></label>
                    <input disabled type="number" class="form-control" v-model="commentUserId" :id="'commentUserId' + comment.userId" aria-label="Comment's user ID"/>
                </div>
            </div>
            <div class="col-6 col-md-6 col-lg-12 mt-2 mb-2">
                <div class="input-group">
                    <label :for="'commentUserName' + comment.name" class="input-group-text"><span>Username:</span></label>
                    <input disabled type="text" class="form-control" v-model="commentUsername" :id="'commentUserName' + comment.id"  />
                    <RouterLink :to="'/user/profile/' + comment.userId" role="link" class="btn btn-outline-secondary" ><span>Show profile</span></RouterLink>
                </div>
            </div>
        </div>
        <div class="input-group mb-2">
            <label :for="'commentRating' + comment.id" class="input-group-text" ><span>Rating:</span></label>
            <input class="form-control" type="number" min="0" max="10" v-model="commentRating" :class="{ disabled: editable}" :aria-disabled="!editable" :disabled="!editable"/>
        </div>
        <div class="form-floating">
            <textarea class="form-control bg-white" v-model="commentContent" :class="{ disabled: editable}" :aria-disabled="!editable" :disabled="!editable"></textarea>
            <label :for="'commentContent' + comment.id">Comment:</label>
        </div>
        <div class="d-flex justify-content-between mt-2">
            <div v-if="accountStore.userId && accountStore.userId == commentUserId">
                <button class="btn btn-sm btn-primary me-2" @click="editable = true" v-if="editable === false" data-testid="editCommentButton">Edit</button>
                <button class="btn btn-sm btn-primary me-2" @click="onConfirmEditComment()" data-testid="saveCommentButton" v-else>Save</button>
                <button class="btn btn-sm btn-danger" @click="onDeleteComment()" data-testid="deleteCommentButton">Delete</button>
            </div>
            <div v-else-if="accountStore.isAdmin">
                <button class="btn btn-sm btn-danger" @click="onDeleteComment()" data-testid="deleteCommentButton">Delete</button>
            </div>
            <div>
                <button class="btn btn-sm btn-primary me-2" @click="() => { editable = false; $emit('updateCommentList'); }" v-if="editable === true" data-testid="cancelEditCommentButton">Cancel</button>
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
            },
            goToProfile(userId){
                console.log(userId);
                this.$router.push({path: `/user/profile/${userId}`});
            }
        },
        emits: ['updateCommentList']
    }
</script>
