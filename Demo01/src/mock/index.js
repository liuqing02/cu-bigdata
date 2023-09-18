import Mock from 'mockjs'

// let data = Mock.mock({
//     string|4:'hello'
// })

// let data = Mock.mock({
//     'string|5': '@cword(3, 10)'
// })

// let data = Mock.mock({
//     'title': '@ctitle(3)',
//     'sentence': '@csentence(6)', 
//     'paragraph': '@paragraph(10)'
// })

// let data = Mock.mock({
//     'number|1-1000': 1
// })

// let data = Mock.mock({
//     'id': '@increment(5)'
// })

// let data = Mock.mock({
//     'name': '@cname', 
//     'id': '@id', 
//     'city': '@city(true)'
// })

// let data = Mock.mock({
//     'date': '@date '
// })

// let data = Mock.mock({
//     'list|3': [
//         {
//             'name': '@cname', 
//             'id': '@increment', 
//             'city': '@city(true)'
//         }
//     ]
// })

// Mock.mock('/api/news', 'get', {
//     status: 200, 
//     msg: '获取数据成功'
// })

// Mock.mock('/api/post/news', 'post', {
//     status: 200, 
//     msg: 'post获取数据成功'
// })

// let newsList = Mock.mock({
//     'list|3': [
//         {
//             'id': '@increment', 
//             'title': '@ctitle', 
//             'content': '@cparagraph(2)', 
//             'img_url': 'http://github.com', 
//             'add_time': '@date'
//         }
//     ]
// })


// 左上
let leftTopChartData = Mock.mock({
    'list|7': [
        {
            'title': '@cname(2)', 
            'num': '@integer(500,3000)'
        }
    ]
})
Mock.mock('/leftTopChartData', 'get', (options)=>{
    return {
        'status': 200, 
        'chartData': leftTopChartData
    }
})

// 左下
let leftBottomChartData = {
    'day': ["星期1","星期2","星期3","星期4","星期5","星期6","星期7"],
    'num': [
        Mock.mock({'colthes|6':['@integer(10, 100)']}),
        Mock.mock({'digit|6':['@integer(10, 100)']}),
        Mock.mock({'electrical|6':['@integer(10, 100)']}),
        Mock.mock({'gear|6':['@integer(10, 100)']}),
        Mock.mock({'chemicals|6':['@integer(10, 100)']}),
    ],
}
Mock.mock('/leftBottomChartData', 'get', ()=>{
    return {
        'status': 200, 
        'chartData': leftBottomChartData
    }
})

// 右上
let rightTopChartData = Mock.mock({
    'list|6': [
        {
            'name':'@cword(2)',
            'value':'@integer(50, 600)', 
        }
    ]
})
Mock.mock('/rightTopChartData', 'get', (options)=>{
    return {
        'status': 200, 
        'chartData': rightTopChartData
    }
})