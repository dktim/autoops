function start_node(obj){
var ip=$(obj).parent().siblings('.ip').find('ipaddress').text();
var reg=$('#regname').text()
if(window.confirm('你确定要开启交易吗？')){ 
	//alert("确定"); 
	$.get('/controller/start_node',{'ip':ip,'reg':reg},function(data){
		if(data=='success'){
			//alert('ssfsfss')
			alert('交易开启成功');
			$(obj).parent().siblings('.main_div').css("backgroundColor", "green");
			$(obj).addClass('disabled')
			$(obj).siblings('a').removeClass('disabled')
		}
		else if(data=='no such file'){
				alert('本地没有可执行脚步，请检查');
		}
		else if(data=='other failure')
		{
				alert('本地没有可执行脚步，请检查');
		}
		else{
			alert('执行失败,返回异常为'+data);
		}
		
	})
	}
else{ 
	return false; 
	} 


}




function stop_node(obj){
	var ip=$(obj).parent().siblings('.ip').find('.ipaddress').text();
	alert(ip)
	var reg=$('#regname').text()
	if(window.confirm('你确定要关闭交易吗？')){ 
		$.get('/controller/stop_node',{'ip':ip,'reg':reg},function(data){
			if(data=='success'){
				alert('交易关闭成功');
				$(obj).parent().siblings('.main_div').css("backgroundColor", "red");
				$(obj).addClass('disabled');
				$(obj).siblings('a').removeClass('disabled');
			}
			else if(data=='no such file'){


	alert('本地没有可执行脚步，请检查');


			}
			else if(data=='other failure'){


	alert('其他错误，错误描述为：'+data);


			}
			else{
				alert('执行失败'+'错误描述为：'+data);
		
				
			}
			
			
		})

		//return true; 
		}
	else{ 
		alert("取消"); 
		return false; 
		} 
var ip=$(obj).parent().siblings('.main_div').find('a').text();
var reg=$('#regname').text()

$(".bar").css("width","0px");
	  //进度条的速度，越小越快
	  var speed = 50;
	  var bar_object=$(obj).parents('table').siblings('.progressBar').children('.bar')
	  bar = setInterval(function(){
	  nowWidth = parseInt($(bar_object).width());
	   //宽度要不能大于进度条的总宽度
	   if(nowWidth<=200){
	    barWidth = (nowWidth + 1)+"px";
	    $(bar_object).css("width",barWidth);
	   }else{
	    //进度条读满后，停止
	    clearInterval(bar);
	 
	   } 
	  },speed);
	 // alert('确定要关闭吗？')

}


$('.status').click(function(){
	var ip=$(this).parents('table').siblings('.ip').text();
	var user=$(this).siblings('.upduser').text()
	//alert(user)
//	alert('!!!')
	//alert(ip)
	//alert(user)
	alert('正在启动，请稍后。')
	$.get('/controller/node_start',{'ip':ip,'user':user},function(data){
		
		if(data=='success'){
			
			alert('应用启动成功');
		}
		else if(data=='no such file'){


alert('本地没有可执行脚步，请检查');

		}
		else if(data=='other failure'){


alert('本地没有可执行脚步，请检查');

		}
		else{
			alert('执行失败'+'返回异常为'+data);
			
		}
		
		
	})
	
	
	
	
	
})

function restart_reg(obj) {
                var this_obj =$(obj)
                var regname=$('#regname').text()
                ip = $(obj).parents('td').siblings('.ip').text()
                appuser = $(obj).parents('td').siblings('.appuser').text()
                var myDate = Date.parse(new Date());
                $.ajax({
                        beforeSend : function() {
                                $('#YWaitDialog').show();
                                $(obj).attr({
                                        disabled : "disabled"
                                });
                               $("#wait").css("display","block");
                                $('#time_span').text(myDate);
				alert('task ready to sent')
                        },
                        url : '/controller/reg_restart',              
                        type : 'get',             
                        dataType : 'json',
                        data : {
                                "ip" : ip,
                                'regname':regname,
                                "appuser" : appuser,
                                'mydate' : myDate

		    },

			  success : function(data) {
				alert('goto execute get_result_method')
                       		 $("#task_id").text(data)
                        	//restart_result(data)
				alert('get_result_succ')
                        },



                         complete : function(XMLHttpRequest, textStatus) {
                                $(obj).removeAttr("disabled");
				restart_result(data)
			$("#wait").css("display","none");

                                alert("task sent..")
                        },
})

}
