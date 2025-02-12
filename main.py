import tkinter as tk
from tkinter import filedialog
import os
from Table_Extraction import process_image  


def main():
    # 创建一个GUI窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏根窗口

    # 打开文件对话框选择图片
    file_path = filedialog.askopenfilename(
        title="选择一个图片文件",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )

    if file_path:
        print(f"选择的文件路径是：{file_path}")
        # 调用处理图片的函数
        process_image(file_path)
    else:
        print("没有选择图片文件。")


if __name__ == "__main__":
    main()
