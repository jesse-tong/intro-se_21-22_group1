<template>
    <div class="mx-auto">
        <div class="alert alert-info mb-2" role="alert" v-if="importSuccess !== null && importFailed !== null">
            <p v-if="importSuccess !== null &Array.isArray(importSuccess) && importSuccess.length > 0">
                {{ 'Import book in rows: ' + importSuccess.join(', ') + ' successfully!' }}
            </p>
            <hr>
            <p class="mb-0" v-if="importFailed !== null && Array.isArray(importFailed) && importFailed.length > 0">Import book in these rows failed: </p>
            <ul v-if="importFailed !== null && Array.isArray(importFailed) && importFailed.length > 0">
                <li v-for="error in importFailed"><span>{{ 'Import book in row ' + error.index + ' failed with error: "' + error.error + '".'}}</span></li>
            </ul>
            <btn class="btn btn-primary mt-1" @click="dismissAlert"><span>Dismiss</span></btn>
        </div>
        <div class="alert alert-danger mb-2" role="alert" v-if="otherError !== null && otherError !== ''">
            <h5 class="alert-heading">Import failed!</h5>
            <p>{{ otherError }}</p>
            <btn class="btn btn-primary mt-1" @click="dismissAlert"><span>Dismiss</span></btn>
        </div>
        <h4 class="ms-2">Import books</h4>
        <vue-excel-editor v-model="jsondata" ref="editor" @select="onSelect" no-header-edit="true" free-select="true">
            <vue-excel-column field="title"  label="Book title" type="string" width="300px" />
            <vue-excel-column field="isbn"   label="ISBN" type="string" width="140px" />
            <vue-excel-column field="publish_year"  label="Publish year"   type="string" width="70px" />
            <vue-excel-column field="stock"  label="Stock"  type="number" width="70px" />
            <vue-excel-column field="languages" label="Languages (comma seperated)" type="string" width="200px" />
            <vue-excel-column field="authors" label="Authors (comma seperated)" type="string" width="200px" />
            <vue-excel-column field="genres" label="Genres (comma seperated)" type="string" width="200px" />
        </vue-excel-editor>
        <div class="d-flex flex-column flex-md-row justify-content-between mt-3" style="max-width: 1220px;">
            <button class="btn btn-primary mb-2" @click="addRow"><span>Add row</span></button>
            <button class="btn btn-success mb-2" @click="importBooks"><span>Import books</span></button>
            <button class="btn btn-danger mb-2" @click="deleteSelectedRows"><span>Delete selected rows</span></button>
        </div>
    </div>
    
    
    
</template>
<script>
import axios from 'axios';
export default {
    data(){
        return {
            jsondata: [
                { title: '', isbn: '', publish_year: '', stock: 0, languages: '', authors: '', genres: '' }
            ],
            selectedRows: [],
            importSuccess: null,
            importFailed: [],
            otherError: null
        }
    },
    methods: {
        addRow(){
            const newRow = { 
                title: '', 
                isbn: '', 
                publish_year: '', 
                stock: 0, 
                languages: '', 
                authors: '', 
                genres: '' 
            };
            this.$refs.editor.newRecord(newRow);
        },
        deleteSelectedRows(){
            this.$refs.editor.deleteSelectedRecords();
        },
        onSelect(selectedRows){
            this.selectedRows = selectedRows;
        },
        importBooks(){
            const JSONdata = JSON.stringify(this.jsondata);
            const config = {
                headers: {'Content-Type': 'application/json'}
            }
            axios.post('/api/import-books', JSONdata, config).then(response => {
                if (response.data.result !== null && response.data.success == true){
                    this.importSuccess = response.data.result.success;
                    this.importFailed = response.data.result.failed;
                }
            }).catch(err => {
                this.otherError = 'Cannot send request to server, please try again.'
            });
        },
        dismissAlert(){
            this.importSuccess = null;
            this.importFailed = null;
            this.otherError = null;
        }
    }
}
</script>