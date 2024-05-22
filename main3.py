import os
import re
import pdfplumber

def extract_law_numbers(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages)
        text = re.sub(r'\n', '', text)
        law_numbers = re.findall(r'((?:法人税法|法人税法施行令|所得税法|消費税法|相続税法|地方税法|国税通則法|国税徴収法|租税特別措置法|労働者協同組合法|課法|直法|規則|措法|令|法)(?:\s*第?\s*\d+\s*条(?:の\d+)?)?(?:\s*第?\s*\d+\s*項)?(?:\s*第?\s*\d+\s*号)?)', text)
        formatted_numbers = []
        for number in law_numbers:
            formatted_number = re.sub(r'\s+', '', number)
            formatted_number = re.sub(r'第(\d+)条の(\d+)', r'第\1条第\2項', formatted_number)
            if re.search(r'\d', formatted_number):
                formatted_numbers.append(formatted_number)
        return formatted_numbers

# 現在のディレクトリのパス
current_directory = os.path.dirname(os.path.abspath(__file__))

# 出力ファイルのパス
output_file = os.path.join(current_directory, 'law_numbers.txt')

# 同じディレクトリ内のすべてのPDFファイルを処理
with open(output_file, 'w', encoding='utf-8') as f:
    for filename in os.listdir(current_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(current_directory, filename)
            law_numbers = extract_law_numbers(pdf_path)
            if law_numbers:
                f.write(f"# {filename}\n")
                for number in law_numbers:
                    f.write(f"- {number}\n")
                f.write("\n")

print(f"法令番号が抽出され、{output_file}に保存されました。")

