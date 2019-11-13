from tkinter import*
import socket
import threading


users={}# 存用户名:专门为该用户服务的客服
friends={}# 存用户名和该用户的IP
len_dict=0# 检测字典长度

def run(client_socket,client_addr):#专门为某个用户服务
    global len_dict
    userName=client_socket.recv(1024)
    users[userName.decode()]=client_socket
    friends[userName.decode()]=client_addr
    text.insert(END,userName.decode()+'连接成功\n')
    while True:
        #循环获取好友列表，给所有用户发
        if len_dict!=len(friends):
            for i in users.keys():
                users[i].send(str(friends).encode("utf-8"))
            len_dict=len(friends)
        # 接收该用户的消息   
        recv_data=client_socket.recv(1024)
        # 服务器收到的是“接收者:message”
        if recv_data and recv_data.decode()!='我要退出':
            toWho_msg=recv_data.decode().split(':')
            users[toWho_msg[0]].send((userName.decode()+'：'+toWho_msg[1]).encode("utf-8"))
        elif recv_data.decode()=='我要退出':
            client_socket.send('你已成功退出'.encode("utf-8"))
        else:
            del friends[userName.decode()]
            del users[userName.decode()]
            for i in users.keys():
                users[i].send(str(friends).encode("utf-8"))
            len_dict=len(friends)
            text.insert(END,userName.decode()+'已成功退出\n')
            print('关闭用户成功')
            break
    client_socket.close()
    

def start():# 连接用户,并开启一个线程为他服务
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 绑定ip和port
    server_ip=entry_ip.get()
    server_port=int(entry_port.get())
    server.bind((server_ip,server_port))
    # 让默认的套接字由主动变被动                
    server.listen(128)
    text.insert(END,'服务器启动成功\n')
    while True:
        client_socket,client_addr=server.accept()
        t=threading.Thread(target=run,args=(client_socket,client_addr))
        t.start()

def startServer():# 改变port可开启多个服务器
    s = threading.Thread(target=start)#启用一个线程开启服务器
    s.start()#开启线程

def look_connect():
    top=Toplevel()
    top.title('已连接的用户')
    top.geometry('350x400+200+20')
    frame1=Frame(top,width=400,height=80,bg='silver')
    frame1.pack(side=LEFT,fill=BOTH,expand=True)#或sticky=N+E+W
    Label(frame1,text='显示已连接的用户',bg='white').grid(row=0,column=0,padx=10,pady=10)
    sb1=Scrollbar(frame1)
    lb=Listbox(frame1,width=40,height=15,yscrollcommand=sb1.set)
    lb.grid(row=1,column=0,rowspan=3,sticky=N+S+W,padx=10,pady=10)
    sb1.grid(row=1,column=1,rowspan=3,sticky=N+S+W)
    for i in friends.keys():
        lb.insert(END,i)

# 界面
tk=Tk()
tk.title('服务器')
tk.geometry('370x400+200+200')

frame=Frame(tk,bg='silver')
frame.pack(side=LEFT,fill=BOTH,expand=True,padx=10,pady=10)
label_ip=Label(frame,text='服务器IP',fg='black')
label_ip.grid(row=1,column=0,sticky=E,padx=10,pady=10)
entry_ip=Entry(frame)
entry_ip.grid(row=1,column=1)
label_port=Label(frame,text='服务器Port',fg='black')
label_port.grid(row=2,column=0,sticky=E,padx=10,pady=10)
entry_port=Entry(frame)
entry_port.grid(row=2,column=1)
button=Button(frame,text='启动服务器',bg='purple',command=startServer)
button.grid(row=3,column=1,padx=10,pady=10,sticky=W)
# 加滚动条
sb=Scrollbar(frame)
text=Text(frame,height=15,width=40,yscrollcommand=sb.set)
text.grid(row=4,column=0,columnspan=2,padx=10,pady=10)
sb.grid(row=4,column=2,sticky=N+S+W)#垂直延申，靠左布放
sb.config(command=text.yview)
# 写菜单栏
menubar=Menu(tk)
menubar.add_command(label='连接的用户',command=look_connect)
tk.config(menu=menubar)#把menubar放进root中
# 菜单栏完毕

mainloop()
