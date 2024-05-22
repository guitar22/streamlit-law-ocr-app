import os
import re
import pdfplumber
import streamlit as st

def extract_law_numbers(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages)
        text = re.sub(r'\n', '', text)
        law_numbers = re.findall(r'((?:法人税法|法人税法施行令|所得税法|消費税法|相続税法|地方税法|国税通則法|国税徴収法|租税特別措置法|労働者協同組合法|課法|直法|規則|措法)(?:\s*第?\s*\d+\s*条(?:の\d+)?)?(?:\s*第?\s*\d+\s*項)?(?:\s*第?\s*\d+\s*号)?|法(?!人税法|所得税法|消費税法|相続税法|地方税法|国税通則法|国税徴収法|租税特別措置法|労働者協同組合法)(?:\s*第?\s*\d+\s*条(?:の\d+)?)?(?:\s*第?\s*\d+\s*項)?(?:\s*第?\s*\d+\s*号)?|令(?!和)(?:\s*\d+\s*[-－]?\s*\d+\s*[-－]?\s*\d+)?)', text)

        formatted_numbers = []
        for number in law_numbers:
            formatted_number = re.sub(r'\s+', '', number)
            formatted_number = re.sub(r'第(\d+)条の(\d+)', r'第\1条第\2項', formatted_number)
            if re.search(r'\d', formatted_number):
                formatted_numbers.append(formatted_number)
        return formatted_numbers

st.title('法令番号抽出アプリ')

uploaded_files = st.file_uploader('PDFファイルをアップロードしてください', type='pdf', accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        law_numbers = extract_law_numbers(uploaded_file)
        if law_numbers:
            st.subheader(f'ファイル名: {uploaded_file.name}')
            for number in law_numbers:
                st.write(f'- {number}')
else:
    st.write('PDFファイルをアップロードしてください。')
