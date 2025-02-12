from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont
import textwrap
import numpy as np

# 指定完整路径
model_path = "D:/Personal_Project/PDF_Extraction/cv_dla34_table-structure-recognition_cycle-centernet"

def process_image(image_path):
    # 1. 表格结构识别
    table_recognition = pipeline(Tasks.table_recognition, model=model_path)
    result = table_recognition(image_path)

    print(result)

    # 2. OCR 文字识别
    ocr = PaddleOCR(
        use_gpu=True,
        lang='ch',
        det_model_dir='D:/Personal_Project/PDF_Extraction/PaddleOCR/models/ch_PP-OCRv4_det_infer/',
        rec_model_dir='D:/Personal_Project/PDF_Extraction/PaddleOCR/models/ch_PP-OCRv4_rec_infer/',
        cls_model_dir='D:/Personal_Project/PDF_Extraction/PaddleOCR/models/ch_ppocr_mobile_v2.0_cls_infer/'
    )

    res = ocr.ocr(image_path, cls=True)
    print(res)

    def calculate_iot(cell, text):
        """
        计算两个矩形框的交集面积和文本框面积的比值（IoT）。

        :param cell: 单元格的坐标 (x1, y1, x2, y2)
        :param text: 文本框的坐标 (x1, y1, x2, y2)
        :return: IoT
        """
        # 计算交集的左上角和右下角坐标
        intersection_x1 = max(cell[0], text['coords'][0])
        intersection_y1 = max(cell[1], text['coords'][1])
        intersection_x2 = min(cell[2], text['coords'][2])
        intersection_y2 = min(cell[3], text['coords'][3])

        # 如果没有交集，返回 0
        if intersection_x1 >= intersection_x2 or intersection_y1 >= intersection_y2:
            return 0.0
        # 计算交集的面积
        intersection_area = (intersection_x2 - intersection_x1) * (intersection_y2 - intersection_y1)

        text_area = (text['coords'][2] - text['coords'][0]) * (text['coords'][3] - text['coords'][1])
        # 计算 IoT
        iot = intersection_area / text_area
        return iot


    def merge_text_into_cells(cell_coords, ocr_results):
        """将文字合并到单元格"""
        # 创建一个字典，键是单元格坐标，值是属于该单元格的文字列表
        cell_text_dict = {cell: [] for cell in cell_coords}
        noncell_text_dict = {}

        # 遍历 OCR 结果，将文字分配给正确的单元格
        for cell in cell_coords:
            for result in ocr_results:
                if calculate_iot(cell, result) > 0.5:
                    cell_text_dict[cell].append(result['text'])

        for result in ocr_results:
            if all(calculate_iot(cell, result) < 0.1 for cell in cell_coords):
                noncell_text_dict[result['coords']] = result['text']

        merged_text = {}
        for cell, texts in cell_text_dict.items():
            merged_text[cell] = ''.join(texts).strip()
        for coords, text in noncell_text_dict.items():
            merged_text[coords] = ''.join(text).strip()

        return merged_text


    cell_coords = [tuple([*i[:2], *i[4:6]]) for i in result['polygons']]
    ocr_results = [
        {'text': i[1][0], 'coords': tuple([*i[0][0], *i[0][2]])} for i in res[0]]
    merged_text = merge_text_into_cells(cell_coords, ocr_results)
    print(merged_text)


    def adjust_coordinates(merged_text, image_path):
        image = Image.open(image_path)
        width, height = image.size
        threshold = height / 100
        groups = {}

        for coordinates, text in merged_text.items():
            # 查找与当前 y 坐标相差不超过 threshold 的分组
            found_group = False
            for group_y in groups.keys():
                if abs(coordinates[1] - group_y) <= threshold:
                    groups[group_y].append((coordinates, text))
                    found_group = True
                    break

            # 如果没有找到合适的分组，则创建一个新的分组
            if not found_group:
                groups[coordinates[1]] = [(coordinates, text)]

        # 计算每个分组的 y 坐标的平均值，并更新坐标列表
        adjusted_coordinates = {}
        for group_y, group_coords in groups.items():
            avg_y = sum(coord[0][1] for coord in group_coords) / len(group_coords)
            for i in group_coords:
                adjusted_coordinates[(i[0][0], avg_y, i[0][2], i[0][3])] = i[1]

        return adjusted_coordinates


    # 调用函数处理坐标
    adjusted_merged_text = adjust_coordinates(merged_text, image_path)

    # 打印结果
    print("原始坐标:", merged_text)
    print("调整后的坐标:", adjusted_merged_text)

    def draw_text_boxes(image_path, boxes, texts):
        img = Image.open(image_path)
        img = Image.new('RGB', img.size, (255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("./chinese_cht.ttf", size=15)  # 选择合适的字体和大小

        for box, text in zip(boxes, texts):
            # 修正坐标顺序：确保 x0 <= x1 且 y0 <= y1
            x0, y0, x1, y1 = box
            x0, x1 = sorted([x0, x1])  # 确保 x0 <= x1
            y0, y1 = sorted([y0, y1])  # 确保 y0 <= y1
            normalized_box = (x0, y0, x1, y1)

            draw.rectangle(normalized_box, outline='red', width=2)

            text_len = draw.textbbox(xy=(x0, y0), text=text, font=font)

            if (text_len[2] - text_len[0]) > (x1 - x0):
                text = '\n'.join(textwrap.wrap(text, width=int(
                    np.ceil(len(text) / np.ceil((text_len[2] - text_len[0]) / (x1 - x0))))))

            draw.text((x0, y0), text, font=font, fill='black')

        img.save('D:/Personal_Project/PDF_Extraction/output.png')


    boxes = list(adjusted_merged_text.keys())
    texts = list(adjusted_merged_text.values())
    draw_text_boxes(image_path, boxes, texts)

    # 输出最终的文本
    adjusted_merged_text_sorted = sorted(adjusted_merged_text.items(), key=lambda x: (x[0][1], x[0][0]))
    adjusted_merged_text_sorted_group = {}
    for coordinates, text in adjusted_merged_text_sorted:
        if coordinates[1] not in adjusted_merged_text_sorted_group:
            adjusted_merged_text_sorted_group[coordinates[1]] = [text]
        else:
            adjusted_merged_text_sorted_group[coordinates[1]].append(text)
    for text_list in adjusted_merged_text_sorted_group.values():
        print(' | '.join(text_list))
