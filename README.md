# EnterpriseReportAnalysisTool



##Overview
将企业报告`pdf`使用 `pdf2htmlEX` 转换成`html文件`并抽取其中信息  

##Environment
[Python version 2.7.13](https://www.python.org/)  
[Docker version 1.12.3](https://www.docker.com/)  
[pdf2htmlEX version 0.14.6](https://github.com/coolwanglu/pdf2htmlEX)  
[pdf2htmlEX docker镜像地址](https://hub.docker.com/r/bwits/pdf2htmlex/)  

	运行时需要开启Docker服务并且拉取pdf2htmlEX镜像

##Now
完成 `第三节 会计数据和财务指标摘要`中的表格信息抽取  
发现问题：  
 
 + 有些pdf转换不成功
 + 转换出来的html存在少许字符不识别现象