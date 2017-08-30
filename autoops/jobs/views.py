from django.shortcuts import render
try:
	from cStringIO import StringIO
except ImportError:
	import StringIO
import StringIO
# Create your views here.
from django.http import StreamingHttpResponse
from autoops.oracle import OracleDb
from autoops.settings import oracle_conn
from django.shortcuts import render,render_to_response,HttpResponse
import xlsxwriter,time

def cron_job_result(request):
	db=OracleDb()
	sql="""

select * from (
SELECT a.host,a.regname ,a.jdbc,b.jms,c.jvm from  
(select HOST,REGNAME,JDBC,jdbcpoolname from (
select host ,REGNAME,jdbcpoolname,
 activecurrent||'/'||activehighcount JDBC ,row_number() over( partition by regname,host order by seqnum desc ) as row_numb
 from monitor.monitor_jdbc where tm_smp > sysdate - 15/(24*60)  and jdbcpoolname='mprac_ds_01'
  ) where row_numb = 1 ) a,
(select HOST,REGNAME,name,JMS from (
  select  HOST,REGNAME,name,
  messagescurrentcount||'/'||messageshighcount JMS ,row_number() over( partition by regname,host order by seqnum desc ) as row_numb
      from monitor.monitor_jms j where tm_smp > sysdate - 15/(24*60)  and name = 'pay_jmsmodule_01!pay_jmsqueue_01'
      ) where row_numb = 1 ) b,
(select HOST,REGNAME,JVM from (
  select  HOST,REGNAME,
  jvmfreeprecent JVM ,row_number() over( partition by regname,host order by seqnum desc ) as row_numb
      from monitor.monitor_jvm  where tm_smp > sysdate - 15/(24*60) 
      ) where row_numb = 1 ) c      
where a.host=b.host and a.regname = b.regname and a.host=c.host and a.regname=c.regname        
ORDER BY HOST,decode(REGNAME,'REG',1,'PAY',2,'WEB',3,'IPS',4,'IPW',5))
union
select * from (
SELECT a.host,a.regname ,a.jdbc,b.jms,c.jvm from  
(select HOST,REGNAME,JDBC,jdbcpoolname from (
select host ,REGNAME,jdbcpoolname,
 activecurrent||'/'||activehighcount JDBC ,row_number() over( partition by regname,host order by seqnum desc ) as row_numb
 from monitor.monitor_jdbc where tm_smp > sysdate - 15/(24*60)  and jdbcpoolname='mprac_ds_01'
  ) where row_numb = 1 ) a,
(select HOST,REGNAME,name,JMS from (
  select  HOST,REGNAME,name,
  messagescurrentcount||'/'||messageshighcount JMS ,row_number() over( partition by regname,host order by seqnum desc ) as row_numb
      from monitor.monitor_jms j where tm_smp > sysdate - 15/(24*60)  and name = 'ptc_SystemModule-0!Queue-0'
      ) where row_numb = 1 ) b,
(select HOST,REGNAME,JVM from (
  select  HOST,REGNAME,
  jvmfreeprecent JVM ,row_number() over( partition by regname,host order by seqnum desc ) as row_numb
      from monitor.monitor_jvm  where tm_smp > sysdate - 15/(24*60) 
      ) where row_numb = 1 ) c      
where a.host=b.host and a.regname = b.regname and a.host=c.host and a.regname=c.regname)
union
select * from (
SELECT a.host,a.regname ,a.jdbc,b.jms,c.jvm from  
(select HOST,REGNAME,JDBC,jdbcpoolname from (
select host ,REGNAME,jdbcpoolname,
 activecurrent||'/'||activehighcount JDBC ,row_number() over( partition by regname,host order by seqnum desc ) as row_numb
 from monitor.monitor_jdbc where tm_smp > sysdate - 15/(24*60)  and jdbcpoolname='fun_ds_01'
  ) where row_numb = 1 ) a,
(select HOST,REGNAME,name,JMS from (
  select  HOST,REGNAME,name,
  messagescurrentcount||'/'||messageshighcount JMS ,row_number() over( partition by regname,host order by seqnum desc ) as row_numb
      from monitor.monitor_jms j where tm_smp > sysdate - 15/(24*60)  and name = 'fun_SystemModule-0!Queue-0'
      ) where row_numb = 1 ) b,
(select HOST,REGNAME,JVM from (
  select  HOST,REGNAME,
  jvmfreeprecent JVM ,row_number() over( partition by regname,host order by seqnum desc ) as row_numb
      from monitor.monitor_jvm  where tm_smp > sysdate - 15/(24*60) 
      ) where row_numb = 1 ) c      
where a.host=b.host and a.regname = b.regname and a.host=c.host and a.regname=c.regname)


"""
	print sql
	output=StringIO.StringIO()
	result=db.executemany(sql)
	f_name="%s.xlsx"%(time.time())
	xls_file=xlsxwriter.Workbook(output,{'in_memory':True})
	xls_sheet=xls_file.add_worksheet()
	row=0
	col=0
	for item in result:
		xls_sheet.write(row,0,item[0])
		xls_sheet.write(row,1,item[1])
		xls_sheet.write(row,2,item[2])
		xls_sheet.write(row,3,item[3])
		xls_sheet.write(row,4,item[4])
		row+=1

	xls_file.close()

	
	output.seek(0)
	response=HttpResponse(output.read(),content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition']="attachment;filename=%s"%(f_name)
	return response
	

def regular_job(request):
	return render(request,'jobs/regular_job.html',{'str':'regular_job'})


def cron_job(request):
	return render(request,'jobs/cron_job.html',{'str':'regular_job'})

