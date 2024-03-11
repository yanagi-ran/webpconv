from flet import Page, Text, ElevatedButton, FilePicker, FilePickerResultEvent, TextField, Row, TextButton
import flet as ft
import subprocess
import os
import time

files = []
output_path = "./"

def main(page:Page):
    page.title = "webpに変換ツール"
    page.padding = 24
    page.window_height = 700
    page.window_width = 900
    page.window_center()

    def pick_output_dir(e: FilePickerResultEvent):
        global output_path
        output_path = e.path if e.path else ""
        output_dir.value = output_path
        output_dir.update()

    pick_dir_dialog = FilePicker(on_result=pick_output_dir)
    output_dir = TextField(value="",expand=True,label="保存先")

    def pick_file_result(e: FilePickerResultEvent):
        global files
        selected_files.value = (
            f"\n".join(map(lambda f: f.name, e.files)) if e.files else ""
        )
        files = [f.path for f in e.files] if e.files else []
        count = len(files)
        files_count.value = f"選択したファイル数: {count}"
        selected_files.update()
        files_count.update()
    
    pick_files_dialog = FilePicker(on_result=pick_file_result)
    selected_files = TextField(value=" ",multiline=True,max_lines=10,min_lines=10,expand=True,label="選択したファイル")
    files_count = Text("選択したファイル数: 0")

    def check(e):
        global files
        global output_path
        progress.visible = True
        progress.update()
        done = 0
        if len(files) != 0:
            for file_path in files:
                
                file_name_with_extension = os.path.basename(file_path)
                file_name, _ = os.path.splitext(file_name_with_extension)
                print(f"ファイル名: {file_name}")
                print(f"パス: {file_path}")
                command = ["cwebp", "-q", "80", file_path, "-o", f"{output_path}/{file_name}.webp"]
                subprocess.Popen(command)
                done += 1
                progress_value = done / len(files)
                progress.value = progress_value
                progress.update()
                print(progress_value)
                time.sleep(0.6)

        else:
            pass
    
    open_dir_dialog = TextButton("保存先を選択",on_click=lambda _: pick_dir_dialog.get_directory_path())
    open_dialog = TextButton("ファイルを選択",on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True))
    conv_btn = ft.FloatingActionButton("変換する",on_click=check,icon=ft.icons.LOOP)
    progress = ft.ProgressBar(disabled=True,visible=False)

    page.overlay.extend([pick_files_dialog,pick_dir_dialog])

    page.add(Row([selected_files,open_dialog]),files_count,Row([output_dir,open_dir_dialog]),progress,conv_btn)

ft.app(main)