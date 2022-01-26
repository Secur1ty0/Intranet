import sys, os, subprocess


def create_file():
    cmd = "schtasks /query /fo LIST /v > temp.txt"
    p = subprocess.Popen (cmd, shell=True, encoding="UTF-8", errors="ignore", stdout=subprocess.PIPE)
    out = p.stdout.readlines ()


def accessChk_en(dict_all):
    new_dict = []
    print ("--------------------------------------------------------------------------\n")
    for da in dict_all:
        # 根据\判断是否存在路径，不存在则增加默认路径%windir%\system32\
        if "\\" in da["Task To Run"]:
            cmd = "accesschk.exe  /accepteula -uwqv \"" + da["Task To Run"] + "\""
        else:
            cmd = "accesschk.exe  /accepteula -uwqv " + "%windir%\\system32\\\"" + da["Task To Run"] + ".exe\""
        p = subprocess.Popen (cmd, shell=True, encoding="UTF-8", errors="ignore", stdout=subprocess.PIPE)
        out0 = p.stdout.readlines ()
        out = "".join (out0).split ("www.sysinternals.com\n")[1]

        # 返回的结果
        print ("执行命令:\n", cmd)
        print ("作为用户运行:", da["RunAsUser"])
        print ("执行结果: ", out)
        print ("--------------------------------------------------------------------------\n")
        # 加入执行命令和执行结果键值
        da["返回结果"] = out
        da["执行命令"] = cmd
        new_dict.append (da)
    # 运行的任务路径单独保存结果，在无法运行py脚本时可以使用bat脚本在远程服务器校验
    with open ("all_check.txt", "w", encoding="UTF-8", errors="ignore") as fn:
        for nd in new_dict:
            if "No matching objects found" in nd["返回结果"]:
                pass
            else:
                fn.write ("任务名：\n" + nd["TaskName"] + "作为用户运行：\n" + nd["RunAsUser"] + "执行命令：\n" + nd["执行命令"] + "\n返回结果：" + nd[
                    "返回结果"] + "\n--------------------------------------------------------------------------\n")


def accessChk_zh(dict_all):
    new_dict = []
    print ("--------------------------------------------------------------------------\n")
    # print(dict_all)
    for da in dict_all:
        # 根据\判断是否存在路径，不存在则增加默认路径%windir%\system32\
        if "\\" in da["要运行的任务"]:
            cmd = "accesschk.exe  /accepteula -uwqv \"" + da["要运行的任务"] + "\""
        else:
            cmd = "accesschk.exe  /accepteula -uwqv " + "%windir%\\system32\\\"" + da["要运行的任务"] + ".exe\""
        p = subprocess.Popen (cmd, shell=True, encoding="GBK", errors="ignore", stdout=subprocess.PIPE)
        out0 = p.stdout.readlines ()
        out = "".join (out0).split ("www.sysinternals.com\n")[1]

        # 返回的结果
        print ("执行命令:\n", cmd)
        print ("作为用户运行：", da["作为用户运行"])
        print ("执行结果: ", out)
        print ("--------------------------------------------------------------------------\n")
        # 加入执行命令和执行结果键值
        da["返回结果"] = out
        da["执行命令"] = cmd
        new_dict.append (da)
    # 运行的任务路径单独保存结果，在无法运行py脚本时可以使用bat脚本在远程服务器校验
    with open ("all_check.txt", "w", encoding="GBK", errors="ignore") as fn:
        for nd in new_dict:
            if "No matching objects found" in nd["返回结果"]:
                pass
            else:
                fn.write ("任务名：\n" + nd["任务名"] + "作为用户运行：\n" + nd["作为用户运行"] + "执行命令：\n" + nd["执行命令"] + "\n返回结果：" + nd[
                    "返回结果"] + "\n--------------------------------------------------------------------------\n")


def check_zh_en(file):
    with open (file, "r", errors="ignore") as f:
        ss = f.read ()
    # print(ss)
    if "主机名" in ss and "任务名" in ss:
        return True
    else:
        return False


