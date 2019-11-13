from tkinter import*
import socket
import threading

tcp_client=None
connect=True
    
def son():
    def send_msg(client):
        friend=entry_receiver.get()
        sendstr=entry_send.get()
        entry_send.delete(0, END)
        text_msg.insert(END,'我：'+sendstr+'\n')
        sendStr=friend+':'+sendstr
        client.send(sendStr.encode("utf-8"))

    def recv_msg(client):
        while True:
            #用户退出
            if connect==False:
                break
            #--------------------------
            recv_data=client.recv(1024)
            recv_str=recv_data.decode()
            # 服务器端friends字典更新，好友列表更新
            if recv_data.decode()[0]=='{' and recv_data.decode()[len(recv_data.decode())-1]=='}':
                friends=eval(recv_str)
                lb.delete(0,END)# 先清除Listbox
                for i in friends.keys():
                    lb.insert(END,i)
            else:
                text_msg.insert(END,recv_data.decode()+'\n')            
        client.close()
        print('成功退出')
        tk.destroy()
           

    def connectServer():
        global tcp_client
        # 用户名
        user=entry_user.get()
        # 创建tcp套接字
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # 连接服务器
        server_ip=entry_ip.get()
        server_port=int(entry_port.get())
        server_addr=(server_ip,server_port)
        client.connect(server_addr)
        
        tcp_client=client# 给send_msg用
        client.send(user.encode("utf-8"))

        t=threading.Thread(target=recv_msg,args=(client,))
        t.start()
        
        # 为好友列表开线程

    def exit_(client):
        global connect
        connect=False
        client.send('我要退出'.encode("utf-8"))

    def clear():
        text_msg.delete('1.0','end')

    def add():
        # 将选中的好友列表中的元素插入接收者输入框
        entry_receiver.delete(0,END)
        entry_receiver.insert(END,lb.get(ACTIVE))
        
    # 界面
    top=Toplevel()
    top.title('聊天窗口')
    top.geometry('600x520+200+20')
    # 写菜单栏
    menubar=Menu(top)
    menubar.add_command(label='清空聊天记录',command=clear)
    top.config(menu=menubar)#把menubar放进top中
    # 菜单栏完毕
    button1=Button(top,text="连接服务器",bg='white',command=connectServer)
    button1.pack()
    frame1=Frame(top,width=400,height=80,bg='silver')
    frame1.pack(side=LEFT,fill=BOTH,expand=True)#或sticky=N+E+W
    label_text=Label(frame1,text=entry_user.get())
    label_text.grid(row=0,column=0,columnspan=4,sticky=E+W,padx=10,pady=10)
    #加滚动条
    sb=Scrollbar(frame1)
    text_msg=Text(frame1,height=22,width=45,yscrollcommand=sb.set)
    text_msg.grid(row=1,column=0,columnspan=3,sticky=E+W,padx=5,pady=5)
    sb.grid(row=1,column=3,sticky=N+S+W)#垂直延申，靠左布放
    sb.config(command=text_msg.yview)

    label_send=Label(frame1,text='输入消息')
    label_send.grid(row=2,column=0,padx=10,pady=10)
    entry_send=Entry(frame1,width=30)
    entry_send.grid(row=2,column=1,padx=5,pady=5)
    label_receiver=Label(frame1,text='接收者')
    label_receiver.grid(row=3,column=0,padx=10,pady=10)
    entry_receiver=Entry(frame1,width=30)
    entry_receiver.grid(row=3,column=1,padx=5,pady=5)

    button2=Button(frame1,text='发送',command=lambda :send_msg(tcp_client))
    button2.grid(row=4,column=2)
    # 好友列表
    Label(frame1,text='好友列表',bg='white').grid(row=0,column=4,padx=10,pady=10)
    sb1=Scrollbar(frame1)
    lb=Listbox(frame1,yscrollcommand=sb1.set)
    lb.grid(row=1,column=4,rowspan=2,sticky=N+S+W,padx=10,pady=10)
    sb1.grid(row=1,column=5,rowspan=2,sticky=N+S+W)
    # 将选中的好友列表中的元素插入接收者输入框-按钮
    Button(frame1,text='确认',bg='white',command=add).grid(row=3,column=4,sticky=E,padx=10,pady=10)

    Button(frame1,text='退出',bg='white',command=lambda :exit_(tcp_client)).grid(row=4,column=4,sticky=E,padx=10,pady=10)
    

# 界面
tk=Tk()
tk.title('客户端')
tk.geometry('300x300+200+20')
big_frame=Frame(tk,bg='silver')
big_frame.pack(side=LEFT,fill=BOTH,expand=True,padx=10,pady=10)
frame=Frame(big_frame,bg='silver')
frame.grid(row=0,column=0)
label_user=Label(frame,text='用户名',fg='black')
label_user.grid(row=0,column=0,columnspan=2,sticky=E,padx=10,pady=10)
entry_user=Entry(frame)
entry_user.grid(row=0,column=2,padx=10,pady=10)
label_ip=Label(frame,text='服务器IP',fg='black')
label_ip.grid(row=1,column=0,columnspan=2,sticky=E,padx=10,pady=10)
entry_ip=Entry(frame)
entry_ip.grid(row=1,column=2,padx=10,pady=10)
label_port=Label(frame,text='服务器Port',fg='black')
label_port.grid(row=2,column=0,columnspan=2,sticky=E,padx=10,pady=10)
entry_port=Entry(frame)
entry_port.grid(row=2,column=2,padx=10,pady=10)
button=Button(frame,text='登录',bg='white',command=son)
button.grid(row=3,column=2,sticky=E,padx=10,pady=10)

mainloop()
