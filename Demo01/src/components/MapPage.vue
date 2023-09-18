<template>
    <div>
        <h2>图表1</h2>
        <div class="mapBody" id="map"></div>
    </div>
</template>

<script setup lang="ts">
import axios from "axios";
import { inject, onMounted, reactive } from "vue";


// 数据
let mapData = reactive({});
let $echarts = inject('echarts');

// 函数
async function getRequestData() {
    mapData = await axios({url:"/map/china-cities.json"})
}

onMounted(()=>{
    getRequestData().then(()=>{
        $echarts.registerMap("china", mapData.data);
        let myChart = $echarts.init(document.getElementById("map"));

        myChart.setOption({
            tooltip:{
                trigger:"item"
            },
            geo: {
                map: "china", 
                itemStyle: {
                    areaColor: "#0099ff",
                    borderColor: "#00ffff",
                    shadowColor: "rgba(230,130,70,0.5)",
                    shadowBlur: 30,
                    emphasis: {
                        focus: "self",
                    },
                },
            },
            title:{
                // text:"城市销量",
                // left:"45%",
                // textStyle:{
                //     color:"#fff",
                //     fontSize:20,
                //     textShadowBlur:10,
                //     textShadowColor:"#33ffff"
                // }
            },
        
            // 散点图    
            visualMap:{
                type:"continuous",
                min:100,
                max:5000,
                calculable:true,
                // inRange:{
                //     color:["#50a3ba","#eac736","#d94e5d"],
                // },
                textStyle:{
                    color:"#fff"
                }
                
            },   
            series: [
            {
                type: "scatter",
                itemStyle: {
                    color: "red",
                },
                coordinateSystem:"geo",
                data: [
                    { name: "北京", value: [116.46, 39.92, 4367] },
                    { name: "上海", value: [121.48, 31.22, 8675] },
                    { name: "深圳", value: [114.07, 22.62, 2461] },
                    { name: "广州", value: [113.23, 23.16, 187] },
                    { name: "西安", value: [108.45, 34, 3421] },
                ],
                },
            ],
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
        font-size: .375rem;
        text-align: center;
    }
    .mapBody {
        // border: 1px solid red;
        height: 7.5rem;
    }
</style>