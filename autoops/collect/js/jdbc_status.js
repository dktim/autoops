var options_cpu = {
    chart: {
        renderTo: 'container1',
        type: 'line',
        marginRight: 90,
        marginBottom: 50
    },
    title: {
        text: '<b>JDBC活动连接数量</b>',
        x: -20 //center
    },
    xAxis: {
        categories: []
    },
    yAxis: {
        title: {
            text: '活动连接数量 （个）'
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

function get_jdbc_state_at_start(){
	var reg=$('#regname').text()
    jQuery.ajax({
        url: "/monitor/get_jdbc1_state_at_start",
        data: {'reg':reg},
        type:"get",
        dataType:"json",
        success: function(data){
        	if (data.count.length==0){
        		options_cpu.xAxis.categories =[];
                options_cpu.series=[];
                var chart_cpu = new Highcharts.Chart(options_cpu);
        	}
        	else{
        		var time_list=data["time"]
                var count = data["count"]
                options_cpu.xAxis.categories = time_list;
                options_cpu.series=count;
                var chart_cpu = new Highcharts.Chart(options_cpu);
        	}
        },
        failure : function(messages) {
            alert(message);
        }
    });
}

function queryFirewallState(){
	var start=$('#d28').val()
	var type=$('#jdbc').text()
	var stop=$('#d29').val()
	var reg=$('#regname').text()
	var ip=$("#ipaddress  option:selected").text();
	jQuery.ajax({
	    url: "/monitor/get_jdbc_state",
	    data: {"start" : start, "stop" : stop,"ip":ip,'type':type,'reg':reg},
	    type:"get",
	    dataType:"json",
	 	success: function(data){
	 		if (data.count.length==0 ||data.time.length==0){
        		options_cpu.xAxis.categories =[];
                options_cpu.series=[];
                var chart_cpu = new Highcharts.Chart(options_cpu);
        	}
	 		else{
	 			var time_list=data["time"]
		 		var count = data["count"]
	 			options_cpu.xAxis.categories = time_list;
                options_cpu.series=count;
		 		var chart_cpu = new Highcharts.Chart(options_cpu);
	 		}
	 	
	    },
	    failure : function(messages) {
			alert(message);
	    }
	});
}

<!--

function Dsy() 
{ 
this.Items = {}; 
} 
Dsy.prototype.add = function(id,iArray) 
{ 
this.Items[id] = iArray; 
} 
Dsy.prototype.Exists = function(id) 
{ 
if(typeof(this.Items[id]) == "undefined") return false; 
return true; 
} 
function change(v){ 
var str="0"; 
for(i=0;i<v;i++){ str+=("_"+(document.getElementById(s[i]).selectedIndex-1));}; 
var ss=document.getElementById(s[v]); 
with(ss){ 
length = 0; 
options[0]=new Option(opt0[v],opt0[v]); 
if(v && document.getElementById(s[v-1]).selectedIndex>0 || !v) 
{ 
if(dsy.Exists(str)){ 
ar = dsy.Items[str]; 
for(i=0;i<ar.length;i++)options[length]=new Option(ar[i],ar[i]); 
if(v)options[1].selected = true; 
} 
} 
if(++v<s.length){change(v);} 
} 
} 
var dsy = new Dsy(); 
dsy.add("0",["CCS","CCAVER","CMS","CLUB","WEBSERVER","BKG","MAL","URMOLN","GME","WAP2","FILSVR","RPT","POSP","FIL","PMCOLN","IPS","IPW","PAY","REG","WEB","PTF","PES","CGW","DWGW","UPGW","OPEN","SLINK"]); 
dsy.add("0_0",["ccs"]); 
dsy.add("0_1",["CCAVER"]); 
dsy.add("0_1_0",["CCAVER1","CCAVER1","CCAVER3"]); 
dsy.add("0_2",["CMS"]); 
dsy.add("0_2_0",["CMS1","CMS1","CMS3"]); 

var s=["province","city","county"]; 
var opt0 = ["集群","实例","连接池"]; 
function setup() 
{ 
for(i=0;i<s.length-1;i++) 
document.getElementById(s[i]).onchange=new Function("change("+(i+1)+")"); 
change(0); 
} 

-->
