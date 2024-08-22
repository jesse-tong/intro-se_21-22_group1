import { defineStore } from "pinia";

export const MiscStore = defineStore("misc", {
    state: () => ({
        currency: '',
    }),
});