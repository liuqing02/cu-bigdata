<template>
    <div>
        <h2>图表1</h2>
        <div class="leftTopBody" id="leftTopChart"></div>
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

// 函数
async function getRequestData() {
    data = await $axios({url:"http://123.56.89.159:8888/category/top"});
}

function processData() {
    xData = data.data.data.map(v => v.category).reverse();
    // console.log("xData", xData);
    yData = data.data.data.map(v => v.count).reverse();
}

// echarts画图
onMounted(()=>{
    // 基于准备好的dom，初始化echarts实例
    var myChart = $echarts.init(document.getElementById('leftTopChart'));

    getRequestData().then(()=> {
        processData();
        
        // 绘制图表
        myChart.setOption({
            title: {
                // text: 'ECharts'
            },
            tooltip: {},
            xAxis: {
                type: 'value',
                axisLine:{
                    lineStyle:{
                        color:"#fff"
                    }
                }
            },
            yAxis: {
                type: 'category',
                data: xData, 
                axisLine:{
                        lineStyle:{
                            color:"#fff"
                    }
                }
            },
            series: [
                {
                    name: '销量',
                    type: 'bar',
                    data: yData, 
                    barWidth: 10,
                    itemStyle: {
                        normal: {
                            barBorderRadius:[0,20,20,0],
                            color: new $echarts.graphic.LinearGradient(0, 0, 1, 0, [
                                {
                                    offset: 0,
                                    color: "#005eaa",
                                },
                                {
                                    offset: 0.5,
                                    color: "#339ca8",
                                },
                                {
                                    offset: 1,
                                    color: "#cda819",
                                },
                            ]),
                        },
                    },
                    
                }
            ], 
            grid:{
                top:"5%",
                left:"3%",
                right:"8%",
                bottom:"5%",
                containLabel:true,
            },
        });
        // //  当窗口或者大小发生改变时执行resize，重新绘制图表
        // window.addEventListener("resize", function () {
        //     $echarts.resize();
        // });
    })
})



</script>

<style lang="less">
    h2 {
        margin: 0;
        height: 0.6rem;
        color: #fff;
        line-height: 0.6rem;
        font-size: 0.25rem;
        text-align: center;
    }
    .leftTopBody {
        /* width: 5rem; */
        height: 3.125rem;
    }
</style>