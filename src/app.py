#!/usr/bin/env python3
"""
CSV数据清洗工具 - 去重/空值处理/格式标准化
"""
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import tkinter as tk

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

class App:
    def __init__(self, root):
        self.root = root
        root.title("CSV数据清洗工具 v1.0")
        root.geometry("700x550")
        self.file = None
        self.df = None
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#0288d1", height=60)
        f.pack(fill="x")
        tk.Label(f, text="🧹 CSV数据清洗工具", font=("Arial",16,"bold"),
                 fg="white", bg="#0288d1").pack(pady=15)
        main = tk.Frame(self.root, padx=20, pady=15)
        main.pack(fill="both", expand=True)
        
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="选择CSV文件", command=self.load_file,
                  bg="#0288d1", fg="white", padx=15).pack(side="left", padx=5)
        
        # 清洗选项
        of = tk.LabelFrame(main, text="清洗选项", font=("Arial",11,"bold"), padx=10, pady=10)
        of.pack(fill="x", pady=10)
        
        self.remove_dup = tk.BooleanVar(value=True)
        self.remove_empty = tk.BooleanVar(value=True)
        self.trim_space = tk.BooleanVar(value=True)
        self.standard_date = tk.BooleanVar(value=False)
        
        tk.Checkbutton(of, text="去除重复行", variable=self.remove_dup,
                       font=("Arial",10)).pack(anchor="w")
        tk.Checkbutton(of, text="删除空值行", variable=self.remove_empty,
                       font=("Arial",10)).pack(anchor="w")
        tk.Checkbutton(of, text="去除首尾空格", variable=self.trim_space,
                       font=("Arial",10)).pack(anchor="w")
        tk.Checkbutton(of, text="日期格式标准化", variable=self.standard_date,
                       font=("Arial",10)).pack(anchor="w")
        
        # 操作按钮
        opf = tk.Frame(main)
        opf.pack(fill="x", pady=10)
        tk.Button(opf, text="🔍 预览数据", command=self.preview,
                  padx=15, pady=5).pack(side="left", padx=5)
        tk.Button(opf, text="🚀 开始清洗", command=self.clean,
                  bg="#4caf50", fg="white", font=("Arial",10,"bold"),
                  padx=20, pady=5).pack(side="left", padx=10)
        tk.Button(opf, text="💾 保存结果", command=self.save,
                  bg="#ff9800", fg="white", padx=15, pady=5).pack(side="left", padx=5)
        
        self.status = tk.Label(main, text="请选择CSV文件",
                              font=("Arial",10), fg="gray", anchor="w")
        self.status.pack(fill="x")
    
    def load_file(self):
        f = filedialog.askopenfilename(title="选择CSV文件",
             filetypes=[("CSV文件","*.csv *.tsv")])
        if f:
            self.file = f
            self.status.config(text=f"已加载：{Path(f).name}")
    
    def preview(self):
        if not self.file:
            messagebox.showwarning("提示", "请先选择CSV文件")
            return
        if not HAS_PANDAS:
            messagebox.showerror("缺少依赖", "请运行：pip install pandas")
            return
        try:
            self.df = pd.read_csv(self.file)
            info = f"行数：{len(self.df)}\n列数：{len(self.df.columns)}\n\n列名：\n"
            info += "\n".join(self.df.columns.tolist())
            messagebox.showinfo("数据预览", info)
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def clean(self):
        if not self.file:
            messagebox.showwarning("提示", "请先选择CSV文件")
            return
        if not HAS_PANDAS:
            messagebox.showerror("缺少依赖", "请运行：pip install pandas")
            return
        try:
            self.df = pd.read_csv(self.file)
            orig_len = len(self.df)
            
            if self.remove_dup.get():
                before = len(self.df)
                self.df = self.df.drop_duplicates()
                removed_dup = before - len(self.df)
            else:
                removed_dup = 0
            
            if self.remove_empty.get():
                before = len(self.df)
                self.df = self.df.dropna()
                removed_empty = before - len(self.df)
            else:
                removed_empty = 0
            
            if self.trim_space.get():
                for col in self.df.select_dtypes(include=["object"]).columns:
                    self.df[col] = self.df[col].str.strip()
            
            self.status.config(text=f"✅ 清洗完成：{orig_len} → {len(self.df)} 行 "
                                   f"(去重{removed_dup}，删空{removed_empty})")
            messagebox.showinfo("完成", f"数据清洗完成！\n原始：{orig_len} 行\n"
                              f"清洗后：{len(self.df)} 行")
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def save(self):
        if self.df is None:
            messagebox.showwarning("提示", "请先清洗数据")
            return
        out = filedialog.asksaveasfilename(title="保存CSV",
             defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if out:
            self.df.to_csv(out, index=False, encoding="utf-8-sig")
            messagebox.showinfo("保存成功", f"已保存至：{out}")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
