#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

'''---------------------------------------- 使用方法 ----------------------------------------'''
# 方法一：file.py方式，因为每次执行更新都需要命令行去执行 (不推荐)
    # 1.文件导入：把当前文件导入到要一键更新的模块中，保证[当前文件]和[模块.podsepc文件]在同一个根路径下
    # 2.变量配置：配置pod_repo_name、pod_repo_url、pod_spec_file
    # 3.执行：1.cd dirs  2.python3 ./fileName.py
# 方法二：file.command方式推荐，每次执行只需要双击即可 (推荐)
    # 1.把当前文件导入到要一键更新的模块中，保证[当前文件]和[模块.podsepc文件]在同一个根路径下
    # 2.变量配置：配置pod_repo_name、pod_repo_url、pod_spec_file 
    #           要在当前文件最顶部导入<#!/usr/bin/env python3>命令
    #           再导入os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    #           把文件后缀修改为command
    #           打开终端，执行chmod +x file.command，注意只需执行一次即可，后续不需要再处理。
    # 3.执行：双击文件即可

'''--------------------------------------- 需配置的参数 --------------------------------------'''
# 远程私有索引库的名称[这个变量才是真正决定要把当前podspec文件上传到哪个远端索引库的决定性参数]
pod_repo_name =  '私有索引库的名称'
# 远程私有库的地址[这个地址虽然是私有索引库的地址，但不决定上传问题，仅仅用于校当前podspec文件中的依赖库能否找到而已]
pod_repo_url = '远端私有库的地址'
# podspec文件名称
pod_spec_file = '要上传的podspec文件名称'


'''----------------------------------------- 开始 ------------------------------------------'''
# ------- 定义全局常量 --------#
# tag版本
tag_version = ''
# 远端公共索引库地址[同样不决定上传问题，仅仅用于校当前podspec文件中的依赖库能否找到而已]
pod_public_repo_url = 'http://192.168.76.214:9091/ios/demo_zjh/podrepo.git'
# podspec相对路径
pod_spec_file_path = './' + pod_spec_file

# ------ def update methods -------#
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

def deal_update():
    git_deal()
    pod_deal()

# ------ def pod methods -------#
def get_pod_version():
    file = open(pod_spec_file_path)
    for line in file:
        #version
        if find_pod_key(line,".version"):
            global tag_version
            start_idx = line.find('"') + 1
            end_idx = line.rfind('"')
            tag_version = line[start_idx:end_idx]
        #source
        if find_pod_key(line,".source"):
            start_idx = line.find('"') + 1
            end_idx = line.rfind('"')
    file.close()

def pod_lint():
    log_waiting('③:正在校验'+pod_spec_file)
    if len(pod_spec_file) == 0:
        log_error('Error:未在当前脚本文件中设置cocoapods的x.podspec描述文件，去设置pod_spec_file');
        os.sys.exit()
    if len(pod_repo_name) == 0:
        log_error('Error:未在当前脚本文件中设置远程私有库的名称，去设置pod_repo_name');
        os.sys.exit()
    if len(pod_repo_url) == 0:
        log_error('Error:未在当前脚本文件中设置远程私有库地址，去设置pod_repo_url');
        os.sys.exit()
    commad = 'pod spec lint' + ' ' + pod_spec_file + ' ' + '--sources=' + pod_repo_url + ',' + pod_public_repo_url + ' ' + '--verbose --allow-warnings'
    os.system(commad)

def pod_push():
    log_waiting('④:上传当前' + pod_spec_file + '文件至{0}私有库'.format(pod_repo_name))
    commad = 'pod repo push' + ' ' + pod_repo_name + ' ' + pod_spec_file + ' ' + '--sources=' + pod_repo_url + ',' + pod_public_repo_url + ' ' + '--allow-warnings'
    os.system(commad)

def pod_deal():
    pod_lint()
    pod_push()

def find_pod_key(line,key):
    return line.find(key) != -1 and line.find(key) < line.find('=')


# ------ def git methods -------#
def git_push():
    log_waiting('①:我们提交的Git的代码正在上传中')
    # 获取当前正在激活使用分支中最新的历史版本(git symbolic-ref方法是获取HEAD的指向引用)
    head = os.popen('git symbolic-ref --short -q HEAD')
    head_result = head.read()
    head.close()
    if len(head_result) != 0:
        push_commad = 'git push origin ' + head_result
        os.system(push_commad)
    else:
      log_error('Error:[GIT] --> HEAD 错误; From commad{git symbolic-ref --short -q HEAD}')
      os.sys.exit()
    return

def git_tag():
    log_waiting('②:正在给我们的提交的代码打上Git标签')
    get_pod_version()
    print('MyLog:要生成tag标签的版本为:<{0}>'.format(tag_version))
    add_local_tag_commad = 'git tag ' + tag_version
    os.system(add_local_tag_commad)
    push_remote_tag_commad = 'git push origin ' + tag_version
    os.system(push_remote_tag_commad)
    return

def git_deal():
 	git_push()
 	git_tag()
 	return

# ------ def log methods ------#
def log_waiting( str ):
	print("\033[1;36;40mMy_LOG: {0}\033[0m".format(str) + "\033[5;36;40m···  \033[0m")
def log_success( str ):
	print("\033[42;1mMy_LOG: {0}  \033[0m".format(str))
def log_error( str ):
	print("\033[22;31;40mMy_LOG:[error]:{0}  \033[0m".format(str))


'''------------------------------------------ 执行函数 ---------------------------------------'''
deal_update()