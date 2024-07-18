<script setup>
import { ref } from "vue";
import { VuePDF, usePDF } from "@tato30/vue-pdf";
import { useNotification } from '@kyvg/vue3-notification';
const page = ref(1);
const scale = ref(1);
const pdfLoadable = ref(true);
const loadError = ref("");

const notify = useNotification();

const props =  defineProps({
    pdf: String,
  });
function onPassword(updatePassword, reason) {
  console.log(`Reason for callback: ${reason}`)
}

function onProgress({ loaded, total }) {
  //console.log(`${loaded / total * 100}% Loaded`)
}

function onError(reason) {
  if (!String(reason).includes("MissingPDFException")){
      notify.notify({
      title: "Cannot open ebook file",
      text: "Cannot open ebook file with reason: " + reason,
      type: "error"
    });
    pdfLoadable.value = false;
    loadError.value = reason;
  }else {
    pdfLoadable.value = false;
    loadError.value = "No PDF for this book or server error";
  }
  
  
}


const { pdf, pages } = usePDF(
  props.pdf, { onPassword, onProgress, onError }
);

  
</script>

<template>
  <div class="mx-auto" v-if="pdfLoadable">
    
    <div class="col overflow-auto">
      <div class="row-1">
        <div class="w-100 d-flex justify-content-center" id="testDiv">
          <button @click="page = page > 1 ? page - 1 : page" class="btn btn-secondary">Prev</button>
          <span class="mx-3 my-2">{{ page }} / {{ pages }}</span>
          <button @click="page = page < pages ? page + 1 : page" class="btn btn-secondary">Next</button>
          <button @click="scale = scale > 0.25 ? scale - 0.25 : scale" class="btn btn-secondary ms-3">
            -
          </button>
          <span class="mx-3 my-2">{{ scale * 100 }}%</span>
          <button @click="scale = scale < 3 ? scale + 0.25 : scale" class="btn btn-secondary">
            +
          </button>
        </div>
        
      </div>
      <VuePDF class="d-flex justify-content-center" :pdf="pdf" :page="page" :scale="scale" id="main-pdf" />
    </div>
  </div>
  <div class="mx-auto d-flex flex-column" v-else>
    <h5>Loading PDF error/Book missing PDF</h5>
    <h6>{{ loadError }}</h6>
  </div>
</template>