def parse_schtasks_en(file_name):
    '''解析导出的计划任务文件，返回筛选后要运行的任务列表'''
    with open (file_name, "r", encoding="UTF-8", errors="ignore") as f:
        s = f.readlines ()
    result = []
    piece = []
    # 对读取的数据列表进行循环
    for k in range (len (s)):
        # 使用\n对分片位置进行判断
        if s[k] == '\n' and k > 0 and len (piece) != 0:
            result.append (piece)
            piece = []
            continue
        else:
            if "TaskName:" in s[k]:
                piece.append (s[k].replace (" ", ""))
            if "Status:" in s[k]:
                piece.append (s[k].replace (" ", ""))
            if "Run As User:" in s[k]:
                piece.append (s[k].replace (" ", ""))
            if "Task To Run:" in s[k]:
                piece.append (s[k])
    if piece != "":
        result.append (piece)
    # 将数据进行dict转换
    result_dict = []
    result_dict2 = []
    for rd in result:
        piece_dict = {}
        # 筛选模式为就绪的计划任务
        if ("Status:Disabled\n" not in rd) and ("Task To Run:                       COM handler\n" not in rd):
            for rd0 in rd:
                if "Task To Run" in rd0:
                    k = rd0.split ("Run:")[0]
                    # 筛选要运行的任务,如果路径带有引号则不按照空格筛选
                    v0 = rd0.split ("Run:")[1].strip ()
                    # 路径上只有两个引号
                    if ("\"" in v0) and (list (v0)[0] == "\""):
                        v = v0.strip ().split ("\"")[1]
                    # 两个引号不在路径上，以空格分割
                    elif ("\"" in v0) and (list (v0)[0] != "\""):
                        v = v0.strip ().split (" ")[0]
                    # 路径有空格和/，且不存在引号
                    elif ("\"" not in v0) and ("/" in v0):
                        v = v0.strip ().split ("/")[0].strip ()
                    # 路径有空格和-，且不存在引号
                    elif "\"" not in v0 and "-" in v0:
                        v = v0.strip ().split ("-")[0].strip ()
                    # 路径有空格，且不存在引号，不存在特殊符号进行分割
                    elif "\"" not in v0 and os.path.exists (v0.strip ()):
                        v = v0.strip ()
                    else:
                        v = v0.strip ().split (" ")[0]
                    # print(v)
                    piece_dict[k + "Run"] = v
                    result_dict2.append (v)
                else:
                    k = rd0.split (":")[0]
                    v = rd0.split (":")[1]
                    piece_dict[k] = v
            # print(piece_dict)
            result_dict.append (piece_dict)
        else:
            # print("计划任务不可用")
            pass

    # 生成待检查的要执行的计划任务列表，先去重
    res = list (set (result_dict2))
    res.sort (key=result_dict2.index)
    fa = []
    for g in res:
        if "\\" in g:
            fa.append (g + "\n")
        elif ("\\" not in g) and ("." not in g):
            fa.append ("%windir%\\system32\\" + g + ".exe\n")
        elif ("\\" not in g) and ("." in g):
            fa.append ("%windir%\\system32\\" + g + "\n")
    res1 = list (set (fa))
    res1.sort (key=fa.index)
    with open ("only_task_path.txt", "w", encoding="UTF-8") as fa:
        for r1 in res1:
            fa.write (r1)
    # 返回字典列表
    return result_dict


