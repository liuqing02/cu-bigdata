<template>
    <div>
        <h2>图表1</h2>
        <div class="leftCenterBody" id="leftCenterChart"> </div>
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, reactive } from 'vue'

var $echarts = inject('echarts');
var $axios = inject('axios');

// 数据
let data = reactive({})
let xData = reactive([])
let yDataPurchaseCount = reactive([])
let yDataCollectCount = reactive([])
let yDataClickCount = reactive([])

// 函数
async function getRequestData() {
    data = await $axios({url:"http://123.56.89.159:8888/pfcb/day"});
}

function processData() {
    xData = data.data.chartData.time;
    yDataPurchaseCount = data.data.chartData.cartCount;
    yDataCollectCount = data.data.chartData.collectCount;
    yDataClickCount = data.data.chartData.clickCount;
}

// echarts画图
onMounted(()=>{
    // 基于准备好的dom，初始化echarts实例
    var myChart = $echarts.init(document.getElementById('leftCenterChart'));

    getRequestData().then(()=> {
        processData();
            
        // 绘制图表
        const colors = ['#5470C6', '#91CC75', '#EE6666']
        myChart.setOption({
            color: colors,
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                type: 'cross'
                }
            },
            grid: {
                top: '10%',
                left: '5%',
                right: '10%', 
                bottom: '20%',
                containLabel: true
            },
            toolbox: {
                // feature: {
                //     dataView: { show: true, readOnly: false },
                //     restore: { show: true },
                //     saveAsImage: { show: true }
                // }
            },
            legend: {
                data: ['Purchase', 'Collect', 'Click']
            },
            xAxis: [
                {
                    type: 'category',
                    axisTick: {
                        alignWithLabel: true
                    },
                    // prettier-ignore
                    data: xData
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: 'Purchase',
                    position: 'right',
                    alignTicks: true,
                    axisLine: {
                            show: true,
                            lineStyle: {
                            color: colors[0]
                        }
                    },
                    axisLabel: {
                        // formatter: '{value} ml'
                    }
                },
                {
                    type: 'value',
                    name: 'Collect',
                    position: 'right',
                    alignTicks: true,
                    offset: 80,
                    axisLine: {
                        show: true,
                        lineStyle: {
                            color: colors[1]
                        }
                    },
                    axisLabel: {
                        // formatter: '{value} ml'
                    }
                },
                {
                    type: 'value',
                    name: 'Click',
                    position: 'left',
                    alignTicks: true,
                    axisLine: {
                        show: true,
                        lineStyle: {
                            color: colors[2]
                        }
                    },
                    axisLabel: {
                        // formatter: '{value} °C'
                    }
                }
            ],
            series: [
                {
                    name: 'PurchaseCount',
                    type: 'bar',
                    data: yDataPurchaseCount
                },
                {
                    name: 'CollectCount',
                    type: 'bar',
                    yAxisIndex: 1,
                    data: yDataCollectCount
                },
                {
                    name: 'ClickCount',
                    type: 'line',
                    yAxisIndex: 2,
                    data: yDataCollectCount
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
    .leftCenterBody {
        /* width: 5rem; */
        height: 3.75rem;
    }
</style>