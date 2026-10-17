using System;
using System.Runtime.InteropServices;
public class VideoLock {
[StructLayout(LayoutKind.Sequential)] public struct UP { public int pid; public System.Runtime.InteropServices.ComTypes.FILETIME time; }
[StructLayout(LayoutKind.Sequential,CharSet=CharSet.Unicode)] public struct PI {public UP process; [MarshalAs(UnmanagedType.ByValTStr,SizeConst=256)] public string name; [MarshalAs(UnmanagedType.ByValTStr,SizeConst=64)] public string service;public uint type;public uint status;public uint session;[MarshalAs(UnmanagedType.Bool)]public bool restart;}
[DllImport("rstrtmgr.dll",CharSet=CharSet.Unicode)] public static extern int RmStartSession(out uint h,int flags,string key);
[DllImport("rstrtmgr.dll",CharSet=CharSet.Unicode)] public static extern int RmRegisterResources(uint h,uint n,string[] files,uint a,IntPtr apps,uint b,IntPtr svcs);
[DllImport("rstrtmgr.dll")] public static extern int RmGetList(uint h,out uint needed,ref uint count,[In,Out] PI[] list,ref uint reasons);
[DllImport("rstrtmgr.dll")] public static extern int RmEndSession(uint h);
public static string Find(string p){uint h;int r=RmStartSession(out h,0,Guid.NewGuid().ToString("N"));if(r!=0)return "start="+r;try {r=RmRegisterResources(h,1,new[]{p},0,IntPtr.Zero,0,IntPtr.Zero);uint need,count=0,reason=0;RmGetList(h,out need,ref count,null,ref reason);count=need;PI[] list=new PI[count];r=RmGetList(h,out need,ref count,list,ref reason);string s="result="+r;foreach(var x in list)s+=" pid="+x.process.pid+" app="+x.name;return s;}finally{RmEndSession(h);}}
}
