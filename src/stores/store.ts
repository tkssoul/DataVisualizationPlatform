import { defineStore } from 'pinia'

export const useDataStore = defineStore('data', {
  state: () => ({
    sharedData: {} as object,
  }),
  actions: {
    setSharedData(data:object) {
      this.sharedData = data
    },
  },
})
