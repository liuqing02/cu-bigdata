<template>
  <div>
      <h2>图表1</h2>
      <div class="rightBottomBody" id="rightBottomChart"></div>
  </div>
</template>

<script setup lang="ts">
import { inject, onMounted, reactive } from "vue";


let $echarts = inject('echarts');
let $axios = inject('axios');

// 数据
let data = reactive({})
let xData = reactive([])
let yData = reactive([])

//函数
async function getRequestData() {
//   data = await $axios({url:"/rightTopChartData"})
}

function processData() {
//   xData = data.data.chartData.list.map(v => v.name);
//   yData = data.data.chartData.list.map(v => v.value)
}

onMounted(()=>{
  getRequestData().then(()=>{
        // processData();

        // 基于准备好的dom，初始化echarts实例
        var myChart = $echarts.init(document.getElementById('rightBottomChart'));
        // 绘制图表
        myChart.setOption({     
            title: {
                text: 'Funnel Compare',
                subtext: 'Fake Data',
                left: 'left',
                top: 'bottom'
            },
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b} : {c}%'
            },
            toolbox: {
                show: true,
                orient: 'vertical',
                top: 'center',
                // feature: {
                //     dataView: { readOnly: false },
                //     restore: {},
                //     saveAsImage: {}
                // }
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: ['Prod A', 'Prod B', 'Prod C', 'Prod D', 'Prod E']
            },
            series: [
                {
                    name: 'Funnel',
                    type: 'funnel',
                    width: '25%',
                    height: '45%',
                    left: '20%',
                    top: '50%',
                    funnelAlign: 'right',
                    data: [
                        { value: 60, name: 'Prod C' },
                        { value: 30, name: 'Prod D' },
                        { value: 10, name: 'Prod E' },
                        { value: 80, name: 'Prod B' },
                        { value: 100, name: 'Prod A' }
                    ]
                },
                {
                    name: 'Pyramid',
                    type: 'funnel',
                    width: '25%',
                    height: '45%',
                    left: '20%',
                    top: '5%',
                    sort: 'ascending',
                    funnelAlign: 'right',
                    data: [
                        { value: 60, name: 'Prod C' },
                        { value: 30, name: 'Prod D' },
                        { value: 10, name: 'Prod E' },
                        { value: 80, name: 'Prod B' },
                        { value: 100, name: 'Prod A' }
                    ]
                },
                {
                    name: 'Funnel',
                    type: 'funnel',
                    width: '25%',
                    height: '45%',
                    left: '60%',
                    top: '5%',
                    funnelAlign: 'left',
                    data: [
                        { value: 60, name: 'Prod C' },
                        { value: 30, name: 'Prod D' },
                        { value: 10, name: 'Prod E' },
                        { value: 80, name: 'Prod B' },
                        { value: 100, name: 'Prod A' }
                    ]
                },
                {
                    name: 'Pyramid',
                    type: 'funnel',
                    width: '25%',
                    height: '45%',
                    left: '60%',
                    top: '50%',
                    sort: 'ascending',
                    funnelAlign: 'left',
                    data: [
                        { value: 60, name: 'Prod C' },
                        { value: 30, name: 'Prod D' },
                        { value: 10, name: 'Prod E' },
                        { value: 80, name: 'Prod B' },
                        { value: 100, name: 'Prod A' }
                    ]
                }
            ]
        });
    })
})

</script>

<style lang="less" scoped>
  h2 {
      margin: 0;
      height: 0.6rem;
      color: #fff;
      line-height: 0.6rem;
      font-size: 0.25rem;
      text-align: center;
  }
  .rightBottomBody {
      margin: 0px;
      height: 3.125rem;
  }

</style>