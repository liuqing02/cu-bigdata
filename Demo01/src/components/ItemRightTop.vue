<template>
    <div>
        <h2>图表1</h2>
        <div class="rightTopBody" id="rightTopChart"></div>
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
    data = await $axios({url:"http://123.56.89.159:8888/variety"})
}

function processData() {
    xData = data.data.chartData.map(v => v.name);
    yData = data.data.chartData.map(v => v.value)
}

onMounted(()=>{
    getRequestData().then(()=>{
        processData();
        // 基于准备好的dom，初始化echarts实例
        var myChart = $echarts.init(document.getElementById('rightTopChart'));
        // 绘制图表
        myChart.setOption({
            title: {
            },
            legend: {
                orient: 'vertical',
                left: 'left'
            },
            toolbox: {
                show: true,
                feature: {
                    // mark: { show: true },
                    // dataView: { show: true, readOnly: false },
                    // restore: { show: true },
                    // saveAsImage: { show: true }
                }
            },
            
            series: [
                {
                    name: 'Nightingale Chart',
                    type: 'pie',
                    radius: [5, 90],
                    center: ['60%', '50%'],
                    roseType: 'area',
                    itemStyle: {
                        borderRadius: 3
                    },
                    data: data.data.chartData,
                }
            ], 
            grid:{
                top:"1%",
                left:"1%",
                right:"1%",
                bottom:"1%",
                containLabel:true

            }, 
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
        // border: 1px solid red;
    }
    .rightTopBody {
        margin: 0px;
        height: 3.125rem;
    }
    
</style>