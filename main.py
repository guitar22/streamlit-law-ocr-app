import os
import re
import pdfplumber

def extract_law_numbers(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages)
        law_numbers = re.findall(r'((?:法人税法|法人税法施行令|所得税法|消費税法|相続税法|地方税法|国税通則法|国税徴収法|租税特別措置法)\s*\d+\s*条(?:\s*\d+\s*項)?(?:\s*\d+\s*号)?)', text)
        formatted_numbers = [re.sub(r'\s+', '', num) for num in law_numbers]
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
