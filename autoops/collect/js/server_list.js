function get_history_cmd(obj)
{	
	reg=$('#regname').text()
	var ip=$(obj).parent().siblings('.ip').find('.ipaddress').text();
	$.ajax({
		url:'/monitor/get_reg_action_history',
		data:{'reg':reg,'ip':ip},
		datatype:'json',
		type:"GET",
		success:function(data){
			var len=data.length
			alert(len)
			htmls=""
			for(i=0;i<len;i++){
				htmls=htmls+"<tr>+<td>"+data[i].username+"</td>"+"<td>"+data[i].regname+"</td>"+"<td>"+data[i].cmd+"</td>"+"<td>"+data[i].cmd_time+"</td>"+"</tr>"
				}
				$(".history1").html(htmls)
			}			
		})
	
	}	










function start_node(obj){
var ip=$(obj).parent().siblings('.ip').find('.ipaddress').text();
var reg=$('#regname').text()
alert(ip)
if(window.confirm('你确定要开启交易吗？')){ 
	//alert("确定"); 
	$.get('/controller/start_node',{'ip':ip,'reg':reg},function(data){
		if(data=='success'){
			alert('交易开启成功');	
	var ip=$(obj).parent().siblings('.ip').find('.ipaddress').removeclass('btn danger')
	var ip=$(obj).parent().siblings('.ip').find('.ipaddress').addclass('btn success')
		$(obj).addClass('disabled')
			//$(obj).siblings('a').removeClass('disabled')
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
				var ip=$(obj).parent().siblings('.ip').find('.ipaddress').removeclass('btn success')
				var ip=$(obj).parent().siblings('.ip').find('.ipaddress').addclass('btn danger')
		$(obj).addClass('disabled')
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
		}
	else{ 
		alert("取消"); 
		return false; 
		} 
}