def parse_schtasks_zh(file_name):
    '''解析导出的计划任务文件，返回筛选后要运行的任务列表'''
    with open (file_name, "r", encoding="gbk", errors="ignore") as f:
        s = f.readlines ()
    result = []
    piece = []

    # 对读取的数据列表进行循环
    for k in range (len (s)):
        # 使用\n对分片位置进行判断
        if s[k] == '\n' and k > 0 and len (piece) != 0:
            result.append (piece)
            piece = []
            continue
        else:
            if "任务名:" in s[k]:
                piece.append (s[k].replace (" ", ""))
            if "模式:" in s[k]:
                piece.append (s[k].replace (" ", ""))
            if "作为用户运行:" in s[k]:
                piece.append (s[k].replace (" ", ""))
            if "要运行的任务:" in s[k]:
                piece.append (s[k])
    if piece != "":
        result.append (piece)
    # 将数据进行dict转换
    result_dict = []
    result_dict2 = []
    for rd in result:
        piece_dict = {}
        # 筛选模式为就绪的计划任务
        if ("模式:禁用\n" not in rd) and ("要运行的任务:                       COM 处理程序\n" not in rd):
            for rd0 in rd:
                if "要运行的任务" in rd0:
                    k = rd0.split ("任务:")[0]
                    # 筛选要运行的任务,如果路径带有引号则不按照空格筛选
                    v0 = rd0.split ("任务:")[1].strip ()
                    # 路径上只有两个引号
                    if ("\"" in v0) and (list (v0)[0] == "\""):
                        v = v0.strip ().split ("\"")[1]
                    # 两个引号不在路径上，以空格分割
                    elif ("\"" in v0) and (list (v0)[0] != "\""):
                        v = v0.strip ().split (" ")[0]
                    # 路径有空格和/，且不存在引号
                    elif ("\"" not in v0) and ("/" in v0):
                        v = v0.strip ().split ("/")[0].strip ()
                    # 路径有空格和-，且不存在引号
                    elif "\"" not in v0 and "-" in v0:
                        v = v0.strip ().split ("-")[0].strip ()
                    # 路径有空格，且不存在引号，不存在特殊符号进行分割
                    elif "\"" not in v0 and os.path.exists (v0.strip ()):
                        v = v0.strip ()
                    else:
                        v = v0.strip ().split (" ")[0]
                    # print(v)
                    piece_dict[k + "任务"] = v
                    result_dict2.append (v)
                else:
                    k = rd0.split (":")[0]
                    v = rd0.split (":")[1]
                    piece_dict[k] = v
            # print(piece_dict)
            result_dict.append (piece_dict)
        else:
            # print("计划任务不可用")
            pass

    # 生成待检查的要执行的计划任务列表，先去重
    res = list (set (result_dict2))
    res.sort (key=result_dict2.index)
    fa = []
    for g in res:
        if "\\" in g:
            fa.append (g + "\n")
        elif ("\\" not in g) and ("." not in g):
            fa.append ("%windir%\\system32\\" + g + ".exe\n")
        elif ("\\" not in g) and ("." in g):
            fa.append ("%windir%\\system32\\" + g + "\n")
    res1 = list (set (fa))
    res1.sort (key=fa.index)
    with open ("only_task_path.txt", "w", encoding="GBK", errors="ignore") as fa:
        for r1 in res1:
            fa.write (r1)
    # 返回字典列表
    return result_dict


if __name__ == '__main__':
    banner = r'''
               _     _              _    
      ___  ___| |__ | |_    ___ ___| | __
     / __|/ __| '_ \| __|  / __/ _ \ |/ /
     \__ \ (__| | | | |_  | (_|  __/   < 
     |___/\___|_| |_|\__|  \___\___|_|\_\
    '''
    help = r'''
    1.默认目标机器运行 
      python3 schtasks_check.py
    2.提取计划任务执行路径，
      python3 schtasks_check.py -f task.txt
      -f 指定目标机器获取的计划任务信息
      默认保存到 only_task_path.txt, (schtasks /query /fo LIST /v > task.txt)
      
    '''
    try:
        print (banner)
        print (help)
        if len (sys.argv) == 1:
            # 生成计划任务列表的temp.txt文件
            create_file ()
            # 检查是否包含中文
            FLAG = check_zh_en ("temp.txt")
            if FLAG:
                # 返回一个解析字典列表
                di = parse_schtasks_zh ("temp.txt")
                # 生成最终检查结果
                accessChk_zh (di)
            else:
                di = parse_schtasks_en ("temp.txt")
                accessChk_en (di)
            print ("结果保存至 all_check.txt")
        elif len (sys.argv) == 3:
            file = sys.argv[2]
            if os.path.exists (file):
                # 检查是否包含中文
                FLAG = check_zh_en (file)
                if FLAG:
                    # 返回一个解析字典列表
                    di = parse_schtasks_zh (file)
                else:
                    di = parse_schtasks_en (file)
                print ("提取成功，结果保存至 only_task_path.txt")
            else:
                print ("指定文件不存在")
    except Exception as e:
        raise e
        print (e)
