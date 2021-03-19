from tkinter import Button,Label,Tk,mainloop,TOP,Frame,filedialog,LEFT,Listbox,Scrollbar
from tkinter import RIGHT,Y,BOTH,END,Scale,HORIZONTAL,StringVar,BooleanVar,IntVar
import pygame
import os
from strwid import get_width as gw
from pymediainfo import MediaInfo
import random
from tkinter.messagebox import showwarning

# 初始化
t=Tk()
pygame.mixer.init()
pygame.init()
#t.geometry('370x345')
t.title('music player')
relists=['顺序循环','单曲循环','随机播放']
randlist=[]

# 取得音乐长度
def getmusiclen(m,reraw=False):
    mi=MediaInfo.parse(m)
    data=mi.to_json()
    dp=data.find('duration')
    mtime=data[dp+11:dp+11+7]
    while not mtime.isdigit():
        mtime=mtime[:-1]
    mti=int(int(mtime)/1000)
    if reraw:
        return(mti)
    ptscl.config(to=mti)
    mt=[int(mti/60),mti%60]
    for i in range(len(mt)):
        if len(str(mt[i]))==1:
            mt[i]='0'+str(mt[i])
        else:
            mt[i]=str(mt[i])
    return(mt)

# 取得字符串真实长度
def realwidth(s):
    a=0
    for c in s:
        a+=gw(ord(c))
    return(a)

# 从txt载入音乐列表
def loadmusic():
    f=open('library.txt','r')
    c=f.readlines()
    f.close()
    for i in range(len(c)):
        c[i]=c[i].rstrip('\n')
    return(c)
    
# 弹出文件选择窗口并播放选择的音乐档案
def playmusic():
    st.set('0')
    ptscl.set(0)
    pygame.mixer.music.stop()
    mn=filedialog.askopenfilename()
    try:
        pygame.mixer.music.load(mn)
    except:
        musicname.config(text='請選擇mp3,ogg等pygame支持的文件',font='None -18 bold')
        return()
    nowplaying.set(mn)
    musiclist.append(mn)
    randlist=makerandomlist()
    if randlist:print()
    mtt.set(getmusiclen(mn)[0]+':'+getmusiclen(mn)[1])
    smn=os.path.basename(mn)
    if smn not in library.get(0,library.size()):
        library.insert(END,smn)
        f=open('library.txt','a')
        f.write(mn+'\n')
        f.close()
    configfontsize(smn)
    musicname.config(text=smn)
    pygame.mixer.music.play()

# 停止播放    
def stopmusic():
    pygame.mixer.music.stop()
    st.set('0')
    
# 暂停播放
def pausemusic():
    pygame.mixer.music.pause()
    
# 取消暂停
def unpausemusic():
    pygame.mixer.music.unpause()
    
# 从列表删除音乐
def deletemusic():
    del musiclist[library.curselection()[0]]
    randlist=makerandomlist()
    if randlist:print()
    library.delete(library.curselection())
    f=open('library.txt','w')
    for line in musiclist:
        f.write(line+'\n')
    f.close()
    pygame.mixer.music.stop()
    
# 播放从列表选择的音乐
def playchosemusic(ev=None):
    st.set('0')
    ptscl.set(0)
    pygame.mixer.music.stop()
    smn=library.get(library.curselection())
    mn=musiclist[library.curselection()[0]]
    if not os.path.exists(mn):
        showwarning('Warning','你選擇的音樂不見了喔~請重新關聯~')
        deletemusic()
    else:
        nowplaying.set(mn)
        mtt.set(getmusiclen(mn)[0]+':'+getmusiclen(mn)[1])
        configfontsize(smn)
        musicname.config(text=smn)
        pygame.mixer.music.load(mn)
        pygame.mixer.music.play()
    
# 设置音量
def setvolume(ev=None):
    if volumescl.get()==0:
        v=0 
    else: 
        v=volumescl.get()/100
    pygame.mixer.music.set_volume(v)
    
# 播放时间设置，每100毫秒刷新(顺便附带歌曲结束判定，切歌等)
def timevarsset():
    if ptscln.get()!='-1':
        s=int(ptscln.get())
    else:
        s=int(pygame.mixer.music.get_pos()/1000)+int(st.get())
        ptscl.set(s)
    ss=[int(s/60),s%60]
    for i in range(len(ss)):
        if len(str(ss[i]))==1:
            ss[i]='0'+str(ss[i])
        else:
            ss[i]=str(ss[i])
    ptlb.config(text=ss[0]+':'+ss[1]+'/'+mtt.get())
    if nowplaying.get()!='':
        if getmusiclen(nowplaying.get(),True)<=s:
            playnextmusic()
    t.update()
    #print("当前窗口的宽度为",t.winfo_width())
    #print("当前窗口的高度为",t.winfo_height())
    t.after(100,timevarsset)
    
# 播放进度条设置
def ptscl0(ev=None):
    ptsclb.set(True)
def ptscl1(ev=None):
    if ptsclb.get():
        ptscln.set(str(ptscl.get()))
def ptscl2(ev=None):
    st.set(str(ptscln.get()))
    pygame.mixer.music.stop()
    pygame.mixer.music.load(nowplaying.get())
    pygame.mixer.music.play()
    pygame.mixer.music.set_pos(int(ptscln.get()))
    ptscln.set('-1')
    ptsclb.set(False)
    
