<template>
  <div>
    <header class="header">
      <h1>数据掌控者 电商转化革命</h1>
    </header>

    <section class="container">
      <!-- 左容器 -->
      <section class="itemLeft">
        <ItemPage>
          <ItemLeftTop/>
        </ItemPage>
        <ItemPage>
          <ItemLeftCenter/>
        </ItemPage>
        <ItemPage>
          <ItemLeftBottom/>
        </ItemPage>
      </section>
      <!-- 中容器 -->
      <section class="itemCenter">
        <MapPage></MapPage>
        <ItemCenterBottom></ItemCenterBottom>
      </section>
      <!-- 右容器 -->
      <section class="itemRight">
        <ItemPage>
          <ItemRightTop/>
        </ItemPage>
        <ItemPage>
          <ItemRightCenter/>
        </ItemPage>
        <ItemPage>
          <ItemRightBottom/>
        </ItemPage>
      </section>
    </section>
  </div>

</template>

<script setup lang="ts">
import ItemPage from '@/components/ItemPage.vue'
import ItemLeftTop from '@/components/ItemLeftTop.vue'
import ItemLeftCenter from '@/components/ItemLeftCenter.vue'
import ItemLeftBottom from '@/components/ItemLeftBottom.vue'
import ItemRightTop from '@/components/ItemRightTop.vue'
import ItemRightCenter from '@/components/ItemRightCenter.vue'
import ItemRightBottom from '@/components/ItemRightBottom.vue'
import MapPage from '@/components/MapPage.vue'
import ItemCenterBottom from '@/components/ItemCenterBottom.vue'

import { inject } from 'vue'

let $echarts = inject('echarts')
let $axios = inject('axios')

</script>

<style lang="less">
  .header {
    height: .625rem;
    width: 100%;
    // border: 1px solid red ;
    background: url("@/assets/top.png");
    h1 {
      font-size: .375rem;
      color: #fff;
      text-align: center;
      line-height: .1875rem;
    }
  }

  .container {
      min-width: 1200px;
      max-width: 2048px;
      margin: 0;
      padding: 0;
      // border: 2px solid red;

      display: flex;
      // 设置左右页面的份数
      .itemLeft, .itemRight {
        flex: 3.5;
        margin: 0;
        padding: 0;
      }
      .itemCenter {
        flex: 4;
        // border: 1px solid red ;
        margin: 0;
        padding: .0625rem;

      }
    }
</style>