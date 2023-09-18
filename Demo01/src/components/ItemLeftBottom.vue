<template>
    <div>
        <h1>图表</h1>
        <div class="leftBottomBody" id="leftBottomChart"></div>
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, reactive } from "vue";

let $echarts = inject('echarts')
let $axios = inject('axios')

// 数据
let data = reactive({})
let xData = reactive([])
let legendData = reactive([])

let seriesFirstName = reactive([])
let seriesFirstData = reactive([])
let seriesSecondName = reactive([])
let seriesSecondData = reactive([])
let seriesThirdName = reactive([])
let seriesThirdData = reactive([])
let seriesFourthName = reactive([])
let seriesFourthData = reactive([])


// 函数
async function getRequestData() {
    data = await $axios({url: 'http://123.56.89.159:8888/pfcb/minute'})
}
function processData() {
    xData = data.data.chartData.time;
    legendData = data.data.chartData.num.map(v => v.name)
    seriesFirstName = data.data.chartData.num[0].name
    seriesFirstData = data.data.chartData.num[0].value
    seriesSecondName = data.data.chartData.num[1].name
    seriesSecondData = data.data.chartData.num[1].value
    seriesThirdName = data.data.chartData.num[2].name
    seriesThirdData = data.data.chartData.num[2].value
    seriesFourthName = data.data.chartData.num[3].name
    seriesFourthData = data.data.chartData.num[3].value
}

onMounted(()=>{
    getRequestData().then(()=>{
        processData();
        // 基于准备好的dom，初始化echarts实例
        var myChart = $echarts.init(document.getElementById('leftBottomChart'));
        // 绘制图表
        myChart.setOption({
            title: {
                // text: 'Stacked Line'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: legendData  // legendData
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {
                feature: {
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: xData,  // xData
                axisLine:{
                        lineStyle:{
                            color:"#fff"
                    }
                }
            },
            yAxis: {
                type: 'value',
                axisLine:{
                        lineStyle:{
                            color:"#fff"
                    }
                }
            },
            series: [
                {
                    name: seriesFirstName,
                    type: 'line',
                    stack: 'Total',
                    data: seriesFirstData
                },
                {
                    name: seriesSecondName,
                    type: 'line',
                    stack: 'Total',
                    data: seriesSecondData
                },
                {
                    name: seriesThirdName,
                    type: 'line',
                    stack: 'Total',
                    data: seriesThirdData
                },
                {
                    name: seriesFourthName,
                    type: 'line',
                    stack: 'Total',
                    data: seriesFourthData
                }
            ]
        }); 
    });

})
</script>

<style lang="less" scoped>
    .leftBottomBody {
        /* margin: 0; */
        /* width: 5rem; */
        height: 3.125rem;
    }
</style>