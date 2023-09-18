<template>
    <div>
        <h2>图表1</h2>
        <div class="rightCenterBody" id="rightCenterChart"> </div>
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, reactive } from 'vue'

var $echarts = inject('echarts');
var $axios = inject('axios');

// 数据
let data = reactive({})
let xData = reactive([])
let yData = reactive([])
let hotData = reactive([])

// 函数
async function getRequestData() {
    data = await $axios({url:"http://123.56.89.159:8888/heatmap"});
}

function processData() {
    console.log(data.data)
    xData = data.data.xChartData;
    console.log("xDataRi", xData)
    yData = data.data.yChartData
    hotData = data.data.data


    // console.log("xDataRi1111", xData)
    // yDataPurchaseCount = data.data.chartData.cartCount;
    // yDataCollectCount = data.data.chartData.collectCount;
    // yDataClickCount = data.data.chartData.clickCount;
}

// echarts画图
onMounted(()=>{
    // 基于准备好的dom，初始化echarts实例
    var myChart = $echarts.init(document.getElementById('rightCenterChart'));

    getRequestData().then(()=> {
        processData();

        // 绘制图表
        const hours = xData;
        // prettier-ignore
        const days = yData;
        // prettier-ignore
        const data = hotData
            .map(function (item) {
            return [item[1], item[0], item[2] || '-'];
        });
        myChart.setOption({
            tooltip: {
                position: 'top'
            },
            grid: {
                height: '50%',
                right: '5%',
                top: '10%'
            },
            xAxis: {
                type: 'category',
                data: hours,
                splitArea: {
                show: true
                }
            },
            yAxis: {
                type: 'category',
                data: days,
                splitArea: {
                show: true
                },
                axisLine:{
                        lineStyle:{
                            color:"#fff"
                    }
                }
            },
            visualMap: {
                min: 0,
                max: 1,
                calculable: true,
                orient: 'horizontal',
                left: 'center',
                bottom: '15%'
            },
            series: [
                {
                name: 'Punch Card',
                type: 'heatmap',
                data: data,
                label: {
                    show: true
                },
                emphasis: {
                    itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
                }
            ]
        })
        
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
    .rightCenterBody {
        margin: 0;
        /* width: 5rem; */
        height: 3.75rem;
    }
</style>