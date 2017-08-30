
var options_jms = {
    chart: {
        renderTo: 'jms_container',
        type: 'line',
        marginRight: 90,
        marginBottom: 50
    },
    title: {
        text: "<b>single_machine_jms</b>",
        x: -20 //center
    },
    xAxis: {
        categories: []
    },
    yAxis: {
        title: {
            text: 'Y',
        },
        min: 0,
        max: 300,
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },
    tooltip: {
        formatter: function() {
                return '<b>'+ this.series.name +'</b><br/>'+
                this.x +': '+ this.y;
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                enabled: true,
                formatter: function() {
                        return this.y;
                },
            },
            enableMouseTracking: true
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: -10,
        y: 100,
        borderWidth: 0
    },
    series: []
};



function single_jms(){
var ip=$("#ip").text()
var reg=$("#reg").text()
    jQuery.ajax({
        url: "/monitor/single_machine_jms_state",
        data: {'ip':ip,'reg':reg},
        type:"get",
        dataType:"json",
        success: function(data){
                if (data.count.length==0){

alert("None")}
                else{
                        var time_list=data["time"]
//alert(time_list)
                var count = data["count"]
//	alert(count)
                options_jms.xAxis.categories = time_list;
                options_jms.series=count;
  //        	alert(count)
                var chart_jms = new Highcharts.Chart(options_jms);
                
        
                }
            
            
        },
        failure : function(messages) {
            alert(message);
        }
    });
}

