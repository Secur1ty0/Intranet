@echo off
echo ----------------------------------------获取当前操作系统的版本号----------------------------------------------------------------->>%~dp0\info.txt
ver>>%~dp0\info.txt
echo -----------------------------------------获取当前机器可用的凭据------------------------------------------------------------------->>%~dp0\info.txt
cmdkey /list>>%~dp0\info.txt
echo --------------------------------------------获取当前机器注册表密码内容------------------------------------------------------------->>%~dp0\info.txt
REG query HKCU /v "pwd" /s>>%~dp0\info.txt
echo ------------------------------------------------获取当前机器所有盘符---------------------------------------------------------------->>%~dp0\info.txt
fsutil fsinfo drives>>%~dp0\info.txt
echo ----------------------------------------------获取当前机器用户登陆的信息------------------------------------------------------------>>%~dp0\info.txt
quser>>%~dp0\info.txt
::echo ----------------------------------------------获取当前域管理员组(enterprise admins)------------------------------------------------->>%~dp0\info.txt
::net group "enterprise admins" /domain>>%~dp0\info.txt
REM:域控使用
::echo -------------------------------------------------------------------获取当前域管理员组(domain admins)-------------------------------------->>%~dp0\info.txt
::net group "domain admins" /domain>>%~dp0\info.txt
REM:域控使用
echo -------------------------------------------------------------获取当前机器本地管理员组----------------------------------------------------->>%~dp0\info.txt
net localgroup administrators /domain>>%~dp0\info.txt
echo ---------------------------------------------------------------获取当前域时间服务器------------------------------------------------------->>%~dp0\info.txt
net time>>%~dp0\info.txt
echo ----------------------------------------------------------------获取当前机器网络连接状态--------------------------------------------------->>%~dp0\info.txt
netstat -an>>%~dp0\info.txt
echo -------------------------------------------------------------------获取当前机器IP配置详细信息---------------------------------------------->>%~dp0\info.txt
ipconfig /all>>%~dp0\info.txt
echo ---------------------------------------------------------------------获取当前机器的计算机列表---------------------------------------------->>%~dp0\info.txt
net view>>%~dp0\info.txt
echo --------------------------------------------------------------------------获取当前域中的计算机列表------------------------------------------>>%~dp0\info.txt
net view /domain>>%~dp0\info.txt
echo ----------------------------------------------------------------获取当前域组--------------------------------------------------------------->>%~dp0\info.txt
net group /domain>>%~dp0\info.txt
echo ------------------------------------------------------------------获取域控制器------------------------------------------------------------->>%~dp0\info.txt
net group "Domain Controllers" /domain>>%~dp0\info.txt
echo ---------------------------------------------------------------------获取详细任务信息------------------------------------------------------->>%~dp0\info.txt
tasklist /v>>%~dp0\info.txt
echo -----------------------------------------------------------------------获取共享信息--------------------------------------------------------->>%~dp0\info.txt
net share >>%~dp0\info.txt
echo ----------------------------------------------------------------------获取服务信息--------------------------------------------------------->>%~dp0\info.txt
net start >>%~dp0\info.txt
echo ---------------------------------------------------------------------打印路由表------------------------------------------------------------->>%~dp0\info.txt
route print>>%~dp0\info.txt
echo ----------------------------------------------------------------------获取域信任信息-------------------------------------------------------->>%~dp0\info.txt
nltest /domain_trusts>>%~dp0\info.txt
echo ------------------------------------------------------------------------获取域控列表------------------------------------------------------------>>%~dp0\info.txt
nltest /dclist>>%~dp0\info.txt
echo ------------------------------------------------------------------------获取当前域所有机器----------------------------------------------------------->>%~dp0\info.txt
dsquery computer>>%~dp0\info.txt
echo ----------------------------------------------------------------------------获取域联系人------------------------------------------------------------>>%~dp0\info.txt
dsquery contact>>%~dp0\info.txt
echo -------------------------------------------------------------------------获取该域内网段划分------------------------------------------------------------>>%~dp0\info.txt
dsquery subnet>>%~dp0\info.txt
echo --------------------------------------------------------------------获取该域内分组--------------------------------------------------------------------->>%~dp0\info.txt
dsquery group>>%~dp0\info.txt
echo ------------------------------------------------------------------获取该域内组织单位------------------------------------------------------------------->>%~dp0\info.txt
dsquery ou>>%~dp0\info.txt
echo -----------------------------------------------------------------搜索域中所有站点的名称----------------------------------------------------------------->>%~dp0\info.txt
dsquery site>>%~dp0\info.txt
echo ----------------------------------------------------------------获取该域内域控制器---------------------------------------------------------------------->>%~dp0\info.txt
dsquery server>>%~dp0\info.txt
echo ---------------------------------------------------------------获取该域内用户-------------------------------------------------------------------------->>%~dp0\info.txt
dsquery user>>%~dp0\info.txt
echo dsquery quota-------------------------------------------------------------------------------------------------------------------------------------->>%~dp0\info.txt
dsquery quota>>%~dp0\info.txt 
echo dsquery partition---------------------------------------------------------------------------------------------------------------------------------->>%~dp0\info.txt
dsquery partition>>%~dp0\info.txt
echo -------------------------------------------------------获取当前域用户名------------------------------------------------------------------------------>>%~dp0\info.txt
net group "domain users" /domain>>%~dp0\info.txt
echo ---------------------------------------------------------------获取当前计算机名---------------------------------------------------------------->>%~dp0\info.txt
net group "Domain Computers" /domain>>%~dp0\info.txt
echo ---------------------------------------------------------------获取当前机器网段内所有活跃的IP地址---------------------------------------------------------------->>%~dp0\info.txt
arp -a>>%~dp0\info.txt
exit
