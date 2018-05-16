# -*- coding:utf-8 -*-
from sys import argv
from string import Template
import os, json
 

#取出字符串中的\r\n
def del_r_n(str):
    return str.replace('\r', '').replace('\n', '')
 
#存储对局参数
head = {'name': [], 'info_lock': 0, 'bid_lock': 0, 'lef_lock': 0, 'play_lock': 0, 'over_lock': 0}

script, from_file = argv

in_file = open(from_file)

#逐行读取并处理
line = in_file.readline()
while line:
    if 'DOUDIZHUVER' in line:             #平台版本
        head['ver'] = del_r_n(line[12:])

    elif 'NAME' in line:                  #队伍名字
        head['name'].append(del_r_n(line[5:]))
        if len(head['name']) == 3:
            filename_tem = Template("P2T1-${player_a}vs${player_b}vs${player_c}.txt")
            filename_str = filename_tem.substitute(player_a = head['name'][0], player_b = head['name'][1], player_c = head['name'][2])
            filename = filename_str #.decode('gbk').encode('utf-8')   #linux兼容
            to_file = open(filename, 'w') 
            to_file.write('(\t\n')
            
         

    elif line.startswith('INFO'):                   #对局信息
        if head['info_lock'] == 0:        #防止重复采集
            
            ###输出对局版本和选手信息
            ver_player_tem = Template(";VER[${ver}]PA[${player_a}]PB[${player_b}]PC[${player_c}]\n")
            ver_player_str =  ver_player_tem.substitute(ver = head['ver'], player_a = head['name'][0], player_b = head['name'][1], player_c = head['name'][2])
            to_file.write(ver_player_str)

            ###输出对局信息
            info = del_r_n(line[5:]).split(',')
            info_tem = Template(";TI[${ti}]TC[${tc}]RI[${ri}]RC[${rc}]UC[${uc}]MS[${ms}]\n")
            info_str = info_tem.substitute(ti = info[0], tc = info[1], ri = info[2], rc = info[3], uc=info[4], ms = info[5])
            to_file.write(info_str)
            head['info_lock'] = 1         #对局信息采集锁定

    elif line.startswith('DEAL'):         #处理配牌
        line = del_r_n(line)
        player = line[5:6]       #获取玩家编号
	code = line[6:]          #获取牌编号
        deal_tem = Template(";D${player}[${code}]\n")
        deal_str = deal_tem.substitute(player = player, code = code)
        to_file.write(deal_str)
        head['info_lock'] = 0        #对局信息采集解锁
        head['bid_lock'] = 0         #叫牌信息采集解锁
        head['lef_lock'] = 0         #叫牌结果采集解锁
        head['over_lock'] = 0        #对局结果采集解锁
            
    elif line.startswith('BID WHAT'):
        player = line[4:5]
        #啥用也没有^-^

    elif line.startswith('BID'):     #叫牌信息
        if(head['bid_lock'] == 0):
            player = line[4:5]
            point = line[5:6]
            bid_tem = Template(";B${player}[${point}]\n")
            bid_str = bid_tem.substitute(player = player, point = point)
            to_file.write(bid_str)
            head['bid_lock'] = 1
        
    elif line.startswith('LEFTOVER'):    #叫牌结果
        if(head['lef_lock'] == 0):
            line = del_r_n(line)
            player = line[9:10]
            code = line[10:]
            lef_tem = Template(";L${player}[${code}]\n")
            lef_str = lef_tem.substitute(player = player, code = code)
            to_file.write(lef_str)
            head['lef_lock'] = 1
   
    elif line.startswith('PLAY WHAT'): 
        head['play_lock'] = 0         #出牌采集解锁
        
    elif line.startswith('PLAY'):     #出牌
        if(head['play_lock'] == 0):
            line = del_r_n(line)
            player = line[5:6]
            code = line[6:]
            play_tem = Template(";${player}[${code}]\n")
            play_str = play_tem.substitute(player = player, code = code)
            to_file.write(play_str)
            head['play_lock'] = 1     #出牌采集锁定
        
    elif line.startswith('GAMEOVER'): #对局结果
        if(head['over_lock'] == 0):
            player = line[9:10]
            over_tem = Template(";OVER[${player}]\n")
            over_str = over_tem.substitute(player = player)
            to_file.write(over_str)
            head['over_lock'] = 1     #对局结果采集锁定

    ##############
    #重新获取一行
    line = in_file.readline()



#转字符集
to_file.write(')')
to_file.close()