def liststatus():
    r=liststatuscode.get()
    if r==2:
        r=0
    else:
        r+=1
    liststatuscode.set(r)
    listbutton.config(text=relists[liststatuscode.get()])

def makerandomlist():
    a=[]
    for i in range(len(musiclist)):
        a.append(i)
    random.shuffle(a)
    return(a)

def playlastmusic():
    playnextmusic(True,False)
    
def playnextmusic_():
    playnextmusic(False,True)

def playnextmusic(last=False,cn=False):
    if liststatuscode.get()==0:
        if not last:
            nextmusic=musiclist.index(nowplaying.get())+1
        else:
            nextmusic=musiclist.index(nowplaying.get())-1
    elif liststatuscode.get()==1:
        if not last and not cn:
            nextmusic=musiclist.index(nowplaying.get())
        elif not cn and last:
            nextmusic=musiclist.index(nowplaying.get())-1
        else:
            nextmusic=musiclist.index(nowplaying.get())+1
    else:
        if not last:
            tp=randlist.index(musiclist.index(nowplaying.get()))+1
        else:
            tp=randlist.index(musiclist.index(nowplaying.get()))-1
        if tp>=len(randlist):
            tp=0
        elif tp<0:
            tp=len(randlist)-1
        nextmusic=randlist[tp]
    if nextmusic>=len(musiclist):
        nextmusic=0
    elif nextmusic<0:
        nextmusic=len(musiclist)-1
    st.set('0')
    ptscl.set(0)
    pygame.mixer.music.stop()
    mn=musiclist[nextmusic]
    smn=os.path.basename(mn)
    nowplaying.set(mn)
    mtt.set(getmusiclen(mn)[0]+':'+getmusiclen(mn)[1])
    configfontsize(smn)
    musicname.config(text=smn)
    pygame.mixer.music.load(mn)
    pygame.mixer.music.play()

def configfontsize(smn):
    if realwidth(smn)>35:
        #smn=(smn[:-4])[:20]+'...'+smn[-4:]
        musicname.config(font='None -16 bold')
    elif realwidth(smn)>24:
        #smn=(smn[:-4])[:20]+'...'+smn[-4:]
        musicname.config(font='None -19 bold')
    else:
        musicname.config(font='None -26 bold')

nowplaying=StringVar() # 现正播放
musiclist=loadmusic()  # 载入音乐列表
randlist=makerandomlist()

# 第一区块（音乐名）（从上往下排列）
mnf=Frame(t)
musicname=Label(mnf,text='請選擇你的音樂',font='None -26 bold')
musicname.pack(side=TOP)
mnf.pack(side=TOP)

# 第二区块（播放，暂停，加入，停止，删除，音量等操作）
bf=Frame(t)
cmbt=Button(bf,text='加入音樂',command=playmusic)
dmbt=Button(bf,text='刪除音樂',command=deletemusic)
smbt=Button(bf,text='■',command=stopmusic)
pmbt=Button(bf,text='||',command=pausemusic)
plbt=Button(bf,text='▶',command=unpausemusic)
volumescl=Scale(bf,orient=HORIZONTAL,from_=0,to=100,label='音量',command=setvolume)
volumescl.set(50)
cmbt.pack(side=LEFT)
plbt.pack(side=LEFT)
pmbt.pack(side=LEFT)
smbt.pack(side=LEFT)
dmbt.pack(side=LEFT)
volumescl.pack(side=LEFT)
bf.pack(side=TOP)

# 第三区块（播放时间，进度条）
duf=Frame(t)

mtt,st,ptscln=StringVar(),StringVar(),StringVar() # 音乐时长，开始播放的位置，拖拽进度条的位置
mtt.set('-:--')
st.set('0')
ptscln.set('-1')
ptsclb=BooleanVar()                               # 是否正在拖拽进度条
ptsclb.set(False)
liststatuscode=IntVar()
liststatuscode.set(0)

ptlb=Label(duf,text=mtt)                          # 总时长显示，↓进度条
ptscl=Scale(duf,length=170,orient=HORIZONTAL,from_=0,to=0,showvalue=False,command=ptscl1)
ptscl.bind('<1>',ptscl0)
ptscl.bind('<ButtonRelease-1>',ptscl2)
listbutton=Button(duf,text='列表循环',command=liststatus)
prebutton=Button(duf,text='⏮',command=playlastmusic)
nextbutton=Button(duf,text='⏭',command=playnextmusic_)
ptlb.pack(side=LEFT)
ptscl.pack(side=LEFT)
prebutton.pack(side=LEFT)
listbutton.pack(side=LEFT)  
nextbutton.pack(side=LEFT)
duf.pack(side=TOP)

# 第四区块（音乐列表）
lbrf=Frame(t)
lbrsb=Scrollbar(lbrf)  # 列表侧滚轮
lbrsb.pack(side=RIGHT,fill=Y)
library=Listbox(lbrf,height=12,width=50,yscrollcommand=lbrsb.set) # 音乐列表
for m in musiclist: # 载入音乐列表
    library.insert(END,os.path.basename(m))
library.bind('<Double-1>',playchosemusic)
library.pack(side=LEFT,fill=BOTH)
lbrf.pack()
timevarsset()

# 主循环，结束后停止播放音乐
if __name__=='__main__':
    mainloop()
    stopmusic()