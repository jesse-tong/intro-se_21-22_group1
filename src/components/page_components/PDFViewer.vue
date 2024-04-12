<script setup>
import { ref } from "vue";
import { VuePDF, usePDF } from "@tato30/vue-pdf";

const page = ref(1);
const scale = ref(1);
const currentFileIdx = ref(0);

  const props =  defineProps({
      pdf: String,
   });
  const { pdf, pages } = usePDF(
    props.pdf,
  );

  
</script>

<template>
  <div class="row">
    
    <div class="col">
      <div>
        <button @click="page = page > 1 ? page - 1 : page" class="btn btn-secondary">Prev</button>
        <span>{{ page }} / {{ pages }}</span>
        <button @click="page = page < pages ? page + 1 : page" class="btn btn-secondary">Next</button>
        <button @click="scale = scale > 0.25 ? scale - 0.25 : scale" class="btn btn-secondary ms-3">
          -
        </button>
        <span>{{ scale * 100 }}%</span>
        <button @click="scale = scale < 2 ? scale + 0.25 : scale" class="btn btn-secondary">
          +
        </button>
      </div>
      <VuePDF :pdf="pdf" :page="page" :scale="scale" />
    </div>
  </div>
</template>