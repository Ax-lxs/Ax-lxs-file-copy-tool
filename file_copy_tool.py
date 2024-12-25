import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import re

class FileCopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件批量复制工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.root.minsize(600, 400)
        
        # 设置整体样式
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)
        
        # 初始化变量
        self.naming_rules = {
            "{n}": "序号",
            "{name}": "原文件名",
            "{date}": "日期(YYYYMMDD)",
            "{time}": "时间(HHMMSS)",
            "{ext}": "文件扩展名"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=50)
        file_entry.pack(side=tk.LEFT, padx=5)
        
        select_btn = ttk.Button(file_frame, text="选择文件", command=self.select_file)
        select_btn.pack(side=tk.LEFT, padx=5)
        
        # 复制设置区域
        copy_frame = ttk.LabelFrame(main_frame, text="复制设置", padding="10")
        copy_frame.pack(fill=tk.X, pady=10)
        
        # 基础设置
        basic_frame = ttk.Frame(copy_frame)
        basic_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(basic_frame, text="复制数量:").pack(side=tk.LEFT, padx=5)
        self.copy_count_var = tk.StringVar(value="1")
        copy_count_entry = ttk.Entry(basic_frame, textvariable=self.copy_count_var, width=10)
        copy_count_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(basic_frame, text="起始序号:").pack(side=tk.LEFT, padx=5)
        self.start_num_var = tk.StringVar(value="1")
        start_num_entry = ttk.Entry(basic_frame, textvariable=self.start_num_var, width=10)
        start_num_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(basic_frame, text="序号位数:").pack(side=tk.LEFT, padx=5)
        self.num_digits_var = tk.StringVar(value="1")
        num_digits_entry = ttk.Entry(basic_frame, textvariable=self.num_digits_var, width=10)
        num_digits_entry.pack(side=tk.LEFT, padx=5)
        
        # 命名规则设置
        naming_frame = ttk.Frame(copy_frame)
        naming_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(naming_frame, text="命名格式:").pack(side=tk.LEFT, padx=5)
        self.naming_pattern_var = tk.StringVar(value="{name}_{n}{ext}")
        naming_entry = ttk.Entry(naming_frame, textvariable=self.naming_pattern_var, width=40)
        naming_entry.pack(side=tk.LEFT, padx=5)
        
        help_btn = ttk.Button(naming_frame, text="格式说明", command=self.show_naming_help)
        help_btn.pack(side=tk.LEFT, padx=5)
        
        # 输出区域
        output_frame = ttk.LabelFrame(main_frame, text="输出信息", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.output_text = tk.Text(output_frame, height=10, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # 预览按钮
        self.preview_btn = tk.Button(
            button_frame,
            text="预览结果",
            command=self.preview_names,
            bg='#28a745',
            fg='white',
            font=('Helvetica', 12),
            padx=30,
            pady=10,
            relief=tk.RAISED,
            cursor='hand2',
            width=15
        )
        self.preview_btn.pack(side=tk.RIGHT, padx=10)
        
        self.start_btn = tk.Button(
            button_frame, 
            text="开始复制", 
            command=self.start_copy,
            bg='#007bff',
            fg='white',
            font=('Helvetica', 12, 'bold'),
            padx=30,
            pady=10,
            relief=tk.RAISED,
            cursor='hand2',
            width=15
        )
        self.start_btn.pack(side=tk.RIGHT, padx=10)
        
        self.clear_btn = tk.Button(
            button_frame, 
            text="清除日志", 
            command=self.clear_output,
            bg='#6c757d',
            fg='white',
            font=('Helvetica', 12),
            padx=30,
            pady=10,
            relief=tk.RAISED,
            cursor='hand2',
            width=15
        )
        self.clear_btn.pack(side=tk.RIGHT, padx=10)
        
        # 添加按钮悬停效果
        def on_enter(e):
            if e.widget == self.start_btn:
                e.widget['bg'] = '#0056b3'
            elif e.widget == self.preview_btn:
                e.widget['bg'] = '#218838'
            else:
                e.widget['bg'] = '#5a6268'

        def on_leave(e):
            if e.widget == self.start_btn:
                e.widget['bg'] = '#007bff'
            elif e.widget == self.preview_btn:
                e.widget['bg'] = '#28a745'
            else:
                e.widget['bg'] = '#6c757d'

        for btn in (self.start_btn, self.clear_btn, self.preview_btn):
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
    
    def show_naming_help(self):
        help_text = "命名规则说明：\n\n"
        for key, desc in self.naming_rules.items():
            help_text += f"{key}: {desc}\n"
        help_text += "\n示例：\n"
        help_text += "1. {name}_{n}{ext}  →  文件_1.txt\n"
        help_text += "2. {date}_{name}{ext}  →  20240301_文件.txt\n"
        help_text += "3. Copy_{n}_{name}{ext}  →  Copy_1_文件.txt"
        
        messagebox.showinfo("命名规则说明", help_text)
    
    def generate_filename(self, original_name, number):
        try:
            # 分离文件名和扩展名
            name, ext = os.path.splitext(original_name)
            
            # 获取当前日期时间
            now = datetime.now()
            date_str = now.strftime('%Y%m%d')
            time_str = now.strftime('%H%M%S')
            
            # 获取序号位数
            digits = max(1, int(self.num_digits_var.get()))
            number_str = str(number).zfill(digits)
            
            # 替换命名模式中的占位符
            pattern = self.naming_pattern_var.get()
            new_name = pattern.replace("{name}", name)\
                            .replace("{n}", number_str)\
                            .replace("{date}", date_str)\
                            .replace("{time}", time_str)\
                            .replace("{ext}", ext)
            
            return new_name
            
        except Exception as e:
            messagebox.showerror("错误", f"生成文件名时出错: {str(e)}")
            return None
    
    def preview_names(self):
        src_file = self.file_path_var.get()
        if not src_file:
            messagebox.showerror("错误", "请先选择要复制的文件！")
            return
            
        try:
            file_count = int(self.copy_count_var.get())
            start_num = int(self.start_num_var.get())
            if file_count < 1:
                raise ValueError("复制数量必须大于0")
        except ValueError as e:
            messagebox.showerror("错误", f"无效的数值设置: {str(e)}")
            return
            
        self.output_text.delete(1.0, tk.END)
        self.log_message("预览生成的文件名：\n")
        
        original_name = os.path.basename(src_file)
        for i in range(file_count):
            new_name = self.generate_filename(original_name, start_num + i)
            if new_name:
                self.log_message(f"{i+1}. {new_name}")
    
    def select_file(self):
        file_path = filedialog.askopenfilename(title="选择要复制的文件")
        if file_path:
            self.file_path_var.set(file_path)
            self.log_message(f"已选择文件: {file_path}")
    
    def log_message(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
    
    def start_copy(self):
        self.log_message("正在处理...")
        self.root.update()
        
        src_file = self.file_path_var.get()
        if not src_file:
            messagebox.showerror("错误", "请先选择要复制的文件！")
            return
            
        try:
            file_count = int(self.copy_count_var.get())
            start_num = int(self.start_num_var.get())
            if file_count < 1:
                raise ValueError("复制数量必须大于0")
        except ValueError as e:
            messagebox.showerror("错误", f"无效的复制数量: {str(e)}")
            return
            
        # 禁用按钮
        for btn in (self.start_btn, self.preview_btn):
            btn['state'] = 'disabled'
            btn['bg'] = '#cccccc'
            btn['fg'] = '#666666'
        
        try:
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            
            original_name = os.path.basename(src_file)
            
            self.output_text.delete(1.0, tk.END)
            self.log_message("开始复制文件...\n")
            
            for i in range(file_count):
                new_name = self.generate_filename(original_name, start_num + i)
                if new_name:
                    new_file_path = os.path.join(output_dir, new_name)
                    shutil.copy(src_file, new_file_path)
                    self.log_message(f"已生成: {new_name}")
                    self.root.update()
            
            self.log_message("\n复制完成！文件保存在 output 目录中。")
            
            result = messagebox.showinfo(
                "操作完成",
                f"成功复制 {file_count} 个文件！\n文件保存在 output 目录中。\n是否打开输出目录？",
                type=messagebox.YESNO
            )
            
            if result == 'yes':
                output_path = os.path.abspath(output_dir)
                os.startfile(output_path)
            
        except Exception as e:
            self.log_message(f"\n错误: {str(e)}")
            messagebox.showerror("错误", f"复制过程中出现错误: {str(e)}")
            
        finally:
            # 恢复按钮状态
            self.start_btn['state'] = 'normal'
            self.start_btn['bg'] = '#007bff'
            self.start_btn['fg'] = 'white'
            self.preview_btn['state'] = 'normal'
            self.preview_btn['bg'] = '#28a745'
            self.preview_btn['fg'] = 'white'

def main():
    root = tk.Tk()
    app = FileCopyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
