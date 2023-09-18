<template>
  <router-view></router-view>
</template>

<script setup lang="ts">
import { provide } from 'vue';
import * as echarts from 'echarts'
import axios from 'axios'

name: 'App';

provide('echarts', echarts)
provide('axios', axios)
// axios.defaults.baseURL = ""

</script>

<style>
  body {
    background: url("@/assets/pageBg.png");
    border: none !important;
  }
</style>
